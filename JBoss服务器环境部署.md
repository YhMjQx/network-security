[TOC]



# ==JBoss服务器环境部署==

## 一、JBoss的安装与配置

JBoss是一个JAVA的应用服务器，由RedHat拥有，由专业版和社区版，与Tomcat功能类似，默认情况下也使用80端口，部署方式也比较像。针对Java的应用服务器：Tomcat、JBoss、Weblogic（Oracle所有）、Webshpere（IBM公司所有）、Resin、apusic（金蝶）等都实现了JavaEE的标准

### 1.JBoss版本：

- Application Server：JBoss AS，更新到了7版本不再更新，截止到2012年
- Wildfly：持续更新，目前最新版本24。https://www.wildfly.org/downloads/
- JBoss EAP：https://developers.redhat.com/products/eap/overview?referrer=jbd

### 2.安装

#### （1）安装并配置JAVA

##### 1.上传文件并解压

这里我们需要的是java1.8的版本，下载好了之后将 压缩包放在 /usr/java 目录下 该目录是我们自己创建的。然后直接解压 `tar -zvxf jdk-8u161-linux-x64.tar.gz ` 就好了

![image-20240120213359740](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120213359740.png)

##### 2.配置环境变量

在 Linux 中，原本可以直接使用 export 命令使得直接配置环境变量，但这样的效果只是一次性的，下一次开机的时候，环境变量就会消失，于是我们选择在每次开机时，都会自动执行的一个文件中加入指令 

在 ~/.bash_profile 文件中 加入以下两条指令：

```
export JAVA_HOME=/usr/java/jdk1.8.0_161
PATH=$JAVA_HOME/bin
```

**注意：PATH之间是使用 : 分隔的**

配置好之后使用命令 `source .bash_profile ` 使得配置立刻生效

##### 3.查看环境变量设置和java命令使用是否成功

- 环境变量查看 ，使用命令 env

![image-20240120214303214](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120214303214.png)

- 查看java是否可以成功使用

```
java -version
```

![image-20240120214340333](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240120214340333.png)

#### （2）安装并配置JBoss

```
unzip wildfly-14.0.0.Final.zip -d /opt/
```

将其解压在 /opt/ 目录下

```
cd wildfly-14.0.0.Final/bin
```

![image-20240124143142928](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124143142928.png)

/opt/wildfly-14.0.0.Final/bin/standalone.sh 就是Linux设备上的开启文件

```
./standalone.sh 
```

我们查看一下开启进程

```
netstat -anlp | grep 8080
```

![image-20240124144245317](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124144245317.png)

由于该JBoss默认端口是8080，因此此时还需要开始防火墙

```
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --reload
```

我们现在去访问 192.168.230.147:8080 

![image-20240124144737895](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124144737895.png)

发现访问失败，我们去找找缘由

![image-20240124144711916](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124144711916.png)

好家伙，原来是 **JBoss默认只能本机访问，只绑定了127.0.0.1**，该问题需要

使用以下指令使其开启时绑定其他IP，可以远程访问

```
#在 /opt/wildfly/bin 执行
./standalone.sh -b 0.0.0.0
```

![image-20240124145139330](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124145139330.png)

然后现在就可以访问成功了

## 二、JBoss上搭建woniusales 

### 1、在 Jboss 文件中搭建woniusales文件

- **把woniusales.war 上传至 /opt/wildfly-14.0.1.Final/standalone/deployments 目录下**

```
mv /opt/woniusales-20180508-V1.4.war /opt/wildfly-14.0.1.Final/standalone/deployments/woniusales.war
```

- **搭建woniusales数据库**

```
mysql -uroot -p  #紧接着数据mysql5.7的密码P-0p-0P-0p-0

create database woniusales character set utf8 collate utf8_general_ci;

create user remote@'%' identified by 'P-0p-0P-0p-0';  #创建 远程连接用户remote使得navicat连接操作数据库 woniusales 以便运行SQL文件

grant all priveleges on woniusales.* to remote@'%';  #授权用户 remote 拥有 woniusales 数据库的所有权限

#可以使用以下命令查看用户是否创建成功：
use mysql
select User,Host,authentication_string from user;

如果要删除某个用户，可使用以下命令:
drop user remote@'%';
如果要收回权限，如DELETE或UPDATE或ALL，下述命令收回所有权限：
REVOKE ALL on woniunote.* FROM remote@'%';
```

但是，使用remote用户远程连接navicat时，给woniusales运行SQL文件时遇到了一个错误

![image-20240124152321012](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124152321012.png)

![image-20240124152523941](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124152523941.png)

这是因为mysql5.7相较于mysql5.6使用了更加严格的策略

> 时间戳报错
> 表设计如上图所示，而timestamp类型对应日期范围为：1970-01-01 00:00:01 ~ 2037-12-31 23:59:5，因为导入的表字段update_time默认值不在该区间内，所以报错。
> 且由于在Mysql5.7之后，Mysql使用的是严格模式，sql_mode默认配置为: ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, NO_ENGINE_SUBSTITUTION
> 而在Navicat中使用select @@sql_mode查看远程数据库的sql_mode为空。

解决办法：修改mysql配置文件 /etc/my.cnf 

```
在[mysqld]模块下，添加如下语句
sql_mode=ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
然后重启mysqld
```

![image-20240124152728923](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124152728923.png)

现在就好了

- **配置好数据库之后，去尝试打开JBoss并访问**

我们先不急着去修改数据库连接权限，因为此时还没有打开JBoss帮我们自动解压woniusales.war，我们无法访问woniusales这个文件夹

