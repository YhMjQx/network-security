[TOC]



# ==LAMPP部署信贷系统==

## 操作大纲

- Xampp默认启动后，Apache使用端口80，所以要让防火墙开放80端口，并且保持防火墙开启状态
- [phpinfo()](http://192.168.230.147/dashboard/phpinfo.php) http://192.168.230.147/dashboard/phpinfo.php 展示了所有运行环境参数，通常情况下，建议删除改页面
- 默认情况下，/opt/lampp/htdocs 目录是应用程序的根目录 （Document Root）/dashboard/phpinfo.php
- 在 /opt/lampp/htdocs 目录下，创建二级目录 xindai，用于部署小额信贷系统，并复制相应文件到该目录
- 在MySQL的客户端环境下，导入该系统的配套资料库，数据库名称叫什么？有什么要求？编码格式是什么？
- 修改配置文件，进行数据库连接，进而实现系统和数据库的融合运行。

紧接着上面的文件继续，课程中说，在 xampp 7.3 的版本上与小额信贷系统是不兼容的，会出现如下错误：

![image-20240118134935394](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118134935394.png)

以上错误是由于小额信贷系统无法兼容 Xampp的较新版本，该版本是PHP7.3版本 ，导致代码不兼容

于是，现在需要安装xampp5.6的版本，但是我先讲xampp7.3的版本留下，用一个干净的虚拟机重新装xampp5.6然后部署小额信贷系统，最后我会反过头来重新测试为什么xampp7.3版本会有不兼容的情况，是在哪一步开始不兼容的

> 任何一套系统，与服务器环境进行整合时，必须要考虑其兼容性

**对于任意一个刚装好的MySQL数据库，我们都需要做两件事情**

- **修改 root 默认密码**
- **配置可远程操作MySQL**
  - **配置 PHPMyAdmin 实现访问和操作 MySQL**
  - **在 MySQL 中新建一个支持远程连接的用户，用于 navicat 进行远程操作**

## 一、安装 xampp5.6

1、上传xampp5.6，并赋予可执行权限

权限1  -  可执行权限 x

权限2  -  写权限 w

权限4 - 读权限 r

即：权限数字越大，权限越小，数字越小，权限越大

![image-20240118140153314](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118140153314.png)

![image-20240118140235348](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118140235348.png)

2、执行安装指令

`./xampp-linux-x64-5.6.40-1-installer.run`

![image-20240118141115448](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118141115448.png)



## 二、在xampp5.6上配置

1、确认服务器端口和服务是否正常启动，某些情况下，可能由于端口冲突或与操作系统或服务器环境不兼容，导致无法正常启动

- 此时我们需要去解决端口冲突的问题，在哪里去修改端口呢，在xampp的配置文件中 Apache的默认核心配置文件是 /opt/lampp/etc 目录下的 httpd.conf 

![image-20240118141525447](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118141525447.png)

​		进入该文件去看看

![image-20240118142225291](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118142225291.png)

​		上面那个是默认根目录，下面就是默认端口，目前端口还没有冲突我们可以不修改

- 开启Xampp 执行指令 

![image-20240118142532992](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118142532992.png)

ok，端口没有冲突，现在报错，没有netstat，那好，我去安装

![image-20240118142624797](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118142624797.png)

ok，没有可用的软件包，完犊子，别急，让我在研究研究

好好好，原来是要安装 net-tools , 不是直接安装netstat，是因为没有安装net-tools工具（[CentOS7](https://so.csdn.net/so/search?q=CentOS7&spm=1001.2101.3001.7020)，Ubnutu16.04，Debian9，openSUSE15等以后版本系统已经默认不再集成这个命令，需要安装相应的软件net-tools），直接 `yum install net-tools -y` 解决

**开启xampp**

![image-20240118143211585](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118143211585.png)

**同时还需要记住，将防火墙的80端口放开**，否则外部访问不了

> 但是还有可能会遇见 及时xampp端口没有冲突，但有可能会与操作系统版本冲突，因为xampp是默认以2.25的操作系统在执行，而我们的操作系统的版本是 3.10 （使用 `uname -a` 查看）
>
> ![image-20240118143624611](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118143624611.png)
>
> 此时就需要进入 /opt/lampp/lampp 文本文件修改 内核版本 2.2.5 变为 2.8.0

## 三、解压 小额信贷系统 到 DocumentRoot 所在目录

DocumentRoot此处为：/opt/lampp/htdocs。 DocumentRoot可在/opt/lampp/etc/httpd.conf中查看和修改

![image-20240118145749863](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118145749863.png)

- 将整个压缩包上传之后，在Linux上下载 unzip 命令 `yum install unzip -y` 即可，然后使用命令 `unzip 小额信贷系统 -d ./` 将压缩包解压至当前目录，然后挑选出我们需要的新版，移动或复制到 /opt/lampp/htdocs

```
yum install unzip -y

unzip 小额借贷系统.zip -d ./

cd 小额借贷系统网站源码（无授权无加密）-后台带信用报告-逾期列表等

cp -r WWW新版 /opt/lampp/htdocs

cd /opt/lampp/htdocs

mv WWW新版 xindai  #以防万一，将qi改成英文

```

![image-20240118151213803](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118151213803.png)

正常情况下我们就可以尝试去访问xindai了，如果不需要数据库支持或不需要疼权限，原则上是可以直接访问的，但毫无疑问，小额信贷是需要数据库的，因此结果就如下图所示

![image-20240118151716123](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118151716123.png)

## 四、开始配置小额信贷系统的数据库

**首先肯定需要有进入的账号**

- xampp自带了一个 /opt/lampp/bin目录下 ./mysql -uroot 该用户没有任何密码，直接进入，但是没有密码是一件很危险的事情，因此我们需要尝试设置密码

### 1、使用默认用户进入mysql

![image-20240118203231465](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118203231465.png)

### 2.去查看用户与密码信息情况

![image-20240118203424134](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118203424134.png)

看一下这张表的具体信息

![image-20240118203702623](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118203702623.png)

![image-20240118203809275](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118203809275.png)

我们可以看到，这所有用户都是没有密码的，而且，前三个用户都是本地连接，都是一样的,都是本地连接。这里的pma用户就是phpmyadmin

### 3.给本地用户root用户设置密码

要知道，这三个用户本质上都是一个用户，所以只要给localhost设置了密码，其他都有了密码

设置密码办法有四：

（1）使用navicat远程操作（但前提是已经连接上）

![image-20240118204911857](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118204911857.png)

（2）在MySQL命令行中执行以下命令

```sql
set password for 用户@localhost = password('新密码');
例如：
set password for root@localhost = password('p-0p-0p-0');
```

![image-20240118210718218](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118210718218.png)

（3）使用 mysqladmin 命令：

```
语法： mysqladmin -u用户名 -p旧密码 password 新密码
cd /opt/lampp/bin
./mysqladmin -uroot -p123456 password p-0p-0p-0
```

（4）直接修改 mysql 数据库的 user 表

```
首先登录 MySQL
mysql> use mysql;
mysql> update user set password=password('p-0p-0p-0') where user='root' and host='localhost';
mysql> flush privileges;
```

> 这里插入一个小知识点：
>
> ./mysql -u root 时，如果不添加 -h 则模式使用 localhost主机登录

ok，我们现在已经将本地连接的root用户的登录Miami设置好了，**但是我们需要给信贷系统一个可以远程登录的用户，从而让信贷系统可以远程操作 MySQL 数据库中的数据**

### 4.配置远程连接 MySQL

在 MySQL 中创建远程和连接用户，并同步设置密码：

```
先切换到执行目录： cd /opt/lampp/bin
再运行 ./mysql -u root -p p-0p-0p-0
运行以下两条指令：

GRANT ALL PRIVILEGES ON *.* TO 'remote'@'%' IDENTIFIED BY 'p-0p-0p-0' WITH GRANT OPTION;
flush privileges;

再利用navicat等其他工具远程连接，确认远程连接开通，也可以在mysql命令行中执行如下操作：
use mysql;
select User,Uassword,Uost from user;
查看用户信息
```

![image-20240118213300079](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118213300079.png)

密码这里输入 p-0p-0p-0 即可

![image-20240118213243285](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118213243285.png)

在select中已经查看到远程登录用户的信息，在进入navicat进行连接

> **注意：MySQL服务默认端口3306一定要打开，不然是连接不上的。Oracle默认1521，redis默认6379**
>
> ![image-20240118213719167](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118213719167.png)
>
> ![image-20240118213744030](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118213744030.png)

![image-20240118213952847](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118213952847.png)

好了，现在navicat也可以远程连接了

![image-20240118214010491](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118214010491.png)

现在就可以看到所有用户的信息，并且可以对这些信息进行操作了

> ![image-20240118215357401](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118215357401.png)
>
> 接下来我们来聊聊关于mysql登录参数信息的问题
>
> 使用 ./mysql -uroot -h127.0.0.1是无法登陆的，即使root用户对应的127.0.0.1没有密码，但是系统依旧会将127.0.0.1翻译为本机，正因为这就是一个本地回路
>
> ![image-20240118215558567](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118215558567.png)
>
>  使用 ./mysql -uroot -p -h192.168.230.147 也是无法登陆的，即使192.168.230.147是本机的ip地址，但是这已经到达了网络范围，超过了本地回路的情况，两块网卡是不一样的，不是一个东西
>
> ![image-20240118215956053](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118215956053.png)
>
> 但是使用 ./mysql -uremote -p -h192.168.230.147 就可以成功，因为没有root用户的host是192.168.230.147，而只有remote用户对应的host才是192.18.230.147，所以remote用户就可以登录
>
> 因此使用remote用户对应localhost也是无法登陆的
>
> ![image-20240118220532621](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118220532621.png)
>
> 不添加 -h 默认代表使用 localhost主机

> 再添加一个关于PHPAdmin远程连接的小知识，PHPAdmin这种Web端的操作，不需要MySQL远程登录的账户。因为PHPAdmin的Web页面属于本机内部，因此，使用PHPAdmin远程连接的时候，什么都不需要，只需要一个root用户就可以直接连接，甚至连防火墙的3306端口都不用打开，当然还是需要设置一个密码的哦，为了安全起见
>
> ![image-20240118221236774](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118221236774.png)
>
> 如图所示，pma就起到了一个跳板一样的作用。由于pma与MySQL都在一台服务器上，因为可以通过内部root用户直接登录，此时MySQL就可以不开启3306端口，外部通过80端口远程登录操作pma，从而就可以间接操作MySQL了

### 5.navicat中创建数据库，并导入sql，记住，需要修改 max_allowed_packet 

我们先尝试，如果不修改 max_allowed_packet  会报什么错

![image-20240118221859473](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118221859473.png)

![image-20240118222129409](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118222129409.png)

![image-20240118222148193](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118222148193.png)

好好好，报错了，它说这个SQL文件太大了，超过了max_allowed_packet  值的允许范围，因此我们需要把这个值上调一点

在mysql的配置文件 /opt/lampp/etc/my.cnf 中去修改，修改完核心参数了之后要重启xampp，继续上述操作。

![image-20240118222755648](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118222755648.png)

![image-20240118222805361](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118222805361.png)

![image-20240118222909475](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118222909475.png)

![image-20240118222918341](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118222918341.png)

终于好了

### 6.修改信贷系统数据库连接信息，确保PHP和MySQL互相通信正常

根据安装说明：

```
安装说明：
1.恢复数据；
2.修改app/conf/config.db.php数据库连接信息；
3.前台账号：13524490259 密码：123456
4.后台管理：http://域名/admin.php 账号：admin   密码：zye.cc888
5.进入后台网站设置，将网站地址修改为你的网站地址，地址末尾不带"/"
6.调试模式请在web/index.php中将APP_DEBUG行删除;
********************************************************************
短信接口模板请如下设置：
【签名】您的验证码为1234，请于5分钟内正确输入，如非本人操作，请忽略此短信。
将1234替换为短信商中的标识符!
修改短信账号密码不在后台，目录是：App\Lib\Class\Smsapi.class.php
请注意啦：
短信接口对接的《短信宝》
支付接口是《天工收银》
征信对接的是 《立木》
运营商数据是《速达数据》
********************************************************************
```

#### 修改app/conf/config.db.php数据库连接信息

进入目录/opt/lampp/htdocs/xindai/App/Conf，修改config.db.php

![image-20240118224852139](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118224852139.png)

修改这三处，就使用对应的登录的 用户@host 以及对应的密码进行修改就好了 （localhost-root-p-0p-0p-0） （192.168.230.147-remote-p-0p-0p-0）

尝试在网页中去访问xindai

本来是如下图所示的错

![image-20240118151716123](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118151716123.png)

解决了my.cnf文件的配置信息之后发现又报错了

![image-20240118225153406](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118225153406.png)

我们仔细阅读这个错误，是因为这个缓存文件的全蝎不够，无法写入，因此，我们需要给这个文件添加写的权限

通过查找，我们发现这个文件的路径为 /opt/lampp/htdocs/xindai/Temp/Cache/Home/8736d67d56905ff7ef653348323ad50d.php

然后 `chmod 666 8736d67d56905ff7ef653348323ad50d.php` ok,返回web端重新访问

![image-20240118230323857](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118230323857.png)

![image-20240118230408981](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118230408981.png)

我草，拿下！！！

### 7.其他

看配置文件说

![image-20240118230959304](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118230959304.png)

我们去访问一下后台

![image-20240118231041703](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118231041703.png)

ok，直接把/opt/lampp/htdocs/xindai/Temp整个目录的权限全都加上写权限得了

在/opt/lampp/htdocs/xindai目录下进行和操作

```
chmod -R 666 Temp
```

![image-20240118232524128](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118232524128.png)

重新访问

因为发现还是有错误

![image-20240118233208909](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118233208909.png)

所以最后还是直接加上所有权限 `chmod 777 -R Temp`

![image-20240118233058350](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118233058350.png)

![image-20240118232732435](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118232732435.png)

使用配置文件当中的账户名和密码进行登录即可进入后台

![image-20240118232829833](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240118232829833.png)

最终，拿下！！！