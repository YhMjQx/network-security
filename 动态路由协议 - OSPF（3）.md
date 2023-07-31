回顾：

1.动态路由

- 原则的方式，向相邻路由器发送对应的协议报文，从而使相邻路由器学习到对应的路由条目
- RIP：发送的是自己的整个路由表
- IS-IS：
- BGP：
- EIGRP：
- cost值：度量值，RIP的度量值是跳数，最大15跳，16跳表示不可达（水平分割）

# ==动态路由协议 - OSPF==

## 一、基本概念

1.OSPF开放式最短路径优先路由协议，是一个内部网关路由协议（在同一个自治系统内进行路由决策）

2.链路状态路由协议：在单一区域内的路由器是向相邻的路由器发送链路状态信息，网络收敛后形成网络拓扑

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230730102444217.png" alt="image-20230730102444217" style="zoom:200%;" />

旁边那些小的三叉的就是链路状态信息

3.工作过程

- 相邻的路由器首先建立**邻接关系**

- 根据链路状态信息，形成对应链路**状态数据库**

-   根据OSPF自己的算法，进行**最短路径树**

- 最终形成**路由表**

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230730104146967.png" alt="image-20230730104146967" style="zoom:200%;" />

## 二、OSPF的区域

### 1.划分区域

- 为了适应大型网络
- 每个OSPF的路由器只维护自己所在区域的链路状态信息（因此处于不同区域的路由器，即便相连，也不能同步链路状态信息）
- 每个区域都有一个区域ID
  - 区域ID可以表示成一个十进制的数
  - 也可以表示成一个IP地址
- 骨干区域
  - 主要负责区域与区域之间的路由信息传播
  - 区域ID：0 或 0.0.0.0
- 非骨干区域
  - 普通区域
- 默认情况下所有的非骨干区域都和骨干区域直连

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230730152320779.png" alt="image-20230730152320779" style="zoom:200%;" />

### 2.单区域

- 在同一区域当中，通过选举DR和BDR来节省网络中的流量
  - 区域中的其他路由器只会和DR和BDR建立邻接关系
- DR和BDR的选举
  - 通过route ID进行选举，route ID最大的最为DR，第二大的作为BDR
  - route ID
    - 首先选取路由器loopback上数值最高的地址
      - loopback是路由器上的虚拟接口（相当于多了一个虚拟的网段），该接口是可以进行收发路由协议报文，也可以配置IP
    - 如果loopback上没有配置地址，选取物理接口上最大的IP地址
    - 也可以直接使用命令 `route-id`直接指定

### 3.OSPF的度量值

- cost值
  - 基于链路带宽来决定
    - 100Mbps   -    1
    - 10Mbps    -   10

### 4.邻接关系建立

- 以什么方式去发送数据报文来建立邻接关系
  - 以组播方式发送
    - 224.0.0.5     代表所有OSPF路由器
      - 在没有选举出DR和BDR之前，会发送报文用来选举，此时的报文用的就是224.0.0.5
    - 224.0.0.6     代表DR、BDR
      - 选举出DR和BDR之后，就要开始同步链路信息，此时所用的就是224.0.0.6
- 报文类型
  - Hello报文：用于发现和维持邻接关系，用于选举DR和BDR
  - 数据库描述包（DBD）：项邻接发送自己的链路状态描述信息用来同步链路状态数据库
  - 链路状态请求包（LSR）：
  - 链路状态更新包（LSU）：
  - 链路状态确认包（LSAck）：

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230730164157974.png" alt="image-20230730164157974" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230730164712687.png" alt="image-20230730164712687" style="zoom:200%;" />

### 5.OSPF和RIP对比

#### RIP：RIPv1和RIPv2

- RIPv1：不支持可变长子网掩码使用广播更新
- RIPv2：使用组播更新
- 二者跳数都是15跳
- 不能划分区域，网络收敛慢
- 宣告时都不携带子网掩码

#### OSPF

- 使用组播更新
- 网络收敛快，通过区域划分
- 支持可变长子网掩码，主要体现在宣告时携带子网掩码

## ==OSPF单区域配置==

实验：

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230731105134179.png" alt="image-20230731105134179" style="zoom:200%;" />

这里R1和R3都是DR，因为R1和R3并没有互联，而且是分别连在R2左右两边，所以相对于R2的左边R1是DR，相对于R2的右边R3是DR

![image-20230731105053642](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230731105053642.png)

​	<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230731105101442.png" alt="image-20230731105101442" style="zoom:200%;" />

![image-20230731105108147](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230731105108147.png)

![image-20230731105111657](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230731105111657.png)

![image-20230731105115557](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230731105115557.png)

以上是对主机和路由器的基本配置

以下是对路由器OSPF协议的配置

```shell
en
conf t
router ospf 10  #10代表OSPF进程
network 10.0.0.0 0.0.0.3 area 0
#10.0.0.0  这是宣告出去的网段
#0.0.0.3   子网掩码的反码（用4个255减掉对应的）
#area 0    表示宣告的区域（位于哪个区域）
```

`show ip ospf `#查看ospf的配置信息

`show ip toute`#查看路由条目

## ==OSPF多区域==

### 一、多区域概念

##### 1.目的

- 实现大型网络环境
- 划分区域后，实现单区域网络收敛

##### 2.好处

- 改善网络，更具有扩展性
- 快速网络收敛
- 减少了路由表，也减少了LSU的流量

##### 3.OSPF的通信流量

- 在区域内（域内通信量）
  - DR和BDR
  - 内部路由器
- 不同区域之间（域间通信量）
  - ABR（区域边界路由器）
- 与其他自治系统之间（外部通信量）
  - ASBR（自治系统边界路由器）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230731124741017.png" alt="image-20230731124741017" style="zoom:200%;" />

##### 4.区域

- 骨干区域
  - area 0
- 非骨干区域
  - 标准区域
  - 末梢区域
  - 完全末梢
  - 非纯末梢

##### 5.链路状态通告（LSA）

- 6种链路状态通告
  - 类型1：**路由器LSA，由区域内的路由器发出**（内部路由器，普通路由器发送给DR和BDR的链路状态）
  - 类型2：**网络LSA，由区域内的DR发出**（发给区域内的其他路由器）
  - 类型3：**网络汇总LSA，由ABR发出**（非骨干区域中的汇总好了之后交由ABR发给骨干区域）
  - 类型4：**ASBR汇总LSA，由ABR发出**（因为ASBR需要汇总ospf区域中其他区域的链路状态，而不同小的区域信息又是由ABR发出的）
  - 类型5：**AS外部LSA，由ASBR发出**（新的OSPF区域整个汇总好了之后交由ASBR发送给另一个OSPF区域）
  - 类型6：**非纯末梢区域的外部LSA**（仅限飞准末梢区域的类型5）

实验：

第一个实验是一个多区域配置问题，就是针对不同区域的接口等等进行不同的配置和宣告，但是所有的ospf进程都是一样的

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230731145425154.png" alt="image-20230731145425154" style="zoom:200%;" />

第二个实验针对的是，不同区域同样形成负载的效果

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230731150643925.png" alt="image-20230731150643925" style="zoom:200%;" />

##### 6.末梢区域

- 只有一个默认路由作为其区域的出口

- 区域不能作为虚链路的穿越区域