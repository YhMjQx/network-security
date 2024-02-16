<?php

    function register(){
        $uname = $_POST["username"];
        $passwd = $_POST["password"];
        $nickname = $_POST["nickname"]; 
        $qq = $_POST["qq"];
    
        //设置连接信息
        $conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote',3306) or die("数据库连接失败");
        //or die("数据库连接失败")  的作用是当数据库连接失败时就结束后面代码的执行并报出自定义错误
    
        //设置编码格式的两种方式
        //  mysqli_query($conn,"set names utf8");
        mysqli_set_charset($conn,'utf8');
    
        //拼写查询用户用的sql语句
        $querysql = "select username from users;";

        //执行查询用户用的sql语句
        $queryresult = mysqli_query($conn,$querysql);

        //将查询结果的结果集转换为数组
        $rows = mysqli_fetch_all($queryresult);
        //记住，获得的数组结构是一张表，是二维数组的结构
        foreach($rows as $row) {
            //判断输入的用户名与数据库中已有的是否相等
            if($row[0] == $uname){
                echo "用户名重复，注册失败"."<br>";
                exit;
            }
        }
    
        //拼接插入sql语句并执行
        $insertsql = "insert into `users` (username,password,nickname,qq) values ('$uname', '$passwd', '$nickname','$qq');";
        $result = mysqli_query($conn,$insertsql);
        if (!$result) {
            printf("Error: %s\n", mysqli_error($conn));
            exit();
        }
    
        // mysqli_affected_rows() 函数返回受影响的行数，如果大于 0，则表示插入成功；如果等于 0，则表示没有插入任何行；如果为 -1，则表示发生了错误。
        if (mysqli_affected_rows($conn) > 0) {
            echo "注册成功";
        }
        else {
            echo "注册失败";
        }
    
        //关闭数据库
        mysqli_close($conn);
    
    // insert into `users` (username,password,nickname,qq) values ('$uname', '$passwd', '$nickname', '1234567890');

    }

    register();

?>