```
./opt/wildfly/bin/stadalone.sh -b 0.0.0.0
```

我靠，发现一大堆错

![image-20240124153643342](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124153643342.png)

我们仔细去分析一下发现了有用的信息

```
Caused by: java.lang.NoClassDefFoundError: Failed to link com/alibaba/druid/support/spring/stat/DruidStatInterceptor (Module "deployment.woniusales.war" from Service Module Loader): org/aopalliance/intercept/MethodInterceptor
```

```
15:30:19,163 ERROR [org.jboss.as.controller.management-operation] (Controller Boot Thread) WFLYCTL0013: Operation ("deploy") failed - address: ([("deployment" => "woniusales.war")]) - failure description: {"WFLYCTL0080: Failed services" => {"jboss.deployment.unit.\"woniusales.war\".POST_MODULE" => "WFLYSRV0153: Failed to process phase POST_MODULE of deployment \"woniusales.war\"
    Caused by: java.lang.NoClassDefFoundError: Failed to link com/alibaba/druid/support/spring/stat/DruidStatInterceptor (Module \"deployment.woniusales.war\" from Service Module Loader): org/aopalliance/intercept/MethodInterceptor"}}

```



因为woniusales使用了一个alibaba数据库连接池的一个库文件，在woniusales/WEB_INF/lib 目录下有很多 jar 包，但还是缺少了一部分,该错误只是因为缺少了一个jar包引起的

![image-20240124153944336](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124153944336.png)

那为什么之前在Tomcat上搭建woniusales就没问题呢？那是因为Tomcat本身就集成了所需要的那些 jar 包，因此可以自动运行。那到底缺少了哪些 jar 包呢

> 连接池的作用：
>
> 可以使得我们在使用完数据库之后不用频繁关闭打开，连接池会为我们保留连接，提高数据库之间传输的效率

```
aopalliance.jar
spring-aop-3.2.0.RELEAES.jar
spring-beans-3.2.0.RELEAES.jar
spring-core-3.2.0.RELEAES.jar
```

找到这些 jar 包之后放进 woniusales/WEB_INF/lib 目录中

![image-20240124160238206](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124160238206.png)

然后删掉Linux之前上传的woniusales，把这个新的上传进去

传好之后，重新开启JBoss

终于没报错了

![image-20240124161709732](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124161709732.png)

也是终于访问成功了

现在我们返回到 /opt/wildfly/standalone/deployments 目录下，去看看woniusales是否解压成功

OK，只有解压的文件

![image-20240124173711450](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124173711450.png)

还记得之前没有处理好的woniusales数据库连接信息的问题吗，现在这样子也是没办法处理了，我们只能将woniusales文件拿到Windows系统上去修改 db.prorerties 文件

```
db_url=jdbc:mysql://localhost:3306/woniusales?useUnicode=true&characterEncoding=utf8 
db_username=root
db_password=P-0p-0P-0p-0
db_driver=com.mysql.jdbc.Driver
```

> 当然，如果不处理这个问题的话，woniusales是连接不上数据库的，如果这个时候直接去访问就会报错
>
> ![image-20240124174226210](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124174226210.png)
>
> 

所以，现在将Linux中的原先的woniusales*文件都删掉，将修改好的woniusales重新上传到 /opt/wildfly-14.0.1.Final/standalone/deployments，并重命名为woniusales.war

重新开启JBoss： `/opt/wildfly/bin/standalone -b 0.0.0.0`

基本上，不出意外的话，到这就部署完成了。但如果你也遇到了上面图片所描述的forbidden，那就真的不知道该怎么办了我所用的数据库时mysql5.7版本，JBoss的部署和配置肯定是没问题的，因为我访问JBoss不管是直接访问IP地址加端口还是访问控制台页面都没问题。但是都在访问woniusales的时候出了问题，页面全都是forbidden，我认为应该是数据库层面的问题，尝试一下使用mysql5.6作为数据库就知道是不是这样了



### 2、使用 JBoss 管理员权限，在网页端搭建

#### 1.启动JBoss，查看 Admin Console的信息

```
17:55:00,413 INFO  [org.jboss.as] (Controller Boot Thread) WFLYSRV0060: Http management interface listening on http://127.0.0.1:9990/management
17:55:00,413 INFO  [org.jboss.as] (Controller Boot Thread) WFLYSRV0051: Admin console listening on http://127.0.0.1:9990

```

上述信息表示：Admin Console 不支持与远程访问，绑定的端口时9990

#### 2.使用以下命令启动JBoss

```
firewall-cmd --add-port=9990/tcp --permanent
firewall-cmd --reload
./standalone -b 0.0.0.0 -bmanagement 0.0.0.0
```



#### 3.添加管理控制台用户：

```
在bin目录下执行： ./add-user.sh
```

按所提示的问题输入信息

然后重新开启JBoss

![image-20240124182507018](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124182507018.png)

即可看到控制台页面



## 四、tomcat的管理控制台

其实tomcat也有类似的功能，我们先去 /opt/tomcat/conf/tomcat-user.xml 文件中去找用户和登录密码，然后去tomcat的管理控制台

![image-20240124183841980](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124183841980.png)

![image-20240124183844468](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124183844468.png)

但这些用户呢都是默认被注释掉的，所以我们在该文件自己添加一个用户

![image-20240124183943883](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124183943883.png)

把这段信息添加进该文件的用户信息下面

然后重启tomcat就可以了

![image-20240124184123019](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124184123019.png)

![image-20240124184151921](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240124184151921.png)