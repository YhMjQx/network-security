# ==ARP协议（地址解析协议）==

## 一、ARP协议

将一个已知的IP地址解析为MAC地址，从而进行二层数据交互

是一个三层的协议，但是工作在二层，是一个2.5层协议

## 二、工作流程

### 1.两个阶段

- ARP请求
- ARP响应

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230809115849059.png" alt="image-20230809115849059" style="zoom:200%;" />

用两台虚拟机ping一下（要在同一网段，没有网关）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230809120913860.png" alt="image-20230809120913860" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230809121203156.png" alt="image-20230809121203156" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230809121442635.png" alt="image-20230809121442635" style="zoom:200%;" />

### 2.ARP协议报文（分组）格式

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230809124821986.png" alt="image-20230809124821986" style="zoom:200%;" />

### 3.ARP缓存

- 主要目的是为了避免重复发送ARP请求
- 在Windows操作系统中使用ARP命令
  - arp -a    显示ARP缓存表
  - arp -d    删除ARP缓存表

在GNS3中（但老师说的是cisco设备上）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230809125914446.png" alt="image-20230809125914446" style="zoom:200%;" />

`show arp`    查看缓存表

`arp ip amc arpa`    绑定目标IP和对应的MAC

## 三、ARP攻击和欺骗

### 1.ARP攻击

- 伪造ARP响应报文，向被攻击主机响应虚假的MAC地址
- 当被攻击主机进行网络通信时，会将数据交给虚假的MAC地址进行转发，由于虚假的MAC地址不存在，所以造成被攻击主机无法访问网络

### 2.ARP欺骗

可以进行ARP绑定防止

- #### **欺骗网关**

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230809131641032.png" alt="image-20230809131641032" style="zoom:200%;" />



伪造ARP应答报文，向被攻击主机和网关响应真实地MAC地址

当被攻击主机进行网络通信时，会将数据交给真实的MAC地址进行转发，从而来截获被攻击主机的数据，这时，被攻击主机还是可以通信的	

- #### **欺骗主机**

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230809132043428.png" alt="image-20230809132043428" style="zoom:200%;" />

伪造ARP应答报文，向被攻击主机和与之通信的主机响应真实地MAC地址

当被攻击主机向与之通信的主机发送数据时，会将数据交给真实的MAC地址进行转发，从而来截获被攻击主机的数据，这时，被攻击主机还是可以通信的	

