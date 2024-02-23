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
```



## 三、修改某个节点内容



## 四、将数组内容写入XML



## 五、使用XPATH操作XML



## 六、XPath语法



## 七、DOMDocument的属性和方法



## 八、读取 防火墙配置文件

