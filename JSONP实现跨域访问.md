[TOC]



# ==JSONP实现跨域访问==

## 课程目标

1、理解JSONP跨域访问的解决方案和实现原理

2、能够利用JavaScript后台和JQuery实现跨域处理

3、理解JavaScript后台代码回调的工作机制，并实现代码回调

4、综合上述，利用JSONP实现跨域访问

## 一、生成JSON响应

### 1、生成json数据的PHP代码

在192.168.2230.147服务器上生成PHP代码，并命名为list-json.php

```php
<?php

// 链接数据库并访问数据
$conn = new mysqli('127.0.0.1','root','','woniunote',3306) or die("数据库连接失败");
$conn->set_charset("utf8");

$sql = "select articleid,headline from article where articleid<5";
$result = $conn->query($sql);

// 输出JSON数据到页面
$json_result = json_encode($result->fetch_all(MYSQLI_ASSOC));
echo $json_result;
//echo "<br>";
//echo gettype($json_result);

$conn->close();

?>
```

在192.168.230.135服务器上生成PHP代码，也命名为list-json.php

```php
<?php

// 链接数据库并访问数据
$conn = new mysqli('127.0.0.1','root','','mysql',3306) or die("数据库连接失败");
$conn->set_charset("utf8");

$sql = "select Host,User from user";
$result = $conn->query($sql);

// 输出JSON数据到页面
$json_result = json_encode($result->fetch_all(MYSQLI_ASSOC));
echo $json_result;
//echo "<br>";
//echo gettype($json_result);

$conn->close();

?>
```

### 2、浏览器访问

浏览器访问http://192.168.230.147/security/list-json.php，结果如下

![image-20240812194429896](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812194429896.png)

浏览器访问http://192.168.230.135/list-json.php，结果如下

![image-20240812194500018](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812194500018.png)

## 二、利用页面ajax访问

### 1、获取JSON数据的html页面

在192.168.230.147构建一个html页面，命名为list-json.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript">
        var listurl = "http://192.168.230.147/security/list-json.php";
        // var listurl = "http://192.168.230.135/list-json.php";

        // 实例化XMLHttpRequest，用于发送AJAX请求
        xmlhttp = new XMLHttpRequest();
        var count = 0;
        // 当页面请求状态发生变化，触发执行代码
        xmlhttp.onreadystatechange=function() {
            if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                // 取得请求后，从响应中通过正则提取Token
                var text = xmlhttp.responseText;
                alert(text);
            }
        };
        xmlhttp.open("GET",listurl,false);
        xmlhttp.send();
    </script>
    <title>跨域访问请求查看JSON数据</title>
</head>
<body>
    welcome to security world
</body>
</html>
```

在192.168.230.135服务器上后见一个html页面，命名为list-json.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript">
        // var listurl = "http://192.168.230.147/security/list-json.php";
        var listurl = "http://192.168.230.135/list-json.php";

        // 实例化XMLHttpRequest，用于发送AJAX请求
        xmlhttp = new XMLHttpRequest();
        var count = 0;
        // 当页面请求状态发生变化，触发执行代码
        xmlhttp.onreadystatechange=function() {
            if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                // 取得请求后，从响应中通过正则提取Token
                var text = xmlhttp.responseText;
                alert(text);
            }
        };
        xmlhttp.open("GET",listurl,false);
        xmlhttp.send();
    </script>
    <title>跨域访问请求查看JSON数据</title>
</head>
<body>
    welcome to security world
</body>
</html>
```

### 2、浏览器同源访问

访问http://192.168.230.147/security/list-json.html，该html页面代码中访问http://192.168.230.147/security/list-json.php，正常弹窗，结果如下：

![image-20240812195902741](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812195902741.png)

访问http://192.168.230.135/list-json.html，该html页面代码中访问http://192.168.230.135/list-json.php，正常弹窗，结果如下：

![image-20240812200347465](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812200347465.png)

### 3、浏览器跨域访问

访问http://192.168.230.147/security/list-json.html，该html页面代码访问http://192.168.230.135/list-json.php，弹窗不显示，结果如下：

![image-20240812210536468](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812210536468.png)

![image-20240812210721221](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812210721221.png)

我们可以发现，明明请求的响应中带有我们所需要的信息，但为社么浏览器没有给我们显示出来呢？是因为响应中没有 Access-Control-Allow-Origin 字段

访问http://192.168.230.135/list-json.html，该html页面代码访问http://192.168.230.147/security/list-json.php，弹窗不显示，结果如下：

![image-20240812210555803](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812210555803.png)

![image-20240812213047845](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812213047845.png)

我们可以看到，以上就是跨域访问的问题，即使服务器响应回了正常的数据，但由于请求头中带有Origin字段表示跨域访问，而响应中又没有Access-Control-Allow-Origin字段来同意跨域访问，所以浏览器解析响应时便认定服务器不同意跨域访问，所以就不显示响应数据

## 三、使用JSONP解决跨域访问的问题

### 1、修改list-json.php

两台服务器上的list-json.php修改方式都一样

```php
#只需将
echo $json_result;
#替换为
echo $_GET['callback']."(".$json_result.")";  //向前端页面输出回调函数，然后再html页面中使用js代码执行。
```

