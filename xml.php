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
        $nodes = $doc->getElementsByTagName("student"); //获取student节点
    $students = array();  //创建一个空数组用于存储xml文件数据
    foreach($nodes as $k=>$v) {  // 这里只有 $k 才是 $nodes 的每一个元素，$k 只是一个数字，相当于是student节点个数的下标
        // echo $k." ";  //0 1 2 3 4 5 代表了6个student节点的下标
        // echo $v->getElementsByTagName('id')->item(0)->nodeName."=";
        $students[$k]['id'] = $v->getElementsByTagName("id")->item(0)->nodeValue;  // $v 节点下的第一个id节点的值
        $students[$k]['name'] = $v->getElementsByTagName("name")->item(0)->nodeValue;  // $v 节点下的第一个id节点的值
        $students[$k]['sex'] = $v->getElementsByTagName("sex")->item(0)->nodeValue;  // $v 节点下的第一个id节点的值
        $students[$k]['age'] = $v->getElementsByTagName("age")->item(0)->nodeValue;  // $v 节点下的第一个id节点的值
        $students[$k]['degree'] = $v->getElementsByTagName("degree")->item(0)->nodeValue;  // $v 节点下的第一个id节点的值
        $students[$k]['school'] = $v->getElementsByTagName("school")->item(0)->nodeValue;  // $v 节点下的第一个id节点的值
        // print_r($student[$k]['id']);
        // echo "<br>";
    }
    // echo "<br>";
    foreach($students as $student) {
        print_r($student);
        echo "<br>";
    }
    echo "</p>";

    /**以上遍历代码可以优化为 */
    $tags = array('id','name','sex','age','degree','school');
    foreach($nodes as $k=>$v) {
        foreach($tags as $tag) {
            $students[$k][$tag] = $v->getElementsByTagName($tag)->item(0)->nodeValue;
        }
    }
    foreach($students as $student) {
        print_r($student);
        echo "<br>";
    }
    echo "</p>";
?>

    /**读取 firewall.xml的所有端口 */
    $doc1->load('../firewalld.xml');
    $nodes = $doc1->getElementsByTagName('port');
    foreach($nodes as $node) {
        $attr = $node->attributes;
        echo $attr->item(1)->nodeName."=";
        echo $attr->item(1)->nodeValue."  ";
    }
    echo "<br>";

    /**使用PHP修改xml文件节点的内容 */
    $doc2 = new DOMDocument();
    $doc2->preserveWhiteSpace = false;  // 该值默认时 true ，意思是默认保留空白，但如果单单设置参数为false，就会将节点前的所有空白删除，此时所有文件内容全都在一行，很丑陋，于是有了下面的参数
    $doc2->formatOutput = true;  // 添加这个参数，使得可以格式化输出文本内容，确保保持xml文件格式
    $doc2->load('../student.xml');
    // $doc2->load('../firewalld.xml');
    $nodes = $doc2->getElementsByTagName('student');
    $nodes->item(0)->attributes->item(0)->nodeValue = '11';
    $doc2->save('../student.xml');

    $nodes->item(0)->childNodes->item(1)->nodeValue = 'ymqyyds';
    $doc2->save('../student.xml');
    // 以上内容修改失败，原因是因为xml文件格式化时前面都有空白，默认时，该空白也会被认为是一个节点，我们可以使用下面foreach循环进行测试，浏览器默认将多个空格转换为一个空格输出
    // foreach($nodes->item(0)->childNodes as $node) {
    //     echo $node->nodeValue."<br>";
    //     // 输出结果和正常的很不一样，为了解决这个问题我们需要加入两个参数  $doc2->preserveWhiteSpace = false  $doc2->formatOutput = true 然后这段代码运行才能成功
    // }
