# ==Redis配置与使用==

首先有个概念：非关系型数据库不一定就是存储在内存中的

Redis是最为流行的缓存服务器：数据是保存在内存中的，所有的IO操作全都在内存中进行，速度非常快，性能非常高 

如果断电了或停止服务，数据就会消失，而内存型数据库恰好可以弥补类似于MySQL等关系型数据库在硬盘中进行IO操作的速度上的局限。

所以最常见的是关系型数据库和非关系型数据库同时配合使用。关系型数据库解决数据永久存储和业务逻辑中表与表之间；而内存型数据库一般处理性能问题

Redis是key-value键值对的存储格式，非关系型，用key=value的方式操作数据，就比如说a=100  name=woniu  ，所以为了找到值，只需要找到key就可以了。而关系型数据库是二维表+SQL语句操作。

![image-20231224202330466](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224202330466.png)

客户端向服务器请求数据，服务器向数据库请求数据，关系型数据库可以将数据库读写进内存型数据库，然后后面的读写都对内存型数据库读写就好了

**计算机内部距离CPU越近的设备，运行速度最快**

![image-20231224205721321](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224205721321.png)

混合硬盘速度

![image-20231224210214040](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224210214040.png)

硬盘速度

![image-20231224210149541](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224210149541.png)

内存与缓存的速度

![image-20231224210132185](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224210132185.png)

## 一、安装redis

```
Redis的安装过程基于C语言源代码，所以安装之前确保已经安装成功 gcc ，如果没有则 yum install gcc -y 

然后再对Redis文件上传，解压，编译，安装

解压：tar -zxvf redis-6.2.5.tar.gz
切换目录： cd redis-6.2.5
编译： make
安装：make install  #默认位置： /usr/local/bin
也可以在安装过程中指定自己目录：  make PREFIX=/usr/local/redis install

切换到redis目录：cd /usr/local/bin
复制配置文件： cp ./redis-6.2.5/redis.conf /usr/localbin
启动服务器： ./redis-server redis.conf
```

### **安装gcc**

![image-20231224212430105](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224212430105.png)

### **然后再make**

![image-20231224211857129](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224211857129.png)

![image-20231224212320522](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224212320522.png)

如果make过程中遇见了以下错误，使用make参数 make MALLOC=libc 

![image-20231224212713306](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224212713306.png)

**make结束之后，再执行make install就OK了**



### 更改redis配置文件

![image-20231224213613262](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224213613262.png)

我么可以看到，这目录下的所有文件都是可执行文件

由于在/usr/local/bin目录下执行 `./redis-server` 时，需要去执行 redis.conf 这个配置文件，而 redis.conf 这个文件在 ~/redis-6.2.5/ 目录下，所以，如果 /usr/loacl/bin 目录下没有该文件就需要 `./redis-server ~/redis-6.2.5/redis.conf  ` 当然，我们可以选择将 ~/redis-6.2.5/redis.conf 文件复制到 /usr/local/bin/ 目录下，此时就可以直接在 /usr/local/bin 目录下执行语句 `./redis-server redis.conf ` 就好了

如下所示：

![image-20231224214240062](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224214240062.png)

![image-20231224223905935](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224223905935.png)

看到这样就成功了

## 二、Redis基本使用





































> 这里说一个关于安装gcc是报错的问题
>
> 如果遇到了下图问题
>
> ![image-20231224222245445](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231224222245445.png)
>
> 是因为DNS解析的问题，需要在网络配置文件  /etc/sysconfig/network-scripts 中添加 DNS=114.114.114.114 然后再重启网卡，重新 yum install gcc -y 就好了
>
> 当然，这只是我这台主机的问题解决办法，还有可能真的是镜像的问题，这时就可以用 [镜像解决]([蓝易云：解决Centos7系统yum出现could not retrieve mirrorlist错误-CSDN博客](https://blog.csdn.net/tiansyun/article/details/133419569?ops_request_misc=&request_id=&biz_id=102&utm_term=centos中 yum安装 gcc 时 报错 Could n&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-133419569.142^v96^pc_search_result_base2&spm=1018.2226.3001.4187)) 这个
