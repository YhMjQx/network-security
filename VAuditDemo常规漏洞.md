[TOC]



# ==VAuditDemo常规漏洞==

1、所有文件读写的敏感操作函数 `file_get_contents,fgets,file_put_contents,fwrite` 避免用户可控点，避免写入木马，避免文件读取，避免读取到全站源码（所导致的黑盒变白盒，渗透变审计）

比如 avatar.php 文件中存在文件读取，且文件参数可控

```php
<?php
error_reporting(0);
session_start();
header("Content-type:image/jpeg");
echo file_get_contents($_SESSION['avatar']);
?> 
```

2、所有用户可输入的对象：`$_POST,$_GET,$_FILES,$_SERVER,$_COOKIE,$_REQUEST` 及 `php://input` 等

在 lib.php 源代码中存在对这些超全局对象的过滤

```php
if( !get_magic_quotes_gpc() ) {
	$_GET = sec ( $_GET );
	$_POST = sec ( $_POST );
	$_COOKIE = sec ( $_COOKIE ); 
}
$_SERVER = sec ( $_SERVER );
```

但是 `$_COOKIE,$_REQUEST` 就没有被处理，使用时就需要注意

3、文件包含 `include,include_once,require,require_once` 确定这些函数中的文件路径参数时用户不可控的

比如 index.php

```php
<?php
    /* Include */
    if (isset($_GET['module'])){
        include($_GET['module'].'.inc');
    }else{
?>
```



4、命令或代码执行或自定义函数调用，比如 `eval,assert,passthru,shell_exec,call_user_func,call_user_func_array,preg_replace,``,system` 等，执行时所执行的内容需要确保用户尽量不可控。

5、关于用户可控点的处理，一定要注意，如果里面的参数不是直接的来源于用户，而是一个变量，那么要回溯去看这个变量的值的来源。

比如 `eval($shell)` 要逆向回 `$shell` 值最开始的地方开始分析

附1：X-Forwarded-For请求字段

如果一个HTTP请求到达服务器之前，经过了三个代理 Proxy1 Proxy2 Proxy3 其中三个代理的IP分别为 IP1 IP2 IP3 ， 如果用户真是 IP 为 IP0，那么按照 XFF 标准，服务器最终会收到以下信息

```
X-Forwarded-For: IP0 IP1 IP2
REMOTE_ADDR: IP3
```

lib.php 源代码中存在

```php
function get_client_ip(){
	if ($_SERVER["HTTP_CLIENT_IP"] && strcasecmp($_SERVER["HTTP_CLIENT_IP"], "unknown")){
		$ip = $_SERVER["HTTP_CLIENT_IP"];
	}else if ($_SERVER["HTTP_X_FORWARDED_FOR"] && strcasecmp($_SERVER["HTTP_X_FORWARDED_FOR"], "unknown")){
		$ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
	}else if ($_SERVER["REMOTE_ADDR"] && strcasecmp($_SERVER["REMOTE_ADDR"], "unknown")){
		$ip = $_SERVER["REMOTE_ADDR"];
	}else if (isset($_SERVER['REMOTE_ADDR']) && $_SERVER['REMOTE_ADDR'] && strcasecmp($_SERVER['REMOTE_ADDR'], "unknown")){
		$ip = $_SERVER['REMOTE_ADDR'];
	}else{
		$ip = "unknown";
	}
	return($ip);
}

```

附2：常用过滤条件：`addslashes,mysql_real_escape_string,htmlspecialchars,str_ireplace` ，后缀名过滤，getimagesize（GIF图片马）

附3：常用的防御方式：php.ini 全局开关，部分功能能不能尽量不使用，使用其他替代方案，如果确实要用一定要确保严格过滤，如果对过滤没有信心，就测试，还没信息就上WAF（软WAF，硬WAF）

## 一、留言类功能漏洞

留言点进来第一个页面 message.php

```php
require_once('sys/config.php');
```

由于包含了 config.php 文件，所以，之前安装漏洞中写入的木马依旧可以利用

