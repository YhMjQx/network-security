[TOC]



# ==Suricata检测HTTPS流量==

> 想办法，把https的流量解密开然后再进行分析

#### 一、HTTPS流量分析配置

HTTPS流量默认是加密状态，无法进行分析和查看，所以要对其进行分析，必须要先进行解密。

##### 1、添加系统环境变量SSLKEYLOGFILE

![image-20211225193737195](https://gitee.com/ymq_typroa/typroa/raw/main/20211226050907.png)

##### 2、打开Chrome并浏览目标网站以生成https_key.log

##### 3、在Wireshark中导入该文件，对HTTPS流量完成解密

![image-20211225201457944](https://gitee.com/ymq_typroa/typroa/raw/main/20220314004806.png)

4、Fiddler解密HTTPS

![image-20211225201147885](https://gitee.com/ymq_typroa/typroa/raw/main/20220314004811.png)

![image-20211225201846810](https://gitee.com/ymq_typroa/typroa/raw/main/20220314004813.png)

以上解密过程仅适用于客户端处理，并不适用于IDS设备，默认情况下，IDS系统是无法处理加密流量的，要解密HTTPS，可以在服务器端安装一个SSL代理，让代理进行解密，再交由IDS进行检测。

> https://github.com/sonertari/SSLproxy
>
> https://www.netresec.com/?page=PolarProxy

教材内容

### Suricata检测HTTPS流量

#### 一、如何实现检测

所有IDS系统对加密流量的处理都是一个巨大的难题，目前市面上并没有好的解决方案，通常来说借助于机器学习，可以实现一些攻击流量的预警，但是准确度均比较低，此时，借助于代码层面的WAF或HIDS才可以弥补这一类缺陷。

但是针对HTTPS流量来说，毕竟不是攻击流量，而是互联网通信的标配，所以服务器端是可以解密的，解密后变成明文HTTP协议，就可以很好地实现入侵检测了。所以，要处理HTTPS流量，最关键的是，先解密HTTPS数据包，才对其进行入侵检测，通常的解决方案有两种：一是直接在代码层面进行检测，类似于程序员要做的事情，对用户输入进行检测判断，但是这一种方案并非NIDS，所以本节内容不专门阐述。第二种方案就是通过配置HTTPS反向代理的方式来进行检测，如下图所示：

![image-20230105185618998](https://gitee.com/ymq_typroa/typroa/raw/main/20230105185619.png)

#### 二、构造实验环境

1、一台客户机，模拟客户端发送HTTPS请求给Nginx服务器，此IP地址为：192.168.112.1

2、一台Nginx服务器，该Nginx配置HTTPS证书，并反向代理到远程Tomcat主机，此IP地址为：192.168.112.183

3、一台Tomcat服务器，该Tomcat服务器正常配置，不配置HTTPS证书，开启8080端口，IP地址为：192.168.112.188

4、在Nginx或Tomcat任意一台服务器上安装Suricata，均可对Tomcat的流量进行入侵检测或防御。

5、还需要在Nginx和Tomcat服务器上安装tcpdump抓包工具，用于抓取所有流量进行验证。

整个过程的通信过程如下：

![image-20230105185804150](https://gitee.com/ymq_typroa/typroa/raw/main/20230105185804.png)

#### 三、配置Tomcat服务器

在Tomcat服务器上安装Tomcat，并部署WoniuSales在此，同时在该服务器上安装Suricata，实现对Tomcat流量的检测。

#### 四、配置Nginx服务器

1、安装Nginx服务器，确保在编译时支持SSL模块

（1）在线安装

```
yum install -y nginx
```

（2）源码安装

![image-20250225225413437](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250225225413437.png)

2、为Nginx生成证书

```shell
第一步：先确认openssl是否已经安装好
[root@centqiang ~]# openssl version
OpenSSL 1.0.2k-fips  26 Jan 2017

第二步：生成私钥，需要输入密码，如123456
openssl genrsa -des3 -out server.pass.key 2048

第三步：去除私钥中的密码
openssl rsa -in server.pass.key -out server.key

第四步：生成CSR证书，注意最后必须是localhost
openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=BeiJing/L=BeiJing/O=dev/OU=dev/CN=localhost"

第五步：生成SSL证书
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

最终只需要三个文件：server.crt， server.csr， server.key
将上述三个文件复制到 /usr/local/nginx/conf目录下
```

3、直接使用以下内容覆盖nginx.conf（先做好备份）

```shell
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {    
	worker_connections 1024;
}

http {    
	include       mime.types;    
	default_type  application/octet-stream;    
	
	sendfile        on;    
	
	keepalive_timeout  65;    
	
	# 添加该upstream节点实现反向代理到Tomcat    
	upstream mytomcat {        
		server 192.168.112.188:8080 weight=1;    
	}    
	
	# 添加server节点，定义SSL证书路径，端口，转发地址等    
	server {        
		listen       443 ssl;        
		server_name  localhost;        
		
		ssl_certificate      server.crt;        
		ssl_certificate_key  server.key;        
		
		ssl_session_cache    shared:SSL:1m;        
		ssl_session_timeout  5m;        
		
		ssl_ciphers  HIGH:!aNULL:!MD5;        
		ssl_prefer_server_ciphers  on;        
		
		# 配置网站目录        
		location / {            
			root   html;            
			index  index.html index.htm;        
		}    
        
		location /woniusales/ {            
			proxy_pass http://mytomcat/woniusales/;            
			proxy_redirect default;        
		}        
		
		error_page  404              /404.html;        
		
		error_page   500 502 503 504  /50x.html;        
		location = /50x.html {            
		root   html;        
		}    
	}
}
```

4、重启Tomcat和Nginx，利用HTTPS访问

![image-20220904162708154](https://gitee.com/ymq_typroa/typroa/raw/main/20220904162708.png)

#### 五、在Nginx和Tomcat上抓包

1、Nginx上数据包

![image-20220904163249749](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20220904163249.png)

也检测到了非加密流量，那是Nginx与Tomcat之间的通信流量，走的是HTTP协议。

![image-20220904162941016](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20220904162941.png)

2、Tomcat上数据包（非加密流量）

![image-20220904163043597](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20220904163043.png)

进而，在Nignx或Tomcat上安装Suricata对其流量进行检测即可，因为Nginx与Tomcat的通信流量是非加密的，所以在哪一台电脑上安装Suricat取决于实际需要，如果要更真实模拟一个IDS或WAF硬件设备的部署方式，通常建议安装在Nginx这台代理服务器上。

> 在WAF中，通常也是通过反向代理的方式来实现对HTTPS流量的解密进而实现检测和防御的。另外，有的WAF宣称支持透明代理，这通常要求通信过程不是ECDHE，但是默认情况下都是ECDHE，无法支持透明代理。

![image-20220904163510094](https://gitee.com/ymq_typroa/typroa/raw/main/20220904163510.png)

#### 六、利用Suricata对流量进行检测

需要注意，此时端口和网段也有了变化，要注意同步更新。

```yaml
alert http any any -> $HOME_NET $HTTP_PORTS (msg: "POST请求时SQL注入";  http.method; pcre: "/POST/i"; http.request_body; pcre: "/updatexml|union|select/i"; sid: 564001; )

alert http any any -> $HOME_NET $HTTP_PORTS (msg: "GET请求时SQL注入";  http.method; pcre: "/GET/i"; http.uri; pcre: "/updatexml|union|select/i"; sid: 564002; )

alert http any any -> $HOME_NET $HTTP_PORTS (msg: "XSS跨站攻击";  http.method; pcre: "/GET/i"; http.uri; pcre: "/script|javascript|alert/i"; sid: 564003; )
```

如果目标服务器是Apache，配置如下：

```shell
upstream myapache {    
	server 192.168.100.222:80;
}

location / {    
	proxy_pass http://myapache/;    
	proxy_redirect default;
}
```

#### 七、利用Nginx-Waf检测流量

Ngx_lua_waf可以直接通过Nginx模块的方式对请求数据进行检测，配置过程参考：https://www.woniuxy.com/book/reading/216 中LNMP配置的内容。在nginx.conf的http节点下，添加以下内容，确保waf生效

```
lua_package_path "/usr/local/nginx/conf/waf/?.lua";
lua_shared_dict limit 10m;
init_by_lua_file  /usr/local/nginx/conf/waf/init.lua;
access_by_lua_file /usr/local/nginx/conf/waf/waf.lua;
```

任意构造一个包含攻击特征的请求，实现以下效果。

![image-20220904165555334](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20220904165555.png)

##### 八、在Nginx+OpenResty环境中配置VeryNginx
