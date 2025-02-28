[TOC]



# ==Suricata基于网关的IPS功能==

## 一、端口转发

（1）第一种：本机端口转发，比如80端口对外封闭，开放一个7777供外部访问，外部只知道7777，不知道80，可以避免协议猜测

（2）第二种：远程端口转发，把本机接收到的请求转发到远程电脑和对应端口上（远程可以是本地局域网，也可以是公网服务器）

```shell
# 本机端口转发：
iptables -t nat -A PREROUTING -p tcp --dport 7777 -j REDIRECT --to-ports 80

# 远程端口转发：
# 需要确保端口转发功能是启用的
sysctl -w net.ipv4.ip_forward=1

# PREROUTING上访问8888时，转发给目标服务器和目标端口
# 将访问192.168.230.188:8888端口的流量转发给192.168.230.147:80
iptables -t nat -A PREROUTING -i ens33 -d 192.168.230.188 -p tcp --dport 8888 -j DNAT --to-destination 192.168.230.147:80

# 将192.168.230.147:80来的流量，交由192.168.230.188进行响应
iptables -t nat -A POSTROUTING -d 192.168.230.147 -p tcp --dport 80 -j SNAT --to 192.168.230.188
iptables -t filter -I FORWARD -j ACCEPT   
# 转发端口放行
```

> PREROUTING是先于FILTER执行的，所以不需要转发时允许8888端口ACCEPT

## 二、远程转发IPS

> 什么意思呢，就是说我有一台公网服务器，比如就是这里的192.168.230.188，然后我开放他的8888端口，然后将访问该 192.168.230.188:8888 的流量转发给该服务器背后的内网主机 192.168.230.147 的 80 端口，也就是访问 192.168.230.188:8888 实际上访问的是 192.168.230.147:80 的流量

##### 1、同网段端口转发

```shell
开启远程转发： sysctl -w net.ipv4.ip_forward=1
# 访问192.168.230.188:9080时，将流量转发给192.168.230.147:80
iptables -t nat -A PREROUTING -d 192.168.230.188 -p tcp --dport 9080 -j DNAT --to-destination 192.168.230.147:80

# 从192.168.230.147:80来的流量，交由192.168.230.188进行响应
iptables -t nat -A POSTROUTING -d 192.168.230.147 -p tcp --dport 80 -j SNAT --to 192.168.230.188

# 使用 iptables -nL -t nat 查看转发规则
```

![image-20250226153206394](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250226153206394.png)

但此时任然无法访问，要想可以访问，我们需要配置 iptables 接受端口转发

```shell
iptables -t filter -I FORWARD -j ACCEPT
```

![image-20250226153935618](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250226153935618.png)

##### 2、配置iptables

```shell
iptables -I FORWARD -j NFQUEUE       # 所有转发流量交由NFQUEUE处理
```

##### 3、为目标服务器192.168.230.147配置白名单，其他IP均拒绝

> 为了防止网管ips沦陷，以及被内网渗透进来

```shell
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.230.188" port port="80" protocol="tcp" accept'
firewall-cmd --remove-port=80/tcp
```

##### 4、编写预警规则，并使用drop或reject进行拦截

## 三、网关IPS

##### 1、开启远程转发： sysctl -w net.ipv4.ip_forward=1

##### 2、为目标服务器230.147手工配置网关地址为230.188。

如果是Windows环境，直接配置网络属性，手工指定网关，如果是Linux环境，要么编辑 /etc/sysconfig/network-scripts/ifcfg-ens33 手工指定GATEWAY，要么运行命令：“ route add default gw 192.168.230.188 ens33”，重启网卡，使用命令 route -n 或 Windows上的route print均可以查看网关信息。

> 此处需要特别注意，230.147上最好只有一块网卡，禁用或删除其他多余网卡，否则可能导致连接不成功。

##### 3、然后在网关230.188上执行以下命令完全配置：

```shell
iptables -t nat -A PREROUTING -i ens37 -d 192.168.19.34 -p tcp --dport 9080 -j DNAT --to-destination 192.168.230.147:80
```

此时，iptables的nat规则如下：

![image-20250220221909188](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220221909188.png)

##### 4、让转发流量进入NFQUEUE：iptables -I FORWARD -j NFQUEUE

此时，正常启动Suricata的IDS或IPS模式均可，同时从230.147上可以看到访问的源IP地址为客户机的真实IP，并且原客户端不需要配置路由，与真实的公网和内网环境一致。

![image-20230324145700181](https://gitee.com/ymq_typroa/typroa/raw/main/20230324145700.png)

> 当然，如果同在一个局域网，也可以为客户机配置网关为19.34，为服务器配置网关为230.188，则此时实现了跨网段路由，则可以直接在客户机上跨网段访问230.147目标服务器。
>
> Suricata也可以工作在核心交换机或者网关上，只需要确保流量经过Suricata或者进行端口镜像即可。
