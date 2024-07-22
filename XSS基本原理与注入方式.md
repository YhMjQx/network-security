[TOC]



# ==XSS基本原理与注入方式==

### 课程目标

1、理解XSS漏洞的形成机制

2、理解XSS的类型和危害（利用PHP开发一个具备XSS漏洞的页面去尝试）

3、基于该漏洞实现XSS的攻击和利用

**开发一个具有XSS漏洞的PHP页面**

```php
if (isset($_GET['content'])) {
    $content = $_GET['content'];
    echo "您输入的内容是：$content";
}
else{
    echo "请输入URL地址参数content";
}
```

### 参数改动，尝试XSS漏洞

- ```
  ?content=Hello World
  ```

  正常输出Hello World

- ```
  ?content=<script>alert('hello')</script> 
  或 
  ?content=<script>alert("hello")</script> 
  或 
  ?content=<script>alert(/hello/)</script>
  ```

  则会弹窗：

    ![image-20240721172754495](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240721172754495.png)![image-20240721172928741](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240721172928741.png)

- ```
  ?content=<button onclick="alert('you have been attacked')">come on</button>
  ```

  ![image-20240721175000506](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240721175000506.png)

- ```
  ?content=
  <script>
      function test() {
          alert("you have been attacked hahaha");
      }
  </script>
  <button onclick='test()'>come on</button>
  ```

  

- ```
  <script>
      var result = 0;
      for(var i=0;i<100;i++) {
          result += i;
      }
      alert(result);
  </script>
  ```

  ![image-20240721182051690](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240721182051690.png)

  会造成死循环，导致脚本执行意外中断，但为什么会死循环呢？

  ![image-20240721182203438](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240721182203438.png)

  我们可以看到，其页面源代码变成了这样，原来浏览器会将我们在url中输入的 加号（+） 变成空格，这样就导致我们的js代码变成了 

  ```js
  <script>
      var result = 0;
      for(var i=0;i<100;i  ) {
          result  = i;
      }
      alert(result);
  </script>
  ```

  所以就造成了死循环

- ```js
  <script>
      var result = 0;
      for(var i=100;i>0;--i) {
          result -= i;
      }
      alert(result);
  </script>
  ```

  ![image-20240721182628649](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240721182628649.png)

  相反，我们只需换成反过来哦的负数就好了，取值的时候去个饭就行

## 一、XSS基本原理概述

XSS全称为：Cross Site Scripting，跨站攻击脚本，XSS漏洞发生在前端，攻击的是浏览器的解析引擎，XSS就是让攻击者的JavaScript代码在受害者的浏览器上执行。

XSS攻击者的目的就是寻找具有XSS楼哦对那个的网页，让受害者在不知情的情况下，在有XSS漏洞的网页上执行攻击者的JavaScript代码。

XSS是提前埋伏好的漏洞陷阱，等着受害者上钩。既然是执行JavaScript代码，所以供给的语句应该能让JavaScript运行。

JavaScript运行条件：

（1）代码位于 `<script></script>` 标签中

（2）代码位于onclick时间中，此类事件带有 onerror onload onfocus onblur onchange onmouseover(鼠标滑过) ondblclick(单击) 等

```js
<button onclick="alert('you have been attacked')">come on</button>
<img src="http://xxx/xxx.jpg" onmouseover="alert(1)" width=200></img>
```

（3）代码位于超链接的href属性中，或者其他类似属性中

```js
<a href="javascript:alert(1)">点击有惊喜</a>
```

XSS的攻击payload一定一定满足上述条件

> XSS学习主要以测试看到效果为主，通常的明显效果就是使用alert弹窗，弹窗意味着我们的js代码成功执行了
>
> XSS是以Web站点的用户为攻击目标，而不是服务器，是一种钓鱼攻击，攻击目标是不确定的。但是如果针对cookie类的攻击，隐含有一种确定目标就是网站管理员（这就是一种越权操作）

![image-20240722112955528](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722112955528.png)

> 受害者为用户，XSS类似于一种钓鱼攻击，用户访问攻击者事先在服务器存留的带有恶意js代码的页面，经过用户的浏览器引擎解析之后执行该恶意代码，导致被攻击

 

**基于XSS配置钓鱼网站**

利用iframe完成XSS攻击，将攻击者的模仿页面嵌入被攻击网页中： `<iframe src="http://www.taobao.com" width=100% height=100%/>`

