# ==OSPF高级配置==

1.路由重分发

2.NSSA区域

3.虚链路

## ==一、路由重分发==

### 1.需要重分发的路由

- OSPF重分发RIP，静态路由，默认路由，直连路由

### 2.基本概念

- 一个单一IP路由协议是管理网络中IP路由的首选方案
- 在大型企业中，可能在同一网内使用到多种路由协议，为了实现多种路由协议协同工作，路由器可以适用路由重分发（route redistribution）将其学习到的一种路由协议的路由通过另一种路由协议广播出去，这样网络的所有部分都可以连通了。为了实现重分发，路由器必须同时运行多种路由协议，这样，每种路由协议才可以获取路由表中的所有或部分其他协议的路由来进行广播

### 3.针对于重分发到OSPF自治系统内路由的路径选择

- 类型1：E1，内部代价加上外部代价（cost）
- 类型2：E2，只考虑外部代价（cost）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230801161623598.png" alt="image-20230801161623598" style="zoom:200%;" />

### 4.实验+配置

这个实验有点难，先想清楚为什么要重分发，是因为**在不同区域中，可能运行的是不同的路由协议，而网段的宣告，只有运行了相同路由协议的设备才可以学习得到，因此我们就需要实现路由协议重分发，这样才可以让运行着不同协议的设备实现相互学习**

重分发的实验：ospf，rip，静态路由的配合

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230802132649192.png" alt="image-20230802132649192" style="zoom:200%;" />

- OSPF重分发静态路由配置实例

  - 例如R3上的配置，将R3上的ip等等以及协议宣告等等配置好了之后在配置这句命令就好了，目的是让静态路由区域中的设备学习到OSPF中的设备

  ```shell
  router ospf 1#在该环境下
  	redistribute static metric 100 subnets metric-type 2
  ```

- OSPF重分发默认路由配置实例

  - 就比如说这里的R1，和上面一样，现将各种配置完成，比如ip，协议，宣告等等然后再配置这个，目的是让默认路由区域的设备可以学习到OSPF中的设备

  ```shell
  router ospf 1
  	default-information originate
  ```

- OSPF重分发到RIP

  - 如图中的R2，**让RIP中的设备学习到OSPF种的设备**

  ```shell
  router ospf 1
  	redistribute rip metric 200 subnets
  ```

- RIP重分发到OSPF

  - 因为在R2上，既运行了OSPF又运行了RIP，因此还需要**让OSPF中的设备也可以学习到RIP中的设备**

  ```shell
  router rip
  	redistribute ospf 1 metric 10
  ```

  - 此外，还需要注意的是，此时是将RIP充分发给OSPF，但那是RIP的度量值是有限的，最大是16，而且16已经是不可达了，但是图中说明R2的左边只有3个路由器，所以这里的度量值写的是10

metric后面跟的是度量值

subnets表示携带子网掩码

## ==二、NSSA区域==