[TOC]



# ==Docker及摘取镜像==

## 一、什么是Docker

![image-20240125130936226](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125130936226.png)

### 1.虚拟环境

目前Docker只能运行在Linux上

（1）完整模拟硬件的虚拟环境：VMware，Hyper-V，Virtual-Box，VMServer等

（2）不模拟硬件，只把虚拟环境当成一个应用程序（进程）来对待：Docker，非常轻量级的虚拟环境

（3）在VMware中安装一个Linux，标配10G+，最小化安装将近2G。在Docker中安装一个最小化CentOS或Ubuntu，大概只需要200M

### 2.Docker的特征与虚拟机的异同：

（1）安装虚拟机软件，如：VMware，在此虚拟机软件上安装操作系统（下载），把操作系统的虚拟文件备份，随时复制并启动该操作系统。

（2）在Linux上安装Docker软件，从镜像仓库拉取（Pull）操作系统或应用环境，基于该镜像文件创建一个容器（运行环境），备份容器以供下次使用（直接export容器，将容器提交（Commit）为本地镜像）。

（3）虚拟机环境直接完全模拟一套全新的硬件环境，在Docker环境下不虚拟硬件，直接使用宿主机资源（Docker默认不限制CPU，内存资源），也可以直接指定分配某个容器的CPU或内存资源。

（4）虚拟机可以直接与宿主机或局域网连接，分配IP地址（Brige，NAT），Docker容器无法获取IP地址（跟随于宿主机的IP地址）。

> 比如两台Docker都装有Tomcat，要想启动是不能全都映射8080端口的，因为一个宿主Linux及其只能开放一个端口供一个服务使用

（5）镜像相当于是容器的模版，通过镜像创建容器，容器修改后也可提交为镜像，删除容器并不会删除镜像，删除镜像则无法创建容器。

Docker与Docker之间可以互相通信，该过程依赖于宿主机网关。Docker与宿主机之间可以互相通信，外部设备无法直接访问Docker，必须把端口映射给宿主机，因此Docker的端口必须保持在宿主机上的唯一性。

### 3.容器使用注意事项：

- 尽量让一个容器做一件事情，或启动一个服务
- 尽量使用挂载的方式将数据文件挂载到容器中，容器里面尽量不要保存数据。
- 尽量让容器按照Docker化的要求来使用容器，而不是安装一个虚拟机
- 尽量不适用交互模式来直接操作容器，而是在宿主机上执行命令，或者使用Docker File
- 只要能解决问题，搞笑的解决问题，无论怎么样都行



## 二、安装过程

1.确保Linux内核版本在3.x以上，建议使用CentOS 7.x，64位

2.先安装一些必备工具包：

- 安装网络相关命令： `yum install net-tools -y`
- 安装使用工具： `yum install -y yum-utils device-mapper-persistent-data lvm2`

3.配置yum下载源

- 添加yum镜像：`yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo`

![image-20240125150705689](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125150705689.png)

- 更新yum缓存： `yum makecache fast`

这个源是为了用来装docker的

4.安装Docker社区版：

- 安装 docker-ce ：`yum -y install docker-ce`

5.关于Docker服务启停

`systemctl start/stop/restart/status docker`

开启之后可是使用 `docker info` 查看一下信息

6.配置Docker国内镜像

`vi /etc/docker/daemon.json`

或

`vi /etc/docker/daemon.conf`

```
{
  "registry-mirrors": [
	"https://registry.docker-cn.com",		 
	"http://hub-mirror.c.163.com",
    "htpps://docker.mirrors.ustc.edu.cn"
  ]
}
```

这个源是用来为docker拉取镜像的

保存，重启Docker，查看docker info是否生效

> 但是在我CentOS上使用该文件名 daemon.json 开启docker服务，他就会报错，根本不行，只能使用 docker.conf ，但是用了这个文件名，服务确实可以自动，但是使用 docker info 命令查看信息，根本没有任何registry的信息，连docker自带的镜像地址都没有。甚至使用 docker images 结果也是空的



## 几个及其重要的概念：

### 1.镜像（image）：

Docker相关站点事先制作好带有操作系统或应用程序的一个文件包，下载回来后便可以启动Docker运行环境，类似VMware中的一个预先安装好虚拟机的虚拟机文件。自己也可以在自己的私有环境中制作镜像，供别人使用。通常的两个用于下载Docker的知名站点：https://hub.docker.com （速度极慢，不推荐） https://hub.daocloud.io/ （国内镜像，推荐）

