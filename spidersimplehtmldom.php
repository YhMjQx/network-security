<?php
    /**这把使用PHP的第三方库实现爬虫 */
    include_once('./simple_html_dom.php');
    $html = file_get_html("http://www.woniunote.com/");

    /**查找超链接 */
    // $links = $html->find('a');
    // foreach($links as $link) {
    //     echo $link->href."<br>";
    // }

    // 查找图片链接,不过该代码因为iconv() 函数的问题导致报错，这个问题一直不知道该如何解决
    // $images = $html->find('img');
    // foreach($images as $image) {
    //     // echo $image->src."<br>";
    //     $src = $image->src;
    //     if(strpos($src,'/') == 0) {
    //         $url = "http://www.woniunote.com/".$src;
    //     }
    //     else if(strpos($src,'http') == 0) {
    //         $url = $src;
    //     }
    //     $filename = end(explode('/',$url));
    //     $content = file_get_html($url);
    //     file_put_contents("./download/image/$filename",$content); 
    //     echo "下载成功：$filename <br>";
    //     ob_flush();
    //     flush();
    //     sleep(0.5);
    // } 

    /**使用其他方式定位元素 */
    // 使用类似XPath方式定位元素
    // $titles = $html->find('div[@class="title"]');  
    // $titles = $html->find('div[class="title"]');
    // $titles = $html->find('div.title');  //由于html中 class 在css样式中使用 . 表示，故在这里也可以已使用 .
    // foreach($titles as $title) {
    //     echo $title->innertext."<br>";
    //     // innertext 表示 被 <div></div> 标签包裹的所有内容，也包含 <a></a> 标签
    //     echo $title->outertext."<br>";
    //     // outertext 表示查找到的 <div></div> 标签本身，和他所包裹的所有内容
    //     echo $title->plaintext."<br>";
    //     // plaintext 表示 被 <div></div> 标签包裹的内容中 <a></a> 标签 所包裹的文本内容
    // }

    // 使用ID属性定位元素
    // $nodes = $html->find('input[@id="keyword"]');  // 这种情况返回的都是数组形式，因为simple_html_php并不知道找出的结果是多少个，于是所有返回结果都是数组
    $nodes = $html->find('input#keyword');
    foreach($nodes as $node) {
        echo $node->placeholder."<br>";  // placeholder 就是标签节点中的文本内容
    }
    // 上面代码可以优化。我们知道一份源代码中 input标签中id=keyword只有一个，那么完全可以不使用数组遍历的方式
    // 直接给定元素下标找对应的某一个元素
    $node = $html->find('input#keyword',0);
    echo $node->placeholder."<br>";
    

    /**元素之间的层次关系 */
    $nodes = $html->find('div.title');
    foreach($nodes as $node) {
        echo $node->first_child()->innertext."<br>";        
    }

    // 使用完DOM结构后，清空内存，减少内存消耗
    $html->clear();


    

?>