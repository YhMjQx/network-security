# ==Docker基础命令与应用==

1.Docker各个应用场景

2.Python+Paramiko实现远程操作

3.Jenkins的Freestyle, Pipline



Docker的特性与虚拟机的异同：
1.安装虚拟机软件如：VMware，在此虚拟机软件上安装操作系统（下载），把操作系统文件进行备份（可以使用快照），随时复制并启动该操作系统。

2.在Linux上安装Docker应用程序，从镜像仓库拉取（Pull）操作系统或应用环境，基于该镜像文件创建一个容器（运行环境），备份容器以供下次使用（直接export容器，将容器提交（commit）为本地镜像）

3.虚拟机环境直接完整模拟一套全新的硬件环境，Docker环境不虚拟硬件，直接使用宿主物理机资源（Docker默认下不限制CPU，内存资源），也可以直接指定分配某个容器的CPU或内存资源

4.虚拟机可以直接与宿主机或局域网连接，分配IP地址（Bridge，NAT），Docker容器无法获取IP地址）（跟随于宿主机的IP地址）



### 安装Docker：

```
1.安装网络相关命令: yum install net-tools

2.安装实用工具: yum install -y yum-utils device-mapper-persistent-data lvm2

3.添加yum镜像:yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

4.更新yum缓存: yum makecache fast

5.安装docker-ce: yum -y install docker-ce

6.启动docker服务: systemctl start docker,
对应的还有stop，restart等

7.查看docker信息: docker info

8.查找centos可用镜像: docker search centos

9.镜像仓库地址: https://hub.docker.com    https: //hub.daocloud.io

10.注意事项:建议在CentoS 7版本上安装Dcker，，确保有足够的硬盘空间，确保内存和CPU资源足够。

11.查看Docker服务，systemctl list-unit-files | grep docker ，如果显示 disable，表名docker不是自启动，可以使用 systemctl enable docker
```



### 快速验证安装是否成功：

```
这里的 hello-world是镜像的名称和容器的名称 
1.搜索镜像: docker search hello-world
2.拉取镜像: docker pull hello-world:版本  默认情况下，会拉取最新版本镜像，如果需要拉取指定版本，则必须指定TAC标签
9.给镜像创建容器：docker create --name hello-docker hello-world:版本
3.运行镜像: dockerrun hello-world
4.查看镜像: docker images
5.查看容器: docker ps, docker container ls -a
6.启停容器: docker start/stop/restart hello-world (容器名)
7.删除容器: docker rm 容器名 (可通过container ls -a查看)
8.删除镜像: docker rmi helld-world

直接创建并运行容器用run，相当于把create和start合在一起使用了
docker run --name hello-first-docker hello-world
```



### 安装MySQL 5.6

```
1.从docker hub上拉取镜像: docker pull mysql:5.6.46

2.从daocloud上拉取镜像: docker pull daocloud.io/library/mysql:5.6.22

3.创建一个容器，并指定容器名称和主机名: docker create --name mysgl-5.6 -h mysgl56 daocloud.io/library/mysql:5.6,22
(可以理解为复制了一台虚拟机过来)

4.列出所有容器: docker container ls -a

5.查看目前正在运行的容器: docker ps

6.启动容器: docker start mysg1-5.6  (可以理解为启动了一个虚拟机的概念)，此时可通过docker ps查看容器启动状态

7.重新建并启动：docker run --name mysql-5.6 -e MYSQL_ROOT_PASSWORD=123456 -d daocloud.io/library/mysql:5.6.22

8.删除一个容器:docker rm mysq1-5.6

9.添加端口映射:
/var/lib/docker/containers/[hash_of_the_container]/hostconfig.json  修改为： "PortBindings":{"80/tcp":[{"HostIp":"","HostPort":"8080"}]}
并确认: ExposedPorts":["3306/tcp":[}} 在config.v2.json 文件中。

10.，停止容器: docker stop mysql-5.6，重启docker服务: systemctl restart docker，重启容器。
```

