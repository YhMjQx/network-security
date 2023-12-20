# ==MySQL补充知识==

## 索引 

- 索引的作用：Index，目录，帮助数据库提升性能，避免全表扫描导致速度极慢，数据量越大越需要索引。

- 在数据库中，如何利用索引实现快速查询

## 一、MySQL索引分类

MySQL索引主要有两种结构：B+Tree索引和Hash索引

### Hash索引：

MySQL中，只有Memory（Memory表只存在于内存中，断电会消失，适用于临时表）存储引擎显示只是Hash索引，是Memory表的默认索引类型，尽管Memory表也可以使用B+Tree索引。Hash索引把数据的索引以Hash形式组织起来，因此当查找某一条记录的时候，速度非常快，当时因为是hash结构，每个键只对应一个值，而且是散列的分布方式。所以他并不支持范围查找和排序等功能

![image-20231220164511378](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220164511378.png)

### B+Tree索引

B+Tree从MySQL5.5之后，就是使用最频繁的一个索引数据结构，是innoDB和MyISAM存储引擎模式的索引类型，相对Hash索引，B+Tree在查找单条记录的速度比不上Hash索引，但是因为更适合排序等操作，索引他更受用户的欢迎。毕竟不可能只对数据库进行单条记录的操作

![image-20231220164903716](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220164903716.png)

- 简要介绍一下原理：
  - 磁盘1中的p1指向小于28的内容
  - 磁盘2中的p1指向小于10的数据，p2指向10-17之间的数据，p3指向17-28之间的数据
  - ...
  - 就通过这样的索引来达到快速查找的功能

## 二、常见的索引类型

- PRIMARY KEY（主键索引）ALTER TABLE `table_name` ADD PRIMARY (`col`)
- UNIQUE(唯一索引) ALTER TABLE `table_name` ADD UNIQUE(`col`)

**创建索引前：**

![image-20231220171724083](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220171724083.png)



**创建唯一索引后：**

![image-20231220171346507](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220171346507.png)

使用关键字 **`EXPLAIN`** 查看查询语句的查询计划

![image-20231220171530707](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220171530707.png)

 key：索引类型

rows：表示查询的行数

> 使用 LIKE 或 聚合函数时，无法使用索引
>
> 创建索引时，需要花费计算资源和存储资源。所以，索引不适用于频繁更新和插入数据的表，或者说：更新次数多于查询次数时没有必要使用索引

- INDEX(普通索引) ALTER TABLE `table_name` ADD INDEX index_name(`col`)
- FULLTEXT(全文索引) ALTER TABLE `table_name` ADD FULLTEXT(`col`)
- 组合索引 ALTER TABLE `table_name` ADD INDEX index_name (`col1`,`col2`,`col3`)

## 其他用法：

### 利用SQL语句写文件

前提是需要对目录有权限，而且，要写的文件不能已经存在

```sql
select "string" into outfile ‘/tmp/xxx.txt’;
```

![image-20231220175233841](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220175233841.png)

![image-20231220175248106](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220175248106.png)

### 创建临时表

是保存在内存中的表，执行速度很快。断开本次连接，就会消失，无法使用 手误 tables 查看到该表

```sql
CREATE TEMPORARY TABLE table_name(
	id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20),
    age TINYINT
);
```

![image-20231220183458407](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220183458407.png)

### 通过SQL语句来创建一张表

#### 利用select语句创建一张表

配合关键字 `create table`

```sql
create table table_name select customerid,name,sex,phone from customer where customerid<10;
```



创建好了之后还可以使用关键字 `INSERT INTO` 对表插入数据

```sql
INSERT INTO table_name select customerid,name,sex,phone from customer where customerid=10;
#相当于将customer表中customerid=10的数据再插入一遍
```



我们还可以利用此方式方式对表进行备份

```sql
create table customer_bak select * from customer; 
```



## 备份

当然，备份的方式有很多

- 上面所说的使用 `create table table_name select ...` 
- 使用工具自带的备份

![image-20231220201046436](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220201046436.png)

![image-20231220201125020](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220201125020.png)

![image-20231220201137576](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220201137576.png)

> 锁住全部表：在备份期间不允许修改，只允许查询

备份的本质就是备份建表和插入语句等这些最本质的东西

而且，我们还可以将备份后的文件提取出SQL

![image-20231220201618875](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220201618875.png)

![image-20231220201630789](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220201630789.png)

实际上就是这些语句

- 通过最本质的备份指令进行备份操作

进入系统终端操作

```sql
#备份数据库到 /opt 目录
mysqldump -h127.0.0.1 -uroot -ppass book > d:/backupfile.sql
#压缩之后备份数据库到 /opt 目录
mysqldump -h127.0.0.1 -uroot -ppass book | gzip > d:/backupfile.sql.gz
#同时备份多个数据库
mysqldump -h127.0.0.1 -uroot -ppass --databases book school > multibackupfile.sql
#以上是备份指令
#以下是还原数据库指令，首先需要创建一个数据库（可以先手工创建好一个数据库，也可以将创建数据库的指令放在被导入的文件中，则会自动创建数据库）
mysql -h127.0.0.1 -uroot -ppass book < backupfile.sql
#针对压缩文件进行导入
gunzip < backupfile.sql.gz | mysql -h127.0.0.1 -uroot -ppass book

```

备份book数据库

![image-20231220204500054](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220204500054.png)

还原book数据库

![image-20231220210141672](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220210141672.png)



## 权限

任何情况下，先授予最小权限，再根据实际需要添加权限

![image-20231220210911001](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231220210911001.png)

```sql
#%表示所有ip
grant all *.* 'woniu'@'%' identify by '123456';  #给woniu以所有数据库的所有权限
flush privileges;  #刷新权限

revoke 	权限1,权限2,... on 数据库名.对象名 from '用户名'@'允许其登录的地址';  #移除权限
eg:
revoke INSERT on *.* from 'woniu'@'%';
flush privileges;
```

**关于权限的可视化操作在第一份视频第161集从一小时04分钟开始**

