[TOC]



# ==CSP内容安全策略==

1、理解CSP内容安全策略的配置项及作用

2、掌握利用CSP机制实现安全数据采集

3、对CSP及逆行安全策略配置

4、开发PHP页面采集安全报告

5、对DVWA的CSP安全进行通关

## 一、引入

XSS中的Get Cookie攻击，可以通过在setcookie字段中增加httponly属性来限制JS读取Cookie，但是并不能从根本上解决XSS攻击，因为XSS攻击的目的不仅仅只是窃取Cookie

```php
修改php.ini配置文件的参数
session.cookie_httponly=On
```

- 没有限制httponly之前

  当我访问一个带有beefxss的页面时，很容易被攻击，因为引用这个hook.js时完全没有受到任何影响

  ![image-20240815163315699](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815163315699.png)

- 那么我添加上httponly

  再来访问这个页面，我们可以发现，在第一次访问时会在SetCookie字段后添加 httponly

  表示，Cookie信息无法被js代码所获取，只能在请求中看到

  ![image-20240815170351803](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815170351803.png)

另外的防御方案就是对用户的输入斤西瓜各种校验，过程非常繁琐，还容易出错或者遗漏，有没有一种方法可以从根本上解决问题，就像CORS那用啊快捷方便的通过响应头的约束，就可以让浏览器执行安全检查，杜绝XSS漏洞呢？

## 二、CSP内容安全策略

CSP的实质就是白名单制度，开发者明确告诉客户端，哪些外部资源可以加载和执行，等同于提供白名单。他的实现和执行全部由浏览器完成（前端方面），开发者只需提供配置。

CSP大大增强了网页的安全性，攻击者及时发现了漏洞，也没法注入脚本，除非还控制了一台列入白名单的可信主机。有两种方法可以启用CSP。

### 1、通过 HTTP 响应头信息的 Content-Security-Policy 的字段

```
Content-Security-Policy: script-src 'self'; Object-src 'none'; style-src cdn.example.org third-party.org; child-src: https:
```

在PHP中直接使用 header() 函数定义响应头即可

### 2、通过网页的 meta 标签

```html
<meta http-equiv="Content-Security-Policy" content="script-src 'self'; Object-src 'none'; style-src cdn.example.org third-party.org; child-src: https:">

<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline';script-src 'self' 'unsafe-eval' 'unsafe-inline';img-src  'self'  'unsafe-inline'  'unsafe-eval'  data:">

```

上述代码中，CSP做了如下配置：

```
default-src 
定义针对所有类型(js/image/css/font/ajax/iframe/多媒体等)资源的默认加载策略，如果某类型资源没有单独定义策略，就是用默认的

script-src 'self' http://www.woniunote.com 
对于引用的脚本，浏览器只信任来自当前域名（也就是正在访问的这个域名）和 http://www.woniunote.com 这个域下的（注意域的组成部分 协议 域名 端口号）

object-src 'none' 
对于 <object> 标签，不信任任何URL，即，不加载任何资源

style-src cdn.example.org third-party.org;
对于样式表，只信任 cdn.example.org 和 third-party.org 俩域名下的

child-src https:
对于框架(frame) 必须使用https协议加载，注意冒号时https协议的一部分

对于其他资源，如若未定义，则使用 default-src
```

一旦启用后，不符合CSP的外部资源就会被阻止加载

> 类似于 script-src 'self' 中和 object-src 'none' 用单引号包裹的self属于CSP 内置的一些属性，需要用单引号包裹起来，其他自己添加的就不需要
>
> 如果 script-src 不允许加载外部的资源，那么<script> 标签也无法引用了。说明CSP等级高于跨域访问

### 3、在security的read.php页面，增加以下响应头

```php
header("Content-Security-Policy: script-src 'self'");
```

![image-20240815182148957](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815182148957.png)

如果出现了类似于下图的**行内代码**

![image-20240815182230628](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815182230628.png)

