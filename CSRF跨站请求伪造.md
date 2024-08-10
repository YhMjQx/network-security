[TOC]



# ==CSRF跨站请求伪造==

1、理解CSRF的形成机制和工作原理

2、理解CSRF与XSS的相似与不同点

3、利用burp模拟一个攻击页面或自行开发一个攻击页面

## 一、概述

### 1、定义

Crose-Site Request Forgery，跨站请求伪造，攻击者利用服务器对用户的信任，从而欺骗受害者去服务器上执行受害者不知情的请求。在CSRF的攻击场景中，攻击者会伪造一个请求(一般为链接)，然后欺骗用户进行点击。用户一旦点击，整个攻击也就完成了。所以CSRF攻击也被称为“one click”攻击。

> 1. 用户登录受信任的网站 A，并在本地生成了相应的 Cookie 用于身份验证。
> 2. 网站 A 没有对用户请求进行有效的同源验证。
> 3. 攻击者构造一个恶意网站 B，在网站 B 的页面中包含指向网站 A 的恶意请求。
> 4. 当用户在浏览器中访问恶意网站 B 时，浏览器会自动带上网站 A 的 Cookie（因为用户之前登录过 A）。
> 5. 网站 A 接收到该请求，由于请求中带有合法的用户 Cookie，网站 A 会认为这是用户发起的合法请求，并执行相应的操作，如修改用户信息、转账等。
>
> CSRF 攻击之所以能够成功，主要是因为浏览器在发送请求时会自动携带相应的 Cookie，而服务器端仅通过 Cookie 来验证用户身份，没有对请求的来源和真实性进行充分的验证。

![image-20240809215015201](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240809215015201.png)

### 2、与XSS的区别

（1）**XSS是利用用户对服务器的信任，CSRF是利用服务器对用户的信任**

- XSS的攻击，主要是让脚本在用户的浏览器执行，服务器端仅仅只是脚本的载体（存储型就是将要执行的恶意脚本发送到客户前端浏览器），服务器端本身不会受到攻击利用（可以说服务端一般不会执行恶意代码）
- CSRF攻击，攻击者会诱使普通用户给正常服务器发送请求（攻击者伪造用户给服务器发送请求，用户本身并不想发送这样的请求），其核心主要是要让已登录（已认证）的用户发请求。CSRF不需要知道用户的cookie,CSRF自己并不会发请求给服务器，一切都是受害者做的

（2）XSS是将恶意代码植入被攻击服务器，利用用户对服务器的信任完成攻击（用户相信服务器，所以在该应用服务中干啥操作就不害怕，但是没想到服务器会给自己传输恶意代码）。CSRF是攻击者预先在自己攻击服务器的页面植入恶意代码，诱使受害者访问，在受害者不知情的情况下执行恶意代码。而攻击服务器是独立的域名或IP地址。

### 3、攻击要点

（1）服务器没有对请求来源进行判断，如IP，Referer等

（2）受害者处于登录状态，其cookie信息在对应目标服务器依旧keep-alive，但是攻击者无法拿到用户的cookie

（3）攻击者需要找到一条可以修改或获取敏感信息的请求

![image-20240809220412880](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240809220412880.png)

> 为了防范 CSRF 攻击，可以采取以下常见的措施：
>
> 1. 在请求中添加不可预测的令牌（Token），并在服务器端进行验证。
> 2. 验证请求的 Referer 头，判断请求来源是否合法。
> 3. 对敏感操作实施二次验证，如短信验证码、密码确认等。

## 二、攻击场景

（1）Alice在购物网站X宝上修改个人资料。正常情况下修改资料的第一步是登录个人账号。Alice登录后对相关参数进行修改:

```
收货姓名:Alice
收货电话:13888888888
收货地址:快乐镇233号
```

Alice编辑好修改的内容，点击提交

此时提交的url请求为:

```
http://www.xbao.com/member/edit.php?name=Alice&phone=13888888888&addr=快乐镇233号&sub
mit=submit
```

（2）这时候有个Bob他想要截获Alice的包裹，所以他要去修改Alice的收货地址。可是他没有Alice的账号权限那么他会怎么做呢?

