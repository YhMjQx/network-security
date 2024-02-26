[TOC]



# ==PHP读取XML文件==

**只能有一个根标签**

## 一、简介

XML文件的全称为 “extensible Markup Language” ，即：可扩展标记语言，与HTML标记语言是属于同一类型，均由 标签+属性+属性值 构成。与HTML用来展示页面元素不一样的是，XML的标签和属性及属性值完全是自定义的，主要用于存储数据，比如下面的这个XML文件内容，就完整的展示了一个班级学生的信息

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<school>
    <class id="WNCDC085">
    <student sequence="1">
        <id>WNCD26221117</id>
        <name>杨明强</name>
        <sex>男</sex>
        <age>20</age>
        <degree>本科</degree>
        <school>西安邮电大学</school>
    </student>
    
    <student sequence="2">
        <id>WNCD26221116</id>
        <name>卢瑞征</name>
        <sex>男</sex>
        <age>20</age>
        <degree>本科</degree>
        <school>西安邮电大学</school>
    </student>
    
    <student sequence="3">
        <id>WNCD26221125</id>
        <name>田宇桐</name>
        <sex>男</sex>
        <age>20</age>
        <degree>本科</degree>
        <school>西安邮电大学</school>
    </student>
    </class>
    <class id="WNCDC086">
        <student sequence="1">
            <id>WNCD26221133</id>
            <name>齐晨婕</name>
            <sex>男</sex>
            <age>20</age>
            <degree>本科</degree>
            <school>西安邮电大学</school>
        </student>
        
        <student sequence="2">
            <id>WNCD26221126</id>
            <name>张雅妮</name>
            <sex>男</sex>
            <age>20</age>
            <degree>本科</degree>
            <school>西安邮电大学</school>
        </student>
        
        <student sequence="3">
            <id>WNCD26221107</id>
            <name>白浩然</name>
            <sex>男</sex>
            <age>20</age>
            <degree>本科</degree>
            <school>西安邮电大学</school>
        </student>
    </class>
</school>
    
```

将上述XML文件内容转换成一张二维表结构，则如下：

| 序号 | 学号         | 姓名   | 性别 | 年龄 | 学历 | 学校         |
| ---- | ------------ | ------ | ---- | ---- | ---- | ------------ |
| 1    | WNCD26221117 | 杨明强 | 男   | 20   | 本科 | 西安邮电大学 |
| 2    | WNCD26221116 | 卢瑞征 | 男   | 20   | 本科 | 西安邮电大学 |
| 3    | WNCD26221125 | 田宇桐 | 男   | 20   | 本科 | 西安邮电大学 |



## 二、利用DOMDocument读取XML

### 1.读取指定节点内容

```php
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
    $nodes3 = $doc->getElementsByTagName("name");
    foreach($nodes3 as $node) {
        echo $node->nodeValue." ";
    }
