<?php
    //这是一段服务器处理的后台代码，用于检测post请求正文

    /**
     * 获取请求的方式
     * GET
     * POST
     * 前端如果使用get请求，后台就需要使用$_GET函数接收
     * 前端如果使用post请求，后台就需要使用$_POPST函数接收
     */

    //GET请求
    //需要将对应的html页面的请求方式method也改为get
    // $uname = $_GET['username'];
    // $passwd = $_GET['password'];
    // $vcode = $_GET['vericode'];



     //POST请求
    //需要将对应的html页面的请求方式method也改为post

    $uname = $_POST["username"];
    $passwd = $_POST["password"];
    $vcode = $_POST["vericode"]; 
    

    // echo "username=".$uname." password=".$passwd." vericode=".$vcode."<br>";
    //输出的是服务器的响应

    /**
     * 在php中如何访问MySQL数据库？有两个模块MySQLi，PDO
     * 1.连接到MySQL数据库
     * 2.执行SQL语句（CRUD）
     * 3.处理SQL语句结果
     *      查询结果用数组保存
     *      更新数据库
     * 4.关闭数据库连接
     * 事实上，所有的I/O操作，都需要实现打开和关闭的两个基本操作，文件读写，网络访问，数据库访问
     */

     if ($vcode == 0000) {

     //设置连接信息
     $conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote',3306) or die("数据库连接失败");
     //or die("数据库连接失败")  的作用是当数据库连接失败时就结束后面代码的执行并报出自定义错误

     //设置编码格式的两种方式
    //  mysqli_query($conn,"set names utf8");
     mysqli_set_charset($conn,'utf8');

     //拼接sql语句并执行
     $sql = "select * from users where username='$uname' and password='$passwd'";
     $result = mysqli_query($conn,$sql);

     //判断查询结果是否为1行，如果为1行，才说明查询真的成功
     if (mysqli_num_rows($result) == 1) {
        echo "登录成功"."<br>";
     }
     else {
        echo "登录失败"."<br>";
     }

     //关闭数据库
     mysqli_close($conn);

    }
    else {
        echo "验证码有误，登录失败"."<br>";
    }

?>