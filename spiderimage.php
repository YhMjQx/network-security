<?php

    $contents = file_get_contents('http://www.woniunote.com/');

    $html = new DOMDocument();
    @$html->loadHTML($contents);

    $links = $html->getElementsByTagName('img'); // $links 是链表的形式存在的

    $LinkList = array();
    foreach($links as $link) {
        // echo $link->attributes->item(0)->nodeName." ";
        // echo $link->attributes->item(0)->nodeValue."<br>";
        foreach($link->attributes as $attr) {
            if($attr->nodeName == 'src') {
                // echo "http://www.woniunote.com".$attr->nodeValue."<br>";
                // $link = "http://www.woniunote.com".$attr->nodeValue;
                // array_push($LinkList,$link);
                if(strpos($attr->nodeValue,'/') == 0) {
                    // echo "http://www.woniunote.com".$attr->nodeValue."<br>";
                    array_push($LinkList,"http://www.woniunote.com".$attr->nodeValue);
                }
                else if(strpos($attr->nodeValue,'https://') == 0) {
                    // echo $attr->nodeValue."<br>";
                    array_push($LinkList,$attr->nodeValue);
                }
            }
        }
    }

    // print_r($LinkList);

    /**将爬取到的图片保存起来 */
    foreach($LinkList as $link) {
        $content = file_get_contents($link);

        // $suffix = end(explode('.',$link));
        // echo $link."<br>";

        // 以下两个判断中，如果不使用 === 强制类型也判断相等的话，那么 http:// == 0 的判断结果 https:// 也能通过，不知道是什么bug
        if(strpos($link,'http://') === 0 ) {  
            // echo $link;

            $filename1 = str_replace('http://www.woniunote.com/','',$link);
            $filename1 = str_replace('/','-',$filename1);
            // echo $filename1."<br>";
            file_put_contents("./download/image/$filename1",$content);
            echo "下载成功：$filename1 <br>"; 
        }
        else if(strpos($link,'https://') === 0) {
            // echo $link;

            $filename2 = str_replace('https://woniuxyopenfile.oss-cn-beijing.aliyuncs.com/woniuxynote/thumb/','',$link);
            // $filename = str_replace('/','-',$filename);
            // $filename = $filename;
            file_put_contents("./download/image/$filename2",$content);
            echo "下载成功：$filename2 <br>";  
        }
        ob_flush();
        flush();
        sleep(0.5);
        
    }
?>