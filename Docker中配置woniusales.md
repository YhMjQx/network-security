[TOC]



# ==Docker中配置woniusales==

> 如果有不想要的容器可以使用  `docker rm 容器名(或id)`
>
> 如果有不想要的镜像，使用 `docker rmi 镜像名`
>
> 查看linux版本：`uname -a` 或 `cat/etc/redhat-release`
>
> 利用run命令一次性处理： run = create + start
>
> 创建并直接启动容器：`docker run -it --name centos8 -h mycentos8 -p 3307:3306 centos:8`
>
> 创建并启动容器且退出容器时不保存数据 ：`docker run ... --rm` --rm 参数表示退出容器时不保存数据
>
> 

## 一、创建符合环境的容器

### 1.拉取镜像

```
docker pull centos:centos.7.2009

```

### 2.创建容器

```
[root@mycentos ~]# docker run -it --name centos7 -h mycentos7 -p 3307:3306 -p 8081:8080 centos:centos.7.2009
[root@mycentos7 /]# 

等价于
docker create -it --name centos7 -h mycentos7 -p 3307:3306 -p 8081:8080 centos:centos.7.2009
docker start centos7
docker exec -it centos7 /bin/bash 
这三条命令结合使用
```

该命令执行之后就会直接进入该容器，该命令相当于将create+start+exec

## 二、tomcat上搭建woniusales

### 安装和配置MySQL5.6

#### 1.安装mysql5.6

```
方法一：
直接在docker容器中执行如下命令：
yum install wget -y

wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm

方法二：
将宿主机的rpm包复制到容器中,在宿主机中执行如下语句
docker cp /opt/mysql-community-release-el7-5.noarch.rpm centos7:/opt/

docker容器中有了rpm包之后，就在docker容器中进行操作就好了

rpm -ivh /opt/mysql-community-release-el7-5.noarch.rpm

vi /etc/yum.repos.d/mysql.community.repo  #将mysql下载版本5.6的enable设置为1

yum install mysql-server
```

##### 报错

当我们安装完成mysql5.6时，使用 `systemctl status mysqld` 来查看服务状态，发现报错 ：操作不被允许？？？

```
Failed to get D-Bus connection: Operation not permitted

```

去网上查了一下，原因是：

> 按照我们普通的拉取镜像，创建容器并开启和进入容器的方式是以普通创建的，默认配置下，Docker不具备一台独立主机的所有功能，此时的容器没有特权模式的操作，需要使用特权模式来解决。
>
> 一般情况下我们是不会这么容器去使用特权模式的
>
> 因为特权模式的容器可能会对宿主机造成影响

##### 解决办法

使用特权模式，该方法需要独立新建一个容器

```
创建容器：
docker create -ti --name centos7 -h mycentos7  -p 3307:3306 -p 8081:8080 --privileged=true centos:centos.7.2009 /sbin/init

开启容器：
docker start centos7

进入容器：
docker exec -it centos7 /bin/bash
```

> **注意：在创建容器时，目录这个参数一定要放在最后，否则就会报错**
>
> ```
> docker: invalid reference format.
> See 'docker run --help'.
> ```

现在按照上面的方式重新安装mysql就可以了

#### 2.配置mysql

- 创建woniusales数据库

- 创建远程连接用户，只拥有woniusales数据库的所有权限

```
#床建数据库
create database woniusales character set utf8 collate utf8_general_ci;

#创建远程连接用户以供navicat连接
create user remote@'%' identified by 'p-0p-0p-0';

#赋予远程连接用户的所有woniusales的权限
grant all privileges on woniusales.* to remote@'%';
```

- naviccat运行SQL文件，插入数据

### 配置woniusales数据库连接信息

将woniusales.war包放在/opt/apache-tomcat-8.0.53/webapps/ 目录下。重启tomcat，此时tomcat就会自动加压war包

- 此时修改 /opt/apache-tomcat-8.0.53/webapps/woniusales/WEB-INF/classes/db.properties文件 中的数据库连接信息即可



现在就可以访问了