```
Bob发现这个网站存在csrf漏洞:
Bob先确定Alice还处于登录状态
接着Bob将修改个人信息的请求伪造，然后去引诱Alice在登录状态下点击
```

此时Alice提交的url请求为:

```
http://www.xbao.com/member/edit.php?name=Bob&phone=13777777777&addr=邪恶村587号&subnit=submit
```

这个请求跟正常修改请求一模一样，而且又是Alice自己账号操作的，所以修改成功，Bob达到了攻击目的。

（3）那么问题来了，为什么Bob攻击成功?

```
条件1:x宝没有对个人信息修改的请求进行防CSRF处理,导致该请求容易伪造。因此，我们判断一个网站是否存在CSRF漏洞，其实就是判断其对关键信息(尤其是密码等敏感信息)的操作(增删改)是否容易被伪造。
条件2:Alice处于登录状态，并且点击了Bob发送的埋伏链接。
```

（4）CSRF漏洞单看之下的利用比较局限，但是和其他漏洞结合起来，威胁性也很大。

Bob觉得直接发链接太明显，会被ailce轻易识破,于是他思考别的方法，Bob利用burpsuite的功能模块做了一个钓鱼网站:

```
使用burpsuite的engagement tools 制作一个csrf攻击钓鱼网站
Bob发给Ailce这个页面，引诱Alice在没有退出x宝账号的情况下访问钓鱼页面
Alice点击了钓鱼网站中的恶意表单,从而在不知情的情况下执行了修改信息的请求。
```

CSRF是借助受書者的权限完成攻击，攻击者全程都没有拿到受害者的权限，而XSS一般直接通过获得用户权限实施破坏。

CSRF比起XSS来说不是很流行，所以对于CSRF防范的措施较少，因此CSRF比XSS更具有危险性。

## 三、使用burp完成DVWA-CSRF-Low

### Pablo作为攻击者，妄图获取admin的密码。Pablo使用firefox-hackbar，admin使用edge。192.168.230.150是攻击者服务器，192.168.230.147是DVWA的服务器，也就是被伪造欺骗的服务器。整个实验的目的无非就是要让Referer字段中包含Host字段的值，内网实验环境中就用ip地址，公网上有域名就用域名，没域名依旧使用ip地址

1、使用非管理员账号登录dvwa，并修改为low

![image-20240810094845788](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810094845788.png)

2、进入CSRF，并修改密码，burp抓包

3、在抓包的页面中，右键，生成 CSRF POC

![image-20240810095015751](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810095015751.png)

![image-20240810095039145](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810095039145.png)

4、复制html，放在攻击服务器下，访问地址例如  

![image-20240810095321067](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810095321067.png)

`192.168.230.150/csrf.html`

5、将该链接发送给dvwa的admin用户点击，此时，一旦已经登录的admin账户访问了这个链接，直接就会修改密码

![image-20240810104646705](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810104646705.png)

但有个不好的点就是访问了之后会停留在成功修改密码的这个界面，这就是burp自己生成的代码的鸡肋了

6、也可以将攻击服务器的页面地址通过DVWA的xss存储型漏洞植入页面中。

7、当DVWA的当前用户去查看XSS存储型漏洞页面时，就会完成攻击，这样我们间接实现了越权，因为我们是利用Pablo用户抓包生成该恶意链接，然后攻击了admin用户，从而得到了admin用户的密码

8、当然，整个过程还可以继续改进，让被攻击用户更加容易完成操作。比如直接将修改密码的请求地址直接内嵌到XSS页面中。

```
<a href="http://192.168.230.147/dvwa/vulnerabilities/csrf/?password_new=123456&password_conf=123456&change=chang"><img src="http://192.168.230.150/dateme.gif"/></a>
```

9、或者直接取消点击操作，进入页面即修改密码

```
<script>new Image().src="http://192.168.230.147/dvwa/vulnerabilities/csrf/?password_new=123456&password_conf=123456&change=chang";</script>
```

