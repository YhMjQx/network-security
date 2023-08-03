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

### 3.针对于重分发到OSPF自治系统内路由的路径选择（链路类型）

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

###  1.基本概念

- 非纯末梢区域：在此区域内肯定会有一个ASBR路由器，需要在ASBR上配置重分发
- OSPF总计的6中LSA：NSSA区域有哪几种
  - type1
  - type2
  - type3
  - type4
  - type5:E1,E2    没有
  - type7：N1，N2

- 对于不支持NSSA属性的路由器是无法学习到或识别到type7的链路通告的，于是协议规定：在NSSA的ABR上将NSSA内部产生的type7类型的LSA转化为type5类型的LSA再发布出去，并同时更改LSA的发布者为ABR自己，这样NSSA区域外的路由器就可以完全不用支持该属性

- 对LSA的影响
  - type7LSA在一个NSSA区域内携带外部信息
  - type7LSA在NSSA的ABR上被转化为type5LSA
  - 不允许外部LSA
  - 汇总LSA被引入

### 2.配置

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803113300580.png" alt="image-20230803113300580" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803113305226.png" alt="image-20230803113305226" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803115058572.png" alt="image-20230803115058572" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803115130347.png" alt="image-20230803115130347" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803115215626.png" alt="image-20230803115215626" style="zoom:200%;" />

以上是IP地址等等的相关配置

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803121504550.png" alt="image-20230803121504550" style="zoom:200%;" />

这是R3的宣告以及网络区域NSSA的设置

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803122945944.png" alt="image-20230803122945944" style="zoom:200%;" />

这是对R3配置的路由重分发，将NSSA重分发到直连路由中去

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803123925416.png" alt="image-20230803123925416" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803123930872.png" alt="image-20230803123930872" style="zoom:200%;" />

以上两张图说明了NSSA重分发后LSA由type 7 N2转化为type 5 E2，在这里，R1识别到的还是N2的LSA,但是由R1转发出来就变成了E2

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803124152486.png" alt="image-20230803124152486" style="zoom:200%;" />

这张图说的是R3除了直连的网段，就只有一条默认路由，这是为什么呢，因为NSSA属于末梢区域，但末梢区域规定只有一条默认路由作为其区域的出口

## ==三、虚链路==

### 1.概念

- 在两台ABR之间建立一条虚拟链路，穿越一个非骨干区域

### 2.目的

- 指一条通过一个非骨干区域连接到分段的骨干区域的链路

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803130538818.png" alt="image-20230803130538818" style="zoom:200%;" />

### 3.穿越区域的要求

- 虚链路必须配置在两台ABR之间
- 传送区域不能是末梢区域
- 虚链路的稳定性取决于当前穿越区域的稳定性
- 虚链路还可以提供链路冗余

### 4.实验配置

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803140453084.png" alt="image-20230803140453084" style="zoom:200%;" />

将各个设备的IP地址和协议都配置好，先看看此时area2和area0能不能连通，如果可以就说明没有虚链路的事了，但是不能连通的话就需要在R3和R1之间配置一条虚链路

配置好之后我们会发现，R5只有一条直连的10.0.0.0的网段，它虽然有ABR但是因为没有和area 0 相连，所以学习不到其他区域的网络情况，即便是和它相连的area 1 也不行，所以我们必须要配置虚链路

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803141202507.png" alt="image-20230803141202507" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803141207673.png" alt="image-20230803141207673" style="zoom:200%;" />

因为需要再R1和R3之间配置虚链路，所以我们需要再R1和R3上同时配置才可，命令如下：

```shell
en
conf t
router ospf 1
area 1 virtual-link 40.0.0.2
#area 1   这是要穿越的区域的编号
#40.0.0.2 这是虚链路要连接的路由器的router ID 
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803141625890.png" alt="image-20230803141625890" style="zoom:200%;" />

这是R5在配置虚链路之前的路由表，发现除了直连的网段什么都没有

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230803141713314.png" alt="image-20230803141713314" style="zoom:200%;" />

这是R5在配置了虚链路之后的路由表，发现该网络中的任何一个网段现在都可达了