# ==Firewalld基础应用==

Linux 防火墙是通过 netfilter 来处理的，它是内核级别的框架，iptables 被作为 netfilter 的用户态抽象层，iptables 将包通过一系列的规则进行检查，如果包与特定的 IP/端口/协议 的组合匹配，规则就会被应用到这个包上，以决定包是被通过、拒绝或丢弃。firewalld 是最新的 netiter 用户态种象层。firewald 可以通过定义的源IP 和/网络接口将入站流量分考到不同区zone每个区基于指定的准则按自己配置去通过或拒绝包，另外的改进是基于 iptables 进行语法简化。firewalld 通过使用服务名而不是它的端口和协议去指定服务，使它更易于使用，例如，是使用 samba 而不是使用 UDP 端口 137和138 和TCP 端口 139 和 445、它进一步简化语法，消除了 iptables中对语句顺序的依赖。

## 一、Firewalld的基本使用

```
启动：systemctl start firewalld
查看状态：systemctl status firewalld
停止：systemctl disable firewalld
禁用：systemctl stop firewalld
重启：systemctl restart firewalld 
```

### IPTables的功能总结

```
1.常用的两张表：filter，nat。filter用于过滤数据包，nat用于路由转发功能
2.常用的两条链INPUT,OUTPUT
3.常见的三个行为：ACCEPT,DROP,REJECT
4.限制流量的三个特征：端口，协议，IP，对应的五元组： -d   -s   --dport    --sport    -p
5.端口转发：本机端口，远程端口

而firewalld中，没有表，没有链，没有行为，默认拒绝所有流量
```

## 二、区域

```
drop：丢弃
任何传入的网络数据包都被丢弃，没有回复，只进行传出网络连接

block：阻止
任何传入的网络连接都被拒绝，其中用于包含IPv4的 icmp-host-prohibited 消息和用于IPv6的icmp6-adm-prohibited。只能从系统内启动网络连接

public：公共（默认）
用于公共场所。您不相信网络上的其他计算机不会损害您的计算机。仅接受选定的传入链接。

external：外部网络
用于特别为路由器启用伪装的外部网络。您不相信网络上的其他计算机不会损害您的计算机。仅接受选定的传入链接。

dmz：管制区
适用于非军事区中的计算机，这些计算机可公开访问，并且对内部网络的访问权限有限。进接受选定的传入连接

work；工作
用于工作区域。您最常信任网络上的其他计算机，以免损害您的计算机。进接受选定的传入连接

home：家庭
适用于家庭区域。您最常信任网络上的其他计算机，以免损害您的计算机。进接受选定的传入连接

internal：内部
用于内部网络。您最常信任网络上的其他计算机，以免损害您的计算机。进接受选定的传入连接

trusted：受信任
接受所有网络连接。
可以将这些区域中的一个指定为默认区域。将接口连接添加到NetworkManager时，会将他们分配给默认区域。安装时，firewalld中的默认区域想设置为公共区域
```

## 三、配置firewalld-cmd

```
firewall-cmd --list-all  #列出目前表中信息

firewall-cmd --set-default-zone=trusted  #更改默认区域为trusted区

```

在更换默认区为trusted之前，我们的xampp是访问不了的，但是区域改为trusted之后xampp立马就可以访问了

![image-20230925171633530](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230925171633530.png)

![image-20230925171707597](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230925171707597.png)

但是如果将默认区域换为drop之后，更访问不了了，因为数据包都直接被丢弃。当然block（reject）区域（这个是带有回复的）是差不多的

```
public (default，active) :  示 public 区域是默认区域(当接口启动时会自动默认)，并且它是活动的。
interfaces：ens33 列出了这个区域上关联的接口。
sources:列出了这个区域的源。现在这里什么都没有，但是，如果这里有内容，它们该是这样的格式 xxx.xxx.xxx.xxx/xx。services: dhcpv6-cient ssh 列出了允许通过这个防火墙的服务。可以通过运行 firewal1-cmd --get-services得到一个防火定义服务的详细列表。
ports:列出了一个允许通过这个防火墙的目标端口。它是用于你需要去允许一个没有在 firewa11d 中定义的服务的情况下
masquerade: no 表示这个区域是否允许 IP 装。如果允许，它将允许 IP 转发，它可以让你的计算机作为一个路由器。
forward-ports: 列出转发的端口。
icmp-blocks: 阳赛的 icmp 流量的黑名单。
rich rules: 在一个区域中优先处理的高级配置。
default:是目标区域，它决定了与该区域匹配而没有由上面设置中显式处理的包的动作。
```

### 运行一下命令理解firewalld规则用法：

```
查看多有打开的端口：firewall-cmd --zone==public --list-port
更新防火墙规则：firewall-cmd --reload
列出所有区域：firewall-cmd --get-zones
查看区域信息：firewall-cmd --get-active-zones
设定默认区域，立即生效：firewall-cmd --set-default-zone=public
查看指定接口所属区域：firewall-cmd --get-zone-of-interface=ens32
查看所有规则：firewal-cmd --list-all
通过以下两种手段可以进行永久修改：
firewall-cmd --permanent <some modification>
firewall-cmd --reload

```

### 常见使用场景

```
firewall-cmd --get-services  #获取firewalld找那个事先定义了那些服务，防止后面添加服务的时候出错

firewall-cmd --add-port=80/tcp
firewall-cmd --add-service=http
#但是上面这些配置一旦systemctl restart firewalld就都会消失，所以为了能够是我们的配置能一直生效，我们应该用下面的方法
firewall-cmd -add-service=http --permanent  #这条命令是将我们的配置信息写入配置文件，此时我们需要重新加载这个firewalld，不然写进去的信息没有被加载到服务中去
firewall-cmd --reload

```

