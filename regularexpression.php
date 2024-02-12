<?php

    //regular expression 正则表达式
    /**
     * 用于判断某个字符串是否满足要求 - 匹配
     * 用于从一个字符串中查找满足要求的内容 - 查找
     * 用于把一个字符串中满足要求的内容替换成其他内容 - 替换
     */

    //匹配

    function re_basic() {
        $source = "ymqyyyyyyyyds";
        // $pattern = "/^ymqy{3,5}.*\.$/";  // - 以ymqy开头，并且匹配到q后面的y至少 3-5 个，同时以 . 结尾
        $pattern = "/^y[a-z][a-z]\w{10}$/"; // - 以y开头，接下来两个在 a-z 的范围内，接着以十个字符结束
                                            //一个 [] 中包裹的是对一位进行的判断
        // $pattern = "/^\./";

        // $pattern = "/ds$/";


        $result = preg_match($pattern,$source);
        if ($result) {
            echo "匹配成功<br>";
            
        }
        else {
            echo "匹配失败<br>";
            
        }

    }

    // re_basic();

    function re_phone() {
        $phone = "13772816626";
        $pattern = "/^1[3-9]\d{9}$/";

        $result = preg_match($pattern,$phone);
        if ($result) {
            echo "匹配成功<br>";
            
        }
        else {
            echo "匹配失败<br>";
            
        }

    }

    // re_phone();


    function re_ip() {
        $ip = "192.168.230.147";
        // $pattern = "/^[01]?\d?\d{1}$/";  // 1 - 199 范围
        // $pattern = "/^2[0-4]\d{1}$/";  // 200 - 249 范围
        // $pattern = "/^2[5][0-5]$/";  // 250 - 255 范围
        $pattern = "/([01]?\d?\d{1})|(2[0-4]\d{1})|(2[5][0-5])
                    \.([01]?\d?\d{1})|(2[0-4]\d{1})|(2[5][0-5])
                    \.([01]?\d?\d{1})|(2[0-4]\d{1})|(2[5][0-5])
                    \.([01]?\d?\d{1})|(2[0-4]\d{1})|(2[5][0-5])/";
        // $pattern = "/^([01]?\d?\d{1})|(2[0-4]\d{1})|(2[5][0-5])(\.([01]?\d?\d{1})|(2[0-4]\d{1})|(2[5][0-5]$)){3}/";
        //当所有结果连起来了之后我们就需要把 ^ 和 $ 放在最前面和最后面，这样才能匹配到完整的一段，否则每个都加上 ^ $ ，那么每一个小的都代表着匹配结束，不合题意
        // $pattern = "/^(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])){3}$/";
        


        $result = preg_match($pattern,$ip);
        if ($result) {
            echo "匹配成功<br>";
            
        }
        else {
            echo "匹配失败<br>";
            
        }
    }

    re_ip();




    //查找
    //通过设定的模式去查找满足该模式的内容
    function re_find() {
        $source = "我很喜欢玩手机，所以我买了很多手机，我爸爸给我买了一个最贵的手机，
        手机号码是18812345678,这个手机号码是不是很牛逼啊，但是我妈妈还给我买了手机，
        号码是138383839438,这个号码可够38的,也不知道咱想的,上次过生日,
        我朋友又给我搞了一部手机,手机号码是18612351233,但是有这么多手机,
        我的每个月的费用也花不少,上个月花了13812312元,这个月又花了188123456元,
        好废钱啊,但是无所谓,老子有的是钱,看了一下账户,一共还有1991334567801901234658765,唉,花不完啊";
    
        $pattern = "/1[3-9]\d{9}/";  //注意这里匹配模式中去除了 ^ 和 $ ，因为我们需要从文本中取出所有电话号码
        //就不能以什么开头和以什么结尾,且文本以 我 开头，根本不符合
        preg_match_all($pattern,$source,$result);
        // $result 的返回结果是一个数组，数组类型的输出不能呢个使用 echo 或 print
        //要使用 print_r 或 var_dump
        print_r($result);
    
    }
    //re_find();
    //通过设定左右边界来查找左右边界夹着的内容
    function re_lr() {
        $source='<li><a href="//www.runoob.com/">首页</a></li>
        <li><a href="/html/html-tutorial.html">HTML</a></li>
        <li><a href="/css/css-tutorial.html">CSS</a></li>
        <li><a href="/js/js-tutorial.html">JavaScript</a></li>
        <li><a href="javascript:void(0);" data-id="vue">Vue</a></li>
        <li><a href="javascript:void(0);" data-id="bootstrap">Bootstrap</a></li>
        <li><a href="/nodejs/nodejs-tutorial.html">NodeJS</a></li>
        <li><a href="/python3/python3-tutorial.html">Python3</a></li>
        <li><a href="/python/python-tutorial.html">Python2</a></li>
        <li><a href="/java/java-tutorial.html">Java</a></li>
        <li><a href="/cprogramming/c-tutorial.html">C</a></li>
        <li><a href="/cplusplus/cpp-tutorial.html">C++</a></li>
        <li><a href="/csharp/csharp-tutorial.html">C#</a></li>
        <li><a href="/go/go-tutorial.html">Go</a></li>
        <li><a href="/sql/sql-tutorial.html">SQL</a></li>
        <li><a href="/linux/linux-tutorial.html">Linux</a></li>
        <li><a href="/jquery/jquery-tutorial.html">jQuery</a></li>
        <li><a href="/browser-history">本地书签</a></li>';
        $pattern = '/<a href="(.+?)">/';
        // 匹配模式中， () 左右两变分别表示被夹部分的左右两边的内容，中间使用非贪婪模式进行查找
        preg_match_all($pattern,$source,$result);
        print_r($result);

    }
    //re_lr();


    //替换

    function re_replace() {
        $source = "我很喜欢玩手机，所以我买了很多手机，我爸爸给我买了一个最贵的手机，
        手机号码是18812345678,这个手机号码是不是很牛逼啊，但是我妈妈还给我买了手机，
        号码是138383839438,这个号码可够38的,也不知道咱想的,上次过生日,
        我朋友又给我搞了一部手机,手机号码是18612351233,但是有这么多手机,
        我的每个月的费用也花不少,上个月花了13812312元,这个月又花了188123456元,
        好废钱啊,但是无所谓,老子有的是钱,看了一下账户,一共还有1991334567801901234658765,唉,花不完啊";
    
        $content = "99999999999";
        $pattern = "/1[3-9]\d{9}/";
        
        print_r(preg_replace($pattern,$content,$source));
        //或者将preg_replace($pattern,$content,$source)赋值给新的变量，然后输出新变量
        
    
    }
    //re_replace();
    

?>