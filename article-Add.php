<?php
// 先判断用户是否为admin或editor权限
session_start();  //要用到$_SESSION[''] 全局变量，一定要先开启session模块
if($_SESSION['role'] != 'admin' || $_SESSION['role'] != 'editor' || $_SESSION['islogin'] != 'true') {
    die("你无权新增文章");
}

$headline = $_POST["headline"];
$content = $_POST["content"];

$conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote',3306) or die("数据库连接失败");
mysqli_set_charset($conn,'utf8');

$sql = "insert into article(headline,content,updatetime) values('$headline','$content',now());";
mysqli_query($conn,$sql) or die("add-fail");

echo "add-pass"."<br>";

mysqli_close($conn);

?>