![image-20240819134834769](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819134834769.png)

留言功能

```php
$query = "SELECT * FROM comment ORDER BY comment_id";
$data = mysql_query($query, $conn) or die('Error!!');
mysql_close($conn);
...
while($com = mysql_fetch_array($data)) {
	$html['username'] = htmlspecialchars($com['user_name']);
	$html['comment_text'] = htmlspecialchars($com['comment_text']);
	
	echo '<tr>';
	echo '<td>'.$html['username'].'</td>';
	echo '<td><a href="messageDetail.php?id='.$com['comment_id'].'">'.$html['comment_text'].'</td></a>';
	echo '</tr>';
}
```

此功能将内容从数据库中查找出来输出到页面，那么是否属于存储型XSS呢，尝试一下

```html
<td><a href="messageDetail.php?id=11">&lt;script&gt;alert(/xss/)&lt;/script&gt;</td></a>
```

这是 payload 为 `<script>alert(/xss/)</script>` 时的页面输出结果，确实符合页面的 htmlspecialchars 函数的功能，但如果我不使用特殊符号呢，比如尝试payload为 `javascript:alert(111)` 此时没有特殊符号，自然也就不会存在被转义的现象，将其放进 html 中 

```html
<td><a href="messageDetail.php?id=11">javascript:alert(111)</td></a>
```

好吧，依旧失败，此时由于尖括号被转义，所以闭合标签也不行，经过对各种情况的测试，发现此处不存在xss漏洞

当然，留言类功能涉及到的网页还有 messageDetail.php messageSub.php  search.php

### messageDetail.php - 存在数字型SQL注入，反射型XSS

#### SQL注入

```php
if ( !empty( $_GET['id'] ) ) {
	$id = sqlwaf( $_GET['id'] );
	$query = "SELECT * FROM comment WHERE comment_id = $id";
	$data = mysql_query( $query, $conn ) or print_r(mysql_error());
```

此处存在sql注入漏洞，虽然对id参数进行了sqlwaf软waf防御，但是该sqlwaf本身就有漏洞

![image-20240819144134649](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819144134649.png)

下面对sqlwaf进行分析

```php
function sqlwaf( $str ) {
	$str = str_ireplace( "and", "sqlwaf", $str );
	$str = str_ireplace( "or", "sqlwaf", $str );
	$str = str_ireplace( "from", "sqlwaf", $str );
	$str = str_ireplace( "execute", "sqlwaf", $str );
	$str = str_ireplace( "update", "sqlwaf", $str );
	$str = str_ireplace( "count", "sqlwaf", $str );
	$str = str_ireplace( "chr", "sqlwaf", $str );
	$str = str_ireplace( "mid", "sqlwaf", $str );
	$str = str_ireplace( "char", "sqlwaf", $str );
	$str = str_ireplace( "union", "sqlwaf", $str );
	$str = str_ireplace( "select", "sqlwaf", $str );
	$str = str_ireplace( "delete", "sqlwaf", $str );
	$str = str_ireplace( "insert", "sqlwaf", $str );
	$str = str_ireplace( "limit", "sqlwaf", $str );
	$str = str_ireplace( "concat", "sqlwaf", $str );
	$str = str_ireplace( "\\", "\\\\", $str );
	$str = str_ireplace( "&&", "", $str );
	$str = str_ireplace( "||", "", $str );
	$str = str_ireplace( "'", "", $str );
	$str = str_ireplace( "%", "\%", $str );
	$str = str_ireplace( "_", "\_", $str );
	return $str;
}
```

虽然里边对很多东西都进行了过滤，但是细细分析还是可以发现 如果输入内容为 `an||d` 那岂不是替换后的结果不还是 and 嘛。此处的修改

#### sqlwaf修改措施

要么所有的替换全都变成sqlwaf，要么，就把替换为空和转义的替换放在最上面，替换为sqlwaf的放在最后。

因为该函数的执行，也是从上到下一次排查，先把空值绕过，再进行排查

下图是原本的sqlwaf对`messageDetail.php?id=7 an||d 1=1`防御的结果

