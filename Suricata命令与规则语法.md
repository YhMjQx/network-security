[TOC]



# ==Suricata命令与规则语法==

教材内容

#### 一、命令行选项

##### 1、常用启动选项

```
-c <path> 指定配置文件 suricata.yaml 所在路径
-i <interface> 指定要监控的网卡名称或IP地址
-T 测试配置文件是否正确
-v 设定日志级别，包括-v: INFO  -vv: PERF  -vvv: CONFIG   -vvvv: DEBUG
-D 后台启动-l 设定日志输出目录，将会覆盖配置文件中的 default-log-dir: /var/log/suricata/ 选项，可保持默认
-s <filename> 临时添加一个新的规则文件
```

![image-20250215130615083](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215130615083.png)

##### 2、离线分析流量

在Suricata启动的时候，可以添加选项来进行离线流量分析，为其指定对应的pcap流量文件即可，参数选项如下

```
-r <path>  在 pcap 离线模式（重播模式）下运行，从 pcap 文件中读取文件。如果 <path> 指定了一个目录，           则该目录中的所有文件将按照修改时间的顺序进行处理，保持文件之间的流状态。

# 还存在几条附加选项，跟随 -r 选项生效
--pcap-file-continuous   指示模式应该保持活动状态直到被中断。这对于添加新文件的目录很有用，不用考虑文件之间的流状态
--pcap-file-recursive    允许递归遍历子目录，最大深度为 255，此选项不能与 –pcap-file-continuous 结合使用
--pcap-file-delete       指示该模式应在处理完 pcap 文件后删除它们
```

> 此处的离线数据包文件，可以是Wireshar、TCPDump、Suricata等各类流量监控工具生成的文件

使用Wireshark监听一段流量，记录下404错误，让Suricata进行离线分析。运行以下 命令：

```
suricata -c suricata.yaml -r /opt/phpinfo-404.pcapng -v
```

![image-20250215170732977](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215170732977.png)

将会在当前运行目录下生成eve.json, fast.log, stats.log, suricata.log 4个标准日志文件，也可以使用 -l 选择指定日志目录

```
suricata -c suricata.yaml -r /opt/phpinfo-404.pcapng -l /var/log/suricata/ -v
```

![image-20250215171242416](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215171242416.png)

> 通过离线分析可以方便地对规则进行测试，而不需要在线多次操作去监听实时数据
>
> 如果规则没有更新，则之前的IDS将无法触发警告，而规则更新后，再进行离线分析，确认是否存在违规流量

##### 3、保存流量数据

通过在 suricata.yaml 中设置以下选项，可以在监控和分析流量的同时，将流量保存下来供后续使用。

```yaml
- pcap-log:  
	enabled: yes  
	filename: log.pcap
```

![image-20250215171311273](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215171311273.png)

![image-20250215194656400](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215194656400.png)

然后正常启动 suricata，再任意进行一些访问操作，比如登录MySQL，访问网页，登录SSH等，此时，IDS功能正常使用，并且也将会在 默认的日志文件夹 /var/log/suricata 目录中，生成 log.pcap.timestamp 的一个抓包文件，下载到Windows上用Wireshark打开。

![image-20250215195000422](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215195000422.png)

![image-20250215195009458](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215195009458.png)

![image-20250215195025066](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215195025066.png)

我们把它下载下来使用 wireshark 打开

![image-20250215195137228](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215195137228.png)

ok

同时注意下图这个选项：

![image-20250215192529447](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215192529447.png)

表示默认 8 秒钟 采集一次 status.log 文件。为了降低频率，我们改成一个小时

#### 二、规则基础语法

##### 1、核心语法

以下面这一条最简单的预警规则为例

```yaml
alert http $EXTERNAL_NET any <> $HOME_NET 80 (msg:"出现404错误"; content: "404"; http_stat_code; sid:561001;)
```

（1）Action字段：如 alert 表示如果触发该条规则，则直接进行预警，还有 pass、drop、reject

（2）协议字段：如 http 协议，或 icmp、tcp、udp、ip、ftp、smtp、snmp、tls、dns、ssh等

