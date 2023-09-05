# ==SQL注入利用-约束注入==

**Mysql中的约束指：对字段的限制，常用约束 主键（primary key）、非空（not null）、默认（default）、唯一键（unique）、外键（foreign key）等。**



## 约束注入原理

**注入位置：基于约束注入适用于 注册功能的位置，实现效果：利用注入可以注册任意用户，导致可以适用任意用户登录系统。**

**当程序员或DBA在创建数据表过程中，没有对用户名称设置唯一键，并且设置了varchar(num)**





### 实验环境创建：

```sql
1.创建实验数据表
mysql> create table admin(
    #创建一个admin数据表
    -> id int primary key not null auto_increment,   #设置一个可以自动增长的id值
    -> username varchar(50) not null,    #设置一个最大为50字符的username
    -> password varchar(50) not null     #设置一个最大字符数为50的password  
    -> );
Query OK,0 rows affected(0.07 sec)


2.插入数据
 mysql> insert into admin values(0,'admin','123456');
 #在admin数据表中插入数据，顺序依次为id username password
 Query OK, 1 row affected (0.02sec)
 
 mysql> select * from admin;
```

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905135014922.png" style="zoom:200%;" />

```sql
mysql> insert into admin values(0,'admin                                                           x','111111');
Query OK,1 row affected, 1 warning (0.01 sec)

3.查询数据 观察结果
mysql> select * from admin;
```

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905135612119.png" alt="image-20230905135612119" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905141426612.png" alt="image-20230905141426612" style="zoom:200%;" />

当用户插入的用户名长度大于varchar(50)个字符的时候，此时后边多余的字符都会被删掉

```sql
SQL语句设置于取消唯一键约束

取消唯一键 alert table admin drop unique username
#此时再进行约束注入使用insert into admin values(0,'admin                                             x','111111');此时这个语句就无法执行了

设置唯一键 alert table admin add unique (username)
```

  



## 约束注入实验

完成注册admin账号，并登录系统获取flag值

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905142905804.png" alt="image-20230905142905804" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905145309747.png" alt="image-20230905145309747" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905145322320.png" alt="image-20230905145322320" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905145345700.png" alt="image-20230905145345700" style="zoom:200%;" />

 <img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905145405072.png" alt="image-20230905145405072" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905145415293.png" alt="image-20230905145415293" style="zoom:200%;" />

**小结：**

**1.约束注入原理 - 字段是否设置unique约束**

**2.设置唯一键就可以防御，作为一名程序员，务必在需要唯一存在的位置 设置唯一键，都则会出现任意用户注册的内容。**