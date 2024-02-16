<?php
//为什么$_GET['']函数中的参数十id，因为我们本意是想要获得articleid
// 然后articleid在上一个页面中，也就是article-list.php中，articleid是以$row[0]变量形式存在的
// 然后呢我们在超连接中将$row[0]赋值给了id地址参数，于是我们在这里采用的是id
$id=$_GET["id"];
// echo $id;

//设置数据库连接信息
$conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote');

//设置字符集编码
mysqli_set_charset($conn,'utf8');

//拼写sql语句
$sql="select content from article where articleid = ".$id;

//执行sql语句
$result = mysqli_query($conn,$sql);

//将查询结果转换为数组
$content = mysqli_fetch_all($result);

//在条换的页面中输出
print_r($content);

//关闭数据库连接
mysqli_close($conn);


?>