`docker pull daocloud.io/library/centos:8.2.2004` 



### 2.容器（Container）：

镜像的具体的可启动的实例：容器要有名称便于唯一区分，如果需要外部访问，则必须映射端口，如果要共享文件夹，还需要做文件映射夹，等等...

`docker create -it --name centos8 -h mycentos8 daocloud.io/libirary/centos8.2.2004`

`docker cintainer ls -a`

### 3.实例

正在运行的容器 ：`docker ps`

交互模式进入 Docker 容器内的命令行 `Docker exec -it centos8 /bin/bash`

### 4.宿主机与容器之间交换文件

docker cp 宿主机文件 容器名:文件路径

### 5.实际操作

> 我们来拉取一个centos8
>
> > `docker pull centos:8` 
> >
> > 后面的参数是  镜像:版本号
>
> ![image-20240125170358919](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125170358919.png)
>
> 当然，我们也可以去上述的两个网站中去下载
>
> 拉取完成之后我们可以使用 `Docker images` 来查看我们拉取了哪些镜像
>
> ![image-20240125171007514](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125171007514.png)
>
> - 创建容器
>
>   - -it 表示以交互模式创建容器
>
>   - --name 指定和这个容器的名称，这是容器的名称，在一台宿主机上要确保唯一性
>
>   - -h 指定该容器的操作系统的主机名（容器的机器名）
>     - -p 映射端口，`-p 外部端口:内部端口`
>
> > eg:
> >
> > `-p 3307:3306`
> >
> > 意思是将容器内部的3306端口映射到宿主机的3307端口上，这个时候我们去访问宿主机的3307端口就可以访问到容器中的MySQL了
>
> 最后指定容器的版本号：如下图
>
> ![](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125171007514.png)
>
> - 版本号
>
> 其版本号由 REPOSITORY+TAG构成
>
> centos:8 或 hello-world:latest 
>
> 最终指令
>
> docker create -it --name centos8 -h mycentos8 -p 3307:3306 centos:8
>
> ![image-20240125182903032](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125182903032.png)
>
> 当出现这么一串随机值，就说明创建容器成功了
>
> 这一串随机值就是该容器的真实编号
>
> - 查看系统内创建的容器
>
> 使用指令 `docker container ls -a `
>
> ![image-20240125183121747](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125183121747.png)
>
> 其内容有 容器编号，镜像...容器名称（就是创建容器时--name指定的名字）
>
> 我们来对容器操作，比如开启，停止，等等都可以用容器名称，或者容器编号的前四，五，六位来指定，为此也是要求容器名称是固定的
>
> - 启动容器
>
> `docker start centos8`
>
> ![image-20240125183816537](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125183816537.png)
>
> 没有报错，说明容器启动成功
>
> - 查看系统内正在启动的容器
>
> `docker ps`
>
> ![image-20240125184007333](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125184007333.png)
>
> - 进入容器
>
> `docker exec -it centos8 /bin/bash`
>
> 其中docker exec表示执行docker里的一条指令 -it 表示 interact terminal 交互终端，以交互模式进入
>
> /bin/bash 时linux下的壳程序，这个就是docker esec所指定的程序
>
> 合起来的意思就是：以交互模式进入centos8的壳程序，将会直接进入centos8的命令行终端
>
> ![image-20240125184931225](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125184931225.png)
>
> 输入命令，进入centos8的命令行终端
>
> 此时我们的用户前端名称就变成了创建容器时 -h 指定的参数（主机名）
>
> [Docker 命令大全 | 菜鸟教程 (runoob.com)](https://www.runoob.com/docker/docker-command-manual.html)
>
> 当我们退出来之后输入 ip addr 就可以看到，系统内多出来一套虚拟网卡
>
> ![image-20240125193335310](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240125193335310.png)
>
> 

## Docker中centos8的问题

21年之后centos8便不再维护镜像源，导致刚装好的centos8容器使用 yum 就会报错

```
Error: Failed to download metadata for repo 'appstream': Cannot prepare internal mirrorlist: No URLs in mirrorlist
```

此时我们需要进行一些操作

```
sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*

sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

yum makecache
```

分别执行上面三句代码就可以解决yum镜像的问题





