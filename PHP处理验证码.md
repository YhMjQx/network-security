[TOC]



# ==PHP处理验证码==

1、理解如何使用PHP动态生成随机验证码图片。

2、理解如何基于Session进行图片验证码校难。

3、利用PHP绘制图片验证码并渲染给前端。

4、利用PHP校验图片验证码防止暴力破解。

验证码有多种形态:图片验证码，短信验证码，邮箱验证码，滑动验证码，复杂图案验证码等。

5、图片验证码是比较主流的验证码之一，其实现原理就是利用后台程序将一个随机字符串生成为一张图片，直接将图片渲染给前端，前端用户识别图片中的字符串并回传给后台进行校验。

6、短信验证码和邮箱验证码的实现原理类似，均是生成一个随机字符围发送给登录者手机或邮箱，再回传给后台进行校验，但是校验过程一这要仔细，避免出现逻辑漏洞。

7、滑动验证码和复杂图案验证码建议使用第三方平台提供的接口，不建议自行开发。

## 一、验证码生成原理

核心目的是确保人为操作设备：图片验证码，短信验证码，邮箱验证码，滑动验证码，复杂图案验证码，拼图验证码，计算验证码等等，原理主要基于以下三个方面：

- 随机生成的字符，确保无规律可言
- 使用图片来进行展示，而非其他手段
- 尽量让文字变形并形成各类扰乱图像

## 二、代码实现

添加源代码 vcode.php ，基于PHP回执基础图片，生成验证码，然后将该验证码保存到Session变量当中

```php
<?php
// 利用Session保存图片验证码
session_start();

function getCode($num, $w, $h) {
    $code = "";
    for ($i = 0; $i < $num; $i++) {
        $code .= rand(0, 9);
    }
    // 4位验证码也可以用rand(1000, 9999)直接生成
    // 将生成的验证码写入session，备验证时用
    $_SESSION["vcode"] = $code;
    //创建图片，定义颜色值
    header("Content-type: image/PNG");
    $im = imagecreate($w, $h);
    $black = imagecolorallocate($im, 0, 20, 50);  // 字体和边框的颜色
    $gray = imagecolorallocate($im, 200, 140, 100);  // 背景画布颜色
    // $bgcolor = imagecolorallocate($im, 100, 200, 200);
    //填充背景
    imagefill($im, 0, 0, $gray);
    //画边框
    imagerectangle($im, 0, 0, $w-1, $h-1, $black);
    //随机绘制两条虚线，起干扰作用
    $style = array($black, $black, $black, $black, $black, $gray, $gray, $gray, $gray, $gray);
    imagesetstyle($im, $style);
    $y1 = rand(0, $h);
    $y2 = rand(0, $h);
    $y3 = rand(0, $h);
    $y4 = rand(0, $h);
    imageline($im, 0, $y1, $w, $y3, IMG_COLOR_STYLED);
    imageline($im, 0, $y2, $w, $y4, IMG_COLOR_STYLED);
    //在画布上随机生成大量黑点，起干扰作用;
    for ($i =0; $i < 80; $i++) {
        imagesetpixel($im, rand(0, $w), rand(0, $h), $black);
    }
    //将数字随机显示在画布上，字符的水平间距和位置都按一定波动范围随机生成
    $strx = rand(3, 8);
    for ($i=0; $i<$num; $i++) {
        $strpos = rand(1, 6);
        imagestring($im, 5, $strx, $strpos, substr($code, $i, 1), $black);
        $strx += rand(8, 12);
    }
    imagepng($im); //输出图片
    imagedestroy($im); //释放图片所占内存
}

getCode(4,60,20);

?>
```

