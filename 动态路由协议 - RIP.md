# ==动态路由协议==

- 静态路由
  - 单向，管理员手动配置
- 动态路由
  - 是在路由器设备上启用某动态路由协议，把自己直连的网段宣告，从而相邻的路由器就可以学习到相邻路由器所宣告的网段
  - 常见动态路由协议
    - RIP：路由信息协议（距离矢量路由协议）
    -  OSPF：开放式最短路径优先（内部网关协议）
    - IS-IS：中间系统到中间系统
    - BGP：边界网关协议
    - EIGRP：增强内部网关路由协议
  - 特点
    - 减少管理员的工作量
    - 增加了网络的带宽
  - 什么是内部，什么是边界
    - AS（自治系统）：运行相同路由协议的路由器属于同一个自治系统（内部网关）
    - 通过自治系统内连接外部的路由器，这个时候就需要有外部网关
    - 内部网关路由协议（IGP）：用于在单一自治系统中去决策路由的，RIP，OSPF
    - 外部网关路由协议（EGP）：用于连接不同自治系统，BGP
  - 动态路由协议需要考虑的内容
    - 度量值：跳数，带宽，负载，时延，成本......
    - 收敛：是所有路由器的路由条目都达到一致的状态（就是宣告和学习个过程最后的结果）
    - 自治系统

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230729134113500.png" alt="image-20230729134113500" style="zoom:200%;" />

## RIP动态路由协议

### 1.基本概念

- 一种内部网关协议，在单一自治系统内的路由器去传递路由信息
- 靠跳数（metric）来衡量到达目的地的距离
  - 最大15跳，16跳表示不可达
- 每隔30秒向相邻的路由器发送路由更新消息，采用的UDP520端口
- RIP动态路由协议是从相邻的路由器去学习对应的路由条目

### 2.RIP的版本

- RIPv1
  - 有类路由协议（采用标准子网掩码 - 对应5种IP地址）
  - 广播更新
  - 不支持VLSM（可变长子网掩码，非标准子网掩码）
  - 自动路由汇总，不可关闭
  - 不支持不连续子网
- RIPv2
  - 无类路由协议（可以适用非标准子网掩码）
  - 组播更新（只会向运行了RIP的路由器发送更新消息）
  - 支持VLSM
  - 自动汇总，可以关闭
  - 支持不连续的子网掩码

### 3.配置

- RIPv1

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230729154331517.png" alt="image-20230729154331517" style="zoom:200%;" />

注意：![image-20230729154428567](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230729154428567.png)

对路由器来说，这三个一定要配置好

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230729154526016.png" alt="image-20230729154526016" style="zoom:200%;" />

由于没有配置DHCP服务，所以这三个点一定要配置好，尤其是默认网关也要配置，不然ping不通的

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230729160235442.png" alt="image-20230729160235442" style="zoom:200%;" />

- RIPv2

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230729155759949.png" alt="image-20230729155759949" style="zoom:200%;" />

配置和上面差不多，不过有几个要注意的点

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230729160128950.png" alt="image-20230729160128950" style="zoom:200%;" />

不是一定要关闭自动汇总，不关闭一样的

RIPv1和RIPv2共有的配置

```shell
Route(config)#router rip
#开启RIP路由协议

Router(config-router)#network 192.168.10.0
#对相邻的路由器宣告自己的直连网段
```

RIPv2特有的

```shell
Router(config-router)#version 2
#因为默认是RIPv1版本，此命令提示使用RIPv2版本

Router(config-router)#no auto-summary
#关闭自动汇总
```

