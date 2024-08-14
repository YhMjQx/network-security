[TOC]



# ==CORS跨域访问漏洞==

## 课程目标

1、理解服务器端跨域访问的漏洞原理

2、理解CORS跨域漏洞的防御机制

## 一、什么是CORS

全称是“跨域资源共享”（Cross-Origin Resource Sharing），CORS规范规定了再Web服务器和浏览器之间交换的标头内容，该标头内容限制了源域之外的域请求Web资源。CORS规范标识了协议头中 Access-Control-Allow-Origin 最重要的一组。当网站跨域请求资源时，浏览器对请求添加标头Origin，服务器将返回标头Access-Control-Allow-Origin。

## 二、如何使用CORS

1、cors.php

在192.168.230.147服务器上实现以下PHP代码

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
// echo $_GET['callback']."(".$json_result.")";
//echo "<br>";
//echo gettype($json_result);

$conn->close();

?>
```

2、cors.html

在192.168.230.50服务器上实现以下HTML，去跨域访问 192.168.230.147上的cors.php

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="jquery-3.4.1.min.js"></script>
    <title>CORS</title>
    <script>
        $.get("http://192.168.230.147/security/cors.php",function(data) {
            alert(data);
        });
    </script>
</head>
<body>
    welcome to CORS-security world
</body>
</html>
```

3、访问http://192.168.230.150/cors.html，用Fiddler抓包查看流量情况

![image-20240814004407757](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240814004407757.png)

![image-20240814004259840](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240814004259840.png)

其中第三个请求就是跨域访问的请求

![image-20240814004332714](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240814004332714.png)

此时，由于同源策略的限制，192.168.230.150无法获取192.168.230.147上的资源

除过JSONP的回调函数利用 <script> 不受同源策略限制的方式，我们更多的使用CORS

4、优化192.168.230.147的cors.php代码，允许任意主机跨域访问

```php
<?php
// 链接数据库并访问数据
$conn = new mysqli('127.0.0.1','root','','woniunote',3306) or die("数据库连接失败");
$conn->set_charset("utf8");
$sql = "select articleid,headline from article where articleid<5";
$result = $conn->query($sql);
// 输出JSON数据到页面
$json_result = json_encode($result->fetch_all(MYSQLI_ASSOC));
header("Access-Control-Allow-Origin: *");
echo $json_result;
$conn->close();
?>
```

> 当然，通常情况下不建议设置为 * ，因为这样，任意域外站点都可以访问服务器

再尝试访问

![image-20240814004843851](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240814004843851.png)

![image-20240814004909992](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240814004909992.png)

5、辅助的响应头

```
Access-Control-Allow-Origin: *

Access-Control-Allow-Method: POST,OPTIONS,GET  //请求的类型，针对复杂请求的预检有效

Access-Control-Max-Age: 3600  // 生命周期，以秒为单位

Access-Control-Allow-Headers: accept,x-requested-with,Content-Type  //可以接受的请求头

Access-Control-Allow-Credentials: true  // 是否允许发送Cookie

Access-Control-Allow-Origin: http://192.168.230.150:80,http://192.168.230.*:80  //只允许哪个源访问
```

> CORS详解[跨域资源共享 CORS 详解 - 阮一峰的网络日志 (ruanyifeng.com)](http://ruanyifeng.com/blog/2016/04/cors.html)
>
> 非简单请求的预检过程，参考 [CORS预检请求详谈 - wonyun - 博客园 (cnblogs.com)](https://www.cnblogs.com/wonyun/p/CORS_preflight.html)

## 三、使用白名单防御跨域漏洞

```php
<?php
// 链接数据库并访问数据
$conn = new mysqli('127.0.0.1','root','','woniunote',3306) or die("数据库连接失败");
$conn->set_charset("utf8");
$sql = "select articleid,headline from article where articleid<5";
$result = $conn->query($sql);
// 输出JSON数据到页面
$json_result = json_encode($result->fetch_all(MYSQLI_ASSOC));
$list = array("http://192.168.230.150","http://192.168.230.2");
if (in_array($_SERVER['HTTP_ORIGIN'],$list)) {
    header("Access-Control-Allow-Origin:".$_SERVER['HTTP_ORIGIN']);
    echo $json_result;
}
else {
    die("Cross-Origin Disallow");
}
$conn->close();
?>
```

直接客户端访问试试，ok，直接没有Origin，确实，客户端直接访问不属于跨域访问，也就没有这个字段。再说了，哪能让用户直接访问服务器代码呀

![image-20240814010211682](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240814010211682.png)

此时，只有定义的白名单中的域外服务器（开启了apache，通过apache服务访问）可以访问

## 四、预防CORS漏洞

CORS漏洞主要是由于配置错误而引起的。所以，预防漏洞变成了一个配置问题。下面介绍了一些针对CORS攻击的有效防御措施。

- 正确配置跨域请求：如果Web资源包含敏感信息，则应在Access-Control-Allow-Origin标头中正确指定来源
- 只允许信任的网站：看起来似乎很明显，但是Access-Control-Allow-Origin中指定的来源只能是受信任的站点。特别是，使用通配符来表示允许的跨域请求的来源而不进行验证很容易被利用，应该避免。
- 避免将nu列入白名单：避免使用标题Access-Control-Allow-Origin: nu，来自内部文档和沙盒请求的跨域资源调用可以指定nul来源。应针对私有和公共服务器的可信来源正确定义CORS头
- 避免在内部网络中使用通配符：避免在内部网络中使用通配符。当内部浏览器可以访问不受信任的外部域时，仅靠信任网络配置来保护内部资源是不够的
- CORS不能替代服务器端安全策略：CORS定义了浏览器的行为，绝不能替代服务器端对敏感数据的保护-攻击者可以直接从任何可信来源伪造请求。因此，除了正确配置的CORS之外，Web服务器还应继续对敏感数据应用保护，例如身份验证和会话管理，