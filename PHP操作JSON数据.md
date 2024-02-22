[TOC]



# ==PHP操作JSON数据==

JSON即 `Java Script Object Notation` 的简写，中文名称为 js对象标记。是一种轻量级的数据交换格式，属于 js 一个子集，简介和清晰的层次结构使得 JSON 称为理想的数据交换语言。易于阅读和编写，同时也易于机器解析和生成，并有效的提升网络传输效率，是目前在互联网上进行数据传输的重要手段。本实验主要为大家介绍JSON数据格式以及如何利用PHP代码对JSON数据进行处理。

> 数据的展现和存储形式
>
> - 数组：索引数组是适用于大多数编程语言的，PHP中有关联数组，JAVA中叫HashMap，Python中叫字典，JavaScript中叫对象
> - CSV：纯文本型的数据，带特定格式，逗号分隔符
> - XML：可扩展标记语言，与HTML格式完全一致，不同的是HTML是预先设定好的标签和属性，用于网页展现；XML的标签是自定义的，用于存储数据
> - JSON：`Java Script Object Notation` 的简写，中文名称为 js对象标记
> - YAML：通产用于服务器端或应用系统的配置文件

## 一、JavaScript的数组与对象

在 JavaScript 中，定义数组的方式与PHP比较类似，只是由PHP中的 圆括号 变成了中括号而已，比如我们定义了一个用户姓名的数组，方式如下

```js
var usernames = ["张三","李四","王五","赵六","周七"];
```

另外，在PHP中我们可以定义关联数组，在JavaScript中也有对应的对象，定义方式如下：

```js
var user1 = {name:"张三",sex:"男",age:30,phone:"13770816666",addr:"陕西西安"};
var user2 = {name:"李四",sex:"男",age:"20",phone:"13778925813",addr:"陕西西安"};
```

我们可以在关联数组中保存索引数组，也可以在索引数组中保存关联数组，在JavaScript中同样可以混合使用，比如可以在JavaScript中定义如下对象：

```js
第一种：索引数组中保存关联数组
var users = [{name:"张三",sex:"男",age:30,phone:"13770816666",addr:"陕西西安"},{name:"李四",sex:"男",age:20,phone:"13778925813",addr:"陕西西安"}];
或：
第二种：关联数组中保存索引数组
var users = {user1:["张三","男",30,"13770816666","陕西西安"],user2:["李四","男",20,"13778925813",陕西西安]};
```

上述的数据定义格式，便构成了JSON的数据格式的基础，并且JSON数据格式在互联晚上方便传输，都是以一个标准的字符串类型存在。



## 二、PHP中处理JSON

```php
<?php
$student01 = array("name"=>"杨明强","age"=>"19","addr"=>"陕西汉中","phone"=>"13845678910");
$student02 = array("name"=>"齐晨婕","age"=>"20","addr"=>"陕西西安","phone"=>"18745612310");
$student03 = array("name"=>"卢瑞征","age"=>"20","addr"=>"陕西西安","phone"=>"13925836910");
$student04 = array("name"=>"刘文轩","age"=>"19","addr"=>"陕西汉中","phone"=>"18725814710");
$student05 = array("name"=>"田宇桐","age"=>"20","addr"=>"陕西榆林","phone"=>"13712345610");

$class = array($student01,$student02,$student03,$student04,$student05);  
echo json_encode($class);
?>
```

直接将数据库中读出来的结果转换为 JSON

```php
<?php
    /**引用commoncondb.php如果之前已经引用则不再引用，使用如下两函数 */
    // require_once('commoncondb.php');
    include_once('commoncondb.php');
    $sql = "select articleid,category,thumbnail,readcount,updatetime from article where articleid < 10;";
    $conn = create_dbcon();
    $result = mysqli_query($conn,$sql);

    $data = mysqli_fetch_all($result,MYSQLI_ASSOC);
    echo json_encode($data);
?>
```

### 对JSON数据进行处理的两个函数

```php
json_encode()  //将JSON的对象或数组形式的数据转换成JSON数据的字符串，也叫做JSON序列化
json_decode()  //将JSON数据字符串转换成数组形式或对象，也叫做JSON反序列化
```

#### JSON序列化

```php
    /**引用commoncondb.php如果之前已经引用则不再引用，使用如下两函数 */
    // require_once('commoncondb.php');
    include_once('commoncondb.php');
    $sql = "select articleid,category,thumbnail,readcount,updatetime from article where articleid < 10;";
    $conn = create_dbcon();
    $result = mysqli_query($conn,$sql);

    $data = mysqli_fetch_all($result,MYSQLI_ASSOC);
    echo json_encode($data);  //JSON序列化，将变量或对象转换成json字符串
```

