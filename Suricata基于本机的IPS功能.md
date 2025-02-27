[TOC]



# ==Suricata基于本机的IPS功能==



#### 一、基础准备

##### 1、工作原理

Suricata 本身是不具有拦截功能的，想要让它拦截数据包需要配合 iptables 使用，在Suricata中，在规则前使用Reject或Drop关键字，即可完成流量拦截的功能，同时也将进行Alert操作，要使用该Action，必须使用NFQueue，配合iptables进行。NFQueue用于将流量导入Suricata，并配合IPTables完成后续处理。

Suricata可以工作在网关或当前主机，当工作于网关时，可以对整个网络的流量进行检测，并决定是将流量拦截或者放行，当然，也可以直接工作于当前主机，对当前主机的流量进行处理。

![image-20211227100833804](https://gitee.com/ymq_typroa/typroa/raw/main/20211227100833.png)

NFQUEUE 是一种 iptables 和 ip6tables 的目标，将网络包处理决定委托给用户态软件。比如，下面的规则将所有接收到的网络包委托给监听中的用户态程序去决策。

```shell
iptables -A INPUT -j NFQUEUE --queue-num 0       # --queue-num 0 参数可选，不指定默认为 0
```

用户态软件必须监听队列 0（connect to queue 0），并从内核获取消息；然后给每个网络包给出判决（verdict）。

##### 2、环境配置

（1）CentOS默认使用firewalld，而Suricata的IPS功能需要使用IPTables，所以先安装iptables-service

```shell
yum install -y iptables iptables-services

然后停止 firewalld，启动 iptables
systemctl stop firewalld
systemctl start iptables.service
```

（2）确认NFQueue组件成功安装，运行 “suricata —build-info” 确认NFQueue是启用状态

```
  AF_PACKET support:                       yes  
  eBPF support:                            no  
  XDP support:                             no  
  PF_RING support:                         no  
  NFQueue support:                         yes      # 默认如果是二进制安装，NFQUEUE是支持的
```

#### 二、iptables命令回顾

##### 1、默认配置

![image-20250220215424101](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220215424101.png)

##### 2、基础参数

| 参数               | 说明                                                         |
| :----------------- | :----------------------------------------------------------- |
| -A                 | 添加一条规则，即添加在规则的最后                             |
| INPUT              | 链名、常用、大写                                             |
| OUTPUT             | 链名、大写                                                   |
| -I                 | 指定链中插入规则，即添加到规则最前                           |
| -s                 | 指定源地址，可以是IP地址，也可以是网段”192.168.109.10/24”；”-s 为空”，表示所有 |
| -d                 | 目标地址                                                     |
| -p                 | 指定协议                                                     |
| —dport             | 指定主机端口（本机开放或拒绝端口）                           |
| —sport             | 指定主机端口（如：禁止连接对方某端口）                       |
| -j                 | 指定所需要的操作                                             |
| -i                 | 指定网卡名，表示报文流入的接口                               |
| -o                 | 指定网卡名，表示报文流出的接口                               |
| -t                 | 指定表名，默认是filter                                       |
| ACCEPT             | 允许                                                         |
| REJECT             | 拒绝，拒绝提供服务                                           |
| DROP               | 拒绝，丢弃数据包不回应                                       |
| -nvL —line-numbers | 查看fliter表中规则的顺序                                     |
| -F                 | 清空filter表                                                 |
| -R                 | 替换规则                                                     |

##### 3、常用命令

```shell
iptables -nL：将端口号以数字的形式显示默认表filter中的规则
iptables -I INPUT -j DROP         所有入站流量全部丢弃，包括SSH请求
iptables -I OUTPUT -j DROP         所有出站流量全部丢弃，包括SSH响应
上述两条命令一旦执行：所有流量无法进来，所有流量无法出去，断网状态

iptables -I INPUT -p tcp --dport 22 -j ACCEPT     打开目标端口22，接受流入该端口的流量
iptables -I INPUT -p tcp --dport 80 -j ACCEPT    打开目标端口80，接受流入该端口的流量

iptables -I INPUT -p icmp -j DROP                拒绝icmp协议，表示无法ping

DRPO：直接丢弃数据包，不会向源端做任何回复
REJECT: 拒绝接收数据包，并向源端发送拒绝响应

iptables -L INPUT --line-numbers         查询某个链上的规则的行号，用于删除规则用
iptables -D INPUT 1                     删除出站的第1行规则

service iptables save                    将现有临时规则进行永久保存
cat /etc/sysconfig/iptables             永久保存的规则文件

iptables -I INPUT -i ens33 -p tcp -s 192.168.112.153 --sport 8088 -j ACCEPT
iptables -I OUTPUT -o ens33 -p tcp -d 192.168.112.153 --dport 8088 -j ACCEPT

# 防止DDOS攻击，设定一些数据的限制条件
iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT

# 可以同时设定多个端口被允许
iptables -I INPUT -p tcp -m multiport --dport 80,22,443,3306 -j ACCEPT

# 封锁IP地址
iptables -I INPUT -s 192.168.112.X -j DROP
```

##### 4、端口转发

（1）第一种：本机端口转发，比如80端口对外封闭，开放一个7777供外部访问，外部只知道7777，不知道80，可以避免协议猜测

（2）第二种：远程端口转发，把本机接收到的请求转发到远程电脑和对应端口上（远程可以是本地局域网，也可以是公网服务器）

```shell
# 本机端口转发：
iptables -t nat -A PREROUTING -p tcp --dport 7777 -j REDIRECT --to-ports 80

# 远程端口转发：
# 需要确保端口转发功能是启用的
sysctl -w net.ipv4.ip_forward=1

# PREROUTING上访问8888时，转发给目标服务器和目标端口
iptables -t nat -A PREROUTING -i ens33 -d 192.168.112.195 -p tcp --dport 8888 -j DNAT --to-destination 192.168.112.188:80
iptables -t nat -A POSTROUTING -d 192.168.112.188 -p tcp --dport 80 -j SNAT --to 192.168.112.195
iptables -t filter -I FORWARD -j ACCEPT   # 转发端口放行
```

> PREROUTING是先于FILTER执行的，所以不需要转发时允许8888端口ACCEPT

#### 三、本机IPS实验

> 实验环境：我们单纯将 22 端口放通，方便xshell连接虚拟机
>
> 然后，让外面访问 192.168.230.188 的80端口的流量交由 suricata 进行处理

##### 1、启动Suricata

```shell
suricata -c suricata.yaml -q 0
```

![image-20250220230223720](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220230223720.png)

这句指令表示，suricata 按照 对应的配置文件来处理 队列号为0的数据包

当启动suricata并且指定q=0后，配合iptables的策略来决定哪些流量会到达Suricata，如果设置为：

```shell
iptables -I INPUT -j NFQUEUE --queue-num 0 （默认为0，可以不指定）
```

这段指令表示iptables将所有流量都交给 suricata 进行处理。

> 如果直接运行上面这条指令而不开启 suricata 的话，会立马将所有流量交给 suricata 进行处理，但是，虚拟机就会处于断网状态，因为 数据全都给 suricata 了，但是suricata 没有开启，那就相当于数据发送过来就没下文了，所以断网。

此时所有流量全部转交给Suricata进行处理，此类场景下，如果Suricata出现异常崩溃（比如性能不足等）的情况，则整个网络将无法访问。所以可以通过以下两种策略进行调整：

（1）在NFQUEUE的策略之前，为特定端口和服务添加ACCEPT，比如SSH 22号端口。

```shell
iptables -I INPUT -p tcp --dport 22 -j ACCEPT
```

什么意思呢，就是说，我们在 NFQUEUE的策略之前 再添加上述的 开放 22 号端口的这条策略

- 先查看一下 iptables 什么情况

  ![image-20250220232127251](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220232127251.png)

  ok，现在是空的，什么都没有，那么接下来操作如下：

- 第一步，先开启 suricata

  ![image-20250220232200146](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220232200146.png)

  目的是，为了防止将iptables流量交给suricata之后，立马就断网了。

- 第二步：将 iptables 的流量都交给 suricata 来处理

  ![image-20250220232302599](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220232302599.png)

- 第三步：在 NFQUEUE 的规则之前，再添加一个开放 22 号端口的流量

  ![image-20250220232522102](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220232522102.png)

  目的是让iptables知道，我首先 要确保ssh协议的联通，然后再将所有流量交给suricata，匹配规则从上到下。

（2）针对需要Suricata检测的端口流量进行NFQUEUE转交，而其他端口或流量还是交给iptables自身的策略。

- 这个策略的意思是，只需要将需要监控的端口上的流量，让 iptables 交给 suricata ，避免其他端口的流量收到误伤

  ```shell
  iptables -I INPUT -p tcp --dport 80 -j NFQUEUE --queue-num 0 （默认为0，可以不指定）
  #意思是iptables单独只将80端口的流量交给suricata进行检测
  ```



##### 2、作为本机的IPS

（1）iptables的配置

```shell
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -I INPUT -p tcp --dport 80 -j NFQUEUE
iptables -I OUTPUT -p tcp --sport 80 -j NFQUEUE
iptables -I INPUT -p tcp --dport 3306 -j NFQUEUE
iptables -I OUTPUT -p tcp --sport 3306 -j NFQUEUE
```

iptables配置完成后，截图如下：

![image-20250221001811636](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250221001811636.png)

（2）启动Suricata

```shell
suricata -c suricata.yaml -q 0
```

##### 3、测试以下规则

```yaml
# 当URL地址存在 and 时，则该流量将不会被通过，无法访问成功
alert http any any -> any $HTTP_PORTS (msg:"检测到SQL注入"; content: "|20|and|20|"; http_uri; sid: 5601001; )
drop http any any -> any $HTTP_PORTS (msg:"封掉SQL注入的ip"; content: "|20|and|20|"; http_uri; sid: 5601002; )


# 当用户上传图片马时，无法通过
alert http any any -> $HOME_NET $HTTP_PORTS (msg:"检测到疑似上传木马"; http.method; content:"POST"; http.content_type; content: "multipart/form-data"; http.request_body; content: "Content-Disposition"; http.request_body; pcre: "/eval|assert|system\(|exec|$_POST|$_GET/i"; classtype: web-file-upload; sid:5601003; rev: 1;)
drop http any any -> $HOME_NET $HTTP_PORTS (msg:"封掉上传木马的ip"; http.method; content:"POST"; http.content_type; content: "multipart/form-data"; http.request_body; content: "Content-Disposition"; http.request_body; pcre: "/eval|assert|system\(|exec|$_POST|$_GET/i"; classtype: web-file-upload; sid:5601004; rev: 1;)

# 当用户登录失败时，产生一条警告
alert tcp any any <> any $MYSQL_PORTS (msg:"MySQL登录失败"; content:"Access denied for user"; nocase; sid:5620001;)
# 当用户频繁登录失败时，拦截本次流量
drop tcp any any <> any $MYSQL_PORTS (msg:"MySQL爆破攻击"; content:"Access denied for user"; nocase; threshold: type threshold, track by_src, count 5, seconds 10; sid:5620002;)
```

注意测试Mysql的时候要把3306也交给suricata进行处理

![image-20250221000115905](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250221000115905.png)

![image-20250221001955575](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250221001955575.png)

#### 三、远程转发IPS

1、同网段端口转发

```shell
开启远程转发： sysctl -w net.ipv4.ip_forward=1
# 访问192.168.112.195:9080时，将流量转发给192.168.112.188:80
iptables -t nat -A PREROUTING -d 192.168.112.195 -p tcp --dport 9080 -j DNAT --to-destination 192.168.112.188:80

# 从192.168.112.188:80来的流量，交由192.168.112.195进行响应
iptables -t nat -A POSTROUTING -d 192.168.112.188 -p tcp --dport 80 -j SNAT --to 192.168.112.195

# 使用 iptables -nL -t nat 查看转发规则
```

2、配置iptables

```shell
iptables -I FORWARD -j NFQUEUE       # 所有转发流量交由NFQUEUE处理
```

3、为目标服务器配置白名单，其他IP均拒绝

```shell
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.112.195" port port="80" protocol="tcp" accept'
firewall-cmd --remove-port=80/tcp
```

4、编写预警规则，并使用drop或reject进行拦截

#### 四、网关IPS

1、开启远程转发： sysctl -w net.ipv4.ip_forward=1

2、为目标服务器112.188手工配置网关地址为112.195。如果是Windows环境，直接配置网络属性，手工指定网关，如果是Linux环境，要么编辑 /etc/sysconfig/network-scripts/ifcfg-ens33 手工指定GATEWAY，要么运行命令：“ route add default gw 192.168.112.195 ens33”，重启网卡，使用命令 route -n 或 Windows上的route print均可以查看网关信息。

> 此处需要特别注意，112.188上最好只有一块网卡，禁用或删除其他多余网卡，否则可能导致连接不成功。

3、然后在网关112.195上执行以下命令完全配置：

```shell
iptables -t nat -A PREROUTING -i ens37 -d 192.168.19.34 -p tcp --dport 9080 -j DNAT --to-destination 192.168.112.188:80
```

此时，iptables的nat规则如下：

![image-20250220221909195](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220221909195.png)

4、让转发流量进入NFQUEUE：iptables -I FORWARD -j NFQUEUE

此时，正常启动Suricata的IDS或IPS模式均可，同时从100.188上可以看到访问的源IP地址为客户机的真实IP，并且原客户端不需要配置路由，与真实的公网和内网环境一致。

![image-20230324145700181](https://gitee.com/ymq_typroa/typroa/raw/main/20230324145700.png)

> 当然，如果同在一个局域网，也可以为客户机配置网关为19.34，为服务器配置网关为112.195，则此时实现了跨网段路由，则可以直接在客户机上跨网段访问112.188目标服务器。
>
> Suricata也可以工作在核心交换机或者网关上，只需要确保流量经过Suricata或者进行端口镜像即可。