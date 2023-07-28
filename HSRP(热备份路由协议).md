# ==HSRP(热备份路由协议)==

热备：两台路由器都是打开状态

冷备：买了一台设备但不用，等另一台设备坏掉了，再让新的这台设备工作，这个新的设备就是冷备

## 目标

1. 了解HSRP的相关概念
2. 理解HSRP的工作原理
3. 会配置HSRP
4. 由于HSRP是思科设备私有的协议，针对此协议有一个标准的协议VRRP（虚拟路由器冗余协议）

**冗余：备份                                       负载：分摊工作**

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230728112525788.png" alt="image-20230728112525788" style="zoom:200%;" />

## 一、HSRP的概念

### 1.HSRP组中的成员

- 活跃路由器：承担网络中数据包的传输
- 备份路由器：监听网络传输并不断确认活跃路由器是否还良好，一旦活跃路由器挂掉了，备份路由器就要上线了
- 虚拟路由器：作为PC的网关，需要MAC地址
- 其他路由器

### 2.虚拟路由器的MAC地址

-  由48位二进制组成，前面24位是厂商编码，后面24位是序列号
- 后面24位：虚拟MAC地址的固定值（07AC）加上HSRP组号（由16进制的两位表示）

### 3.HSRP消息

- 采用UDP协议，端口号1985
- 采用的是组播方式，组播地址224.0.0.2

- 生命周期 TTL=1

## 二、具体工作过程

如下图所示，主机想要访问172.16.3.127，发现不是同一网络，会将数据交给自己的网关，在这里，主机配置的网关为HSRP组中的虚拟路由器，虚拟路由器接收到数据后，根据HSRP组中的机制（组中路由器的优先级来决定谁是活跃路由器，谁是备份路由器），将数据交给活跃路由器进行转发，活跃路由器再根据自身路由表进行转发数据

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230728125211158.png" alt="image-20230728125211158" style="zoom:200%;" />

后面的配置

- 设置组号（用来决定虚拟路由器的MAC地址）
- 优先级（用来确定活跃路由器，优先级高的为活跃）
- 占先（网络中已经存在活跃路由器后，当一个新的且优先级更高的路由器想要进入网络并成为活跃路由器，就需要配置占先）
- 端口跟踪

## 三、HSRP状态与计时器

### 1.状态

- 初始状态
- 学习状态：该组员未设定虚拟IP地址，并等待从本组活跃路由器发出的认证的Hello报文中学习得到自己的虚拟IP地址
- 监听状态：该组员已得知或设置了虚拟IP地址，通过监听Hello报文监视活跃/备份路由器，一旦发现活跃/备份路由器长时间未发送Hello报文，则进入发言（Speak）状态，考试竞选
- 发言状态：加竞选活动/备份路由器的组员所处的状态，通过发送 Hello 报文使竞选者间相互比较、竞争
- 备份状态：组内备份路由器所处的状态，备份组员监视活动路由器，准备随时在活动路由器坏掉时接营活动路由器。备份路由器也周
  期性发送 Hello 报文告诉其他组员自己没有坏掉
- 活跃状态：组内活动路由器即负责虚拟路由器实际路由工作的组员所处的状态。活动路由器周期性发送 Helo 报文告诉其他组员自己没有坏掉

### 2.计时器

- Hello报文的间隔时间（3秒）
- 保持时间（10秒，如果10秒后还没有收到Hello报文，就说明某一台路由器挂掉了）

## 四、配置

1.配置虚拟路由器IP（单vlan）

```
Switch(config-if)#standby 33 ip 192.168.10.250
#33 - 是组号
#192.168.10.250 - 是虚拟路由器IP

Switch(config-if)#standby 33 priority 200
#200 - 是优先级

Switch(config-if)#standby 33 preempt
#33 - 是组号
#设置占先
```

2.使用HSRP和STP（PVSTP+）实现冗余和负载（多生成树）

实验：

1.可以实现活跃路由器转换

2.端口跟踪

3.负载均衡（靠中间的那条线路）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230728191141120.png" alt="image-20230728191141120" style="zoom:200%;" />

配置：

```shell
二层交换机配置
en
conf t
vlan 10
vlan 20
exit
int f0/1
sw acc vlan 10
exit
int f0/2
sw acc vlan 20
exit
int f0/9-10
sw mo trunk
exit

外部路由器
en
conf t 
int g0/0
ip add 10.10.10.2 255.255.255.0
no shut
exit
int g0/1
ip add 20.20.20.2 255.255.255.0
no shut
exit
int g0/2 
ip add 172.16.10.254 255.255.255.0
no shut
exit
ip route 0.0.0.0 0.0.0.0 10.10.10.1
ip route 0.0.0.0 0.0.0.0 20.20.20.1
#这两条路由是给PC2配的

三层交换机0的配置
en
conf t
vlan 10
vlan 20
exit
int f0/9
sw mo trunk
exit
int f0/24
sw tr enca dot1Q
sw mo trunk
exit
int vlan 10
ip add 192.168.10.254 255.255.255.0
no shut
exit
int valn 20
ip add 192.168.20.254 255.255.255.0
no shut
exit
int f0/23
no switchport
ip add 10.10.10.1 255.255.255.0
no shut
exit
spanning-tree vlan 10 priority 4096
int vlan 10
standby 10 192.168.10.250
standby 10 priority 150
standby 10 preempt
standby 10 track f0/23
exit
int vlan 20 
standby 20 192.168.20.250
standby 20 priority 145
standby 20 preempt
exit
ip route 172.16.10.0 255.255.255.0 10.10.10.2
#活跃路由器配置占先的目的是：当路由器坏掉了，重新搬回来时可以占先
#备份路由器配置占先的目的是：活跃路由器优先级降低了（因为有跟踪端口，当端口不工作了，这个路由器的优先级会降低10），备份路由器可以变为活跃路由器


三层交换机1的配置
en 
conf t
vlan 10
vlan 20
exit
int f0/10
sw mo trunk 
exit
int f0/24
sw tr enca dot1Q
sw mo trunk 
exit
int vlan 10
ip add 192.168.10.253 255.255.255.0
no shut
exit
int vlan 20
ip add 192.168.20.253 255.255.255.0
no shut
exit
int f0/23
no switchport
ip add 20.20.20.1 255.255.255.0
no shut
exit
spanning-tree vlan 20 priority 4096
int vlan 10
standby 10 192.168.10.250
standby 10 priority 145
standby 10 preempt
int vlan 20
standby 20 192.168.20.250
standby 20 priority 150
standby 20 preempt
standby 20 track f0/23
exit
ip route 172.16.10.0 255.255.255.0 20.20.20.2

```