如下是JSON序列化的输出结果，这是JSON的数据类型

```
[{"articleid":"1","category":"5","thumbnail":"1.jpg","readcount":"1510","updatetime":"2017-11-10 12:28:08"},{"articleid":"2","category":"5","thumbnail":"2.jpg","readcount":"2865","updatetime":"2017-11-15 15:53:13"},{"articleid":"3","category":"5","thumbnail":"3.jpg","readcount":"3124","updatetime":"2017-11-12 00:31:03"},{"articleid":"4","category":"5","thumbnail":"4.jpg","readcount":"5783","updatetime":"2017-11-17 14:43:53"},{"articleid":"5","category":"5","thumbnail":"5.jpg","readcount":"1215","updatetime":"2017-12-05 15:15:32"},{"articleid":"6","category":"5","thumbnail":"6.jpg","readcount":"962","updatetime":"2017-11-20 16:49:00"},{"articleid":"7","category":"5","thumbnail":"7.jpg","readcount":"917","updatetime":"2017-11-12 00:31:57"},{"articleid":"8","category":"5","thumbnail":"8.jpg","readcount":"1091","updatetime":"2017-12-05 15:17:29"},{"articleid":"9","category":"7","thumbnail":"9.jpg","readcount":"900","updatetime":"2017-11-11 03:24:21"}]
```

#### JSON反序列化

```php
json_decode()  //将JSON数据字符串转换成数组形式或对象，也叫做JSON反序列化
```

```php
    $string = '[{"articleid":"1","category":"5","thumbnail":"1.jpg","readcount":"1510","updatetime":"2017-11-10 12:28:08"},{"articleid":"2","category":"5","thumbnail":"2.jpg","readcount":"2865","updatetime":"2017-11-15 15:53:13"},{"articleid":"3","category":"5","thumbnail":"3.jpg","readcount":"3124","updatetime":"2017-11-12 00:31:03"},{"articleid":"4","category":"5","thumbnail":"4.jpg","readcount":"5783","updatetime":"2017-11-17 14:43:53"},{"articleid":"5","category":"5","thumbnail":"5.jpg","readcount":"1215","updatetime":"2017-12-05 15:15:32"},{"articleid":"6","category":"5","thumbnail":"6.jpg","readcount":"962","updatetime":"2017-11-20 16:49:00"},{"articleid":"7","category":"5","thumbnail":"7.jpg","readcount":"917","updatetime":"2017-11-12 00:31:57"},{"articleid":"8","category":"5","thumbnail":"8.jpg","readcount":"1091","updatetime":"2017-12-05 15:17:29"},{"articleid":"9","category":"7","thumbnail":"9.jpg","readcount":"900","updatetime":"2017-11-11 03:24:21"}]';
    $jsonarray = json_decode($string);  //JSON反序列化，将json字符串转换为数组
    print_r($jsonarray);
```

以下是JSON反序列化的输出结果，这是数组类型

```
Array ( [0] => stdClass Object ( [articleid] => 1 [category] => 5 [thumbnail] => 1.jpg [readcount] => 1510 [updatetime] => 2017-11-10 12:28:08 ) [1] => stdClass Object ( [articleid] => 2 [category] => 5 [thumbnail] => 2.jpg [readcount] => 2865 [updatetime] => 2017-11-15 15:53:13 ) [2] => stdClass Object ( [articleid] => 3 [category] => 5 [thumbnail] => 3.jpg [readcount] => 3124 [updatetime] => 2017-11-12 00:31:03 ) [3] => stdClass Object ( [articleid] => 4 [category] => 5 [thumbnail] => 4.jpg [readcount] => 5783 [updatetime] => 2017-11-17 14:43:53 ) [4] => stdClass Object ( [articleid] => 5 [category] => 5 [thumbnail] => 5.jpg [readcount] => 1215 [updatetime] => 2017-12-05 15:15:32 ) [5] => stdClass Object ( [articleid] => 6 [category] => 5 [thumbnail] => 6.jpg [readcount] => 962 [updatetime] => 2017-11-20 16:49:00 ) [6] => stdClass Object ( [articleid] => 7 [category] => 5 [thumbnail] => 7.jpg [readcount] => 917 [updatetime] => 2017-11-12 00:31:57 ) [7] => stdClass Object ( [articleid] => 8 [category] => 5 [thumbnail] => 8.jpg [readcount] => 1091 [updatetime] => 2017-12-05 15:17:29 ) [8] => stdClass Object ( [articleid] => 9 [category] => 7 [thumbnail] => 9.jpg [readcount] => 900 [updatetime] => 2017-11-11 03:24:21 ) )
```





