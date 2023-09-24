# ==IPTables进阶用法==

在上节课我们余留了一个问题：别人可以访问我，我不可以访问别人，但要是我这台服务器想要从另一台服务器中获取数据该怎么办。今天我们就来完成这个实验。

首先，通过画图构建思维

![image-20230924111645583](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230924111645583.png)

既然是要我访问别人，那么我首先OUTPUT链中需要一个dport为80的规则，然后INPUT链中需要一个sport为80 的端口，且动作都是ACCEPT

我们思考：我的服务器要想访问别人，那么首先要OUTPUT一个出去的请求，此时 dport 是80，然后别的服务器要返回给我响应，此时对于我来说，这个数据包的 sport 就是80。我们还可以换一个思考方式，我的服务器自身的端口是随机分配的，所以规则不可能是通过配置我自身服务器的端口来实现的

如果遇到 `curl http://101.37.65.91/` 然后CentOS没有任何反应，可能会有以下几种原因 

> 1：太多数据包太快,数据包到打印缓冲区运行已满,并且内核“丢弃”curl发送的数据包,然后tcpdump才有机会将它们打印给您.解决方案是增加缓冲区空间,例如使用–buffer-size = 102400(这会将大约100MB的ram专用于缓冲区,我不确定默认大小是多少,但我认为它在1-4MB)
>
> 2：你有多个网络“接口”,而你正在聆听错误的接口.我不知道如何询问curl它使用哪个界面,但你可以通过curl –interface eth0 URL – 以及在Linux& Mac& BSD,您可以通过执行sudo ifconfig获取可用接口列表(我认为windows等效于某个控制面板,但是idk)
>
> 3：tcpdump的默认用户无法读取用户curl正在运行的数据包因为某些原因…默认情况下tcpdump会在捕获时掉入自己的用户名为tcpdump,你可以尝试从卷曲的同一用户捕获通过使用-Z curluser运行,或强制tcpdump通过执行-Z root以root身份捕获



```
#允许本地访问外部IP地址和端口号,通过设定白名单的方式可以防止本机去访问别的服务器
#通过这种场景的设置，可以最大可能得避免反弹shell和挖矿程序去试图通过本地访问目标服务器下载恶意程序或执行恶意命令
iptables -o ens32 -I OUTPUT -p tcp -d 192.168.112.153 --dport 80 -j ACCEPT
iptables -o ens32 -I OUTPUT -p tcp -d 192.168.112.153 --dport 80 -j ACCEPT

#防止DDOS攻击，设定一些数据的限制条件
iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minite --limit-burst 100 -j ACCEPT

#可以同时设定多个端口允许
iptables -I INPUT -p tcp -m multiport --dport 80,22,443,3306 -j ACCEPT

#端口转发：
#第一种：本地端口转发，比如80端口对外封闭，开放一个7777端口供外部访问，外部只知道7777端口，不知道80端口，可以避免协议猜测
iptables -t nat -A PREROUTING -p tcp --dport 7777 --to-port 80 

#第二种：远程端口转发，把本机接收到的请求转发给远程电脑和对应端口上（远程可以是本地局域网，也可以是网络服务器）
#此时需要确保转发功能是启用的
vi /etc/sysctl.conf
然后添加net.ipv4.ip_forward=1
sysctl -p /etc/sysctl.conf
#PREROUTING上访问8888端口时，转发给目标服务器和目标端口
#PREROUTING是先于FILTER执行的，所以不需要转发时允许8888端口（也就是说PREROUTING的优先级高于FILTER，对PREROUTING的命令配置是不需要经过FILTER规则通过的）

iptables -t nat -A PREROUTING -d 192.168.112.188 -p tcp --dport 7777 -j DNAT --to-destination 101.37.65.91:80
#上面配置的意思是，当有人访问192.168.112.188:7777端口时，就会通过DNAT的模式跳转到101.37.65.91:80（即；将数据报远程出去）

iptables -t nat -A POSTROUTING -d 101.37.65.91 -p -tcp --dport 80 -j SNAT --to 192.168.112.188
#要想可以达到真正跳转的目的，不仅要有请求，还要有回去的响应。我上面将用户的请求转发到101.37.65.91:80，这里就是用户在101.37.65.91:80里面做的请求再路由到192.168.112.118我的这台服务器上 （即：将远程的数据包转发回来）


iptables -t nat -A PREROUTING -p tcp --dport 7777 --to-port 80

iptables -t nat -A PREROUTING -d 192.168.230.147 -p tcp --dport 7777 -j DNAT --to-destination 101.37.65.91:80 

iptables -t nat -POSTROUTING -d 101.37.65.91  -p tcp --dport 80 -j SNAT --to 192.168.230.147
```

这个端口转发的功能可以达到钓鱼网站的做法，我将你访问的

## 四、命令参数表

|                     |                                       |
| ------------------- | ------------------------------------- |
|                     |                                       |
|                     |                                       |
|                     |                                       |
|                     |                                       |
|                     |                                       |
|                     |                                       |
|                     |                                       |
|                     |                                       |
|                     |                                       |
| -p                  | 指定协议                              |
| --dport             | 指定主机端口 (本机开放或拒绝端口)     |
| --sport             | 指定主机端口 (如: 禁止连接对方某端口) |
| -i                  | 指定网卡名，表示报文流入的接口        |
| -o                  | 指定网卡名，表示报文流出的接口        |
| -j                  | 指定所需要的操作                      |
| ACCEPT              | 允许                                  |
| REJECT              | 拒绝，拒绝提供服务                    |
| DROP                | 拒绝，丢弃数据包不回应                |
| --src-range         | 源地址范围， (如: 拒绝某IP段访问)     |
| --dsc-range         | 目惨出颠步版辈豹撑镑地址的范围        |
| --mac-source        | 源主机的mac地址                       |
| -t                  | 指定表名，默认是filter                |
| -v                  | 查看详细信息                          |
| -nvl --line-numbers | 查看fliter表中规则的顺序              |
| -nvl -t mangle      | 查看mangle表中的防火墙规则            |
| -F                  | 清空filter表                          |
| `-I`                | 指定链中插入规则                      |
| -R                  | 替换规则                              |
| -m                  | 指定模块                              |

