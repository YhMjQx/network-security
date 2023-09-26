# ==Firewalld进阶用法==

## 常见使用场景

```
拒绝所有包：firewall-cmd --panic-on
取消拒绝状态：firewall-cmd --panic-off
查看是否拒绝：firewall-cmd --query-panic

暂时开放 ftp 服务：firewall-cmd --add-service=ftp
永久开放 ftp 服务：firewall-cmd --add-service=ftp --permanent
查询服务的启用状态：firewall-cmd --query-service ftp
开放MySQL端口：firewall-cmd --add-service=mysql
阻止http端口：firewall-cmd --remove-service=http
查看开放的服务：firewall-cmd --list-services
查看对应的规则库文件：cd /usr/lib/firewalld/services

开放通过tcp访问3306：firewall-cmd --add-port=3306/tcp
阻止通过tcp访问3306：firewall-cmd --remove-port=80/tcp
永久开放80端口：firewall-cmd --zone=public --add-port=80/tcp --permanent
查看80端口：firewall-cmd --zone=public --query-port=80/tcp
查看所有开放端口：firewall-cmd --zone=public --list-ports
删除80端口：firewall-cmd --zone=public --remove-port=80/tcp --permanent
开放postgresql服务：firewall-cmd --add-service=postgresql --permanent

允许http服务通过1分钟：firewall-cmd --zone=public --add-service=http --timeout=1m,这个 timeout 选项是一个以秒（s），分（m）或小时（h）为单位的时间值

重置防火墙：firewall-cmd --reload
检查防火墙状态：firewall-cmd --state
让设定生效：systemctl restart firewalld
检查设定是否生效：iptables -L -n | grep 21    
               firewall-cmd --list-all       
```

## 富规则

```
#在firewalld中accept和drop都是小写，但IPTables中都是大写
#firewalld中单次都是全拼，IPTables都是简写


添加指定ip访问特定端口规则：
firewall-cmd --permanent --add-rich-rule 'rule family=ipv4 source address=192.168.1.178 port protocol=tcp port=80 accept'
#family=ipv4  表示基于ipv4的数据包执行

删除指定某个ip访问特定端口规则：
firewall-cmd --permanent --remove-rich-rule 'rule family=ipv4 source address=192.168.1.178 port protocol=tcp poer=80 accept'

禁止某个ip访问
iptables -I INPUT -s 192.168.1.178 -j DROP
firewall-cmd --add-rich-rule 'rule family=ipv4 source address=192.168.1.178 drop'

允许ping：
firewal-cmd --add-rich-rule='rule family=ipv4 protocol value=icmp source address=192.168.1.178 accept'

端口转发：
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

接受192.168.1.0网段所有ip访问ssh服务：
firewall-cmd --add-rich-rule 'rule family=ipve source address=192.168.1.0/24 service name=ssh accept'

直接模式：
firewall-cmd --direct --add-rule ipv4 filter INPUT 1 -p tcp --dport 80 -s 192.168.1.178 -j ACCEPT
#这里的数字1表示匹配时的优先级，数字越小优先级越高，建议优先级从1开始
注意：firewall-cmd --direct --get-all-rules
```

![image-20230926143902268](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230926143902268.png)

像这种情况优先级高，但是顺序在下面，还是根据优先级来执行规则 

## 端口转发

端口转发可以将指定地址访问指定端口时，将流量转发至指定地址的指定端口。转发的目的如果不指定ip的话就默认为本机，如果指定了ip却没有端口，则默认使用来源端口。

如果配置号端口转发之后不能用，可以去检查下面两个问题：

- 比如我将80端口转发至8080端口，首先检查本地的80端口和目标的8080 端口是否开放监听了
- 其次是检查是否允许伪装ip，没允许的话要开启伪装

```
#将8888端口的ll转发至80端口
firewall-cmd --add-forward-port=port=8888:proto=tcp:toport=80

firewall-cmd --remove-forward-port=port=8888:proto=tcp:port=80


#开启伪装IP
firewall-cmd --query-masquerade  #检查是否允许伪装IP
firewall-cmd --add-masquerade  #允许防火墙伪装IP
firewall-cmd --remove-masquerade  #禁止防火墙伪装IP

#将8888端口的流量转发至101.37.65.91的80端口
firewall-cmd --add-forward-port=port=8888:proto=tcp:toaddr=101.37.65.91:toport=80
```

- 当我们想把某个端口隐藏起来的时候，就可以在防火墙上阻止那个端口访问，然后再开一个不规则的端口，之后配置防火墙的端口转发，将流量转发过去

- 端口转发还可以做流量分发，一个防火墙拖着好多台运行着不同服务的机器，然后用防火墙将不同端口的流量转发至不同机器。

## 扩展内容

### 第一部分

在firewalld中，--timeout参数是用于设置规则的超时时间，而富规则（rich rule）是用于定义更复杂的防火墙规则。虽然--timeout可以和普通规则一起使用，但并不能与富规则搭配使用。

富规则使用的是XML格式的规则文件，其中包含了多个规则元素和条件元素，可以定义更复杂的匹配和操作。然而，--timeout参数是针对单个规则的超时设置，无法直接应用于富规则中。

如果你想要在富规则中设置超时时间，需要在富规则中定义一个普通的规则，并使用--timeout参数进行设置。例如，你可以创建一个富规则，然后在其中定义一个规则元素，使用--timeout参数来设置超时时间。

以下是一个示例的富规则文件（假设名为rich-rule.xml）：

xml

```
<规则>
  <来源>
    <地址>192.168.0.0/24</地址>
  </来源>
  <目的>
    <地址>10.0.0.0/24</地址>
  </目的>
  <服务>
    <协议>tcp</协议>
    <端口>8080</端口>
  </服务>
  <规则>
    <来源>
      <地址>192.168.0.1</地址>
    </来源>
    <目的>
      <地址>10.0.0.1</地址>
    </目的>
    <协议>tcp</协议>
    <端口>8080</端口>
    <行动>允许</行动>
    <超时>300</超时> <!-- 这里设置了超时时间 -->
  </规则>
</规则>
```




然后，使用firewall-cmd命令加载和应用该富规则文件：

css

```
firewall-cmd --permanent --direct --add-rule rich-rule.xml
firewall-cmd --reloadfirewall-cmd --permanent --direct --add-rule rich-rule.xml
firewall-cmd --reload
```




这样，在富规则中定义的规则将会生效，并具有指定的超时时间。

请注意，上述示例仅为了演示如何在富规则中设置超时时间，并非一个完整的富规则示例。你需要根据自己的需求和环境来编写适合的富规则文件。

### 第二部分

了解一下frewalld 运行后台的各类配置文件、日志文件等信息，为后续课程学习做准备。在Linux中，通常配置文件是在/etc/目录下，所以可以使用 find /etc/ -name"firewal"，另外，Linux下的很多日志信息都保存在 var/log 目录下

在网络安全领域，各类应用系统或操作平台的 配置信息和 日志信息，是进行安全分析非常重要的参考。