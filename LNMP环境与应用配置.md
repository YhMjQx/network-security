[TOC]



# ==LNMP环境与应用配置==

整个woniunote系统的所有者是www:www，但是woniunote连接数据库时使用的权限又是root@localhost

然后woniunote与nginx联动，因为nginx的默认访问DocumentRoot是woniunote/Public，然后MySQL又和woniunote联动，因为woniunote访问了MySQL。所以间接的形成了 LNM 环境。

至于PHP环境是如何与这三个环境联动形成LNMP的我就不太理解了

## 一、安装配置mysql5.7

### 1.下载源，安装源，查询默认密码，修改默认密码

```
下载源：wget http://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
安装源：rpm -ivh mysql57-community-release-el7-8.noarch.rpm

编辑：/etc/yum.repos.d/mysql-community.repo,确保 5.7 版本 enabled=1

在线安装：

yum install mysql-server

启动MySQL服务： systemctl start mysqld
查看MySQL服务： systemctl status mysqld

#mysql5.7安装完成之后，在 /var/log/mysqld.log 文件中给root生成了一个默认密码.找到root默认密码。#然后登录mysql进行修改：
grep "temporary password" /var/log/mysqld.log

#会有以下信息：
#2024-01-23T05:11:28.224807Z 1 [Note] A temporary password is generated for #root@localhost: 7)?&yBo1oa?f

#此时7)?&yBo1oa?f就是mysql5.7生成的默认密码，使用改密码登录mysql再去修改mysql用户密码，不修改默认#密码是无法使用mysql的。不过此时需要注意，mysql5.7版本对密码有强制密码策略
#密码长度至少为8位
#必须要有大小写特殊符号

set password for root@localhost = password('P-0p-0P-0p-0');
或
ALTER USER root@localhost IDENTIFIED BY 'P-0p-0P-0p-0';

#现在就好了


```

> 安装过程中可能遇到以下问题
>
> ```
> mysql-community-server-5.7.44-1.el7.x86_64.rpm 的公钥尚未安装
> 
> 
>  失败的软件包是：mysql-community-server-5.7.44-1.el7.x86_64
>  GPG  密钥配置为：file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
>  
>  请使用：
>  rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
>  可能是MySQL GPG 密钥已过期导致，改一下密钥。
> ```
>
> ```
> mysql> use mysql;
> ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
> mysql> set password for root@localhost = password('YhMjQx521134');
> ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
> 
> 上面两条错误表示你使用默认密码进入mysql之后必须要先修改默认密码，且密码必须符合密码安全策略
> ```
>
> 

### 2.mysql5.7密码策略

修改默认密码时需注意，在mysql5.7版本中，数据库密码被强制要求了密码强度必须包含大小写和特殊字符且长度不能少于8位，弱密码不能使用

通过mysql环境变量可以查看密码策略相关信息： `mysql> show variables like '%password%';`

```
+----------------------------------------+-----------------+
| Variable_name                          | Value           |
+----------------------------------------+-----------------+
| default_password_lifetime              | 0               |
| disconnect_on_expired_password         | ON              |
| log_builtin_as_identified_by_password  | OFF             |
| mysql_native_password_proxy_users      | OFF             |
| old_passwords                          | 0               |
| report_password                        |                 |
| sha256_password_auto_generate_rsa_keys | ON              |
| sha256_password_private_key_path       | private_key.pem |
| sha256_password_proxy_users            | OFF             |
| sha256_password_public_key_path        | public_key.pem  |
| validate_password_check_user_name      | OFF             |
| validate_password_dictionary_file      |                 |
| validate_password_length               | 8               |
| validate_password_mixed_case_count     | 1               |
| validate_password_number_count         | 1               |
| validate_password_policy               | MEDIUM          |
| validate_password_special_char_count   | 1               |
+----------------------------------------+-----------------+

其中：
validate_password_policy：密码策略，默认为MEIDIUM策略
validate_password_dictionary_file：密码策略文件，策略为STRONG才需要
validate_password_length：密码最小长度
validate_password_mixed_case_count：大小写字符长度，至少各包含个数
validate_password_number_count：密码中数字至少包含个数
validate_password_special_char_count：密码中特殊字符至少包含个数

```

在 `/etc/my.cnf` 文件添加 validate_password_policy 配置，指定密码策略

选择0（LOW），1（MEIDIUM），2（STRONG）其中一种，选择2时需要提供密码字典文件

validate_password_policy = 0

如果不需要密码策略，在my.cnf文件中添加如下配置禁用即可：

validate_password_policy = off

### 3.创建数据库和账号

完成上述配置后，按照正常流程配置远程访问或数据库创建等，本处使用以下方法创建一个远程登录账号且只用于新建的数据库，此处以 woniunote 为例

此过程我们当然可以使用navicat连接使用GUI界面直接操作，但是我们总是要学会使用命令行界面进行操作的

