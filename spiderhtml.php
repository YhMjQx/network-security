<?php
    /**爬取页面源代码 */
    $contents = file_get_contents("http://www.woniunote.com/");
    // echo $contents;  //获取到页面的内容，其源代码和源页面源代码一致
    $html = new DOMDocument();
    $html->preserveWhiteSpace = false;

    @$html->loadHTML($contents);  //在前面加 @ 可以防止warnning警告的输出
    $links = $html->getElementsByTagName("a");
    // print_r($links);  // 输出结果 DOMNodeList Object ( [length] => 93 ) 我们可以看出这是一个链表，下面我们来遍历

    /**输出页面源代码中的超链接并存储到数组中 */
    $LinkList = array();
    foreach($links as $link) {     
        // echo $link->nodeValue."<br>";  // 这个输出的是 <a></a> 中的值
        // echo $link->attributes->item(0)->nodeValue."<br>";  // 但注意，不是所有的<a></a>节点中的第一个属性都是href  
        foreach($link->attributes as $attr) {
            if($attr->nodeName == 'href') {
                // echo $attr->nodeValue."<br>";  // 得到的结果有三个类型 分别是以 / # http 开头
                // 利用 / # http 三个特征来判断href值的类型，以此分别拼接超链接
                if($attr->nodeValue[0] == '/' || $attr->nodeValue[0] == '#') {
                //if(strpos($attr->nodeValue,'/') == 0) //用这个判断也是可以的
                    // echo $attr->nodeValue[0];
                    echo "http://www.woniunote.com".$attr->nodeValue."<br>";
                    $link = "http://www.woniunote.com".$attr->nodeValue;
                    array_push($LinkList,$link);
                }
                else if(strpos($attr->nodeValue,'http://') == 0) {
                    echo $attr->nodeValue."<br>";
                    array_push($LinkList,$attr->nodeValue);
                }
            }
        }
    }

    /**将爬取到的网页源代码存起来 */
    foreach($LinkList as $link) {
        $filename = str_replace('http://www.woniunote.com/','',$link);
        $filename = str_replace('/','-',$filename);
        $content = file_get_contents($link);
        file_put_contents("./download/html/$filename.html",$content);
        echo "成功下载：$filename <br>";
        ob_flush();
        flush();
        sleep(0.5);
    }

    //Warning: file_get_contents(http://www.woniunote.com/page/25): 
    //failed to open stream: HTTP request failed! HTTP/1.1 500 Internal Server Error in 
    //D:\WEB\XAMPP5.6\htdocs\learn\PHP\spider.php on line 40
    //报这个错的原因是woniunote自身框架出了问题
?>