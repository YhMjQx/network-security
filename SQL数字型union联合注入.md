# ==SQL数字型union联合注入实验==

**注意：union联合查询注入利用只适用于页面中有返回结果的SQL语句查询**

实验1：Burpsuite数字型联合注入利用

```php
实验php源代码：
	$id = $_GET["id"]; 
#通过url的方式传递相应的参数，然后赋值给$id这个变量
	$conn = mysql_connect('localhost’，'root'，'123456') or die('连接数据库失败!');
#开始链接mySQl数据库
	mysql_query('set names utf-8',$conn);
#设置当前数据编码为utf-8
	mysql_query('use web_sql', $conn);
#设置使用的数据库是websql
	$sql = "select * from person where id = {Sid}";
#将传递的参数带入到sql语句当中进行执行，完成sql语句构造
	$res = mysql_query($sql,$conn) or die(mysql_error());
#通过mysql将构造的SQL语句带入到$conn的链接当中进行执行，并将返回结果赋给$res
	$arr = mysql_fetch_assoc($res);
#通过函数对返回的结果进行查找，查找的结果放在一个数组中，而数组的索引就是查询到的字段的名称 
	
页面输出代码：
	<td><?php echo $arr['id'];?></td>
	<td><?php echo $arr['name'];?></td>
	<td><?php echo $arr['age'];?></td>
	<td><?php echo $arr['phone'];?></td>
	<td><?php echo $arr['email'];?></td>
```

实验开始：

首先配合使用 `order by num` 来测试列数

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828184644790.png" alt="image-20230828184644790" style="zoom:200%;" />

这是第一个开始报错的num，说明当前id对应的数据库的字段表的字段数是5

然后让union前半部分报错，然后后面开始构造sql

tables_schema是information_schema.tables这个表名当前所保存的数据库的名称，其实也就是让他等于database()

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828185851546.png" alt="image-20230828185851546" style="zoom:200%;" />

然后查看admin当中相关的数据和字段名

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828190154850.png" alt="image-20230828190154850" style="zoom:200%;" />

然后将字段名下的数据连接起来并显示

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828190404704.png" alt="image-20230828190404704" style="zoom:200%;" />



