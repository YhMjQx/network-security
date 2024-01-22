[TOC]



# ==Nginx+Tomcat集群环境==

## 一、集群环境架构

![image-20240122104512728](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240122104512728.png)

一台Nginx可以与多台Tomcat服务器挂钩，此时客户端访问的都是Nginx反向代理的IP地址和端口，然后Nginx通过一些分流策略等等，将流量分配到不同的Tomcat上，最后由Tomcat连接数据库，并处理Java的请求。该图中的Nginx和MySQL等都是可以继续扩展的

集群的作用：

（1）负载均衡：Load-Balance，表示有多台服务器同时提供服务，每一台服务器的负载就会降低，提升性能和并发量

（2）故障转移：Fall-Over，其中一台崩溃，则数据流转移到另外一台上

## 二、配置单机应用

配置一个Nginx+一个Tomcat

1.确保Tomcat正常访问，配置参考Tomcat的步骤

```
开启：/opt/apache-tomcat-8.0.53/bin/startup.sh
关闭：/opt/apache-tomcat-8.0.53/bin/shutdown.sh
```

2. 配置Nginx 的核心配置文件 /usr/local/nginx/conf/nginx.conf

```
#此节点在 http 节点下，与 server 节点同级
upstream mytomcat {
	## 指定Tomcat的服务器IP地址和端口，及权重（针对多套Tomcat服务器时使用）
	server 192.168.230.147:8080 weight=1;
	##也可以添加第二台，第三台，第四台等构成集群环境
}
```

![image-20240122121248257](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240122121248257.png)

由于nginx默认端口为80，而MySQL默认端口也是80，因此我将nginx的默认端口改为了8088

```
## 如果通过nginx访问 http://192.168.230.147:8088/woniusales,则通过 proxy_pass 反向代理将该目录下的所有请求，转发给 http://mytomcat/woniusales,其中mytomcat是由upstream节点定义的名称

location / {
	proxy_pass http://mytomcat/woniusales/;  # 此处最后务必添加 /
	proxy_redirect default;
}
```

```
# 当用户访问nginx的80端口下的woniusales时，访问mytomcat下的woniusales，此节点在 server 节点中
location /woniusales/ {
	proxy_pass http://mytomcat/woniusales/;
	proxy_redirect default;
}
```

![image-20240122121703644](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240122121703644.png)

重启nginx

现在我们就配置好了nginx的单机反向代理，此时我们就可以通过访问nginx来访问woniusales

![image-20240122121934248](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240122121934248.png)

原本的8088端口配置的是Nginx，但由于现在配置了nginx的反向代理，于是访问8088端口时nginx都会自动将请求递交给Tomcat服务器，然后根据nginx.conf 的配置文件我们可以知道其实是直接访问了tomcat下的woniusales。所以现在访问8088端口就会自动跳转到woniusales页面呢

## 三、配置Tomcat集群

1.准备至少两台可用的Tomcat，确保两台Tomcat连接到同一个数据库，配置文件在 /opt/apache-tomcat-8.0.53/webapps/woniusales/WEB-INF/classes/db.properties 中

2.确保Nginx所在服务器，可以正常访问到这两台Tomcat，如果不能，请检查防火墙是否放行了Tomcat端口8080等

3.将所有的Tomcat服务器，配置于nginx核心配置文件/usr/local/nginx/conf/nginx.conf的upstream节点中

```
#此节点在 http 节点下，与 server 节点同级
upstream mytomcat {
	ip_hash;  
	## ip_hash 使得访问哪个IP地址，就将数据交给哪个Tomcat
	## 指定Tomcat的服务器IP地址和端口，及权重（针对多套Tomcat服务器时使用）
	server 192.168.230.148:8080 weight=2;
	server 192.168.230.147:8080 weight=1;
	##也可以添加第二台，第三台，第四台等构成集群环境
}

其他配置保持不变
```

4.重启nginx

```
/usr/local/nginx/sbin/nginx -s reload
```

5.测试集群的功能

![image-20240122162130437](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240122162130437.png)

nginx默认端口是80

使用192.168.112.1访问一下192.168.112.188/woniusales 我们去看access_log，先去192.168.112.188上的Tomcat发现并没有日志记录，然后再去192.168.112.1上面去看发现有日志记录，说明该流量确实是被nginx转发给了192.168.112.1，从侧面也验证了192.168.112.188上的nginx确实搭载了两台Tomcat，不然也不会将访问192.168.112.188:80的流量转发给192.168.112.1。

但我们明明配置的是ip_hash，但为什么访问的是192.168.112.188，怎么流量都转发给了192.168.112.1呢，也许是因为配的权重比较高吧

（1）确保所有Tomcat节点连接到同一个数据库，保持数据同步

（2）必须确保客户端有不同的IP地址访问，Nginx的集群会根据IP地址来分给后台服务器

（3）在Tomcat节点上，`tall -f /opt/apache-tomcat/logs/access.log` 实时刷新访问日志，如果有请求进来，可以看到客户端的IP地址