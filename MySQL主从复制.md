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

### 1.修改mysql配置

同样找到 my.cnf 配置文件，添加 Server-id

```sql
```

