# ==Windows防火墙==

1.了解防火墙基本内容

2.掌握Windows图形化界面的防火墙操作

3.掌握Windows命令界面防火墙操作

## 一、基本内容

### 1.防火墙

- 防火墙技术主要是通过有机结合各类用于安全管理与筛选的软件或硬件设备，体现形式采用规则的方式，从而去帮助计算机网络与其内，外网之间构造一条相抵隔绝的保护屏障
- 一般情况下将防火墙放在区域的边界，从而保护区域的安全性

网络分为5个大区

- 内网接入区
- 外网接入区
- 服务器区
- 运维管理区
- 核心区

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830192903520.png" alt="image-20230830192903520" style="zoom:200%;" />

### 2.分类

- 物理特性分类
  - 软件防火墙（Windows defender    Linux iptables    Linux firewalld）
  - 硬件防火墙（Cisco ASA    华为USG    启明星辰（天清汉马）    深信服（AF）   安恒（明御安全网关））
- 性能划分：百兆级，千兆级等等
- 结构划分：单一主机，路由集成，分布式
- 技术划分：包过滤，应用代理，状态监测

### 3.防火墙功能

- 访问控制
- 地址转换
- 网络环境支持（DHCP，vlan，动态路由....）
- 带宽管理（Qos，服务访问质量（流量管理）：主要目的针对不同的业务分配对应的带宽，从而保障关键性业务带宽）
- 入侵防御（入侵检测和防御）
- 用户认证
- 高可用（VRRP/HA）

### 4.防火墙策略

本质是控制和防护，主要工作原理通过设置安全策略进行安全防护

例如：虚拟机开启防火墙之后，物理机ping虚拟机ping不通，但是虚拟机ping物理机就可以ping通。防火墙将物理机的ICMP协议拒绝掉，所以是请求超时（流量过去了但是回不来），而不是目标主机不可达

- 定义：按照一定的规则，对流量进行检测的策略，包过滤（第三层和第四层的流量，基于数据包的五元组）
- 应用：对跨防火墙的互联网络进行控制，对本身的访问控制

## 二、防火墙发展

### 1.包过滤防火墙

- 判断信息：五元组

- 工作范围：3-4层

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830205416471.png" alt="image-20230830205416471" style="zoom:200%;" />

### 2.应用代理

- 判断信息：应用层数据（HTTP  ftp ......）
- 工作范围：应用层（7层）

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830210219130.png" alt="image-20230830210219130" style="zoom:200%;" />

### 3.状态监测

- 判断信息：IP地址，端口号，TCP标记
- 工作范围：2-4层

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830204852525.png" alt="image-20230830204852525" style="zoom:200%;" />

### 4.web应用防火墙（WAF）

- 判断信息：http协议数据（request（请求）和responds（响应））
- 工作范围：应用层（7层）

### 5.多合一网关

- FW（防火墙），IDS（入侵检测），IPS（入侵防御），AV（防病毒（工作在7层））
- 工作范围：2-7层
- 串行机制

### 6.下一代防火墙（NGFW）

- FW（防火墙），IDS（入侵检测），IPS（入侵防御），AV（防病毒（工作在7层）），WAF

- 工作范围：应用层（7层）
- NGFW是并行处理机制， 会更高效

## 三、Windows defender防火墙

```
ping 192.168.230.150 -S 192.168.233.1
#指定用192.168.233.1来使用ICMPv4协议ping192.168.233.150
```

![image-20230831204443273](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230831204443273.png)

```shell
netsh advfirewall firewall show rule name = all
#查看所有规则
netsh advfirewall firewall show rule name = permitTCMP
```

![image-20230831204727714](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230831204727714.png)

```shell
netsh advfirewall set allprofiles state off/on
#关闭/打开防火墙
netsh advfirewall reset
```

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230831205329115.png" alt="image-20230831205329115" style="zoom:200%;" />

```shell
netsh advfirewall set currentprofile loggin filename "C:\tmp\pfilewall.log"
#将防火墙的日志文件粗放在指定路径
```

```shell
netsh advfirewall firewall add rule name="permitICMP(In)" dir=in remoteip=192.168.233.1 protocol=icmpv4 action=allow
#创建一个允许远程IP为192.168.233.1，使用ICMP协议进站的规则，dir表示方向
```

```shell
netsh advfirewall firewall add rule name="deny233.1(in80)" dir=in remoteip=192.168.233.1 protocol=tcp localport=80 action=block
#阻止客户机访问我的80端口
```

```shell
netsh advfirewall firewall set rule name="远程桌面 - 用户模式(TCP-In)" new enable=yes
#开始防火墙的远程桌面访问权限
net start "remote desktop services"
#开启远程桌面的服务
#要想开启远程服务就必须要开启这两个，也可以直接在计算机管理中开启
```

