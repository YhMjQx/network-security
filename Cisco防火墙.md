# ==Cisco防火墙==

ASA系列

1.防火墙工作原理（状态化防火墙）

2.在防火墙上配置ACL（基本都是命名的ACL）

3.在防火墙上配置NAT（防火墙设备一般放在局域网出口）

## 一、工作原理

### 1、系列

ASA5500系列

### 2.ASA防火墙状态化防火墙

- 里面维护了一张表：状态化链接表（conn表）。数据出去的时候是这些信息，回来的时候也还得是这些信息才可以放通
  - 源IP地址
  - 目标IP地址
  - IP协议（TCP/IP）
  - IP协议信息（端口号，序列号，控制位）
- 默认情况下，ASA对 TCP UDP 协议提供状态化链接（一台设备通过防火墙去访问另一台设备的TCP UDP的时候，回来的报文是可以通过防火墙的），对ICMP协议是非状态化的（例如采用的是ping命令，回来的报文是无法通过防火墙的）

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230902120709579.png" alt="image-20230902120709579" style="zoom:200%;" />

- 状态化防火墙的处理过程

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230902122528552.png" alt="image-20230902122528552" style="zoom:200%;" />

- ASA的安全算法
  - 接口安全级别
  - 访问控制列表
  - 记录conn表
  - 连接表
  - 检测引擎（根据接口安全级别来决定数据室放通还是阻止）
    - 默认情况下，ASA自动放通高安全级别访问低安全级别，阻止低安全级别访问高安全级别，安全级别一致，直接阻止

## 二、ASA接口

### 1.物理接口

- 基于防火墙自身模块来决定

### 2.逻辑接口

- 用来描述物理接口所处的安全区域（inside（内网区域），outside（外网区域），DMZ（服务器区域））
  - inside：安全级别设置为100
  - outside：安全级别设置为0
  - DMZ：安全级别设置为50

实验情况

ASA配置

```shell
ciscoasa(config)#int g1
ciscoasa(config-if)#name if inside
ciscoasa(config-if)#security-level 100
ciscoasa(config-if)#ip add 192.168.1.254 255.255.255.0
ciscoasa(config-if)#no shut

ciscoasa(config)#int g2
ciscoasa(config-if)#name if DMZ
ciscoasa(config-if)#security-level 50
ciscoasa(config-if)#ip add 192.168.2.254 255.255.255.0
ciscoasa(config-if)#no shut

ciscoasa(config)#int g3
ciscoasa(config-if)#name if outside
ciscoasa(config-if)#security-level 0
ciscoasa(config-if)#ip add 23.34.45.56 255.255.255.0
ciscoasa(config-if)#no shut
```

主机配置：

```shell
LAN_PC1
en
conf t
no ip routing
int f0/0
ip add 192.168.1.10 255.255.255.0
no shut
exit
line vty 0 4
password 123
loggin
exit
enable password 111
ip default-gateway 192.168.1.254


```

服务器配置：

```shell
DMZ_server
conf t
int f0/0
ip add 192.18.2.10 255.255.255.0 
no shut
exit
ip default-gateway 192.168.2.254
no ip routing
exit
telnet 192.168.1.10    //尝试对LAN_PC1 telnet


```

## 三、ASA配置ACL

### 1.标准

### 2.扩展

不管是标准还是扩展，使用的是ACL表名的方式

在ASA上配置ACL

```
conf t
access-list dmz_to_in permit icmp host 192.168.2.10 host 192.168.1.10
//允许dmz的ICMP流量从dmz进入防火墙
access-group dmz_to_in in interface DMZ
//将上面的配置运用到防火墙上与dmz相连的接口上

access-list dmz_to_in permit tcp host 192.168.2.10 host 192.168.1.10 eq 23

```

