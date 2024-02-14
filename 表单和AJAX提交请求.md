[TOC]



# ==表单和AJAX提交请求==

## 前后端交互过程

### 一、简介

前后端的交互过程就是HTTP协议的处理过程：请求与响应的处理过程。单纯只有前端，无法使用后台服务器的能力，或者无法访问数据库，如果单纯只有后端，也无法形成业务流程，无法为客户产生价值。

![image-20240214150006887](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214150006887.png)

三种方式：

（1）资源获取型：GET请求+URL地址

（2）数据提交型：POST请求+URL地址+请求正文

（3）AJAX提交：利用异步提交方式，在不刷新当前页面情况下，提交数据给后台

第三种就类似于，如下两种情况

![image-20240214152047889](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214152047889.png)

![image-20240214152101341](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214152101341.png)

### 二、POST请求

**以下请求方式使用form表单的形式发送post请求**

（1）必须使用form标签将所有表单元素包裹起来

（2）必须要在form标签中指定action属性

（3）必须要在form标签中指定method属性

`<form action="../PHP/login.php" method="post">`

（4）必须要确保在form标签内，有至少一个按钮，且按钮 `type="submit"`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ymqyyds</title>
    <style>

        div {
            width: 310px;
            height: 75px;
            margin: auto;
        }

        .title {
            color: rgb(6, 255, 52);
            font-size: 30px;
            text-align: center;
            margin-top: 200px;
            padding-bottom: 10px;  /*和底部下一个容器相隔一点距离*/
            font-weight: bold;  /*加粗*/
            font-style: italic;  /*斜体*/
            
        } 

        input {
            width: 300px;
            height: 50px;
            background-color: antiquewhite;
            border-radius: 5px;  /*让边框看起来圆润一点*/
            text-align: center;
            margin: auto;
        }

        button {
            width: 310px;
            height: 50px;
            background-color: fuchsia;
            color: chartreuse;
            font-size: 20px;
            font-weight: bold;  /*加粗*/
            font-style: italic;  /*斜体*/
            border-radius: 5px;  /*让边框看起来圆润一点*/
        }

        .footer {
            width: 500px;
            height: 50px;
            border: solid 0px blue;
            margin: auto;
            text-align: center;
            color: aliceblue;
        }

    </style>
</head>

<body background="../image/code.png" style="background-repeat: repeat;background-attachment:fixed;background-size:100%">

    <div class="title top-100 font-30">登 录</div>

    <form action="../PHP/login.php" method="post">
        <div class="login">
            <input type="text" name="username" />
        </div>
        <div class="login" >
            <input  type="text" name="password" />
        </div>
        <div class="login">
            <input type="text" name="vericode" />
        </div>
        <div class="login" >
            <button type="submit">登 录</button>
        </div>
    </form>

    <div class="footer top-100"> 
        版权所有@华明网络安全科技有限公司
    </div>


</body>
</html>
```

上面代码是前端html页面输入和登录所用到的，同时利用表单form发送post请求

而下面的代码就是用来接收和处理前端发送的post请求的后台php代码。我们测试就输出以下post请求的正文

```php
<?php
    //这是一段服务器处理的后台代码，用于检测post请求正文

    /**
     * 获取请求的方式
     * GET
     * POST
     * 前端如果使用get请求，后台就需要使用$_GET函数接收
     * 前端如果使用post请求，后台就需要使用$_POPST函数接收
     */

    //GET请求
    //需要将对应的html页面的请求方式method也改为get
    // $uname = $_GET['username'];
    // $passwd = $_GET['password'];
    // $vcode = $_GET['vericode'];

     //POST请求
    //需要将对应的html页面的请求方式method也改为post
    $uname = $_POST["username"];
    $passwd = $_POST["password"];
    $vcode = $_POST["vericode"]; 

    echo "username=".$uname." password=".$passwd." vericode=".$vcode."<br>";
    //输出的是服务器的响应
