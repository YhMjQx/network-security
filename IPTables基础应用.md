# ==IPTables - 基础用法==

## 一、IPTables防火墙介绍

**IPTables默认没有设置规则的情况下，是允许所有流量还是拒绝呢？？？**

> 在默认情况下，iptables规则是允许所有流量的。也就是说，如果没有显式地定义任何规则，那么iptables将不会阻止或过滤任何流量。
>
> 然而，这并不意味着它是完全无保护的。默认情况下，iptables有一些内置的规则，称为"INPUT"、"FORWARD"和"OUTPUT"链，它们对某些流量进行了基本的限制。例如，INPUT链规则会阻止从外部网络到本地网络的未请求的流量，但不会阻止本地网络之间的流量。
>
> 因此，尽管在默认情况下iptables不阻止任何流量，但仍然建议为特定的应用程序或服务定义明确的规则，以确保只有预期的流量能够通过。



**但为什么我的CentOS上并没有给刚安装好的IPTables配置任何规则，但他依旧阻止了来自外部的流量？？？**

> 这可能是因为CentOS在安装时默认配置了iptables规则以保护系统的安全。虽然你没有显式地配置任何规则，但CentOS可能已经设置了一些默认规则来限制外部访问。
>
> 这些默认规则可能包括阻止未请求的流量、只允许本地流量等。这些规则的目的是防止潜在的攻击或未经授权的访问。
>
> 如果你发现你的CentOS系统阻止了外部访问流量，但你并没有配置任何规则，那么你可以通过运行以下命令来查看iptables的默认规则：
>
> `iptables -L`
>
>
> 这将列出当前配置的iptables规则。在输出中，你应该能看到INPUT、FORWARD和OUTPUT链的默认规则。
>
> 如果你确定这些默认规则是导致问题的原因，并且你希望允许外部流量，你可以使用以下命令暂时禁用iptables：
>
> `service iptables stop`
>
>
> 请注意，这只是一个临时解决方案，并且可能会降低系统的安全性。在禁用iptables后，请确保你理解了如何配置和启用适当的防火墙规则来保护你的系统。
>
> 如果你希望修改默认规则或添加自定义规则，你可以使用以下命令来编辑iptables配置文件：
>
> ` vi /etc/sysconfig/iptables`
>
> 在文件中，你可以添加、修改或删除规则以满足你的需求。完成后，保存文件并重新加载iptables规则：
>
> ` service iptables restart`
>
>
> 这样，你就可以根据自己的需求配置和调整iptables规则了。

而我就是在文件 `/etc/sysconfig/iptables` 这个中添加了一个允许80 端口访问的规则，这样才可以使得我在开启iptables的同时可以使用http访问，如果我不想通过添加规则仅仅使用默认来使得iptables允许外部流量访问，又该怎么做呢，应该就是上面使用 `service iptables stop`





## 三、基本命令的使用

```
-A  表示append追加的意思
—I  表示insert在最上面插入的意思
-j  表示接上对应的动作，是同意还是丢弃
-D  表示删除对应的规则

iptables -L OUTPUT --line-numbers  查看出站规则的行号

iptables -nL ：将将端口号以数字的形式显示默认表filter中的规则

iptables -I INPUT -j DROP ：将所有入栈流量全部丢弃，包括ssh请求
iptables -I OUTPUT -j DROP ： 将所有出栈流量全部丢弃，包括ssh响应
上述两条命令一旦执行，所有流量进不来也出不去，处于断网状态

iptables -A INPUT -j DROP ：
iptables -A OUTPUT -j DROP ：

iptables -I INPUT -p tcp --dport 22 -j ACCEPT ：打开目标端口22，接受流经该端口的流量
iptables -I INPUT -p tcp --dport 80 -j ACCEPT ：打开目标端口80，接受流经该端口的流量

```

要想阻止其他所有流量，只放通ssh即22号端口的流量，可以使用以下

`iptables -I INPUT -j DROP`
`iptables -I INPUT -p tcp --dport 22 -j ACCEPT `
这四条命令配合使用，先阻止所有入站流量，然后在阻止所有入站流量的规则基础上前方插入一个允许22号端口流量入站的规则或者我们不适用 `-I`而使用 `-A`，那么就是
`iptables -A INPUT -p tcp --dport 22 -j ACCEPT`
`iptables -A INPUT -j DROP`
这样就是先放通22号端口流量，再追加拒绝所有

别忘了，只允许进来，但不允许出去，22号端口依旧连通失败，所以我们还需要和上面一样的配置一下出站的情况，即：

`iptables -I OUTPUT -j DROP`
`iptables -I OUTPUT -p tcp --sport 22 -j ACCEPT`

或

`iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT`
`iptables -A OUTPUT -j DROP`



`iptables -nL` 列出表中链的信息（将端口号以数字的形式显示默认表filter中的规则）

![image-20230923163911857](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230923163911857.png)

`iptables -t` 用来指定表名

![image-20230923163715686](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230923163715686.png)

当然，通过以上的方式还可以做到**防止反弹shell**的目的：开通INPUT中的dport为80，OUTPUT中的sport为80，此时就已经可以做到别人可以访问我这个服务器，但OUTPUT中我并不配置dport为80，也就是说对于我本身服务器来说，我是无法访问出去的，只能别人访问我，我无法访问别人，前提是我在INPUT和OUTPUT中的最下面都配置了DROP all



```
DORP：直接丢弃数据包，不会向源端做任何回复
REJECT：拒绝接收数据包，并向源端口发送拒绝响应

iptables -f  刷新
service iptables save  保存规则
cat /etc/sysconfig/iptables
```

