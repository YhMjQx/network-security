# ==UDP协议==

UDP（用户数据报）协议，是传输层的另外一个协议

# 一、简单概念

## 1.概念

- 不需要建立连接，直接发送数据，不会去重新排序，不需要确认

## 2.报文字段

- 源端口
- 目标端口
- UDP长度
- UDP校验和

## 3.常见的UDP端口号

| port | protocol |
| ---- | -------- |
| 53   | DNS      |
| 69   | TFTP     |
| 111  | RPC      |
| 123  | NTP      |
| 161  | SNMP     |

实验：

环境和TCP Flood一样的，只不过攻击的服务不同罢了

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813125133062.png" alt="image-20230813125133062" style="zoom:200%;" />

进入服务器安装DNS服务，安装好之后说明53号端口就打开了



```
hping3 -q -n --rand-source --UDP -p 53 --flood 192.168.2.100 -d10000

#-q 表示使用安静模式
#-n 表示使用数字化输出
#--rand-source  表示随机地址
#--udp  采用UDP模式
#-p  端口号
#--flood  表示快速攻击
#192.168.2.100  服务器IP地址
#-d  表示每次发送数据包的个数
```

然后去抓取这些攻击报文，去检索dns报文

会发现这些dns报文请求的时候并没有携带任何关于域名有关的信息，在DNS内容信息下的Queries中没有任何数据，但正常的dns报文中是一定会有信息的

这是畸形报文：

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813142359705.png" alt="image-20230813142359705" style="zoom:200%;" />

这是正常的报文：

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813142412623.png" alt="image-20230813142412623" style="zoom:200%;" />

为了验证攻击效果，我们可以去创建一个dns 域名和对应的IP，然后用第三台虚拟机去使用该dns服务解析该域名，看看在攻击状态下会不会受到影响

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813143013136.png" alt="image-20230813143013136" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813143024024.png" alt="image-20230813143024024" style="zoom:200%;" />

然后点下一步就好

![image-20230813143110332](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813143110332.png)

然后一直下一步确定就好

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813143200683.png" alt="image-20230813143200683" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813143223049.png" alt="image-20230813143223049" style="zoom:200%;" />

开始测试：

使用四个终端攻击：

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813143342760.png" alt="image-20230813143342760" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230813143439578.png" alt="image-20230813143439578" style="zoom:200%;" />

等一会就会发现，域名解析出问题了，说明攻击见效了

### 综上：

也因此我们可以根据畸形报文的特征，来过滤这一类的报文，此技术就要用到拆包了，在服务器之前加一个专门用来拆包和检包的机器，将畸形这一类的UDP报文全都过滤掉

