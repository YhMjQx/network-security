<?php
/*
必须是11位：如何计算字符串的长度
第一位必须是1：如何取得第一位数字
第二位只能在 3-9（使用白名单）：如何取得第二位，且与 3-9 的范围作比较
所有位（后9位）数必须是数字： 0-9 对每一位进行判断
*/ 

/**
 * 这是Add函数的定义
 * 有参数，有返回值，有函数体
 * 作用，两个数字取和
 * $a - 第一个数字
 * $b - 第二个数字
 * 返回值：返回$a+$b的结果
 */
    // function Add($a,$b) {
    //     $result = $a+$b;
    //     echo "计算结果：$result <br>";
    //     return $result;
    // }

    // $result = Add(100,200);
    // echo $result;


    function checkPhone_01($phone) {

        // return false  使得一旦执行，便返回结果，同时结束函数的调用

        $len = strlen($phone);
        if ($len != 11) {
            echo "请输入有效电话号码，长度必须为11。<br>";
            return false;
        }

        if ($phone[0] != "1") {
            echo "请输入有效电话号码，第一位必须是1。<br>";
            return false;

        }

        if (!($phone[1] >= "3" && $phone[1] <= "9")) {
            echo "请输入有效电话号码，第二位只能在 3-9。<br>";
            return false;

        }

        for($i = 2;$i>=2 && $i<=10;++$i) {
            if (!($phone[$i] >= "0" && $phone[$i] <= "9")) {
            echo "请输入有效的电话号码，必须全为数字。<br>";
            return false;
            }
        }

        return true;
    }
    //以下代码是对上面函数的测试
    // $result = checkPhone_01("13772816626");
    // if($result) {
    //     //正式注册，insert一条数据到数据库中

    // }
    // else {
    //     echo "<script>window.alert('你输入的电话号码有误')</script>";
    // }


    echo "*****************checkPhone_01*******************<br>";

    /**
     * 改造checkPhone_01函数，并进行测试
     * 
     */

     function checkPhone_02($phone) {

        $len = strlen($phone);
        if ($len != 11) {
            // echo "请输入有效电话号码，长度必须为11。<br>";
            return false;
        }

        if ($phone[0] != "1") {
            // echo "请输入有效电话号码，第一位必须是1。<br>";
            return false;

        }

        if (!($phone[1] >= "3" && $phone[1] <= "9")) {
            // echo "请输入有效电话号码，第二位只能在 3-9。<br>";
            return false;

        }

        for($i = 2;$i>=2 && $i<=10;++$i) {
            if (!($phone[$i] >= "0" && $phone[$i] <= "9")) {
            // echo "请输入有效的电话号码，必须全为数字。<br>";
            return false;
            }

        }
        return true;
        
    }

    echo "*****************checkPhone_02*******************<br>";



    /**
     * 改造checkPhone_02函数，并进行测试
     * 将所有判断合在一起，并引入 is_numeric() 函数
     */

    function checkPhone_03($phone) {
        $len = strlen($phone);

        // is_numeric() 函数判断字符串是否为数字，就代替了for循环
        if(($len != 11) || ($phone[0] != "1") || (!($phone[1] >= "3" && $phone[1] <= "9")) || (!is_numeric($phone))) {
            return false;    
        }
        return true;
    }

    echo "*****************checkPhone_03*******************<br>";




    /**
     * 如果自己不知道php中有内置的 is_numeric() 函数
     * 自己实现is_numeric()函数
     */

    function checkNum($number) {
        for($i = 0;$i>=0 && $i<=strlen($number)-1;++$i) {
            if (!($number[$i] >= "0" && $number[$i] <= "9")) {
            //echo "请输入有效的电话号码，必须全为数字。<br>";
            return false;
            }
        }
        return true;

    }

    function checkPhone_04($phone) {
        $len = strlen($phone);

        if(($len != 11) || ($phone[0] != "1") || (!($phone[1] >= "3" && $phone[1] <= "9")) || (!checkNum($phone))) {
            return false;    
        }
        return true;
     }

    /**
     * 使用正则表达式判断手机号
     */
    function checkPhone_05($phone) {
        $result = preg_match("/^1[3-9]\d{9}$/",$phone);
        return $result;
    }


    /**
     * 自动化功能测试部分
     */
    function text_checkPhone($phone,$expect) {
        $result = checkPhone_05($phone);
        if ($result == $expect) {
            echo "$phone 测试成功<br>";
        }
        else {
            echo "$phone 测试失败<br>";
        }
    }

    text_checkPhone("13892696338",true);
    text_checkPhone("13892696338",true);
    text_checkPhone("18710666870",true);
    text_checkPhone("13772816626",true);

    echo "<br>";

    text_checkPhone("12892696338",false);
    text_checkPhone("13892w96338",false);
    text_checkPhone("08710666870",false);
    text_checkPhone("1377281662",false);

?>