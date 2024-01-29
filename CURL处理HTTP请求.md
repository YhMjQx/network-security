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

