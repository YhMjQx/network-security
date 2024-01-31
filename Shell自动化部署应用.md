[TOC]



# ==Shell自动化部署应用==

## 一、基础版：编写一段Shell脚本部署woniusales系统，全自动无人值守实现如下安装（40分）

`vi /opt/install.sh`

**预设前提：全新CentOS最小化安装版，已经有woniusales.war文件和对应的SQL语句，均保存在 /opt 命令下，无其他文件**

#### 1.在线安装 MySQL Community Server 5.6 版本，并确保MySQL服务正常启动（8分）

```
wget -b -O mysql.rpm https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm

rpm -ivh mysql.rpm  #将mysql下载的源安装在 /etc/yum.repos.d/ 目录下

linea=$(grep -n "mysql56-community" /etc/yum.repos.d/mysql-community.repo | awk -F : '{print $1}')

((linea+=3))

sed -i "${linea}c enabled=1" /etc/yum.repos.d/mysql-community.repo

lineb=$(grep -n "mysql80-community" /etc/yum.repos.d/mysql-community.repo | awk -F : '{print $1}')

((lineb+=3))

sed -i "${lineb}c enabled=0" /etc/yum.repos.d/mysql-community.repo

yum install mysql-server -y

systemctl start mysqld
```

- wget -b 参数表示在后台执行，信息不输出到终端
- wget -O 表示下载之后重命名
- 注意sed操作中，如果有变量参与，你们需要将包裹操作的 ' ' 变为 " "
  - `sed -i "${lineb}c enabled=0"`

> 现在我们需要修改 /etc/yum.repos.d/mysql-comnunity.repo 文件中，mysql5.6 版本的enable为1，而其他版本的mysql-server的enable为0。此时不能进入vi界面，因为我们需要全自动，那么就只能使用 sed 和 awk 。
>
> **sed使用方法：**
>
> > （1）a：新增，a 的后面可以接字符串，而这些字符串会在新的一行出现（目前的下一行）
> >
> > （2）c：取代，c的后面可以接字符串，这些字符串可以取代n1,n2 之间的行（按行取代）
> >
> > （3）d：删除，因为是删除，所以 d 后面通常不会接任何字符串
> >
> > （4）i：插入，i的后面可以接字符串，二这些字符串会在新的一行出现（目前的上一行）
> >
> > （5）P：打印，将某个选择的数据印出。通常 p 会与参数 sed -n 一起运行
> >
> > （6）s：取代，可以直接进行取代工作，通常这个 s 的动作可以搭配正则表达式进行（查找替换，正则匹配替换）
>
> 

#### 2.为MySQL创建woniusales数据库并创建可以远程登录的账号，同时为woniusales生成数据(8分)

**注意：此时需要执行语句从而创建数据库和远程登录用户，但这些操作按照以往也是需要进入交互模式的，该怎么办呢**

```
#因mysql5.6默认root用户无密码，故使用 mysql -uroot -e " " ，引号内执行语句即可
mysql -uroot -e "use mysql;"
mysql -uroot -e "create database woniusales character set utf8 collate utf8_general_ci;"
mysql -uroot -e "create user remote@'%' identified by 'p-0p-0p-0';"
mysql -uroot -e "grant all priveleges on woniusales.* to remote@'%';"
mysql -uroot -e "source woniusales.sql"

```

> 但是就算mysql5.6可以这样登录，那要是换成mysql5.7呢，mysql5.7是默认拥有密码的，又该怎么操作？
>
> - 先找到默认密码，进入mysql，修改root默认密码，再执行上述操作

#### 3.解压Tomcat到/opt/tomcat目录，并修改端口为8088，启动服务并测试网站是否正常(8分)

```
#下载java，注意版本
#配置java环境变量，每次开启都生效
#下载tomcat，并配置
#使用curl来测试网站是否正常

```



#### 4.如果Tomcat成功启动，则部署woniusales.war到Tomcat的webapps目录中，同时修改woniusales的数据库连接信息(8分)

```
先判断tomcat是否启动成功
mv /opt/woniusales.war /opt/tomcat/webapps/
/opt/tomcat/bin/startup.sh
rm -f /opt/tomcat/webapps/woniusales/WEB_INF/classes/db.profiles
vi /opt/tomcat/webapps/woniusales/WEB_INF/classes/db.profiles
输入：
db_url=jdbc:mysql://localhost:3306/woniusales?useUnicode=true&characterEncoding=utf8 
db_username=root
db_password=p-0p-0p-0
db_driver=com.mysql.jdbc.Driver
保存退出,重启 tomcat
/opt/tomcat/bin/shutdown.sh
/opt/tomcat/bin/startup.sh
```



#### 5.使用curl命令访问woniusales，并通过curl发送Post请求登录到系统中，验证登录是否成功(8分)

