# ==Redis主从复制==

## 单机Redis的问题

单机Redis的问题很明确，如果当前的Redis服务器宕机了，则系统的整个缓存系统瘫痪，导致灾难性的后果，另外单机Redis也有内存容量瓶颈

### Redis主从复制

一个master可以有多个slave，一个slave只能有一个master

![image-20240112191234942](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112191234942.png)

#### 二、Redis的主从复制作用

1.读写分离，提高服务读写负载能力

2.提高了整个Redis的服务可用性

#### 三、搭建redis主从复制

1.准备3台虚拟机，分别装好了redis

![image-20240112192634200](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112192634200.png)

2.开放每台服务器的6379端口

```
firewall-cmd --add-port=6379/tcp --permanent
```



3.编辑redis master服务的配置文件redis.conf

```
daemonize yes
requirepass p-0p-0p-0
logfile redis.log
注释掉：bind 127.0.0.1 -::1 或修改为 bind 0.0.0.0 表示支持远程连接
```



4.编辑redis slave 服务的配置文件redis.conf

```
daemonize yes
masterauth p-0p-0p-0
requirepass p-0p-0p-0
logfile redis.log
注释掉： bind 127.0.0.1 -::1 或修改为 bind 0.0.0.0 表示支持远程连接
```



5.分别启动三个虚拟机的redis服务，且使用redis客户端连接redis服务，输入以下命令

```
> info replication

会发现此时3个redis服务的role都是master
```

![image-20240112194020299](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112194020299.png)

6.在slave服务器上运行以下命令，完成主从复制

```
slaveof 192.168.230.147 6379
```

#### 