（3）源IP：$EXTERNAL_NET 表示从 suricata.yaml 中读取该变量的值即为源IP地址，也可以指定IP或any

（4）源端口：any 表示任意端口，通常情况下，源端口是随机生成的，不建议指定，除非很清楚规则

（5）方向：有单向 -> 表示仅检测从源到目的地，也可以是双向 <>，但是没有 <- 反向

（6）目的IP和端口

（7）预警规则选项，必须要被包含在 ( ) 中，且每一个关键字之间，用 ; 分隔开，所以如果需要匹配的是 ; 或 “” 或 : ，则必须转义

##### 2、IP地址规则

可以使用的语法如下：

| 操作员  | 描述                   |
| :------ | :--------------------- |
| ../..   | IP 范围（CIDR 表示法） |
| ！      | 异常/否定              |
| [..,..] | 分组                   |

如以下示例均可以用于定义源和目标IP地址

| 例子                          | 意义                                       |
| :---------------------------- | :----------------------------------------- |
| `！1.1.1.1`                   | 除了 1.1.1.1 之外的每个 IP 地址            |
| `![1.1.1.1, 1.1.1.2]`         | 除了 1.1.1.1 和 1.1.1.2 之外的每个 IP 地址 |
| `$HOME_NET`                   | 您在 yaml 中的 HOME_NET 设置               |
| `[$EXTERNAL_NET, !$HOME_NET]` | EXTERNAL_NET 而不是 HOME_NET               |
| `[10.0.0.0/24, !10.0.0.5]`    | 10.0.0.0/24 除了 10.0.0.5                  |

##### 3、端口规则

| 例子          | 意义                          |
| :------------ | :---------------------------- |
| [80, 81, 82]  | 端口 80、81 和 82             |
| [80:82]       | 范围从 80 到 82               |
| [1024：]      | 从 1024 到最高端口号          |
| !80           | 除了 80 之外的每个端口        |
| [80:100,!99]  | 范围从 80 到 100 但不包括 99  |
| [1:80,![2,4]] | 范围为 1-80，端口 2 和 4 除外 |

##### 4、Meta Keyword 元关键字

在 Suricata 的规则选项中，针对不同的协议类型有不同的关键字，同时，针对所有协议生效的关键字，称之为元关键字。

（1）msg：预警信息的详细描述，也是用于快速了解规则所描述的问题所在

（2）sid：规则编号，用于唯一识别规则项，建议自定义规则也要有一套自己的标准，避免与已有规则重合

（3）rev：规则的修订版本，默认为 0，可以自由设定版本号

（4）classtype：规则所属的类的类型，在 classification.config 中进行定义，同时也包含规则的 priority 优先级字段（1-4，1的优先级最高，4最低）比如：

![image-20250215171925413](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215171925413.png)

![image-20250215172224418](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215172224418.png)

（5）reference：引用参考，一个URL地址或是一条 CVE 编号，如 reference: url, www.info.com， reference: cve, CVE-2014-1234

（6）priority：优先级选项，如果明确指定，将覆盖 classtype 中的优先级设定，范围为1-255，建设设定1-4级，1级为最高

（7）metadata：元数据，添加非功能性数据，建议以键值对形式指定，如 metadata: key value, key value;

（8）target：允许指定警报的哪一侧是攻击的目标。如果指定，警报事件将被增强以包含有关源和目标的信息。target:[src_ip|dest_ip]

#### 三、规则示例

```yaml
alert http any any <> any $HTTP_PORTS (msg:"页面出来500错误"; content:"500"; http_stat_code; sid: 561002;)

alert pkthdr any any -> any any (msg:"SURICATA IPv6 wrong IP version"; decode-event:ipv6.wrong_ip_version; classtype:protocol-command-decode; sid:2200022; rev:2;)

alert tcp any any <> any $MYSQL_PORTS (msg:"Login MySQL Failed"; content:"Access denied for user"; nocase; sid:561001;)
```

![image-20250215171645190](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215171645190.png)

> https://suricata.readthedocs.io/en/latest/command-line-options.html
>
> https://suricata.readthedocs.io/en/latest/rules/index.html