```
create database woniunote character set utf8 collate utf8_general_ci; #创建数据库 woniunote

create user remote@'%' identified by 'P-0p-0P-0p-0';  #创建 远程连接用户remote使得navicat连接操作数据库 woniunote 以便运行SQL文件

grant all priveleges on woniunote.* to remote@'%';  #授权用户 remote 拥有 woniunote 数据库的所有权限

#可以使用以下命令查看用户是否创建成功：
use mysql
select User,Host,authentication_string from user;

如果要删除某个用户，可使用以下命令:
drop user remote@'%';
如果要收回权限，如DELETE或UPDATE或ALL，下述命令收回所有权限：
REVOKE ALL on woniunote.* FROM remote@'%';
```

完成上述配置后，重启mysqld，使用navicat远程连接，此时便只会出现woniunote数据库，远程连接用户remote无法查看其他数据库，按照正常流程，运行woniunote的SQL文件（注意修改最大文件大小）完成数据库的创建，记得让防火墙允许 3306 端口通过

```
vi /etc/my.cnf
#在末尾添加
max_allowed_packet = 20M
即可
```

> **注意：这里的远程用户remote是不能用在第四小节中woniunote配置数据库连接信息中的，因为woniunote使用的是本地用户，要用root**

## 二、安装配置PHP7.3

### 1.安装依赖库

```
yum install -y gcc gcc-c++ make sudo autoconf libtool-ltdl-devel gd-devel freetype-devel libxml2-devel libjpeg-devel libpng-devel curl-devel patch libmcrypt-devel libmhash-devel ncurses-devel bzip2 libcap-devel ntp sysklogd diffutils sendmail iptables unzip cmake pcre-devel zlib-devel openssl openssl-devel
```

如果其中的sysklogd无法安装就安装syslog-ng，因为sysklogd太古老了

### 2.创建www用户

之前的安装配置，均使用root账户，如果一旦应用系统被攻击成功，那么攻击者将直接拥有root权限，极其危险。所以，建议在配置web应用时，将整个web应用程序的各级的各级目录和文件的所有者和组（owner，group）的所有者修改为www这个普通账户

```
创建www组：groupadd www
创建系统账户www：useradd -r www -g www
```

### 3.安装PHP7.3

```
下载PHP7.3版本： http://www.php.net/download.php
解压： tar -zxvf php-7.3.30
切换到解压后目录：cd cd php-7.3.30

配置php安装路径和模块：
./configure --prefix=/usr/local/php --enable-fpm --with-fpm-user=www --with-fpm-group=www --with-openssl --with-libxml-dir --with-zlib --enable-mbstring --with-mysqli=mysqlnd --enable-mysqlnd --with-pdo-mysql=mysqlnd --with-gd --with-jpeg-dir --with-png-dir --with-zlib-dir --with-freetype-dir --enable-sockets --with-curl --enable-maintainer-zts

编译：make (耗时较长)
测试：make test (此步骤可以不用，耗时也很长，大约有13000多个文件需要进行测试，文件多少取决于安装了哪些模块)
安装：make install  # --prefix=/usr/local/php 指定了PHP的安装路径
```

fpm：php执行nginx所传来的php代码所需的模块

### 4.配置PHP环境

```
复制配置文件：
cd /usr/local/php
cp etc/php-fpm.conf.default etc/php-fpm.conf
cp etc/php-fpm.d/www.conf.default etc/php-fpm.d/www.conf
cp /opt/php-7.3.30/php.ini-production /usr/local/php/lib/php.ini

启动：
/usr/local/php/sbin/php-fpm
```

![image-20240123194035913](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123194035913.png)

## 三、安装配置Nginx（带Lua支持）

Lua脚本开发的一个WAF，可自动阻挡一些攻击

### 1.安装LuaJIT 2.0.5

```
cd /opt
wget http://luajit.org/download/LuaJIT-2.0.5.tar.gz
tar -zxvf LuaJIT-2.0.5.tar.gz
cd LuaJIT-2.0.5
make && make install
```

### 2.安装Ngx_devel_kit

NDK（nginx development kit）模块是一个扩展nginx服务器核心功能的模块，第三方那个模块开发可以基于它来实现。

```
wget https://github.com/simplresty/ngx_devel_kit/archive/v0.3.0.tar.gz
tar -zxvf v0.3.0.tar.gz
解压即可，无需配置安装，在编译nginx指定该目录
```

### 3.安装nginx_lua_module

```
wget https://github.com/openresty/lua-nginx-module/archive/v0.10.13.tar.gz
tar -zxvf v0.10.13.tar.gz
解压即可，无需配置安装，在编译Nginx时指定该目录
```

### 4.导入环境变量

```
编辑 /etc/profile 文件（这是系统环境变量配置文件），在末尾添加：
export LUAJIT_LIB=/usr/local/lib
export LUAJIT_INC=/usr/local/include/luajit-2.0
保存并让改脚本生效
source /etc/profile

运行 env | grep LUA 确保环境变量已生效
```

![image-20240123200920157](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123200920157.png)

### 5.编译安装Nginx

