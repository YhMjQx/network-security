[TOC]



# ==Suricata检测MySQL和SSH==

#### 一、MySQL流量检测

![image-20250220151110354](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220151110354.png)

![image-20250220151102074](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220151102074.png)

针对mysql的流量，我们应该也是比较熟悉了

##### 1、MySQL爆破检测

Suricata默认并没有提供对MySQL的应用层协议的支持，所以只能使用TCP协议。

```yaml
alert tcp $EXTERNAL_NET any <> $HOME_NET $MYSQL_PORTS (msg:"MySQL登录失败"; content:"Access denied for user"; nocase; sid:5621001; rev:1;)

alert tcp $EXTERNAL_NET any <> $HOME_NET $MYSQL_PORTS (msg:"MySQL登录失败-HEX"; flow: established, to_client; content:"|41 63 63 65 73 73 20 64 65 6e 69 65 64 20 66 6f 72 20 75 73 65 72|"; nocase; sid:5621002; rev:1;)

alert tcp $EXTERNAL_NET any <> $HOME_NET $MYSQL_PORTS (msg:"MySQL登录爆破"; content:"Access denied for user"; nocase; threshold: type both, track by_src, count 5, seconds 5; sid:5621003; rev:1;)
```

在Suricata中，针对所有内容的过滤，无论是特殊字符或正常字符还是不可见字符，均可以用十六进制进行检测（常规ASCII码，建议不使用十六进制，因为会降低规则的可读性）。

> 我们将 
>
> ![image-20250220151236629](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220151236629.png)
>
> 这一段数据，以十六进制复制出来
>
> ```
> 4163636573732064656e69656420666f722075736572
> 
> 这段十六进制对应的就是 Access denied for user
> 
> 写进 suricata 中就是
> |41 63 63 65 73 73 20 64 65 6e 69 65 64 20 66 6f 72 20 75 73 65 72|
> ```

![image-20250220151817074](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220151817074.png)

![image-20250220151922267](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220151922267.png)

![image-20250220152413109](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220152413109.png)

##### 2、MySQL木马写入

```sql
select "<?php eval($_POST['code']); ?>" into outfile "/opt/shell.php";
```

![image-20250220153344885](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220153344885.png)

```yaml
alert tcp $EXTERNAL_NET any <> $HOME_NET $MYSQL_PORTS (msg:"MySQL木马写入"; content:"into outfile"; pcre:"/select|eval|exec|shell_exec|system|assert|$_POST|$_GET/i"; classtype:mysql-shell-attack; sid:5621004; rev:1;)
```

![image-20250220153724143](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220153724143.png)

> 尝试编写针对UDF和MOF的入侵检测规则。

##### 3、其他的MySQL攻击性特征

```sql
show global variables like "%secure_file_priv%";  或者是响应中存在 secure_file_priv，说明有可能在试探权限

select load_file("/etc/passwd");

select "<?php eval($_POST['code']); ?>" into outfile "/tmp/shell.php";

select * from information_schema where table_schema="databaase";
经常使用concat， group_concat， updatexml， extract等关键字的，加上阈值预警一样也是检测依据
```

虽然常规的SQL语句在MySQL层面不能作为检测依据，但是攻击者必然需要利用一些MySQL的其他特征来进行入侵，而这些特征，通常是一个业务系统的正常SQL语句不具备的特征。

#### 二、SSH爆破检测

##### 1、特征分析

SSH 协议交互主要分为三个阶段，传输层协议，用户认证协议，连接协议。在传输层协议中主要完成服务端和客户端之间的ssh版本协商，密钥和算法协商，在该阶段的最后客户端会发送New Keys数据包，表示双方构建了一个加密通道，从而开始用户认证。最后就是如果认证登录成功后，持续不断地进行数据通信，这个过程不再具备用户认证的数据和交换密钥的过程。

![image-20250220155525974](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220155525974.png)

我们通过观察其实可以发现，每一次登录失败的ssh的 NewKeys 和 Key Exchange Init 的数据包内容，都是会变的，也就是每次的 NewKeys 内容都不一样，尽管是相同的用户名，相同的IP地址，数据包内容依然不同，因此我们只采取最后一段字节 ，即 1500000000000000000000

而对应的 Key Exchange Init 数据包的相同点，那就是最后的 o 字节太多了，即：0000000000000000000000000000000000000000000000

![image-20250220155546498](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220155546498.png)

因此，根据New Keys数据包中总是0x15和10个字节的0x00结尾的特点，可以标记该类数据包，与之类似的，Key Exchange Init过程也存在以较多的 00 00 00 00 等特征可以使用。当完成认证后，后续的通信全是常规加密流量，并且也不再存在Key Exchange或者New Keys流量。所以，针对SSH爆破的情况，必须存在较多的Key Exchange和New Keys流量。

下图是登录成功后的常规流量 。

![image-20250220155624218](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220155624218.png)

此处根据New Keys来写规则：

```yaml
alert ssh $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SSH登录"; content:"|15 00 00 00 00 00 00 00 00 00 00|"; sid: 5622001; rev:1;)

alert ssh $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SSH爆破"; content:"|15 00 00 00 00 00 00 00 00 00 00|"; threshold: type both, track by_src, count 5,seconds 20; sid:5622002; rev:1;)
```

![image-20250220160642335](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220160642335.png)

另外，在Key Exchange的流量中，也存在一些明显的特征：

![image-20211225200249847](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20211226050923.png)