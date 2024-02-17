<?php

    // 设置使用中国北京时间作为时区
    // date_default_timezone_get("PRC");

    function register(){
        $uname = $_POST["username"];
        $passwd = $_POST["password"];
        $nickname = $_POST["nickname"]; 
        $qq = $_POST["qq"];

        //下面的取值就相当于在二维数组当中取值
        $tmpPath = $_FILES["headphoto"]["tmp_name"];  //获取上传的文件的临时路径名（文件会默认上传到这个临时路径）
        // echo $tmpPath;  
        // die();
        $headPhotoName = $_FILES["headphoto"]["name"]; //获取上传文件的原始文件名
        // echo $headPhotoName;  
        // die();
    
        //设置连接信息
        $conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote',3306) or die("数据库连接失败");
        //or die("数据库连接失败")  的作用是当数据库连接失败时就结束后面代码的执行并报出自定义错误
    
        //设置编码格式的两种方式
        //  mysqli_query($conn,"set names utf8");
        mysqli_set_charset($conn,'utf8');
    
        //拼写查询用户用的sql语句
        $querysql = "select username from users;";

        //执行 查询用户 的sql语句
        $queryresult = mysqli_query($conn,$querysql);

        //将查询结果的结果集转换为数组
        $rows = mysqli_fetch_all($queryresult);
        //记住，获得的数组结构是一张表，是二维数组的结构
        foreach($rows as $row) {
            //判断输入的用户名与数据库中已有的是否相等
            if($row[0] == $uname){
                // echo "user-exists";
                // exit;
                //上面两句代码可以适用die函数替代
                die("user-exists");
            }
        }
        //使用时间戳为文件重命名
        //$headPhotoName结果为 灞忓箷鎴浘 2024-02-06 222915.png
        // explode('.',$headPhotoName) 结果为 灞忓箷鎴浘 2024-02-06 222915  png  的一个数组
        // end(explode('.',$headPhotoName)) 结果为 png
        // $newFileName = date('Ymd-His.').end(explode('.',$headPhotoName));

        //注册成功后，上传文件，从临时路径移动到指定路径
        // 如果想用时间作为文件名，那么就释放上面的代码并将下面代码中的 $headPhotoName 改为 $newFileName
        // 同时修改数据库插入语句中的 $headPhotoName
        move_uploaded_file($tmpPath,"../Upload/".$headPhotoName) or die("文件上传失败");
    

        //拼接 插入sql语句 并执行
        $now = date('Y-m-d H:i:s');
        $insertsql = "insert into `users` (username,password,nickname,qq,avatar,createtime,updatetime) values ('$uname', '$passwd', '$nickname','$qq','../Upload/$headPhotoName','$now','$now');";
        $result = mysqli_query($conn,$insertsql);
        if (!$result) {
            printf("Error: %s\n", mysqli_error($conn));
            exit();
        }
    
        // mysqli_affected_rows() 函数返回受影响的行数，如果大于 0，则表示插入成功；如果等于 0，则表示没有插入任何行；如果为 -1，则表示发生了错误。
        if (mysqli_affected_rows($conn) > 0) {
            echo "register-pass";
        }
        else {
            echo "register-fail";
        }
    
        //关闭数据库
        mysqli_close($conn);
    }
    register();
?>
