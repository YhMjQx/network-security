# ==MySQL主从复制==

主从复制：两台机器进行数据的实时同步。主：Master 从：Slave。将所有数据以 Master为准，Slave进行实时复制同步 -> 实时备份，读写分离写数据到 Master ，读可以直接从Slave读

## 一、安装MySQL服务器

rpm安装repo，再 yum insatll mysql-server 

```sql
rpm -ivh mysql80-community-release-el6-1.noarch.rpm

vi /etc/yum.repo.d/mysql-community.repo

设置5.6版本节点 enabled=1
设置8.0版本节点 enabled=0

yum install mysql-server
```

安装过程可能会报错，就根据提示来操作即可

![image-20231221121747619](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231221121747619.png)

## 二、授权远程连接

进入mysql数据库

```shell
cd /opt/lampp/bin
./mysql -u root -p

```

![image-20231221220330083](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231221220330083.png)

刚开始就这些

`GRANT ALL PRIVILEGES *.* 'ymq'@'%' IDENTIFIED BY 'P-0P-0P-0' WITH GRANT OPTION;`

`flush privileges;`

利用以上语句可以创建用户 ymq 并为 ymq 这个用户设置登录密码

> 如果单纯只是为了同步数据，此同步用户的权限可以只分配：REPLICATION SLAVE, 不需要其他权限

创建好之后就类似于下面的情况

![image-20231221220543155](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231221220543155.png)

## 三、配置主服务器

### 1.修改mysql配置

找到主数据库的配置文件 /etc/my.cnf ,在 [mysql] 部分插入如下两行：

```sql
[mysql]
log-bin=mysql-bin  #开启二进制日志
server-id=1  #设置server-id
```

### 2.重启mysql，创建用于同步的用户和账号

打开mysql会话shell>mysql -h localhost -u name -p password

创建用户并授权：用户：rel1  密码：slavepass

```sql
mysql> CREATE USER 'repl'@'123.57.44.85' IDENTIFIED BY 'slavepass';  #创建用户

mysql> GRANT REPLICATION SLAVE ON *.* TO 'repl'@'123.57.48.85';  #分配权限
mysql> flush privileges;  #刷新权限
```

### 3.查看master状态，记录二进制文件名（mysql-bin.000001）和位置（120）：

```sql
mysql> show master status;
+------------------+----------+--------------+-------------------+
| File             | Position | Binlog_do_DB | Binlog_Ignore_DB  |
+------------------+----------+--------------+-------------------+
| mysql-bin.000001 | 120      | test         | manual,mysql      |
+------------------+----------+--------------+-------------------+
```

## 四、配置从服务器

### 1.==修改==mysql配置

同样找到 my.cnf 配置文件，添加 Server-id

```sql
[mysqld]
server-id=2  #设置server-id，必须唯一
```

![image-20231224145358232](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224145358232.png)

### 2.重启mysql，打开mysql会话，==执行==同步SQL语句

（需要主服务器主机名，登录凭据，二进制文件的名称和位置）

在slave服务器上执行以下语句

```
change master to master_host="192.168.112.177",master_port=3306,master_user="qiang",master_password="p-0p-0p-0",master_log_file="mysql-bin.000004",master_log_pos=120,master_connect_retry=10;
```

这里的master_log_file和master_log_pos就是 一、3. 中 `show master status` 的查看结果

### 3.==启动==slave同步进程

```
mysql> start slave;
```

### 4.==查看==slave状态

![image-20231224145901945](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224145901945.png)

![image-20231224150235602](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224150235602.png)

有这两部分，说明同步成功

当Slave_IO_Running和Slave_SQL_Running都为YES时就表示主从同步设置成功了。接下来就可以进行一些验证了，比如在主master数据库的test数据库的一张表中插入一条数据，在slave的test数据库的相同数据表查看是否有新增的数据即可验证主从复制功能是否有效，还可以关闭slave（mysql> stop slave; ）然后再修改master，验证slave是否有相应的修改（停止slave后，master的修改不会同步到slave），就可以完成主从复制功能的验证了。

如果上述无法同步成功，通常是因为在MySQL5.6及以上版本中，存在一个UUID表示重复的问题，修改Slave机器上的UUID

```
vi /var/lib/myslq/auto.cnf

[auto]
server-uuid=0c5ac732-938a-000c292030a7
#任意修改一位，保持不重复，然后再重启mysql即可
```

![image-20231224151323769](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224151323769.png)

改完配置别忘记重启一下 mysqld 

systemctl restart mysqld

然后再进入mysql去查看一下上面两个YES是否都成功出现了

```
mysql> show slave stauts\G;
```



![image-20231224151532743](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224151532743.png)

### 5.还可以用到其他的相关参数：

master开始二进制日志后默认记录所有所有库所有表的操作，可以通过配置来指定只记录指定的数据库甚至指定的表的操作，具体在mysql配置文件的 [mysqld] 可添加修改如下选项：

```
#不同步哪些数据库
binlog-ignore-db = mysql
binlog-ignore-db = test
binlog-ignore-db = information_schema

#只同步哪些数据库，除此之外，其他不同步
binlog-do-db = game
```

如之前查看master状态时就可以看到只记录了test库，忽略了manual和mysql库

