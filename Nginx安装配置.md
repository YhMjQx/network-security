[TOC]



# ==Nginx安装配置==

## 一、特点

1.是一个web服务器，主要用于处理HTTP/HTTPS等协议，含SMTP/POP3/FTP等协议。与Apache相似

2.轻量，速度极快，支持高并发（号称支持50000并发请求），电脑和带宽得支持。用C语言编写（Apache，MySQL，PHP，Linux等，均由C语言编写），C语言是目前世界上已知的编程语言中，速度最快的，没有之一

3.Nginx是目前企业的标配，但是Nginx只能处理如HTTP协议等，不能解析PHP，Java（Tomcat）。通常是都是Nginx+PHP、Nginx+Tomcat、Nginx+Python等

4.Nginx的反向代理：

> - 正向代理：比如上网用的正向代理服务器（作为客户端与服务器的中间人，处理客户端的请求）
>   - 可以访问原来无法访问的资源，如google
>   - 可以做缓存，加速访问资源（当客户端访问的资源代理服务器中已有时，便不需要在访问真正的服务器）
>   - 对客户端访问授权，上网进行认证
>   - 代理可以记录用户访问记录（上网行为管理），对外隐藏用户信息
>
> ![image-20240121195009237](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121195009237.png)
>
> 解释一下正向代理：客户端知道服务器端，但是客户端访问服务器端IP的流量都会先经过正向代理服务器，只有通过了正向代理服务器流量才会与真正的服务器交互。其中客户端知道服务器端，但是服务器端并不知道客户端



- 反向代理
  - 保证内网的安全，阻止web攻击，大型网站，通常将反向代理服务器作为公网访问地址，web服务器是内网
  - 负载均衡，通过代理服务器来优化网站的负载

解释一下反向代理服务器：公开反向代理服务器的IP地址和对应端口，客户端不知道真是的服务器，只会一味地访问反向代理服务器，但是真正的服务器却是知道客户端的，因为访问的流量中都会带有IP参数之类的

比如如图所示的反向代理服务器就是一台Nginx，后面可能连着2台，20台，200台真是的服务器，很多很多都有可能，但是当我去访问的时候访问的都是反向代理服务器的IP地址

![image-20240121200026895](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121200026895.png)

## 二、配置

1.在Windows上，解压然后双击运行nginx.exe即可开启服务

2.在Linux上，是C语言源代码，需要先配置，再编译，再安装

- 先安装gcc编译器：`yum install gcc pcre-devel zlib-devel openssl openssl-devel`
- 进入到nginx源码文件中
- 配置：`./configure --prefix=/usr/local/nginx --with-http_ssl_module` **注意：这里的/usr/local是nginx的默认安装目录，不要改，nginx不允许解压目录和安装目录为同一个**

安装过程中如果遇见下图所示情况，是因为安装gcc时没有安装 pcre-devel,此时就需要安装gcc时，执行上面的指令，而不是只要装了gcc就万事大吉

```
./configure: error: the HTTP rewrite module requires the PCRE library.
You can either disable the module by using --without-http_rewrite_module
option, or install the PCRE library into the system, or build the PCRE library
statically from the source with nginx by using --with-pcre=<path> option.
```

- 编译C语言的源代码为二进制文件：`make`
- 安装： `make install`

安装好之后可以使用两条命令查看一下nginx的位置

```
whereis nginx
find / -name nginx
```

![image-20240121210509463](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121210509463.png)

- 启动nginx： `./usr/local/nginx/sbin/nginx`

![image-20240121211022702](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121211022702.png)

当显示如此页面的时候就说明配置成功了，但值得注意的是需要避免本台机器80端口被占用（如果需要两台服务都开始，那么就需要修改修改其中一个服务的默认端口）

比如：**我们把nginx的默认端口改为8088，然后照旧开启xampp**

修改nginx核心配置文件 /usr/local/nginx/conf/nginx.conf

![image-20240121214712334](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121214712334.png)

修改监听端口为8088并同时开启防火墙

 `firewall-cmd --add-port=8088/tcp --permanent``
``systemctl restart firewalld`

重启nginx

关闭服务： `kill pid `  或  `pkill servename`
开启服务：  `./usr/local/nginx/sbin/nginx`

![image-20240121215711803](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121215711803.png)

![image-20240121215809841](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121215809841.png)

![image-20240121215826161](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121215826161.png)

现在80端口的mysql可以开，8080端口的Tomcat可以开，8088端口的nginx也可以开

## 三、核心配置文件 /usr/local/nginx/conf/nginx.conf

下面内容中我将使用 -- 来注释我自己添加的内容

```
#user  nobody;
worker_processes  1;  --表示该服务进程为单进程

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;   --这些都是一些错误信息重定向文件

#pid        logs/nginx.pid;


events {
    worker_connections  1024; --对应于链接数量，和同时处理并发量以及服务器速率有关
}


http {
    include       mime.types;
    default_type  application/octet-stream; --log_format是定义的日志文件的格式

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;  

    sendfile        on;  --开启发送文件功能
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;  --设置长连接的超时时间

    #gzip  on; --用于网页压缩，提高传输效率

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html; --这里指定的是根目录，就相当于Apache里的DocumentRoot
            index  index.html index.htm;
        }

        #error_page  404              /404.html; --遇到访问错误页面时，重定向到哪个页面

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;  --遇到错误代码为500的情况，跳转到该
        location = /50x.html {                                         --默认首页
            root   html;
        }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}

```