![image-20240819143932946](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819143932946.png)

下图是替换顺序后的sqlwaf对`messageDetail.php?id=7 an||d 1=1`防御的结果

![image-20240819144115441](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819144115441.png)

#### 反射型XSS

```php
<?php echo 'The result for ['.$id.'] is:'?>
```

这行代码会将$id的值输出，所以存在反射型XSS

![image-20240819153319197](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819153319197.png)

### messageSub.php

```php
include_once('sys/config.php');

if (isset($_POST['submit']) && !empty($_POST['message']) && isset($_SESSION['username'])) {

	$clean_message = clean_input($_POST['message']);
	
	$query = "INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('{$_SESSION['username']}','$clean_message',now())";
	mysql_query($query, $conn) or die(mysql_error());
	mysql_close($conn);
	header('Location: message.php');
}
```

其中 有 clean_input 函数，代码如下

```php
function clean_input( $dirty ) {
	return mysql_real_escape_string( stripslashes( $dirty ) );
}
```

这完全是防止sql注入专用的函数 此处无漏洞

### search.php - 存在反射型xss

```php
<?php
include_once 'sys/config.php';
include_once 'header.php';

if ( !empty( $_GET['search'] ) ) {
	$query = "SELECT * FROM comment WHERE comment_text LIKE '%{$_GET['search']}%'";
	$data = mysql_query($query, $conn);
?>
```

由于 % 之间包裹的是字符型数据，除非想办法闭合 % 。但是别忘了，该页面包含了 config.php 而 config.php 又包含了 lib.php ，该文件对 `$_GET ` 请求的参数做了全面的封锁，无从注入。

但是可以发现，对search参数提交的内容都会原封不动的输出到页面上，这不正是符合反射型XSS嘛

```php
<?php echo 'The result for [ '.$_GET['search'].' ] is:'?>
```

和上面的反射型XSS形成原因一样，要将参数输出，从而导致的漏洞

![image-20240819152014088](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819152014088.png)

既然存在了反射型xss，我在想，那是否可以将hook.js注入进来，试试

- 先将 `<script src="http://127.0.0.1:3000/hook.js"></script>` 留言
- 在进入search.php页面查找 script 
- 好的，行不通，只有在给search传递参数时输入 `<script>alert(/xss/)</script>` 时，仅仅存在反射型xss，hook.js 不属于反射型，无法实现攻击

## 二、用户操作类漏洞

### 1、登录功能

为login.php，除了包含了几个文件，其他都是html标签元素，然后提交输入内容到 logCheck.php

```php
include_once('../sys/config.php');
include_once('../header.php');
```

#### logCheck.php - 空验证码绕过漏洞

```php
<?php
include_once('../sys/config.php');  // 既然包含了该文件，那么首先排除sql注入的问题

if (isset($_POST['submit']) && !empty($_POST['user']) && !empty($_POST['pass'])) {
	include_once('../header.php');

    // 竟然还存在 (@$_POST['captcha'] !== $_SESSION['captcha'] 但是我访问的页面根本没有，依旧可以登陆，这也是一个漏洞，没有验证码也可以登录
	if(@$_POST['captcha'] !== $_SESSION['captcha']){
		header('Location: login.php');
		exit;
	}

	$name = $_POST['user'];
	echo $_POST['user'];
	$pass = $_POST['pass'];
	echo $_POST['pass'];

    $query = "SELECT * FROM admin WHERE admin_name = '$name' AND admin_pass = SHA('$pass')";
    $data = mysql_query($query, $conn) or die('Error!!');

    if (mysql_num_rows($data) == 1) {
		$_SESSION['admin'] = $name;
        header('Location: manage.php');
        }
	else {
		$_SESSION['error_info'] = '用户名或密码错误';
		header('Location: login.php');
	}
	mysql_close($conn);
}
else {
	not_find($_SERVER['PHP_SELF']);
}
?>

```

由于 包含了 lib.php 而该页面对 `$_GET  $_POST` 都做了处理，在函数外在加了一层函数sec，导致无法SQL