10、上述两项操作的前提是被攻击服务器存在XSS漏洞，如果不存在XSS漏洞，则需要诱使登录用户访问攻击服务器连接即可。

## 四、使用burp完成DVWA-CSRF-Medium

首先admin需要将DVWA的security设置为medium，否则无论如何Pablo的csrf都不正确，因为对于Pablo来说session是错的。

- 先尝试使用Low级别的csrf.html，诱使admin用户访问一下，发现报错 以下问题

![image-20240810165450416](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810165450416.png)

- 查看源码到底怎么回事

![image-20240810165751466](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810165751466.png)

```php
if(stripos($_SERVER['HTTP_REFERER'],$_SERVER['SERVER_NAME']) != false)
//stripos($_SERVER['HTTP_REFERER'],$_SERVER['SERVER_NAME']的意思是查找$_SERVER['SERVER_NAME']的值在$_SERVER['HTTP_REFERER']中第一次出现的位置，存在则返回开始的下标，否则返回false
```

所以这道题，是referer在其中捣蛋

- 我们再用Low级别的csef.html进行一次，这次需要抓包，我们去看看具体情况

![image-20240810170750400](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810170750400.png)

我们可以发现，HOST也就是`$_SERVER['SERVER_NAME']` 的值为192.168.230.147，而Referer也就是`$_SERVER['HTTP_REFERER']` 的值为 http://192.168.230.150  所以这天判断语句的结果一定是false，也就失败了

- 想办法使得判断成立

> 大多数教的方法都是抓包然后直接修改Referer的值，使得Referer包含Host_name即可，这样这道题目确实可以做到，但是，实际应用中是不可能的。
>
> 由攻击者构造的 恶意链接 ，交由 受害者 访问，难道受害者访问了连接，还要自己截包自己修改Referer？这完全是不可能的，所以我们得想个办法让 受害者 访问该链接的时候，Referer会自动加上。

- 修改 csrf.html  为 change_192.168.230.147.html 我们要告诉被欺骗的服务器，我们不是跨域请求的，我就是从你本地域发来的请求。所以修改文件名包含被欺骗服务器的IP地址或域名

![image-20240810181755547](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810181755547.png)

这里虽然修改了文件名，但依旧使用表单方式提交数据

让受害者admin的浏览器访问一下

![image-20240810182532013](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810182532013.png)

![image-20240810182353996](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810182353996.png)

![image-20240810182418246](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810182418246.png)

可以发现，Referer字段中并没有携带change_192.168.230.147.html的字样，老师说，因为使用的是表单提交方式，这个提交方式并不记录Referer，我们应该使用超链接方式提交数据

修改change_192.168.230.147.html文件中的内容为 

```html
<a href="http://192.168.230.147/DVWA/vulnerabilities/csrf/?password_new=123456&password_conf=123456&Change=Change"><img src="https://cbu01.alicdn.com/img/ibank/O1CN01tS9HLF1mjT1koO6Hz_!!2200735664990-0-cib.jpg"/></a>
```

![image-20240810183022359](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810183022359.png)

再诱使让受害者admin的浏览器访问一下，注意使用fiddler监听（由于我的电脑服务器环境配置有点问题，导致无法直接访问该界面，会自动跳转，所以我用一下老师的环境）

![image-20240810183852174](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810183852174.png)

![image-20240810183922503](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810183922503.png)

然后点击图片

![image-20240810184004161](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810184004161.png)

![image-20240810184035186](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810184035186.png)

基于此，我们就绕过了 `if(stripos($_SERVER['HTTP_REFERER'],$_SERVER['SERVER_NAME']) != false)` 这个判断，完成了请求伪造

- 既然做了，就要做得像一点，我们应该使用一个更又没，更具有吸引力的钓鱼网站，然后诱使受害者点击，同时，点击了之后，请求发送了之后，我们还需要让页面不要跳转到修改密码的界面，我们让页面跳转到另一个页面，做得更像一点，否则很容易就被发现了不是吗。比如利用ajax方式发送请求

![image-20240810184619329](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810184619329.png)

![image-20240810185344863](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240810185344863.png)
