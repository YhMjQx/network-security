<?php

    /* 以下都是索引数组 */
    echo "=======================索引数组==========================="."<br>";

    $students = array("起陈姐","名杨天下","林俊杰","周姐","周杰伦","卤瑞征","牛文轩",
                    "张明宇","白浩然","王滋帆","田宇桐","范媛僧","王昊","慰问");
    //增
    array_push($students,"工程选");
    print_r($students);
    echo "<br>";
    //这里也可以使用 array_splice($array1,start,length,$array2); 函数进行增加

    //删
    array_pop($students);
    print_r($students);
    echo "<br>";

    //查
    $len = count($students);
    echo "count= ".$len."<br>";
    echo $students[1]."<br>";

    //改
    $students[0] = "齐晨婕";
    print_r($students);
    echo "<br>";

    array_splice($students,1,0,"杨明强yyds");
    print_r($students);
    echo "<br>";

    //使用数组函数 array_rand($array,num) 随机取下标
    //array_rand($array1,num),num表示返回多少个，默认值是1个，
    $index=array_rand($students,1);
    echo "index= ".$index." name= ";
    echo $students[$index]."<br>";

    //如果num是多个，那么就返回的是值为随机键名的数组
    $random_students=array_rand($students,3);
    print_r($random_students);
    echo "<br>";
    //利用随机生成的下标取原数组内容
    echo "index= ".$random_students[0]." name= ".$students[$random_students[0]]."<br>";
    echo "index= ".$random_students[1]." name= ".$students[$random_students[1]]."<br>";
    echo "index= ".$random_students[2]." name= ".$students[$random_students[2]]."<br>";

    echo "</p>";

    //使用原始的随机数生成器
    // 生成 [5,10] 范围内的整数
    //echo rand(5,10)."<br>";   

    //利用随机数生成器随机取数组元素
    echo "index= ".rand(0,count($students)-1)." name= ".$students[rand(0,count($students)-1)];  
    echo "<br>";

    //数组去重
    $number = array(123,456,789,147,258,369,753,951,159,357,951,753);
    $unique_number = array_unique($number);
    print_r($unique_number);
    echo "<br>";


    //数组遍历
    //使用for循环生成下标的方式
    for($i=0;$i<count($number);++$i) {
        echo $number[$i]." ";
    }
    echo "<br>";

    //使用foreach进行循环遍历
    foreach($number as $num) {
        echo $num." ";
    }
    echo "<br>";


    //数组排序
    // sort - 升序排列
    // rsort - 降序排列
    sort($number);
    for($i=0;$i<count($number);++$i) {
        echo $number[$i]." ";
    }
    echo "<br>";
    rsort($number);
    for($i=0;$i<count($number);++$i) {
        echo $number[$i]." ";
    }
    echo "<br>";

    /* 以下都是关联数组 */
    echo "=======================关联数组==========================="."<br>";
    
    //以 key => value 组成的键值对，取值的时候用key来取值，而不是下标
    //索引数组的 key 就是 下标，也就是0,1,2...这种数字
    $student01 = array("name"=>"杨明强","age"=>"19","addr"=>"陕西汉中","phone"=>"13845678910");
    $student02 = array("name"=>"齐晨婕","age"=>"20","addr"=>"陕西西安","phone"=>"18745612310");
    $student03 = array("name"=>"卢瑞征","age"=>"20","addr"=>"陕西西安","phone"=>"13925836910");
    $student04 = array("name"=>"刘文轩","age"=>"19","addr"=>"陕西汉中","phone"=>"18725814710");
    $student05 = array("name"=>"田宇桐","age"=>"20","addr"=>"陕西榆林","phone"=>"13712345610");

    print_r($student01);
    echo "<br>";

    //查
    echo $student01["name"]."<br>";

    //改
    $student01["addr"]="陕西西安";
    echo $student01["addr"]."<br>";

    //遍历关联数组的value
    foreach($student01 as $stu) {
        echo $stu." ";
    }
    echo "<br>";

    //遍历关联数组的key
    foreach($student01 as $key=>$value) {
        echo $key."=".$value." ";
    }
    echo "<br>";

    //array_keys() 返回关联数组的所有key作为一个数组
    print_r(array_keys($student01));
    echo "<br>";

    //因此我们可以通过使用 aarray_keys() 的返回数组来遍历原数组
    $keys=array_keys($student01);
    foreach($keys as $key) {
        echo $student01[$key]." ";
    }
    echo "<br>";



    echo "=======================内置函数==========================="."<br>";
    //直接取得数组的最后一个值，无所谓数组类型
    echo end($student02)."<br>";  

    //判断一个值是否在数组中,使用 in_array() 函数
    if(in_array("田宇桐",$student05)) {
        echo "bingo"."<br>";
    }
    else {
        echo "oh,no"."<br>";
    }
    
    //explode() 把字符串打散为数组。第一个参数为打散字符窜时所用到的分隔符
    $source = "ymqyyds-ymqnb-ymq30W";
    $newarray =  explode("-",$source);
    print_r($newarray);
    echo "<br>";

    //implode() 返回一个由数组元素组成的字符串
    $numarray = array(123,456,789,147,258,369,753,951,159,357,951,753);
    $numstr = implode("-",$numarray);  //第一个参数为合并元素时所用到的分隔符
    echo $numstr."<br>";



    echo "=======================二维数组==========================="."<br>";
    $student01 = array("name"=>"杨明强","age"=>"19","addr"=>"陕西汉中","phone"=>"13845678910");
    $student02 = array("name"=>"齐晨婕","age"=>"20","addr"=>"陕西西安","phone"=>"18745612310");
    $student03 = array("name"=>"卢瑞征","age"=>"20","addr"=>"陕西西安","phone"=>"13925836910");
    $student04 = array("name"=>"刘文轩","age"=>"19","addr"=>"陕西汉中","phone"=>"18725814710");
    $student05 = array("name"=>"田宇桐","age"=>"20","addr"=>"陕西榆林","phone"=>"13712345610");

    $class = array($student01,$student02,$student03,$student04,$student05);
    echo $class[1]["name"]."<br>";

?>