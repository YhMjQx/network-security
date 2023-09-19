# ==在Linux下安装应用==

## 一、使用Rpm离线安装

先下载到本地，一rpm文件名结尾，下载完成后，再安装

```
rpm -qa | grep mysql    检索含有mysql的rpm包

rpm -ivh mysql80-community-release-e16-1.noarch.rpm    离线安装这个rpm包

rpm -e mysql80-community-release-e16-1.noarch    删除这个应用
```

利用rpm安装MySQL服务器版：

```
[root@centqiang opt]# rpm -ivh MysQL-server-5.6.40-1.e16.x86_64.rpmwarning: Mysol-server-5.6.40-1.el6,x86_64.rpm: Header V3 D5A/SHA1 Signature, key ID 5072e1f5: NOKEYerror: Failed dependencies:
/usr/bin/per1 is needed by MysoL-server-5.6.40-1.e16.x86_64[root@centqiang opt]#


Failed dependencies: 失败的依赖，缺少per1，此时就需要我们去在线安装perl
即：yum install perl
```

## 二、基于源代码安装应用

源代码安装比较适合于专业人员，并不需要要求安装人员能看懂代码，但要知道源代码的基本过程

nginx安装好了之后是这样的：

![image-20230919132510979](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230919132510979.png)

```
[root@centqiang nginx-1.21.0]# ./confiqure
checking for oS
+ Linux 3.10.0-1160.e17.x86_64 x86_64checking for C compiler ... not found
/confiqure: error : C compiler cc is not found
[root@centqiang nginx-1.21.0]# yum instal1 gcc -y

安装完成后再进行配置，如果提示缺少依赖库pcre或zlib等，则可以继续yum instal1 pcre-devel 和 yum install zlib-devel通常情况下，如果提示缺少什么库，一般先尝试 yum instal1 pcre,如果不行，再尝试 yum instal1 pcre-devel
```

## 三、yum命令操作

Yum (全称为 Yellow dog Updater,Modified) 是一个在Fedora和RedHat以及CentOS中的Shell前端软件包管理器。甚于RPM包管理，能够从指定的服务器自动下载RPM包并且安装，可以自动处理依赖性关系，并且一次安装所有依赖的软件包，无须繁琐地一次次下载、安装。

```
yum 1ist:查询本机已经安装的包
yum search mysq1:在线搜索当前源（库）可用的包
yum repolist:列出当前的库

yum instal1 gcc: 安装gcc
yum instal1 gcc -y: 不再提示是否确认，直接选择Yes
yum insta1gcc cmake gcc-c++ mysql wget -y: 不再提示是否确认，直接选择Yes

yum deplist curl 查看应用程序curl的依赖库（library）

yum clear a11 ：清空缓存的镜像列表
yum makecache：重新根据配置文件构建镜像缓存列表


yum erase wget ： 卸载wget，卸载过程最好不要加 -y ，最好二次确认 
yum remove wget ： 卸载wget，卸载过程最好不要加 -y ，最好二次确认 

yum update：更新
```

## 四、Yum配置源

默认配置文件:  /etc/yum.repo.d/CentOS-Base.repo

主要就是将该文件后缀一修改，使得yum在访问的时候不会去寻找到该文件，然后我们重新下一个国内的repo镜像文件，然后放在这个目录下

![image-20230919154233028](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230919154233028.png)

红色的文件就是原先的默认镜像文件，我将其后缀修改一下，使得yum在线使用时不会用这个文件，而是强制去使用蓝色框中的文件中的镜像文件地址去寻找

```
[basel
name=CentOS-Sreleasever - Base
mirrorlist=http://mirrorlist.centos .org/?release-Sreleasever&arch=Sbasearch&repo=os&infra=Sinfra
#baseur1=http://mirror .centos.org/centos/$releasever/os/$basearch/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Cent05-7

mirrorlist并非镜像本身的地址，而是一堆境像网址的集合，Centos会自动选择速度最快的一个，每一个对应就是具体的仓库，比如 http://mirrors.163.com/centos/7.9.2009/os/x86_64/Packages/

baseur1:对应的是具体的镜像地址，里面保存着仓库的各个安装包程序，也就是真正的国外的访问地址

```

```
http://mirrors.tuna.tsinghua.edu.cn/centos/7.9.2009/os/x86_64/
http://mirrors.ustc.edu.cn/centos/7 .9.2009/os/x86_64/
http://mirror .1zu.edu.cn/centos/7.9.2009/os/x86_64/
http://mirrors.nju.edu.cn/centos/7 .9.2009/os/x86_64/
http://mirrors.neusoft.edu.cn/centos/7 .9.2009/os/x86_64/
http://mirrors.bfsu.edu.cn/centos/7 .9.2009/os/x86_64/
http://mirrors.163.com/centos/7.9.2009/os/x86_64/
http://mirrors.cqu.edu.cn/Cent0s/7.9.2009/os/x86_64/
http://mirrors.huaweicloud.com/centos/7 .9.2009/os/x86_64/
http://mirrors.aliyun.com/centos/7.9.2009/os/x86_64/
```

下载阿里云的Repo源配置文件 http://mirrors.aliyun.com/repo/Centos-7.repo
替换CentOS-Base.repo
yum repolist

```
baseur1:对应的是目录内容
http://mirrors.aliyun.com/centos/Sreleasever/extras/Sbasearch/http://mirrors.aliyun.com/centos/7/extras/x86_64/

/etc/yum.conf
/var/1og/yum.1og
```

## 五、Apt安装

对于Redhat体系的Linux发行版本，目前主流的是Yum+Rpm的方式，安装方式:dnf，本质上跟yum几乎没有区别
可以在线安装依赖。
在新的Centos-8以后的版本中引入了新的对于Debian体系的Linux发行版本，主要安装命令两个: apt-get，apt，优先考虑使用apt.

```
阿里云：



中科大云：



清华云：




163云：



```

```
配置云缓存：
使用方法:
cd /etc/apt
cp sources.list sources.list.bak，备份原来的自带的源
sudo vi  /etc/apt/sources.list，将上面的源挑选一个黏贴进文本，保存
sudo apt-get update

apt install wget
apt-get install wget
```