例子如下：

- 自行构建一个与淘宝一模一样的网页，并且点击登录跳转到一模一样的登录界面

![image-20240722122822132](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722122822132.png)

- 一旦用户点击登录进行账密的输入并且提交，那么这些账密的数据就会传送至我们的后台服务器并获取。不过我们需要做的是这个登录页面要我们自己做，否则登录的请求就直接发给淘宝了，只需点击登录时跳转的页面是我们自己的就可以，其他淘宝的功能就用淘宝自己的

![image-20240722123249749](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722123249749.png)

- 然后我们可以再将获得的账密通过post请求发给真正的淘宝登录，如果登录成功，就保存该账密，并且重定向页面到一个登录失败的页面，这个登录失败也可以做的和真正淘宝登录失败的页面一样，然后再跳转到真正的淘宝页面，大不了再重新登录一次，让用户以为自己账密输错了

自己服务器端的代码类似于：

```php
if (isset($_GET['content'])) {
    $content = $_GET['content'];
    echo "您输入的内容是：$content";
}
else{
    echo "请输入URL地址参数content";
}

// 获取用户的淘宝账密
$username = $_POST['username'];
$password = $_POST['password'];

//将数据发送真正淘宝并POST登录检查是否登录成功

echo "<script>document.write('用户名或密码错误，请重新登录'); setTimeout(function() { location.href='https://www.taobao.com'}, 3000);</script>";

?>
```

## 二、XSS注入步骤

XSS攻击，一定牢记 “输入输出”，输入指的是攻击者对服务器网页输入恶意代码，输出指的是浏览器接收到代码后能解析并输出到前端。

XSS的原理就是开发者没有对输入内容进行过滤，导致通过攻击者精心构造的前端代码，输入后和原有的前端代码产生混淆，形成新的页面语句，并且新的页面语句能被浏览器解析并输出。

### XSS注入步骤：

- 找到输入点，输入任意字符串，查看输出位置
- 打开网页源代码，在源代码中查看输出的位置。（有可能输入和输出不在同一个页面）
- 查看输出位置的内容与输入的内容之间的关系，构建闭合和拼接脚本。
- 利用 `<script>` 或 `onclick` 或 `alert(1)` 进行测试，确认食肉存在XSS注入点。
- 开始利用该注入点完成各类复杂的操作，实现攻击目的。

**优化PHP代码为以下代码，并在一个文本框中进行输出：**

```php  
if (isset($_GET['content'])) {
    $content = $_GET['content'];
    echo '您输入的内容是：<input type="text" id="content" value="'.$content.'"/>';
}
else{
    echo "请输入URL地址参数content";
}
```

![image-20240722150123950](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722150123950.png)

那如果此时输入 `<script>alert(1)</script>` ，就不会再出现弹窗了，我们来看看为什么

![image-20240722150243262](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722150243262.png)

![image-20240722150324742](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722150324742.png)

这段脚本完全作为了字符串，要想让其执行，就需要**闭合引号**，所以我们输入 `点我一下" onclick="alert(1)` 会是什么样子

![image-20240722150839646](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722150839646.png)

**那如果修改后端代码为下面这样呢**

```php
if (isset($_GET['content'])) {
    $content = $_GET['content'];
    echo '您输入的内容是：<input type="text" value="'.$content.'" id="content"/>';
}
else{
    echo "请输入URL地址参数content";
}
```

这样我们该如何闭合引号？

- 直接闭合 
  - `click here" onclick="alert(1)`

![image-20240722153241113](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722153241113.png)

- 注释 
  - `click here" onclick="alert(1)"/> <!--` 

![image-20240722153123846](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722153123846.png)

- `type="hidden` 或 `maxlength="100` 等

![image-20240722153213998](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722153213998.png)

得到的结果和修改代码之前的结果是一样的

**那如果修改后端代码为下面这样呢**

```php
 if (isset($_GET['content'])) {
    $content = $_GET['content'];
    echo "<a href='$content'>please click here</a>";
}
else{
    echo "请输入URL地址参数content";
}
```



> 甚至我们还可以标签闭合标签
>
> ![image-20240722155115322](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722155115322.png)
>
> ![image-20240722155209710](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722155209710.png)
>
> ![image-20240722155239267](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240722155239267.png)