访问http://192.168.230.147/security/list-json.php?callback=test之后输出结果如下：

```
test([{"articleid":"1","headline":"\u6f2b\u8c08\uff1a\u5f3a\u54e5\u5728\u5f3a\u54e5\u5b66\u5802\u60f3\u5bf9\u670b\u53cb\u4eec\u8bf4\u7684\u4e00\u4e9b\u8bdd"},{"articleid":"2","headline":"\u6f2b\u8c08\uff1a\u5df2\u7ecf\u6709\u8717\u725b\u5b66\u9662\u4e86\uff0c\u4e3a\u4ec0\u4e48\u8fd8\u8981\u521b\u529e\u5f3a\u54e5\u5b66\u5802\uff1f"},{"articleid":"3","headline":"\u6f2b\u8c08\uff1a\u8f6f\u4ef6\u5f00\u53d1\u548c\u8f6f\u4ef6\u6d4b\u8bd5\uff0c\u6211\u8be5\u5982\u4f55\u9009\u62e9\uff1f"},{"articleid":"4","headline":"\u6f2b\u8c08\uff1aJava\u548cPython\u73b0\u5728\u90fd\u633a\u706b\uff0c\u6211\u5e94\u8be5\u600e\u4e48\u9009\uff1f"}])
string
```

访问http://192.168.230.135/list-json.php?callback=test之后输出结果如下：

```
test([{"Host":"%","User":"root"},{"Host":"127.0.0.1","User":"root"},{"Host":"::1","User":"root"},{"Host":"localhost","User":""},{"Host":"localhost","User":"pma"},{"Host":"localhost","User":"root"}])
string
```

### 2、修改list-json.html

192.168.230.147要跨域访问192.168.230.135上的list-json.php，所以 ` <script src="http://192.168.230.135/list-json.php?callback=test"></script>`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript">
        // 先定义好一个js函数
        function test(args) {
            //alert(args); args是一个json对象，直接显示我们看到的结果只是 object 这样的内容
            alert(JSON.stringify(args));
        }

    </script>
    <!--形成回调之后，在直接去调用test($json_result)，所以要保证test函数先定义callback函数参数值必须是回调函数名-->
    <script src="http://192.168.230.135/list-json.php?callback=test"></script>
    <title>跨域访问请求查看JSON数据</title>
</head>
<body>
    welcome to security world
</body>
</html>
```

一旦远程代码包含了之后，就会变成

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript">
        // 先定义好一个js函数
        function test(args) {
            //alert(args); args是一个json对象，直接显示我们看到的结果只是 object 这样的内容
            alert(JSON.stringify(args));
        }

    </script>
    <!--形成回调之后，在直接去调用test($json_result)，所以要保证test函数先定义callback函数参数值必须是回调函数名-->
    <script>
        test([{"Host":"%","User":"root"},{"Host":"127.0.0.1","User":"root"},{"Host":"::1","User":"root"},{"Host":"localhost","User":""},{"Host":"localhost","User":"pma"},{"Host":"localhost","User":"root"}])
    </script>
    <title>跨域访问请求查看JSON数据</title>
</head>
<body>
    welcome to security world
</body>
</html>
```

所以下面的 <script> 标签中的test()就会执行上面 <script> 标签中的函数。

修改192.168.230.135上的list-json.html

> 同样的，192.168.230.135要跨域访问192.168.230.147上的list-json.php，所以对应的html代码中 ` <script src="http://192.168.230.147/security/list-json.php?callback=test"></script>`

**注意，我们包含的不是一份代码，而是以恶url地址请求，所以包含之后得到的内容将会是url地址请求之后的响应内容**

### 3、浏览器访问

访问http://192.168.230.147/security/list-json.html，通过192.168.230.135的list-json.php代码执行之后，包含到前端页面进行回调，将可以弹窗得到192.168.230.135的数据库的json数据

![image-20240812215228600](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812215228600.png)

同样的，访问http://192.168.230.135/list-json.html，通过192.168230.147的list-json.php代码执行后的结果包含到前端页面，进行回调得到的是192.168.230.147的woniunote数据库中的内容

![image-20240812215552160](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812215552160.png)

### 4、思考总结

JSONP这种基于回调函数的方式，为什么可以实现跨域？

因为script标签不受同源策略的影响，再通过回调将script标签中远程包含的输出结果作为代码执行，执行的代码就是访问list-json.php的响应结果。

### 5、使用JQuery完成跨域回调

```js
<script src="jquery-3.4.1.min.js"></script>
<script>
    $.getJSON("http://192.168.230.135/list-json.php?callback=test",function(data) {
        alert(JSON.stringify(data));
    });
</script>
```

### 6、JSONP跨域要点

当list-json.php实现了跨域访问后，任意网站的页面均可以访问其数据，只要知道其参数名称`$_GET['callbsck']`，从而在js代码（该代码执行的函数名称要和`$_GET['callbsck']` 传递的参数值一样）中进行函数回调，即可完成访问。

另外一点就是将 `<script src="http://192.168.230.135/list-json.php?callback=test"></script>` 放在 <script> 标签中不受同源策略的影响，该标签允许跨域访问。

JSONP存在的限制：只能处理GET请求，必须经过回调，在真实场景中比较受限。