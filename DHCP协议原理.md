# ==DHCP协议==

#### 1.掌握DHCP工作原理

#### 2.会在Windows server上去部署DHCP服务

#### 3.抓流量

- 正常
- 受到攻击后

## 一、DHCP

#### 1.DHCP基本概念

- dhcp（动态主机配置协议）：主要是给客户机提供TCP/IP参数（IP地址，子网掩码，网关，DNS等）

#### 2.好处

- 减少管理员的工作量
- 避免输入出错可能性
- 避免IP冲突
- 提高IP地址利用率

#### 3.DHCP工作原理

- 应用层协议，基于UDP协议，主机是向服务器的67号端口，服务器响应给客户机的68号端口 
- 客户机与服务器的交互过程

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230814143524550.png" alt="image-20230814143524550" style="zoom:200%;" />

DHCP discover，client以广播的方式去请求，所有的服务器都会收到这个请求，也都会响应（DHCP offer），client会向收到的第一个offer报文（其中会提供client可使用的IP地址）的服务器发送DHCP request（标明client要的是哪一个IP地址），然后服务器就会向client发送DHCP ACK确认报文，此时就将client要的IP地址赋给了client，client获得TCP/IP参数 

## 二、在Windows server上部署DHCP服务器

实验：

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230814155150209.png" alt="image-20230814155150209" style="zoom:200%;" />

**详细情况见蜗牛第一阶段课程的DHCP服务器部署这节课**

dhcp上路由器中继（因为该实验VM1并没有开启dhcp服务，因此此时是无法直接跨网段访问服务器的，那么就只能做一个中继，让VM1可以跨越路由器请求服务器）

```shell
en
conf t
int f0/0
ip helper-address 192.168.120.100
#192.168.120.100  这是后面的服务器地址
```

### 1.DHCP的8种报文

- DHCP discover
- DHCP offer
- DHCP request
- DHCP ack
- DHCP release
- DHCP nak：服务器对client的request报文的拒绝响应报文
- DHCP decline：当client发现服务器分配给他的IP地址发生冲突时会通过发送次报文来通知服务器，并且会重新向服务器申请地址
- DHCP inform：客户机已经获得了IP地址，发送此报文的目的是为了从服务器获得其他的一些网络配置信息，比如网关地址，DNS，服务器地址等等
