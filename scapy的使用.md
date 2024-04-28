[TOC]

scapy解决三个问题：

- 监听流量（wireshark）
- 分析流量
- 编辑流量数据包（链路层，网络层，传输层），应用层也可以编辑，但是意义不大。

# ==scapy的使用==

## 一、命令行交互模式

以管理员身份打开cmd，然后在cmd中输入scapy打开

![image-20240428194224461](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240428194224461.png)

### 1、sniff流量嗅探

```
>>>show_interfaces()  # 查看本机所有网卡

>>>sniff(count=10)  # 基于所有网卡监听10个数据包

>>>sniff(count=10,iface="网卡名")  # 在指定网卡上监听10个数据包

>>>pkg=sniff(count=10,iface="网卡名")  # 将指定网卡上监听到的10个数据包赋值给某个变量

>>>pkg=sniff(count=10,iface="网卡名",filter="icmp")  # 监听指定网卡指定协议类型的数据包

>>>pkg.summary()  # 查看每个数据报的摘要信息

>>>pkg[0]  #展示监听到的数据包中的第一个

>>>pkg[0].show()  #列出监听到的数据包中的第一个

>>>pkg[0][Raw].load  #查看数据包中的具体数据信息
```

### 2、编辑数据包

```
#发送数据包
>>>send(IP(dst="192.168.110.37")/ICMP())  # 发送一个数据包，IP层中目标IP地址为192.168.110.37，ICMP()层表示我使用ICMP协议发送

>>>send(IP(dst="192.168.110.37")/ICMP()/"abcdefghijklmnopqrstuvwabcdefghi")  # 放松一个带有payload的icmp数据包（类似于标准的ping的格式）

>>>pkg=IP(dst="192.168.110.37")/ICMP()/"abcdefghijklmnopqrstuvwabcdefghi"
>>>send(pkg,count=5,inter=1)
# 间隔为1，发送5个icmp数据包


# 发送数据包并接收响应
>>>pkg=sr1(IP(dst="192.168.110.37")/ICMP()/"abcdefghijklmnopqrstuvwabcdefghi")
>>>pkg  # 查看响应
>>>pkg[IP].id  # 获取对应字段的值，[] 中是标签的值， .后面跟的是该标签中所对应的字段的值




# ARP数据包发送
>>>send(ARP(psrc="192.168.110.37",pdst="192.168.230.135"))
或
>>>pkg=sr1(ARP(psrc="192.168.110.37",pdst="192.168.230.135"))
>>>pkg

>>>pkg=sr1(ARP(psrc="192.168.110.37",pdst="192.168.230.135"),timeout=3)  # 如果给一个不存在的IP地址发送数据包，我们可以通过设置超时时间来提高查询效率
#如果可以正确接收到数据包并且可以获得响应及其中的源MAC地址，那么就说明该IP地址是online的
>>>pkg[ARP].hwsrc  # 所需要主机的MAC地址
>>>pkg[ARP].psrc  # 所需主机的IP地址
```

### 3、读写流量文件

```
>>>wrpcap(D:/test.cap,pkg)
>>>pkr=rdcap("D:/test.cap")
>>>pkr
```



## 二、python代码调用