# 使用堡塔和XShell

## 课程目标

1.理解Windows与Linux实现远程通信的过程和所使用的协议**SSH**

2.款练使用远程连接工具堡塔KShell等工具及SSH和SCP命令

**我们要知道，Windows的命令提示符也是可以通过ssh直接远程连接到Linux的，这是除了堡塔工具和XShell之外也可以使用的远程连接**

## 课程实验

1.使用堡塔远程连接并操作Centos并实现与Windows之间的文件传输

2.使用XShell远程连接并操作Centos并实现与Windows之间的文件传输

3.使用SSH命令远程连接并操作作CentOs，使用SCP命令进行文件传输

## 课堂引入

在VMWare中直接使用CentOS非常不方便，不仅鼠标需要不停切换，而且无法直接复制命令或文本内容到命令提示符中，在与Windows主机之间实现文件传输也是比较麻烦的事情，所以，我们非常需要一款方便的远程连接工具，目前主流的工具有XShell，XFTP.SecureCRT，SecureFX等，也包括免费的国产作品堡塔，但是目前堡塔还存在一些Bug，不是大稳定，所以后续主要以XShel为主。

## 授课进程

### 一、SSH协议介绍

SSH 为 Secure shell的缩写，由IETF 的网络小组 (Network Working Group) 所制定 SSH 为建立在应用层基础上的安全协议。SSH是较可靠，专为违程登录会话和其他网络服务提供安全性的协议，利用 SSH 协议可以有效防止远程管理过程中的信息泄露问题，SSH最初是UNIX系统上的一个程序，后来又迅速扩展到其他操作平台。SSH在正确使用时可弥补网络中的漏洞。SSH客户端适用于多种平台，常见的可视化操作工具如本节内容所个绍的两款工具，也可以是基于命令行的SSH命令。SH提供两种级别的安全验证。

### 1、第一种级别 (基于口今的安全验证)

只要你知道自己账号和口令，就可以登录到远程主机。所有传输的数据都会被加密，但是不能保证你正在连接的服务器就是你想连接的服务器。可能会有别的服务器在冒充真正的服务器，也就是受到“中间人“这种方式的攻击。

### 2、第二种级别 (基于密匙的安全验证)

需要依靠密匙，也就是你必须为自己创建一对密匙，并把公用密匙放在需要访问的服务器上，如果你要连接到SSH服务器上，客户端软件就会向服务器发出请求，请求用你的密匙进行安全验证，服务收到请求之后，先在该服务器上你的主目录下寻找你的公用密匙，然后把它和你发送过来的公用密匙进行比较，如果两个密匙一致，服务器就用公用密匙加密"质询”(challenge) 并把它发送给客户端软件。客户端软件收到“质询”之后就可以用你的私人密匙解密再把它发送给服务器。

用这种方式，你必须知道自己密匙的口令。但是，与第一种级别相比，第二种级别不需要在网络上传送口令，相对来说更加安全

## 二、堡塔的基本使用



## 三、XShell的使用

也就是打开，建立会话，链接好了就可以了

这个没啥难的

## 四、SSH和SCP命令

### 1.SSH命令

```ssh
c:\Users Denny>ssh -1 root 192.168.112.225
root@192.168.230.140's password:
Last login: wed Aug 11 01:44:40 2021 from 192.168.112.1
[root@centqiang ~]#
[root@centqiang ~]# hostname
 centqiang
```

如果是首次链接，会提示类似以下的信息，输入yes回车即可：

```ssh
The authenticity of host '192.168.112.173 (192.168.112.173)' can't be established.
ECDSA key fingerprint is SHA256:w6m47u3C2ygg3m8U7TW1KJidwhz+D7oKWNT2/zHzNf8.
Are you sure you want to continue connecting (yes/no)?
```

上述命令表似乎成功使用Windows的SSH内置命令连接到Linux上，进而可以不需要借助于XSheel等工具进行远程连接，也可以使用以下方式进行链接：

```ssh
c:\users\Denny>ssh root@192.168.112.225
root@192.168.112.225's password:
Last login: wed Aug 11 02:01:50 2021 from 192.168.112.1
[root@centqiang ~]#
```

### 2.scp命令

#### 从Windows上传文件到Linux

```scp
C: Users Denny>scp D: test.htm] root@192.168.112.225:/opt
root@192.168.112.225's password:
test .htm1                                                       100% 206KB
28.9MB/s    00:00
```

![image-20230911195759678](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230911195759678.png)

然后使用scp命令让文件从windows传输到Linux中去

scp windows中文件目录位置 root@192.168.230.140:/opt

解释（scp浏览到Windows中文件位置以及远程登录的主机，然后:/加上需要上传的远程目录）

![image-20230911200340544](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230911200340544.png)

![image-20230911200411920](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230911200411920.png)

现在Linux这个文件目录下就有了这个文件

#### 从linux下载文件到Windows

```scp
C: Users\Denny>scp root@192.168.112.225:/opt/test.html E:
root@192.168.112.225's password:
test .htm]                                                       100%206KB
50.4MB/s     00:00
```

其实这个也就是将从Windows下载文件到Linux的命令调换了一下位置

![image-20230911200706232](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230911200706232.png)

这是Windows下的E盘，并没有capture.png这个文件

![image-20230911200842666](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230911200842666.png)

![image-20230911200855163](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230911200855163.png)

然后再回来看就有了

## 扩展内容

在手机端也可以使用SSH客户端工具：JuiceSSH。