?>
```

上述代码针对student.xml的输出结果如下

```
class id=WNCDC085
WNCD26221117 WNCD26221116 WNCD26221125 WNCD26221133 WNCD26221126 WNCD26221107
杨明强 卢瑞征 田宇桐 齐晨婕 张雅妮 白浩然
```

### 2.读取特定节点的属性

```php
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
```

上述代码输出结果如下：

```
name= 杨明强 卢瑞征 田宇桐 齐晨婕 张雅妮 白浩然
sequence= sequence=1 sequence=2 sequence=3 sequence=1 sequence=2 sequence=3
```

除了可以利用nodeValue取得各节点的值，也可以使用nodeName取得节点名称，使用nodeType获取节点类型，这样，就可以在代码中对其进行取值或判断，进而避免一些不必要的输出。

### 3.将XML转换成二维数组

```php
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
```





## 三、修改某个节点内容
```PHP
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
// 第一次以上内容修改失败，原因是因为xml文件格式化时前面都有空白，默认时，该空白也会被认为是一个节点，我们可以使用下面foreach循环进行测试，浏览器默认将多个空格转换为一个空格输出，因此可以利用换行体现
// foreach($nodes->item(0)->childNodes as $node) {
//     echo $node->nodeValue."<br>";
//     // 输出结果和正常的很不一样，为了解决这个问题我们需要加入两个参数  $doc2->preserveWhiteSpace = false  $doc2->formatOutput = true 然后这段代码运行才能成功
// }
```


## 四、将数组内容写入XML
- 创建根节点class，并设置其属性和值
- 利用 foreach 创建根节点下的第一类子节点student，并设置其属性和值
- 利用 foreach 创建第二类子节点name age addr phone，并设置其值

```php
/**将数组内容写入XML */
$student01 = array("name"=>"杨明强","age"=>"19","addr"=>"陕西汉中","phone"=>"13845678910");
$student02 = array("name"=>"齐晨婕","age"=>"20","addr"=>"陕西西安","phone"=>"18745612310");
$student03 = array("name"=>"卢瑞征","age"=>"20","addr"=>"陕西西安","phone"=>"13925836910");
$student04 = array("name"=>"刘文轩","age"=>"19","addr"=>"陕西汉中","phone"=>"18725814710");
$student05 = array("name"=>"田宇桐","age"=>"20","addr"=>"陕西榆林","phone"=>"13712345610");
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
```




## 五、使用XPATH操作XML
### 1.使用XPath读取XML节点

XPath：XML Path 语言，专门用来定位XML标签位置

```php
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
```




## 六、XPath语法
### 1.基本语法

| 表达式            | 描述                                       |
| ----------------- | ------------------------------------------ |
| nodename          | 选取此节点的所有子节点                     |
| /                 | 从当前节点选取直接子节点                   |
| //                | 从当前节点选取子孙节点                     |
| .                 | 选取当前节点                               |
| ..                | 选取当前节点的父节点                       |
| @                 | 选取属性                                   |
| *                 | 通配符，选择所有元素节点与元素名           |
| @*                | 选取所有属性                               |
| [@attrib]         | 选取具有给定属性的所有元素                 |
| [@attrib='value'] | 选取给定属性具有给定值的所有元素           |
| [tag]             | 选取所有具有指定元素的直接子节点           |
| [tag='text']      | 选取所有具有指定元素并且文本内容是text节点 |



### 2.层次与路径

| 路径表达式      | 结果                                                         |
| --------------- | ------------------------------------------------------------ |
| bookstore       | 选取 bookstore 元素的所有子节点。                            |
| /bookstore      | 选取根元素 bookstore。 注释:假如路径起始于正斜杠(/)，则此路径始终代表到某元素的绝对路径! |
| bookstore/book  | 选取属于 bookstore 的子元素的所有 book 元素。                |
| //book          | 选取所有 book 子元素，而不管它们在文档中的位置。             |
| bookstore//book | 选择属于 bookstore 元素的后代的所有 book 元素，而不管它们位于 bookstore 之下的什么位置 |
| //@lang         | 选取名为 lang 的所有属性。                                   |



### 3.谓语属性

| 路径表达式                         | 结果                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| /bookstore/book[1]                 | 选取属于 bookstore 子元素的第一个 book 元素。                |
| /bookstore/book[last()]            | 选取属于 bookstore 子元素的最后一个 book 元素。              |
| /bookstore/book[last()-1]          | 选取属于 bookstore 子元素的倒数第二个 book 元素。            |
| /bookstore/book[position()<3]      | 选取最前面的两个属于 bookstore 元素的子元素的 book 元素。    |
| /title[@lang]                      | 选取所有拥有名为 lang 的属性的 title 元素。                  |
| //title[@lang='eng']               | 选取所有 tite 元素，且这些元素拥有值为 eng的 lang 属性。     |
| /bookstore/book[price>25.00]       | 选取 bookstore 元素的所有 book 元素，且其中的 price 元素的值须大于 25.00 |
| /bookstore/book[price>35.00]/title | 选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于35.00. |

除了上述的基础语法外，XPath还有很多高级语法，比如**模糊查询**等，下面简单举几个事例：

```
//input[@type='submit' and @name='woniuxy']
//input[@type='submit' and not(contains(@name,' woniuxy'))]
//input[starts-with(@id,'woniuxy')]
//input[ends-with(@id,'woniuxy")]
//input[contains(@id, 'woniuxy')]
//bookstore/book[last()-1]
//li[@class="aaa" and @name="fore"]/a/text()
//li[contains(@class ,"aaa") and @name="fore"]/a/text()
//class/title[text()="张三"]
```




## 七、DOMDocument的属性和方法
### 1.属性

```
Attributes 存储节点的属性列表(只读)
chi1dNodes 存储节点的子节点列表(只读)
dataType 返回此节点的数据类型
Definition 以DTD或xML模式给出的节点的定义(只读)
Doctype 指定文档类型节点(只读)
documentElement 返回文档的根元素(可读写)
firstChi1d 返回当前节点的第一个子节点(只读)
1astchi1d 返回当前节点最后一个子节点(只读)
Implementation 返回XMLDOMImplementation对象
nextSib1ing 返回当前节点的下一个兄弟节点(只读)
nodeName 返回节点的名字(只读)
nodeType 返回节点的类型(只读)
nodeTypedvalue 存储节点值(可读写)
nodevalue 返回节点的文本(可读写)
ownerDocument 返回包含此节点的根文档(只读)
parentNode 返回父节点(只读)
Parsed 返回此节点及其子节点是否已经被解析(只读)
Prefix 返回名称空间前缀(只读)
preservewhitespace 指定是否保留空白(可读写)
previousSibling 返回此节点的前一个兄弟节点(只读)
Text 返回此节点及其后代的文本内容(可读写)
ur1 返回最近载入的XML文档的URL(只读)
xml 返回节点及其后代的XML表示(只读)
```

### 2.方法

```
appendchi1d 为当前节点添加一个新的子节点,放在最后的子节点后
c1oneNode 返回当前节点的拷贝
createAttribute 创建新的属性
createCDATASection 创建包括给定数据的CDATA段
createcomment 创建一个注释节点
createDocumentFragment 创建DocumentFragment对象
createElement 创建一个元素节点
createEntityReference 创建EntityReference对象
createNode 创建给定类型,名字和命名空间的节点
createPorcessingInstruction创建操作指令节点
createTextNode 创建包括给定数据的文本节点
getElementsByTagName 返回指定名字的元素集合
haschi1dNodes 返回当前节点是否有子节点
insertBefore 在指定节点前插入子节点
Load 导入指定位置的XML文档
1oadxML 导入指定字符串的XML文档
removeChi1d 从子结点列表中删除指定的子节点
replaceChi1d 从子节点列表中替换指定的子节点
Save 把XML文件存到指定节点
se1ectNodes 对节点进行指定的匹配，并返回匹配节点列表
se1ectSing1eNode 对节点进行指定的匹配，并返回第一个匹配节点
setAttribute 对节点设需属性值
transformNode 使用指定的样式表对节点及其后代进行转换
transformNodeTo0bject使用指定的样式表将节点及其后代转换为对象
```




## 八、读取 防火墙配置文件

