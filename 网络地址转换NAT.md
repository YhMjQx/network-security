# ==网络地址转换NAT==

NAT：Network Address Translation

**1.静态转换**

**2.动态转换**

**3.端口被多路复用PAT**

**4.端口映射（服务器映射）**

## 一、NAT基本概念

在IPv4的网络环境中，由于网络分为私网和公网，死亡的地址无法在网上进行路由检测

### 1.目的

- 将私网的地址转化为公网地址

### 2.出现背景

- IP地址不够用

### 3.转换方式

- 静态转换   仅进行IP地址转化    1对1转
- 动态转换   仅进行IP地址转化     多对多转   内网的一部分转换为外网的一部分
  - 内网地址  多余  外网地址    eg：5  多余  3
  - 外网地址  多余  内网地址
- 端口多路复用PAT  多（内网）对一（外网）转
  - 192.168.1.1:8899  ------>  64.23.54.99:6677
  - 192.168.2.1:2277  ------>  64.23.54.99:886
- 端口映射（服务器映射）
  - 将一台内网的服务器发布到外网，从而使外网的主机可以访问到内网的服务器
  - 192.168.1.1:80 --------> 64.23.54.99:80
  - 目的地址转换

注意：除了静态转换可以直接配置，其他的转换都需要配置值ACL

### 4.转换表中的4类地址

- 内部局部地址：发送方内网
- 内部全局地址：发送方外网
- 外部局部地址：接收方内网
- 外部全局地址：接收方外网

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230806192821299.png" alt="image-20230806192821299" style="zoom:200%;" />

192.168.1.1访问23.34.45.56，现将数据通过交换机交给自己的路由器进行处理，路由器会用配置好的转换表进行查看是否要将192.168.1.1转换为23.34.45.100，然后再转发数据。而23.34.45.56认为是23.34.45.100在访问自己，于是只会将回应报文发送给路由器然后由路由器在进行转发

## 二、静态转换实验

固定  1 ------》 1  转     192.168.10.10 ------》23.34.56.100

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230806194059076.png" alt="image-20230806194059076" style="zoom:200%;" />

- 为了验证通过转换使得PC0可以访问PC2，我们就不要设置PC2的网关，因为如果PC2有网关，那么PC0访问PC2就是通过路由实现的了，就用不着转换了

- 然后指定出口路由器内外网接口

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230806194614164.png" alt="image-20230806194614164" style="zoom:200%;" />

  ```shell
  en
  conf t
  int g0/0
  ip nat inside
  exit
  int g0/1
  ip nat outside
  ```

  

- 配置静态转换表

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230806194944049.png" alt="image-20230806194944049" style="zoom:200%;" />

```shell
en
conf t
ip nat inside source static 192.168.10.10 23.34.56.100
#静态转换将内网源为192.168.10.10的IP转换为23.34.56.100
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230806195557706.png" alt="image-20230806195557706" style="zoom:200%;" />

此时PC0可以ping通PC2，但PC1ping不通

## 三、动态转换实验

- 动态的  多对多  范围对范围

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230806203802478.png" alt="image-20230806203802478" style="zoom:200%;" />

- 命令

  ```shell
  #1.定义内网范围，使用ACL来定义允许的范围
  en 
  conf t
  access-list 1 permit 192.168.10.0 0.0.0.255
  #2.定义外网范围，使用名称指定范围IP
  en
  conf t
  ip nat pool ymq 23.34.56.70 23.34.56.71 netmask 255.255.255.0
  #3.应用
  en
  conf t
  ip nat inside source list 1 pool ymq
  #list 1     内网的范围
  #pool ymq   外网的范围
  ```

清除所有转换表

```shell
en
clear ip nat translations *
```

注意：由于上面外网范围ymq只给了23.34.56.70和23.34.56.71，所以这里只能容纳两台主机同时上线，故实验中必有一台主机下线，那么要想使用，就需要先清除转换表，然后再使用