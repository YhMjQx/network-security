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
  - 区域中的其他路由器智慧和DR和BDR建立邻接关系
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



​	