### 2、编辑用户信息类

avatar.php

```php
<?php
error_reporting(0);
session_start();
header("Content-type:image/jpeg");
echo file_get_contents($_SESSION['avatar']);
?> 
```

这个文件上传没有做任何过滤

#### updateAvatar.php - 疑似存在文件名造成SQL注入

这里虽然包含了 **lib.php 但是这个文件中也没有对上传的文件名做过滤**，所以疑似存在，还没有利用的了

```php
include_once('../sys/config.php');

$avatar = $uploaddir . '/u_'. time(). '_' . $_FILES['upfile']['name'];

$query = "UPDATE users SET user_avatar = '$avatar' WHERE user_id = '{$_SESSION['user_id']}'";
```

```sql
$query = "UPDATE users SET user_avatar = '007.png' and updatexml(1,concat(0x7e,database(),0x7e),1)#.png' WHERE user_id = '{$_SESSION['user_id']}'";
```

最终构造出的语句结构是这样的，在navicat中尝试了一下可以报错，但是通过请求发过去之后就失败了，不知道怎么回事

#### updateName.php - id参数存在SQL越权

由于 clean_input 函数只是对字符型数据进行预防，但是 id 参数时数字，所以 id 参数根本不受 clean_input 函数的影响，所以在下面的 update 语句中，攻击者可以任意构造 id  参数的值，从而改掉任意用户的 username。知道用户名之后，对于爆破来说简直少了很多事，方便多了

```php
<?php
include_once('../sys/config.php'); //包含了 lib.php
if (isset($_POST['submit']) && !empty($_POST['username']) ) {

	if (strlen($_POST['username'])>16) {
		$_SESSION['error_info'] = '用户名過長（用戶名長度<=16）';
		header('Location: edit.php');
		exit;
	}

	$clean_username = clean_input($_POST['username']);
	$clean_user_id = clean_input($_POST['id']);
	
	//判断用户名已是否存在
	$query = "SELECT * FROM users WHERE user_name = '$clean_username'";
    $data = mysql_query($query, $conn);
	if (mysql_num_rows($data) == 1) {
		$_SESSION['error_info'] = '用户名已存在';
		header('Location: edit.php');
		exit;
	}
	
	$query = "UPDATE users SET user_name = '$clean_username' WHERE user_id = '$clean_user_id'";
	mysql_query($query, $conn) or die("update error!");
	mysql_close($conn);
	//刷新缓存
	$_SESSION['username'] = $clean_username;
	header('Location: edit.php');
}
else {
	not_find($_SERVER['PHP_SELF']);
}
?>
    
    
function clean_input( $dirty ) {
	return mysql_real_escape_string( stripslashes( $dirty ) );
}
```

##### SQL越权利用

比如我现在有一个用户 为 wwww

![image-20240819173304873](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819173304873.png)

![image-20240819172938258](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819172938258.png)

此时使用该用户进行修改用户名，同时开启抓包

![image-20240819173037358](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819173037358.png)

修改参数id的值为自己想越权的用户，放行

![image-20240819173130724](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819173130724.png)

此时，我们就变成了用户baba

![image-20240819173219348](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819173219348.png)

![image-20240819173516086](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819173516086.png)

#### 修改用户密码存在csrf漏洞

![image-20240819153759682](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819153759682.png)

先尝试修改密码，抓包观察信息

![image-20240819173842215](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819173842215.png)

好得很，啥都没防范，没有旧密码校验就算了，连动态Token也没有，随意构造一个恶意链接，诱使受害者访问就可以改他密码了

##### csrf修改密码利用

比如我现在依旧是wwww这个用户

![image-20240819174622211](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819174622211.png)

![image-20240819174952587](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819174952587.png)

由于只是测试，所以不需要再在攻击服务器上构建链接，用本地用户测试一下就ok

访问之后（浏览器开启代理访问到页面后关闭burp代理，然后点击按钮）

尝试用这个用户登录，发现wwww用户密码已被修改
