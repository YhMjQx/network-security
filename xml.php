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


/**将数组内容写入XML */
    $student01 = array("name"=>"杨明强","age"=>"19","addr"=>"陕西汉中","phone"=>"13845678910");
    $student02 = array("name"=>"齐晨婕","age"=>"20","addr"=>"陕西西安","phone"=>"18745612310");
    $student03 = array("name"=>"卢瑞征","age"=>"20","addr"=>"陕西西安","phone"=>"13925836910");
    $student04 = array("name"=>"刘文轩","age"=>"19","addr"=>"陕西汉中","phone"=>"18725814710");
    $student05 = array("name"=>"田宇桐","age"=>"20","addr"=>"陕西榆林","phone"=>"15529790215");
    $students = array($student01,$student02,$student03,$student04,$student05);


    $doc = new DOMDocument('1.0','utf8'); // 先实例化DOMDocument对象
    $doc->preserveWhiteSpace = false; // 不保留空格
    $doc->formatOutput = true; // 格式化输出XML节点格式

    //  创建根节点，并设置其id属性和值
    $class = $doc->createElement('class');  //创建根节点
    $class->setAttribute('id','安全2204'); //设置根节点class的属性名和属性值
    $doc->appendChild($class);  //将创建好的根节点放在文件中

    //为class根节点创建子节点
    foreach($students as $index=>$student) {
        // 创建student节点,并设置属性和属性值,将其添加在class根节点下
        $nodestudent = $doc->createElement('student');
        $nodestudent->setAttribute('sequence',$index+1);
        $class->appendChild($nodestudent);
        foreach($student as $key=>$value) {
            // 创建student下的子节点，并将其添加在student子节点下
            $nodename = $doc->createElement($key); 
            $nodestudent->appendChild($nodename);

            // 给student下的每一个子节点设置值
            $nodevalue = $doc->createTextNode($value);
            $nodename->appendChild($nodevalue);
        }
    }

    // 最后一定要保存文件
    $doc->save('../write.xml');



    /**使用XPath操作XML XPath定位*/
    $doc = new DOMDocument();
    $doc->preserveWhiteSpace = false;
    $doc->load('../student.xml');
    $xpath = new DOMXPath($doc);  //实例化XPath对象

    // 定义一个表达式
    // $expression = "/school/class[@id='WNCDC086']/student[@sequence='2']/school";
    // $expression = "/school/class[@id='WNCDC085']/student[@sequence='3']/name";
    // $expression = "//class[@id='WNCDC085']/student[@sequence='2']/name";
    // $expression = "//class[2]/student[1]/name";  //查找xml文件下school根节点下的第二个class节点下的第1个student的name 
    // $expression = "//class[2]/student/school[contains(text(),'邮电')]";  // 模糊查询xml文件下school根节点第二个class节点下的student中的school中包含 邮电 两个字的学校
    $expression = "//class[2]/student[age=21]/name";
    $nodes = $xpath->query($expression);  //返回的是找到的所有节点，返回的还是一个数组，即使只找到一个
    echo $nodes->item(0)->nodeValue;


?>

    
