[TOC]



# ==Tomcat下配置WoniuSales==

![image-20240120215949651](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120215949651.png)

这样就形成了服务器环境和数据库环境。目前相对而言，Nginx会更比Apache实用度更好，也更受欢迎

## 一、搭建java环境

### 1.上传文件并解压

这里我们需要的是java1.8的版本，下载好了之后将 压缩包放在 /usr/java 目录下 该目录是我们自己创建的。然后直接解压 `tar -zvxf jdk-8u161-linux-x64.tar.gz ` 就好了

![image-20240120213359740](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120213359740.png)

### 2.配置环境变量

在 Linux 中，原本可以直接使用 export 命令使得直接配置环境变量，但这样的效果只是一次性的，下一次开机的时候，环境变量就会消失，于是我们选择在每次开机时，都会自动执行的一个文件中加入指令 

在 ~/.bash_profile 文件中 加入以下两条指令：

```
export JAVA_HOME=/usr/java/jdk1.8.0_161
PATH=$JAVA_HOME/bin
```

**注意：PATH之间是使用 : 分隔的**

配置好之后使用命令 `source .bash_profile ` 使得配置立刻生效

### 3.查看环境变量设置和java命令使用是否成功

- 环境变量查看 ，使用命令 env

![image-20240120214303214](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120214303214.png)

- 查看java是否可以成功使用

```
java -version
```

![image-20240120214340333](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120214340333.png)

## 二、安装Tomcat

### 1.上传文件至 /opt 目录

![image-20240120220809081](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120220809081.png)

### 2.直接解压即可

![image-20240120220918914](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120220918914.png)

### 3.查看配置信息

Tomcat的核心配置文件在  /opt/apache-tomcat-8.0.53/conf/server.xml 中

![image-20240120221011266](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120221011266.png)

> **注意：.xml 语法中 <!--           -->  中间包裹的信息都是被注释掉的**

进入文件，我们可以看到，只有中间一块没有被注释

![image-20240120221543272](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120221543272.png)

这短信息表名了 Tomcat 连接时，默认的端口时 8080

于是要想访问 Tomcat 就需要开启 8080端口

`firewall-cmd --add-port=8080/tcp --permanent`

### 4.启动Tomcat

- /opt/apache-tomcat-8.0.53/bin/shutdown.sh  （关闭Tomcat）
- /opt/apache-tomcat-8.0.53/bin/startup.sh  （启动Tomcat）

![image-20240120222535640](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120222535640.png)

### 5.访问 192.168.230.147:8080

![image-20240120222713222](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120222713222.png)

## 三、配置woniusales数据库

### （1）Tomcat中配置woniusales

> 因为在这里，Tomcat就起到了和Xampp类似的作用（即作为一个载体），所以需要将woniusales配置在Tomcat中。
>
> 这里的woniusales是一个web应用程序，我们看他的文件结尾就是 .war 这是一个标准的web 应用程序的归档文件，Linux中使用unzip就可以解开

#### 1.查看 /opt/apache-tomcat-8.0.53/conf/server.xml 文件

其内部有一个策略 叫 appBase

![image-20240120225023976](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120225023976.png)

```
      <Host name="localhost"  appBase="webapps"
            unpackWARs="true" autoDeploy="true">
            
host name 表示 服务器域名
appBase相当于xampp中的htdocs，就是部署在其上的应用程序的根目录
unpackWARs="true"表示可以自动解压war包
autoDeploy="true"表示可以自动部署应用程序
```

#### 2.将woniusales文件上传并解压好之后，存放在 /opt/apache-tomcat-8.0.53/webapps 中即可，他会自动帮我们解压并部署

> 值得注意的是，我们这个war包的文件名太长了，我们要访问在网页端访问应用程序的话难免会输入这么长一串，很不符合用户需求，因此为了避免在webapps目录下他会帮我们自动解压，我们现将war包放在opt目录下，然后移动到webapps目录下并重命名为 woniusales.war 这样，自动解压之后就变成了woniusales，我们访问时直接输入woniusales即可

![image-20240120230104973](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120230104973.png)

如图所示，将该war包移动到webapps目录下就会自动被解压和部署

现在去尝试访问，页面就会如下

![image-20240120230252366](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120230252366.png)

### （2）远程连接navicat并导入数据信息

#### 1.mysql中创建远程连接用户

```
GRANT ALL PRIVILEGES ON *.* TO 'remote'@'%' IDENTIFIED BY 'P-0P-0P-0' WITH GRANT OPTION;
flush privileges;
```

#### 2.使用navicat远程连接，并创建数据库和导入信息

- navicat远程连接

![image-20240120223507114](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120223507114.png)

- 创建数据库，并导入信息

![image-20240120223546636](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120223546636.png)

![image-20240120223615589](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120223615589.png)

> 因为这个sql文件只有68k，因此不需要修改 /opt/lampp/etc/my.cnf 文件中的 max_allowed_packet 值

现在就成功导入了数据库信息

![image-20240120223844472](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120223844472.png)



## 四、配置Tomcat与mysql进行连接

![image-20240120230252366](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120230252366.png)

上图中的情况类似于，mysql配置好了，PHPMyAdmin配置好了，但是他俩没有连好

，所以访问不了。在这里就是因为Tomcat（woniusales）配好了，mysql配好了，但是没有连接成功，所以访问不了

**开始配置**

进入woniusales目录中，配置与数据库的连接信息：修改 /opt/apache-tomcat-8.0.53/webapps/woniusales/WEB-INF/classes/db.properties 文件，确认MySQL连接信息和数据库名称

![image-20240120231631060](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120231631060.png)

然后重启Tomcat

```
关闭：/opt/apache-tomcat-8.0.53/bin/shutdown.sh 
开启：/opt/apache-tomcat-8.0.53/bin/startup.sh 
```

重新访问

![image-20240120231852277](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120231852277.png)

ok，拿下！
