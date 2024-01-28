[TOC]

# ==Docker化运行和部署环境==

## Docker化运行方式

一般去 https://hub.daocloud.io/ ，实在不行 可以翻墙去https://hub.docker.com 这两个网站去寻找有用的docker镜像，去寻找别人已经配置好的，然后去拉取镜像，利用此镜像配置容器

### 每一个Docker解决一个问题



针对woniusales的环境配置，分三步：

#### 配置mysql容器

- 下载一个包含MySQL5.6的Docker镜像，并映射端口3306，再启动即可

去 daocloud 官网寻找mysql5.6的资源，确定好版本号及其他，然后拉取镜像

```
docker pull daocloud.io/library/mysql:5.6.36
docker pull mysql:5.6.36
```

![image-20240128204813621](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240128204813621.png)

镜像拉取成功之后配置容器

```
docker create -it --name mysql5.6 -h mymysql56 -p 3309:3306 -e MYSQL_ROOT_PASSWORD=p-0p-0p-0 mysql:5.6.36

docker start mysql5.6
```

![image-20240128204849555](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240128204849555.png)

使用navicat连接一下，使用root用户以及-e参数设置的mysql环境变量的root用户的密码。连接成功以后创建woniusales数据库并运行对应的sql文件。

![image-20240128205021783](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240128205021783.png)

#### 配置tomcat容器

- 下载一个包含Tomcat 8.0的Docker镜像，并映射端口8080，再启动即可

一样的还是去对应的网站中去寻找对应的版本镜像,woniusales 基于tomcat8.0和jre8的版本

```
docker pull daocloud.io/library/tomcat:8.0.45-jre8-alpine
或
docker pull tomcat:8.0.23-jre8

```

在这里使用 **容器挂载宿主机,参数 -v** 的方式来访问数据。即：宿主机上创建webapps目录，然后将其挂载到tomcat的docker中的用来部署服务器应用的目录内

```
mkdir /opt/webapps

cp /opt/usr/local/tomcat/webapps /opt/webapps/woniusales.war

docker create -it --name tomcat8.0 -h mytomcat -p 8083:8080 -v /opt/webapps/:/usr/local/tomcat/webapps daocloud.io/library/tomcat:8.0.45-jre8-alpine

docker start tomcat8.0
```

`-v /opt/webapps/:/usr/local/tomcat/webapps ` 表示将 /opt/webapps/ 目录下的文件都挂载到 tomcat的docker容器的 /usr/local/tomcat/webapps 目录下。挂载好之后，宿主机的 /opt/webapps/ 目录下的内容和 容器的 /usr/local/tomcat/webapps 目录下的内容是同步的，修改其中任何一个都会同时进行修改

![image-20240128212954652](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240128212954652.png)

看，原本该目录下只有woniusales.war文件，但是当我把目录挂载好，并创建和开启tomcat8.0容器之后，就会帮我自动解压woniusales.war并同步到宿主机上

#### 修改tomcat容器上服务器应用对数据库的连接信息

- 在Tomcat的Docker中配置woniusales和数据库连接信息重启Docker，完成配置

由于挂载后的目录，宿主机和容器内文件是同步，因此我们只需要在宿主机中直接修改即可，然后重启tomcat8.0容器

**注意：此时mysql和tomcat分开了，此时的配置信息就需要进行修改一下，我们需要使用mysql5.6容器的ip地址，而不再是localhost了。这里就是容器与容器之间互相访问**

- 进入mysql5.6的容器，查看ip地址，结果为 172.17.0.2

![image-20240128213820716](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240128213820716.png)

- 修改tomcat容器上服务器应用对数据库的连接信息如下

```
db_url=jdbc:mysql://172.17.0.2:3306/woniusales?useUnicode=true&characterEncoding=utf8
db_username=root
db_password=p-0p-0p-0
db_driver=com.mysql.jdbc.Driver
```

这里的密码就是我们创建mysql5.6容器时，使用 -e 参数指定的环境变量 `-e MYSQL_ROOT_PASSWORD=p-0p-0p-0`

- 重启tomcat容器

```
docker stop tomcat8.0

docker start tomcat8.0
```

现在去访问 192.168.230.147:8083/woniusales 即可成功

![image-20240128214116776](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240128214116776.png)

但是此时并无法直接访问 192.168.230.147:8083 页面，因为没有默认页面了

### 此过程解决了以下问题

- 一个容器做一件事情
- 数据库容器可以使用 -e 参数指定数据库root用户的环境变量密码 `-e MYSQL_ROOT_PASSWORD=p-0p-0p-0`
- -v 参数 实现目录挂载，宿主机的目录映射到容器中的目录，且挂载的目录中的内容都是同步的
- 容器与容器之间的互访，这里指的是 tomcat 容器 访问 mysql5.6 的数据库

## Docker  File

Docker File 批处理文件