我们需要使用 **unsafe-inline** ，当然，如果使用了这个属性，上面这样的代码就可以被执行然后加载外部资源

![image-20240815182252502](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815182252502.png)

![image-20240815184047970](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815184047970.png)

![image-20240815184227602](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815184227602.png)

经过测试可以发现，firefox-hackbar 不受CSP的限制（我已经在read.php中配置好了CSP，但是firefox-hackbar访问被注入了XSS代码的页面，竟然无法阻止hook.js的引用），简直太nb了，c

### 4、report-uri安全报告

在 Content-Security-Policy 中，我们还可以设置 report-uri 属性，用于象一个指定的服务器地址提交 JSON 格式的安全报告。该属性一旦开启，当任何违背了 CSP 的外部资源要被加载时，都会形成报告。

```php
Content-Security-Policy: script-src 'self'; report-uri http://192.168.230.147/security/temp/cspreport.php
```

一旦访问到受到攻击的页面并触发了脚本执行，浏览器除了阻止攻击脚本执行外，还会按照 以下 JSON 格式提交安全报告内容

```json
{
    "csp-report":
    {"document-uri":"http://192.168.230.147/security/read.php?articleid=146",
     "referrer":"http://192.168.230.147/security/list.php",
     "violated-directive":"script-src-elem",
     "effective-directive":"script-src-elem",
     "original-policy":"script-src 'self' http://192.168.230.150; report-uri http://192.168.230.147/security/temp/cspreport.txt",
     "disposition":"enforce",
     "blocked-uri":"http://192.168.230.128:3000/hook.js",
     "status-code":200,
     "script-sample":""}
}
```

然后我们编写 cspreport.php 用于接收这些 JSON 数据并处理保存到文件中

```php
<?php

$time = date("Y-m-d H:i:s");
$file = fopen("./temp/cspreport.txt",'a');
$jsondata = file_get_contents('php://input');  // 利用php伪协议获取POST提交数据
$data = json_decode($jsondata,true);  // true 表示生成关联数组
// fwrite($file,$jsondata);
fwrite($file,"report-time:".$time."\r\n");
foreach($data['csp-report'] as $key => $value) {
    // echo $key."===".$value;
    fwrite($file,$key.":".$value."\r\n");
}
fwrite($file,"\r\n-------------------------------------------\r\n\r\n");
fclose($file);

?>
```

访问一下被攻击的页面http://192.168.230.147/security/read.php?articleid=146

![image-20240815223116781](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815223116781.png)

查看cspreport.txt文件中的内容

![image-20240815223155676](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815223155676.png)

ok

> 需要注意，该操作需要将cspreport.txt文件所在目录库和本身都添加写的权限
>
> 如果设置响应头Content-Security-Policy-Report-Only，则表示只进行请求拦截，但不会上报日志。也就是
>
> ```php
> header("Content-Security-Policy: script-src 'self' http://192.168.230.150; report-uri http://192.168.230.147/security/cspreport.php");
> ```
>
> 和
>
> ```php
> header("Content-Security-Policy-Report-Only: script-src 'self' http://192.168.230.150; report-uri http://192.168.230.147/security/cspreport.php");
> ```
>
> 二者的区别就是，前者既拦截白名单之外的外部资源加载，又会上报拦截信息到指定文件。而后者单纯只是拦截而已

### 5、其他安全配置

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815224343589.png" alt="image-20240815224343589" style="zoom:150%;" />

更多CSP安全策略，可参考[Content Security Policy 入门教程 - 阮一峰的网络日志 (ruanyifeng.com)](https://www.ruanyifeng.com/blog/2016/09/csp.html)

![image-20240815224235809](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815224235809.png)

### 6、Web服务器全局配置

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815224453847.png" alt="image-20240815224453847" style="zoom:150%;" />

## 三、DVWA中的CSP

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815224546939.png" alt="image-20240815224546939" style="zoom:150%;" />

## 四、其他安全响应头

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240815224620534.png" alt="image-20240815224620534" style="zoom:150%;" />