?>
```



以上方式发送post请求，最重要的就是**表单form标签包裹**的内容，我们使用了**action属性和method属性**，并对按钮设置了**type="submit"**属性，还有每一个文本框都要有**name属性**，这个name属性对应于请求正文当中的信息

此时我们在页面输入正文，点击登录时就可以进行页面的跳转，会跳转到当前目录下的login.php后台页面，我们可以通过浏览器和Fidder进行查看

![image-20240214165943548](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214165943548.png)

然后点击登录，就会跳转，至于为什么会跳转到这个页面，是因为这是我们自己设置的

```html
<form action="../PHP/login.php" method="post">
```



![image-20240214222345362](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214222345362.png)

Fidder中我们可以看到请求和响应

![image-20240214170119480](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214170119480.png)

### 三、GET请求

对于一些数据量较小的提交时，其实也可以使用get提交，因为url地址栏其实是有长度限制的，比如需要上传一个文件时，就只能使用post请求。

对应的html页面只需要将表单中的method参数改为get即可

但此时点击了登录之后，跳转的情况就发生了些许变化

![image-20240214202916335](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214202916335.png)

后面携带了一块地址参数，如果我们知道则个地址参数，我们可以通过直接输入地质参数登录，但事实我们知道，这样更不安全了

### 四、AJAX请求

![image-20240214212703487](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214212703487.png)

浏览器发送请求给服务器，服务器创建响应返回给浏览器，浏览器后台通过js处理响应，自动更新页面内容。

## AJAX与表单提交的区别

AJAX和表单提交都可以向服务器发送数据，但它们之间有很大的区别。

1. 页面刷新：使用表单提交时，整个页面会刷新，而使用AJAX时，只有部分页面内容会更新。
2. 用户体验：由于使用AJAX不需要刷新整个页面，用户可以在不中断操作的情况下与网页进行交互和操作。
3. 异步通信：AJAX使用异步通信，可以在后台与服务器进行数据交换，而表单提交是同步的，会阻止用户与页面的其他交互。
4. 数据处理：使用表单提交时，数据会被服务器处理和重定向到新的页面。而使用AJAX时，数据可以在后台被服务器处理，并将结果返回给客户端，客户端可以根据结果进行相应的操作。

（1）引入jquery的js库

在head标签当中输入以下代码，说明这包含javascript代码，以及引入jquery之后可以使用这个库中的代码，src确保jquery库的正确路径即可

```html
<script type="text/javascript" src="../jquery-3.4.1.min.js"></script>

```

（2）不再需要from，只需要任意一个元素（就比如说单击button）发起一个js事件，让js代码进行处理即可

```html
<script>
    //取每一个文本框中的值，响应button单击事件
    function doPost() {
        //获取表单元中的值，使用函数$("#id").val()
        var username = $("#username").val();
        var password = $("#password").val();
        var vericode = $("#vericode").val();
        //通过字符串方式将上面的值拼接为正文
        var param = "username=" + username + "&password=" + password + "&vericode=" + vericode;
        //利用ajax发送post请求，并获取服务器的响应
        //利用js内置的函数 $.post()，其中有三个参数
        //参数一：请求的网页
        //参数二：请求的正文
        //参数三：js处理响应的匿名函数（因为服务器将响应返回给浏览器需要使用js代码进行处理，就利用的是此函数）
        $.post("../PHP/login.php",param,function(data){
            //处理服务器响应的js代码
            window.alert(data);
        })
    }
</script>

<body background="../image/code.png" style="background-repeat: repeat;background-attachment:fixed;background-size:100%">
    <div class="title top-100 font-30">登 录</div>
    <div class="login">
        <input type="text" name="username" id="username" />
    </div>
    <div class="login" >
        <input  type="password" name="password" id="password"/>
    </div>
    <div class="login">
        <input type="text" name="vericode" id="vericode"/>
    </div>
    <div class="login" >
        <button onclick="doPost()">登 录</button>
    </div>
    <div class="footer top-100"> 
        版权所有@华明网络安全科技有限公司
    </div>
</body>
```



**至于为什么要加一个id**，而且其内容还和name的值是一样的，这是为了在取值时更加方便，可以直接使用 `#id` 这个方式直接取值，我们看代码就知道了，相应的css中的id选择器也是这样写的，而css中并没有对name属性选择器有规定的语法，而id有。（当然，也可以使用name进行取值，但很显然，会比使用id取值更麻烦）

![image-20240214221824803](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214221824803.png)

此时点击登录之后，就不会进行页面跳转和刷新，而是直接弹窗，至于为什么弹窗是这个内容，是因为我们的在函数中设置的post请求，请求的页面就是login.php

```html
$.post("../PHP/login.php",param,function(data){
            //处理服务器响应的js代码
            window.alert(data);
        })
```

而login.php的代码就是

```php
<?php
    $uname = $_POST["username"];
    $passwd = $_POST["password"];
    $vcode = $_POST["vericode"]; 
    echo "username=".$uname." password=".$passwd." vericode=".$vcode."<br>";
?>
```

因此输出和弹窗的内容会如图所示

当然我们也可以测试不使用弹窗，而是将服务器响应的数据复制给某一个文本框

```js
$.post("../PHP/login.php",param,function(data){
    //处理服务器响应的js代码
    // window.alert(data);
    $("#username").val(data);
})
```

效果如下

![image-20240214224019250](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240214224019250.png)