```
curl -d "username=admin&password=admin123&verifycode=0000" http://192.168.230.147:8083/woniusales/user/login
```



**要求:Shell脚本必须有中文注释，同时，将上述作过程中，每一个关键步骤的日志，以中文信息输出到/opt/woniusales.log文件中(上述5题如果没有输出脚本操作日志或者没有写好中文注释，最高可扣10分)**

最终执行代码

```
rpm -qa | grep mysql-community-server 1> /dev/null 2> /dev/null
if [ $? -eq 0 ]; then
	echo "MySQL数据库已经安装" | tee -a /opt/mysqlinstall.log
else
	echo "MySQL数据库没有安装，准备安装" | tee -a /opt/mysqlinstall.log

	yum install wget -y 1> /dev/null
	slepp 7
	
	wget -b -O mysql.rpm https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm 1> /dev/null
	slepp 7
	
	rpm -ivh mysql.rpm 1> /dev/null
	slepp 3
	
	linea=$(grep -n "mysql56-community" /etc/yum.repos.d/mysql-community.repo | awk -F : '{print $1}')
	((linea+=3))
	sed -i "${linea}c enabled=1" /etc/yum.repos.d/mysql-community.repo

	lineb=$(grep -n "mysql80-community" /etc/yum.repos.d/mysql-community.repo | awk -F : '{print $1}')
	((lineb+=3))
	sed -i "${lineb}c enabled=0" /etc/yum.repos.d/mysql-community.repo
	echo "MySQL数据库源配置完成，开始安装" | tee -a /opt/mysqlinstall.log

	yum install mysql-server -y 1> /dev/null
	slepp 30
	systemctl list-unit-files | grep mysqld
	if [ $? -eq 0 ]; then 
		echo "MySQL数据库安装成功" | tee -a /opt/mysqlinstall.log
		systemctl start mysqld 1> /dev/null
		echo "MySQL数据库打开成功" | tee -a /opt/mysqlinstall.log
	else
		echo "MySQL数据库安装失败" | tee -a /opt/mysqlinstall.log
		exit 1
	fi
	
fi

systemctl list-unit-files | grep mysqld
if [$? -eq 0]; then
	mysql -uroot -e "use mysql;" 1> /dev/null 2> /dev/null
	mysql -uroot -e "create database woniusales character set utf8 collate utf8_general_ci;" 1> /dev/null 2> /dev/null
	echo "woniusales数据库创建完成" | tee -a /opt/woniusalesinstall.log 
	
	mysql -uroot -e "create user remote@'%' identified by 'p-0p-0p-0';" 1> /dev/null 2> /dev/null
	mysql -uroot -e "grant all priveleges on woniusales.* to remote@'%';" 1> /dev/null 2> /dev/null
	echo "woniusales远程用户创建完成" | tee -a /opt/woniusalesinstall.log 
	
	mysql -uroot -e "source woniusales.sql" 1> /dev/null 2> /dev/null
	echo "woniusales数据库数据插入成功" | tee -a /opt/woniusalesinstall.log 
else
	echo "MySQL数据库安装失败" | tee -a /opt/mysqlinstall.log
	exit 1;
	
	
```

这里只展示到配置tomcat之前，即安装配置好数据库



> ## 二、进阶版:编写一段Shell脚本部署WoniuNote系统，全自动无人值守实现如下功能:(60分)
>
> **预设前提:全新Cent0S最小化安装版，已经有woniunote.zip文件，和对应的数据库SQL语句，均保存于/opt目录下，无其他文件**
>
> 1.在线安装MySQL Community Server 5.7版本，并确保MySQL服务正常启动，同时修改root的密码为MyPass12!! (10分)
>
> 2.为MySQL创建woniunote数据库并创建可以远程登录的账号，同时为woniunote生成数据(6分)
>
> 3.在线安装PHP 7.3版本并配置环境变量和www账号，完成后启动php-fpm服务，用于与Nginx进行通信(10分)
>
> 4.从Nginx官网自动下载最新版本Nginx，并进行源码安装(不要求LuaJIT等额外模块)，测试Nginx是否安装成功(8分)
>
> 5.解压woniunote.zip文件到/www/web目录，修改woniunote与数据库的连接信息，确保可以正常连接到数据库(8分)
>
> 6.配置Nginx与PHP的连接，将默认首页指向/www/web/woniunote/public，并确保nginx.conf配置文件支持URL重定向(8分)
>
> 7.使用curl命令访问woniunote，并将成功与否的测试结果以及上述操作步骤的日志信息发送到你的QQ邮箱(10分)
>
> **要求:Shell脚本必须有中文注释，同时，将上述操作过程中，每一个关键步骤的日志，以中文信息输出到/opt/woniunote.log文件中(上述7题如果没有**
> **输出脚本操作日志或者没有写好中文注释，最高可扣10分)**