![vcode.php](https://gitee.com/ymq_typroa/typroa/raw/main/vcode.php)

## 三、修改登录源文件

### 1、login.html

```html
input[name='vericode'] {
width: 220px;
}

<div class="login">
    <input type="text" name="vericode" />&nbsp;&nbsp;&nbsp;
    <img id="vcode" src="./vcode.php"></img>
</div>
```

### 2、login.php

```php
// 验证码的判断换成如下代码
if ($_SESSION['vcode']==$vcode) {

}
```

xampp中的session变量的文件存放路径在 `/opt/lampp/temp` 

![image-20240604211130289](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240604211130289.png)

使用 `ll` 查看文件存储时间来手动对应和检查session

> 验证码一旦生成后，不一定必须保存在SESSION中，任何可以存储数据的方式均可以，比如数据库，文件，内存，或者保存在Redis的缓存服务器中。比如短信验证码，通常会有一个时间限制（5分钟内有效），最好的解决办法就是使用Redis缓存，并设置key的 过期时间。


## 四、SQL注入-登录漏洞-验证码防护

目前的问题是，如果我不刷新login.html页面，就不会调用vcode.php这份代码，也就无法生成新的验证码，并且不刷新login.html页面，SESSION['vcode']也不会改变，那么用户就可以一直使用这个SESSION['vcode']实现不间断的登录请求

![image-20240605205903244](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605205903244.png)

比如此时SESSION['vcode']是6592，那么之后我可以一直使用这个SESSION['vcode']来发送大量的登录请求

![image-20240605211438328](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605211438328.png)

![image-20240605211452952](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605211452952.png)

这样使用同一个SESSION['vcode']一样可以实现爆破的目的

### 1、修复验证码

需要让验证码每取出判断一次就清空SESSION['vcode']，此时，不输入验证码无法登录，输入旧的验证码也登录错误。这样就可以让下一次刷新页面重新获得该验证码，然后再进行登录。

```php
if ($vcode === '0000' or $_SESSION['vcode']==$vcode) {
    unset($_SESSION['vcode']);

}
else { 
    // die("vericode-error");
    login_result('vericode-error');
    unset($_SESSION['vcode']);

}
```

每次不管验证码输入正确与否都清空SESSION中的的vcode字段

![image-20240605213103626](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605213103626.png)

但是以上代码就会有以下问题：暴露了文件的绝对路径，因此还需要修改

![image-20240605212751668](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605212751668.png)

```php
if (isset($_SESSION['vcode']) and $vcode === '0000' or $_SESSION['vcode']==$vcode) {
    unset($_SESSION['vcode']);

}
else {
    // die("vericode-error");
    login_result('vericode-error');
    unset($_SESSION['vcode']);
}
```

## 五、避免使用cookie验证码

SESSION的生成过程，当用户第一次访问服务器时，如果请求中没有带Cookie字段，则服务器会在首次调用session_start()的页面中响应一个SESSION ID，默认命名为：PHPSESSION，响应的字段值如下：

```
Set-Cookie: PHPSESSID=f00fc086dc2d24f2f50928063b919c0a; path=/
```

![image-20240605231901006](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605231901006.png)

接下来，后续的每一个请求，将会在请求头的Cookie字段中添加SESSION ID，目的是为了告诉服务器，我是谁

```
Cookie: PHPSESSID=f00fc086dc2d24f2f50928063b919c0a
```

![image-20240605232210025](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605232210025.png)

> 也是基于此，存在cookie和SESSION的欺骗

另外，在服务器端也可以直接手工生成Cookie

```php
// 调用setcookie() 函数自定义生成Cookie，Cookie是保存在客户端的，服务器端本身不保存cookie
setcookie("vcode",$vcode,time()+3600*24*30*12);
settcookie(cookie的名字，cookie的值，cookie的超时时间);
```

> 因为setcookie之后，该cookie会哦保存在客户端浏览器中，当第一次生成之后，在cookie过期之前客户端访问服务器时都会在请求中携带该cookie字段。但是这就存在一种问题如果这个cookie由hack自己生成，然后再发送数据包的时候，hack提前那发送自己的cookie，然后在登录的时候post请求中发送cookie，就可以达到以假乱真的目的

第一个数据包来进行setcookie

![image-20240605235628755](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605235628755.png)

第二个数据包使用自定义cookie来进行登录

![image-20240605235732926](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605235732926.png)

现在我们尝试使用该自定义cookie来composer

![image-20240605235905946](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605235905946.png)

![image-20240605235931426](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240605235931426.png)

访问成功

**那么我们随便自定义cookie来发送数据包**

![image-20240606000050069](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240606000050069.png)

直接访问成功

![image-20240606000112191](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240606000112191.png)
