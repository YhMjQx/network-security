<?php

$conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote');
mysqli_set_charset($conn,'utf8');

$sql = "select articleid , headline , updatetime from article";
$result = mysqli_query($conn,$sql);

//将数据库查询的 结果集 中的数据取出，保存到一个数组中
$rows = mysqli_fetch_all($result);
// print_r($rows);  最终的数组是一个二维数组，联想数据库中的表，
// 二维数组第一个元素就是第一行，第一行的第一个元素就是 articleid

//foreach中 每一个$row 都是$rows的一个元素，所以每一个$row就是一行数据
foreach($rows as $row) {
    echo $row[0]." ~ ".$row[1]." ~ ".$row[2]."<br>";
}


?>