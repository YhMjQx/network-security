<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905171400806.png" alt="image-20230905171400806" style="zoom:150%;" />

# ==应用控制策略进制上网==

在AF上控制AD域不能上网

本实验在AF2上启用策略

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905170111811.png" alt="image-20230905170111811" style="zoom:200%;" />

#### 第一步：

先填选基础信息

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905170549290.png" alt="image-20230905170549290" style="zoom:150%;" />

####  第二步：

选填源的信息

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905170911459.png" alt="image-20230905170911459" style="zoom:150%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905170833068.png" alt="image-20230905170833068" style="zoom:150%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905170849249.png" alt="image-20230905170849249" style="zoom:150%;" />

#### 第三步：

选填目的区域的信息

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905171003484.png" alt="image-20230905171003484" style="zoom:150%;" />

#### 第四步：

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905171022751.png" alt="image-20230905171022751" style="zoom:150%;" />







# ==用户防护策略==

服务器的防护一般内外网的防护都要有

主机的防护一般是防的外网

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905171637138.png" alt="image-20230905171637138" style="zoom:150%;" />

 <img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905183010049.png" alt="image-20230905183010049" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905184939526.png" alt="image-20230905184939526" style="zoom:150%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905185128677.png" alt="image-20230905185128677" style="zoom:150%;" />





### 安全策略模板

#### 漏洞攻击防护

##### **默认模板_上网管控场景**

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905190022428.png" alt="image-20230905190022428" style="zoom:150%;" />

![image-20230905190224050](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905190224050.png)

这个主要是来保护客户端的



##### **默认模板_业务保护场景**

![image-20230905190307014](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905190307014.png)





#### 内容安全

![image-20230905190659711](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905190659711.png)

##### 上网管控场景

![image-20230905190734736](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905190734736.png)

##### 业务保护场景

![image-20230905190859781](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905190859781.png)

##### 防勒索文件下载查杀



#### 僵尸网络

![image-20230905191242619](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905191242619.png)



web应用防护是专门针对服务器的防护模版







# ==业务防护策略==

![image-20230905192347365](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905192347365.png)

因为我们的服务器可能会产生来自互联网区域的攻击和内网区域的攻击

![image-20230905195511132](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905195511132.png)

选择访问源未经过原地址转换或CDN的原因：

NAT地址转换：NAT主要作用其实就是,将私有内网转换为可访问的外网网络;转换过程中,“内网到外网转换的是源IP地址,外网到内网转换的是目的IP地址。

![image-20230905200853135](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905200853135.png)



![image-20230905203921715](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905203921715.png)



![image-20230905203053543](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905203053543.png)

 

![image-20230905203231992](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905203231992.png)





开启的所有策略都会消耗硬件本身

应用隐藏和口令防护比较重要







# ==网站防篡改==

本实验针对的是HTTP Server，这是一台Linux服务器

我们最好还是在AF2上做这个策略，因为如果实在AF1上做该策略的话，内网主机访问该服务器时根本不会经过AF1，那么此时就防不住内网的网站篡改

![image-20230905210411814](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905210411814.png)

 

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905210943461.png" alt="image-20230905210943461" style="zoom:150%;" />



![image-20230905210950902](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905210950902.png)

注意，这里是3.100不是3.200，别写错了，图上是错的



![image-20230905211028809](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905211028809.png)



![image-20230905211131002](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905211131002.png)



![image-20230905211208339](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905211208339.png)



然后使用xshell连接linux的这个服务器HTTP Server

![image-20230905212553578](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905212553578.png)



![image-20230905211729560](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905211729560.png)



![image-20230905211735003](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905211735003.png)



![image-20230905211802513](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905211802513.png)



现在想起刚刚装的Linux 防篡改客户端，使用xshell中的xftp工具

![image-20230905212003803](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905212003803.png)

 

![image-20230905212407645](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905212407645.png)



这个客户端就是EPS这个文件，因为课堂老师提前安装的有这个客户端，需要先将其删除

![image-20230905213808467](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905213808467.png)



然后开始我们的应该做的

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905214823651.png" alt="image-20230905214823651" style="zoom:200%;" />

![image-20230905215048881](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905215048881.png)

![image-20230905215455066](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905215455066.png)

![image-20230905215757734](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905215757734.png)

![image-20230905220101606](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905220101606.png)

这个用来提权的账号和密码也就是实验中的epsgreat888，如上图中白色的文档

![image-20230905220428683](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905220428683.png)

现在配置完成了，那么我们就要开始测试一下，怎么测试呢，需要关掉xshell，因为xshell打开，连接存在导致该策略无法生效，所以关掉一个窗口，重打开一个窗口进行连接

账户名和密码分别是 root 和 sangfor123，连接linux一般采用ssh协议

![image-20230905220737019](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905220737019.png)

![image-20230905221038028](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905221038028.png)

![image-20230905221204495](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905221204495.png)

![image-20230905221302384](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905221302384.png)

此时说明我们的方修改策略生效了

![image-20230905221429346](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905221429346.png)







# ==网站后台页面二次防护==

![image-20230905222230308](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905222230308.png)

![image-20230905222334942](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905222334942.png)

![image-20230905222358148](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905222358148.png)

![image-20230905222437510](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905222437510.png)

我们可以先发一个测试文件看看是否创建邮箱成功

![image-20230905222531040](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905222531040.png)

点击邮件认证下面的配置邮箱列表

![image-20230905222825923](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230905222825923.png)

![image-20230905223200591](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905223200591.png)

也不能说是收件的邮箱，是上面那个管理员邮箱

输入验证码之后就会跳转到后台登录页面

![image-20230905223428781](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230905223428781.png)