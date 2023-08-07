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

## 四、PAT

- 端口多路复用

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230807132614487.png" alt="image-20230807132614487" style="zoom:200%;" />

  - 主要是将内网的多个地址转换为外网的一个IP地址（将端口一起转换，从而进行区分）

    - 有多余外网地址的情况

      ```shell
      en
      conf t
      int g0/0
      ip nat inside
      exit
      int g0/1
      ip nat outside
      access-list 1 permit any
      ip nat pool ymq 23.34.56.80 23.34.56.80 netmask 255.255.255.0
      ip nat inside source list 1 pool ymq overload
      #加上overload的目的是，鞋带端口断专，这就是端口多路复用
      ```

  - 将内网的多个地址直接转换为外网接口地址

    - 没有多余外网地址可以转换（这个时候就直接转换到路由器外网地址接口的IP地址上）

    ```shell
    en
    conf t
    int g0/0
    ip nat inside
    exit
    int g0/1
    ip nat outside
    access-list 1 permit any
    ip nat inside source list 1 int g0/1 overload
    ```

  - 是目前企业中最常用的方式（源地址转换，NAT代理上网）

- 端口映射

  - 主要是将内网中的某一台服务器（服务器上会有对应的服务）映射到外网的某一个IP地址的某一个端口

    - 192.168.1.100:80 --------->23.34.56.78:80
    - 因为内网的端口标识了服务器的服务类型，所以不能更改
    - 映射出去的外网端口可以更改，但会影响外网客户端访问时的端口号，如果映射的外网端口为8088端口，这时外网客户机在访问内网服务器时，访问的是映射出去的IP地址及端口号（8088）（http://23.34.56.78:8088）（也就是说，更改了映射出去的外网端口号，影响的是外网主机访问的时所使用的端口号）

    ```shell
    en
    conf t
    ip nat inside source static 192.168.1.100 80 23.34.56.78 80
    ```

    这个是有点类似于静态转换的，只不过静态转换是没有跟随端口的，而这个映射是跟随端口的

    映射前：

    <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230807135822296.png" alt="image-20230807135822296" style="zoom:200%;" />

    映射后：

    <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230807135841644.png" alt="image-20230807135841644" style="zoom:200%;" />

  - 需要注意的是，在配置的时候外网映射的IP地址的端口号（配置命令中的第二个端口）改变了，那么外网主机在访问的时候需要加上对应的端口号

    <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230807140030821.png" alt="image-20230807140030821" style="zoom:200%;" />

  - 是目前企业中针对内网服务器对外提供服务时使用的最多的方式（目的地址转换）

**总结：**

- 静态转换
  - 1对1转换    1个内网地址转换为1个外网地址，形成永久性的对应关系，可以根据外网地址直接定位到内网地址，可以实现内网访问外网，也可以实现外网访问内网
- 动态转换
  - 多对多转换    内网多个IP地址转换为外网多个IP地址，当内网主机数多余外网IP地址个数时，无法实现内网所有主机同时上网，由于是动态的对应关系，所以无法根据外网地址定位内网地址，只能实现内网访问外网
- 端口多路复用
  - 多对1转换（源地址转换，NAT代理上网）    内网多个IP地址转换为外网一个IP地址（外网接口IP地址），使用不同端口号进行区分，行成的是动态的对应关系，只能实现内网访问外网
- 端口映射（服务器映射）目的地址转换
  - 主要是将内网中某一台服务器（服务器上对应的有服务）映射到外网的某一个IP地址的某一个端口上
  - 形成的是一个永久性的对应关系，但只能实现外网访问内网，无法实现内网访问外网

