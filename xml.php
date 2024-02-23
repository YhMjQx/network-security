<?php

    $doc = new DOMDocument();  // 实例化一个DOMDocument对象
    $doc->load('./student.xml');

    // 读取class节点的属性 id 和 对应的值
    $nodes1 = $doc->getElementsByTagName('class');  
    // 现在的 $nodes 就是 class 节点，返回的结果是数组形式
    // 因为可能会有多个class节点，但是XML文件只能有一个根节点
    echo $nodes1->item(0)->nodeName." ";  //获取第一个class节点的节点名
    echo $nodes1->item(0)->attributes->item(0)->nodeName."="; //获取第一个class节点的第一个属性节点的名字
    echo $nodes1->item(0)->attributes->item(0)->nodeValue."<br>"; //获取第一个节点的第一个属性节点的值

    // 遍历id标签的值
    $nodes2 = $doc->getElementsByTagName("id");
    foreach($nodes2 as $node) {
        echo $node->nodeValue." ";
    }
    echo "<br>";

    // 遍历name标签的值
    echo "name= ";
    $nodes3 = $doc->getElementsByTagName("name");
    foreach($nodes3 as $node) {
        echo $node->nodeValue." ";
    }
    echo "<br>";

    // 遍历student标签的节点名和节点值
    echo "sequence= ";
    $nodes4 = $doc->getElementsByTagName("student");
    foreach($nodes4 as $node) {
        echo $node->attributes->item(0)->nodeName."=";
        echo $node->attributes->item(0)->nodeValue." ";
    }
    echo "<br>";

    // 读取第二个学生的所有信息
    $studentnodes = $doc->getElementsByTagName("student");
    $nodes = $studentnodes->item(1)->childNodes;  // childNodes 表示 该节点下的所有子节点
    foreach($nodes as $node) {
        echo $node->nodeName."=";
        echo $node->nodeValue." ";
    }

    // 读取XML文件数据保存在PHP的二维数组当中
    
?>