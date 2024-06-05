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

