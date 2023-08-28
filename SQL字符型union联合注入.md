# ==SQL在burp中字符型联合注入利用==

```SQL
数字型注入:$sql = "select * from person where id = {Sid)";

字符型注入: $sql ="select * from person where id = '{Sid}'";
要在''之中进行sql语句
Mysql中注释： #、--+  闭合引号

select * from articles where id = '1'
目的是形成' ' 1 ' '这样的情况效果
select * from articles where id ='1'注入语句部分 (与数字型类似) --+''
```

select * from articles where id ='***1'注入语句部分 (与数字型类似) --+'***’这里面斜体和加黑的才是我自己构造的SQL语句，最外面的两个''是人家默认自带的，然后再url中没有显现出来而已

实验：

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230828222924360.png" alt="image-20230828222924360" style="zoom:200%;" />

前面2右上角的'是用来逃逸第一个单引号的，后面的--+是用来逃逸后面的单引号的

至于为什么呢，

`192.168.0.102/01SQL/03Table/?id=2`的实际样子是什么样的呢 `192.168.0.102/01SQL/03Table/?id='2'`，这就是为什么在

查看表名

![image-20230828223343795](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230828223343795.png)

然后查看admin这张表中的字段

```sql
table_name -> column_name
information_shema.tables -> information_schema.columns
table_schema ->table_name
database() -> 'admin'
```

如果这里的'admin'的返回结果会出问题，那么就把'admin'换为0x61646D696E

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230828223811071.png" alt="image-20230828223811071" style="zoom:200%;" />

最后查看admin这张表中字段名对应的数据

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230828224128692.png" alt="image-20230828224128692" style="zoom:200%;" />

**总结：**

**1.从原理上掌握联合查询注入利用技术**

**2.掌握Burpsuite对注入点进行Union联合查询注入**

