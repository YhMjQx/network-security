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

### 2.DHCP报文格式

- m t：消息类型（1表示请求，2表示响应）
- H t：硬件类型
- hops：DHCP报文经过的DHCP中继的数目
- T ID：事务ID
- Client IP address：客户机的IP
- Your(Client) IP address：服务器可以提供给客户机的IP
- Next server IP address：DHCP服务器地址
- Relay agent IP address：中继代理的IP

### 三、实施DHCP欺骗

描述：kali与win10处于同一网段，用kali攻击服务器，占用服务器，直至server无法再向wein10提供服务，此时kali将自己伪装成服务器对win10提供服务

- 配置win10和kali的IP参数

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815154206326.png" alt="image-20230815154206326" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815154232123.png" alt="image-20230815154232123" style="zoom:200%;" />

完事之后可以再ifconfig查看一下信息，或者ping一下win10和server

使用Yersinia（记住，这个攻击需要在配置之前，也就是在联网的情况下进行安装）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815162358821.png" alt="image-20230815162358821" style="zoom:200%;" />

```shell
Yersinia -G     #使用工具的图形化模式
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815162704370.png" alt="image-20230815162704370" style="zoom:200%;" />

这是开始攻击的操作步骤

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815163358066.png" alt="image-20230815163358066" style="zoom:200%;" />

于是服务器便变成了这样

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815163759184.png" alt="image-20230815163759184" style="zoom:200%;" />

**在将自己伪造成服务器之前，一定要先将自己的攻击停掉然后等一会，否则，自己的攻击也会将自己干掉**

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815163416806.png" alt="image-20230815163416806" style="zoom:200%;" />

这是kali伪造服务器的操作步骤

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815164003270.png" alt="image-20230815164003270" style="zoom:200%;" />

然后让win10释放掉原先从server上获取到的ip，然后重新获取，由于此时的serverDHCP已经被攻击满了，所以不能在提供服务了，于是win10就会像kali这台伪造的服务器请求DHCP

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815170731232.png" alt="image-20230815170731232" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815170822776.png" alt="image-20230815170822776" style="zoom:200%;" />

## 四、DHCP防御

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230815202854837.png" alt="image-20230815202854837" style="zoom:200%;" />

由于伪造的DHCP服务器会截胡客户机对真正的服务器的请求，于是就要想办法去解决这个问题，我们可以利用交换机上的信任和非信任端口来处理

由于在交换机上开启监听后，交换机的所有端口都会变成非信任端口，那么此时，任何dhcp的数据报文都无法通过交换机进行转发，于是我们可以在此环境下配置信任端口，使得该端口上的数据得以转发

#### 1.在交换机上配置信任端口

- 开启DHCP监听

  ```
  ip dhcp snooping
  ```

- 指定监听vlan

  ```
  ip dhcp snooping vlan 1
  ```

- 由于开启监听后，交换机上的接口就全部变成了非信任端口（会拒绝DHCP报文），需要将正常的接口添加为信任端口

  ```
  en 
  conf t
  int f0/1
  ip dhcp snooping trust 
  exit
  int f0/3
  ip dhcp snooping trust
  ```

- 启用“选项82”

  ```
  Switch(config)#ip snoping information option
  ```

- 限制DHCP的报文速率

  ```
  en
  conf t
  int f0/3
  ip dhcp snooping limit rate 100
  ```

- 启用核实MAC地址功能

  - 检测非信任端口的请求报文中中，源MAC地址和DHCP请求报文中的客户端MAC地址是否相同

  ```
  en
  conf t
  ip dhcp snooping verify mac-address	
  ```

当交换机开启DHCP snooping后，所有接口都变成了非信任端口（会拒绝DHCP报文），当把交换机上的某一个接口变为可信任端口，其他端口都会变为可信任端口（会拒绝DHCP offer）
