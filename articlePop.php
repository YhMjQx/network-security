<?php

    $articleid = $_POST["articleid"];

    //配置数据库连接信息
    $conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote') or die("数据库连接失败");

    //设置数据库字符集编码
    mysqli_set_charset($conn,'utf8');      

    //拼接删除文章的sql语句
    $popsql = "delete from article where articleid=$articleid;";

    //执行删除文章的sql语句
    mysqli_query($conn,$popsql) or die("delete-fail");
    
    echo "delete-pass";

?>