```
tar -zxf nginx-1.21.2.tar.gz

cd nginx-1.21.2

 ./configure --user=www --group=www --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --pid-path=/usr/local/nginx/nginx.pid --with-http_realip_module --add-module=/opt/ngx_devel_kit-0.3.0 --add-module=/opt/lua-nginx-module-0.10.13 --with-ld-opt="-Wl,-rpath,$LUAJIT_LIB"
 
 make -j2  #多任务执行编译，加快速度
 
 make install
```

### 6.运行nginx并确认安装成功

```
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --reload
/usr/local/nginx/sbin/nginx

如果需要重启nginx
/usr/local/nginx/sbin/nginx -s reload
```

完成上述配置后，就可以直接访问该服务器的80端口了

![image-20240123203219509](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123203219509.png)



## 四、配置woniunote系统

### 1.创建主目录并复制woniunote文件夹

```
创建主目录：mkdir -p /www/web
修改目录所有者： chown -R www:www /www/web
解压woniunote： unzip woniunote-本书全套-20200331.zip -d www/web
重命名目录：mv woniunote-本书全套-20200331.zip woniunote
修改目录所有者： chown -R www:www woniunote  #确保该目录及其所有子目录和文件均修改了文件所有者为www:www
修改数据库连接信息： vi /www/web/woniunote/config/database.php  #制定正确的数据库连接信息（不能使用远程用户）

```

### 2.修改nginx.conf文件配置

先将原始nginx.conf文件重命名

```
cd /usr/local/nginx/conf/
nginx.conf nginx,conf.orig
```

然后新建nginx.conf文件，输入以下内容：

```
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;

    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location / {
            root   /www/web/woniunote/public;
            index  index.php index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        
        location = /50x.html {
            root   html;
        }
        
        root /www/web/woniunote/public;
        index index.php index.html;
        
        location ~ \.php$ {
        	fastcgi_pass	127.0.0.1:9000; #这是php的服务端口，这个fpm是nginx与php交互的桥梁
        	fastcgi_index	index.php;
        	
        	fastcgi_param	SCRIPT_FILENAME    $document_root$fastcgi_script_name;
        	
        	include			fastcgi_params;
        }
    }
}

```

`$document_root$fastcgi_script_name` 表示用户主目录下的以 .php 结尾的文件，通过 fastcgi_param 将文件的参数交给 127.0.0.1:9000 来解析这份PHP代码

### 3.重启nginx

```
/usr/local/nginx/sbin/nginx -s reload
```

### 4.访问woniunote

直接访问nginx的默认80端口即可

![image-20240123211328306](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123211328306.png)

虽然首页访问成功，但是不仅右边栏没有任何信息，而且不管点击哪里都是404，这不是权限的问题

![image-20240123211758523](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123211758523.png)

在权限这一栏，左边是用户的权限，右边是root的权限，之前我们在xampp上搭建woniunote使用的是root权限，因此需要添加的是右边栏的写权限，而现在我们的用户是www:www，其左边栏的写权限是有的，因此不是这个问题

根本问题是这里的nginx和apache的区别。woniunote使用了一个开发框架叫ThinkPHP，该框架有url地址重写的功能，apache自带的就有url地址重写的框架，而nginx中默认自带的是没有的

### 5.配置URL地址重写

woniunote使用了ThinkPHP开发框架，ThinkPHP支持用过PATHINFO和URL rewrite的方式来提供友好的URL，只需要在配置文件中设置 'URL_MODEL' => 2 即可。在Apache下只需要开启mod_rewrite模块就可以正常访问了，但是nginx中默认是不支持PATHINFO的，所以nginx默认情况下是不支持ThinkPHP的。不过我们可以通过修改nginx的核心配置文件让其支持ThinkPHP。

修改 nginx.conf 配置文件信息如下：

```
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
 
    sendfile        on;

    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location / {
            if (!-e $request_filename) {
            	rewrite ^/(.*)$	 /index.php/$1	last;
            	break;
            }
        }

        error_page   500 502 503 504  /50x.html;
        
        location = /50x.html {
            root   html;
        }
        
        root /www/web/woniunote/public;
        index index.php index.html;
        
        location ~ \.php {
        	fastcgi_pass	127.0.0.1:9000;
        	fastcgi_index	index.php;
        	include fastcgi.conf;
        	set $real_script_name $fastcgi_script_name;
        	if ($fastcgi_script_name ~ "^(.+?\.php)(/.+)$") {
        		set $real_script_name $1;
        		set $path_info $2;
        	}
        	fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        	fastcgi_param SCRIPT_NAME $real_script_name;
        	fastcgi_param PATH_INFO $path_info;
        }
    }
}

```

![image-20240123215256823](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123215256823.png)

![image-20240123215330886](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123215330886.png)

这下，访问woniunote右边栏既有信息，也可以点开其他网页访问了

## 五、nginx中配置WAF

![image-20240123215348112](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123215348112.png)

![image-20240123215354775](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123215354775.png)

![image-20240123215359933](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240123215359933.png)
