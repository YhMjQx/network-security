[TOC]



# ==VAuditDemo管理员后台与存储型XSS漏洞==

## 一、留言处存在无法利用的存储型XSS漏洞

该漏洞的原因是，用户在发表留言时可以发表一个<script>标签的脚本，然而往数据库插入内容时竟然没有做htmlspecialchars字符实体转码，我们可以通过代码调试来看一下，下面第一张图是留言页面的图

![image-20240822102909203](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822102909203.png)

下面三张图是代码调试图，我们可以看到，在插入数据库时`$clean_message` 竟然还是原封原样的<script>脚本

![image-20240822103859614](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822103859614.png)

![image-20240822103522998](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822103522998.png)

![image-20240822103538014](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822103538014.png)

在进入数据库去看，还真是

![image-20240822102935786](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822102935786.png)

但是我们再看message.php页面的情况

message.php

```php
<?php
while($com = mysql_fetch_array($data)) {
	// echo $com['user_name']."<br>";  // xxxx',
	$html['username'] = htmlspecialchars($com['user_name']);
	// echo htmlspecialchars($com['user_name'])."<br>";  // xxxx',
	$html['comment_text'] = htmlspecialchars($com['comment_text']);
	
	echo '<tr>';
	echo '<td>'.$html['username'].'</td>';
	echo '<td><a href="messageDetail.php?id='.$com['comment_id'].'">'.$html['comment_text'].'</td></a>';
	echo '</tr>';
}
?>
```

可以看到，从数据库中取出数据后进行实体字符转换后再输出到页面，从而才没有弹窗

**但是，真的不确保程序员开发时在其它页面也能记得起来使用htmlspecialchars，如果忘了就出现漏洞了**

## 二、管理员后台漏洞

### 1、任意命令执行

![image-20240822110037829](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822110037829.png)

### 2、任意添加管理员，CSRF漏洞

抓包添加管理员

![image-20240822110323390](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822110323390.png)

生成恶意链接，诱使已登录的管理员点击 http://burpsuite/show/1/e2wtf80t84m8izy2oukktup3dihqze4c 

![image-20240822110641961](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822110641961.png)

![image-20240822110656769](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822110656769.png)

此时就可以发现，已成功添加管理员aaaa，这时攻击者就可以登录了，然后再删掉admin，使得自己成为唯一管理员

当然，我们完全可以将恶意链接的页面做的足够优美，诱惑性十足，并且用户点了之后都不知道自己干了什么，页面跳转也处理好。

## 三、存储型XSS漏洞

登录时，通过审计logCheck.php可以发现，还有一个字段 login_ip ，而这个字段刚好又在管理员界面中会显示

logCheck.php

```php
$ip = sqlwaf(get_client_ip());
$query = "UPDATE users SET login_ip = '$ip' WHERE user_id = '$row[user_id]'";
```

而其中的sqlwaf和get_client_ip两个函数都存在于lib.php文件中

lib.php

```php
function sqlwaf( $str ) {
	$str = str_ireplace( "||", "", $str );
	$str = str_ireplace( "&&", "", $str );
	$str = str_ireplace( "'", "", $str );
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
	$str = str_ireplace( "%", "\%", $str );
	$str = str_ireplace( "_", "\_", $str );
	return $str;
}

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

这代码分析一看 首先sqlwaf无法防御 <script>，其次get_client_ip函数，如果没有 `$_SERVER["HTTP_CLIENT_IP"]` 那么就使用 `$_SERVER["HTTP_X_FORWARDED_FOR"]` 作为 login_ip 字段的值，而`$_SERVER["HTTP_X_FORWARDED_FOR"]` 值，我们可以自己构造

> `$_SERVER["HTTP_X_FORWARDED_FOR"]` 与 `$_SERVER["REMOTE_ADDR"]` 的关系在之前已经讲解过了，就是代理与源IP的关系

payload `X-Forwarded-For: <script>alert(document.cookie)</script>` 

![image-20240822115249599](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822115249599.png)

> 从请求中我们也可以看出来，并没有 `$_SERVER["HTTP_CLIENT_IP"]` 值可以让攻击者控制

此时再用管理员登录，查看用户信息

![image-20240822115156029](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240822115156029.png)

