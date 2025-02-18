[TOC]



# ==Linux配置rsyslog日志==

教材内容

#### 一、什么是syslog

##### 1、syslog

完善的日志分析系统应该能够通过多种协议（包括syslog等）进行日志采集并对日志分析，因此日志分析系统首先需要实现对多种日志协议的解析。其次，需要对收集到的海量日志信息进行分析，再利用数据挖掘技术，发现隐藏在日志里面的安全问题。

Syslog在Unix/Linux系统中应用非常广泛，它是一种标准协议，负责记录系统事件的一个后台程序，记录内容包括核心、系统程序的运行情况及所发生的事件。Syslog协议使用UDP作为传输协议，通过514端口通信，Syslog使用syslogd后台进程，syslogd启动时读取配置文件/etc/syslog.conf，它将网络设备的日志发送到安装了syslog软件系统的日志服务器，Syslog日志服务器自动接收日志数据并写到指定的日志文件中。

##### 2、rsyslog

rsyslog可以简单的理解为syslog的超集，在老版本的Linux系统中，Red Hat Enterprise Linux 3/4/5默认是使用的syslog作为系统的日志工具，从RHEL 6 开始系统默认使用了rsyslog。

其特性包括：

（1）支持输出日志到各种数据库，如 MySQL，PostgreSQL，MongoDB，ElasticSearch，等等；

（2）通过 RELP + TCP 实现数据的可靠传输（基于此结合丰富的过滤条件可以建立一种 可靠的数据传输通道供其他应用来使用）；

（3）精细的输出格式控制以及对消息的强大 过滤能力；

（4）高精度时间戳；队列操作（内存，磁盘以及混合模式等）； 支持数据的加密和压缩传输等。

#### 二、rsyslog语法规则

##### 1、rsyslog的主要模块

（1）modules，模块，配置加载的模块，如：ModLoad imudp.so 配置加载UDP传输模块

（2）global directives，全局配置，配置rsyslog守护进程的全局属性，比如主信息队列大小（MainMessageQueueSize）

（3）rules，规则（选择器+动作），每个规则行由两部分组成，selector部分和action部分，这两部分由一个或多个空格或tab分隔，selector部分指定源和日志等级，action部分指定对应的操作

（4）模板（templates）

（5）输出（outputs）

##### 2、常用的modules

（1）imudp，传统方式的UDP传输，有损耗

（2）imtcp，基于TCP明文的传输，只在特定情况下丢失信息，并被广泛使用

（3）imrelp，RELP传输，不会丢失信息，但只在rsyslogd 3.15.0及以上版本中可用

##### 3、规则的选择器（selectors）

（1）日志设施有：

```
auth(security), authpriv: 授权和安全相关的消息
kern: 来自Linux内核的消息
mail: 由mail子系统产生的消息
cron: cron守护进程相关的信息
daemon: 守护进程产生的信息
news: 网络消息子系统
lpr: 打印相关的日志信息
user: 用户进程相关的信息
local0 to local7: 保留，本地使用
```

![image-20250223034444513](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250223034444513.png)

（2）日志级别有（升序）：

```
0 debug：包含详细的开发情报的信息，通常只在调试一个程序时使用。
1 info：情报信息，正常的系统消息，比如骚扰报告，带宽数据等，不需要处理。
2 notice： 不是错误情况，也不需要立即处理。
3 warning： 警告信息，不是错误，比如系统磁盘使用了85%等。
4 err：错误，不是非常紧急，在一定时间内修复即可。
5 crit：重要情况，如硬盘错误，备用连接丢失。
6 alert：应该被立即改正的问题，如系统数据库被破坏，ISP连接丢失。
7 emerg：紧急情况，需要立即通知技术人员。
```

在 默认的 rsyslod.conf 配置文件中，默认使用的等级是所有 也就是上一张图片中的所有使用通配符 * 代替的等级，但还是有 *.emerg 以及 mail.none 或者 authpriv.none 等等

（3）日志设施的配置

```
`.` 代表比后面还要高的消息等级都会记录下来

`. =` 代表只有后面的这个消息等级会被记录下来

`. !` 代表除了后面的这个消息等级，其他的都会被记录下来

举例：

mail.info /var/log/maillog: 比指定级别更高的日志级别，包括指定级别自身，保存到/var/log/maillog中

mail.=info /var/log/maillog: 明确指定日志级别为info，保存至/var/log/maillog

mail.!info /var/log/maillog: 除了指定的日志级别(info)所有日志级别信息，保存至/var/log/maillog

*.info /var/log/maillog: 所有facility的info级别，保存至/var/log/maillog

mail.* /var/log/maillog: mail的所有日志级别信息，都保存至/var/log/maillog

mail.notice;news.info /var/log/maillog: mail的notice以上级别的日志级别和news的info以上级别保存至/var/log/maillog

mail,news.crit -/var/log/maillog: mail和news的crit以上的日志级别保存/var/log/maillog中；“-”代表异步模式
```

##### 4、动作（action）

action是规则描述的一部分，位于选择器的后面，规则用于处理消息。总的来说，消息内容被写到一种日志文件上，但也可以执行其他动作，比如写到数据库表中或转发到其他主机。

```
# 写本地日志文件
local0.*    /var/log/lyh.log

# modules, 要将日志写到mysql中需要加载ommysql模块
$ModLoad ommysql 
*.*       :ommysql:127.0.0.1,Syslog,syslogwriter,topsecret
```

##### 5、模板（templates）

模板允许你指定日志信息的格式，也可用于生成动态文件名，或在规则中使用。

| 属性                    | 释义\                                                        |      |
| :---------------------- | :----------------------------------------------------------- | :--- |
| **msg**                 | 日志的信息内容，message。                                    |      |
| **rawmsg**              | 不转义的日志内容。转义是默认开启的(EscapecontrolCharactersOnReceive),所以它有可能与socket中接收到的内容不同。 |      |
| **rawmsg-after-pri**    | 几乎与rawmsg相同，但是删除了syslog PRI。                     |      |
| **hostname**            | 打印该日志的主机名。                                         |      |
| **source**              | hostname属性的别名。                                         |      |
| **fromhost**            | 接收的信息来自于哪个节点。这里是DNS解析的名字。              |      |
| **fromhost-ip**         | 接收的信息来自于哪个节点，这里是IP，本地的是127.0.0.1。      |      |
| **syslogtag**           | 信息标签。大致形如 programed[14321] 。                       |      |
| **programname**         | tag的一部分，就是上面的programed那个位置。                   |      |
| **pri**                 | 消息的PRI部分-未解码(单值)                                   |      |
| **pri-text**            | 文本形式的消息的PRI部分，并在括号中添加数值PRI(例如“`local0.err<133>`”) |      |
| **iut**                 | InfoUnitType 一款监视器软件，在与监视器后端通信的时候使用    |      |
| **syslogfacility**      | 设备信息，数字形式表示                                       |      |
| **syslogfacility-text** | 设备信息，文本形式表示                                       |      |
| **syslogseverity**      | 日志严重性等级，数字形式表示                                 |      |
| **syslogseverity-text** | 日志严重性等级，文本形式表示                                 |      |
| **syslogpriority**      | 同 syslogseverity                                            |      |
| **syslogpriority-text** | 同 syslogseverity-text                                       |      |
| **timegenerated**       | 高精度时间戳                                                 |      |
| **timereported**        | 日志中的时间戳。精度取决于日志中提供的内容(在大多数情况下，为秒级) |      |
| **timestamp**           | 同 timereported                                              |      |
| **protocol-version**    | IETF draft draft-ietf-syslog-protocol 中的 PROTOCOL-VERSION 字段的内容 |      |
| **structured-data**     | IETF draft draft-ietf-syslog-protocol 中的 STRUCTURED-DATA 字段的内容 |      |
| **app-name**            | IETF draft draft-ietf-syslog-protocol 中的 APP-NAME 字段的内容 |      |
| **procid**              | IETF draft draft-ietf-syslog-protocol 中的 PROCID 字段的内容 |      |
| **msgid**               | IETF draft draft-ietf-syslog-protocol 中的 MSGID 字段的内容  |      |
| **inputname**           | 生成日志的输入模块的名称(如“imuxsock”、“imudp”)              |      |
| **jsonmesg**            | 整个日志对象作为json表示。可能出现数据重复，譬如syslogtag包含着programname，但两者都会分别表示。所以这个属性有一些额外开销，建议只有在实际需要的时候再用。 |      |

**与时间相关的系统属性**（以 `2020-07-08 16:57:36` 为例）

| 属性        | 释义                                            |
| :---------- | :---------------------------------------------- |
| **$now**    | 当前日期时间戳，格式为YYYY-MM-DD (2020-07-08)   |
| **$year**   | 当前年份， 四位数 (2020)                        |
| **$month**  | 当前月份， 两位数 (07)                          |
| **$day**    | 当前月份的日期，两位数 (08)                     |
| **$wday**   | 当前天数周几 ：0=Sunday,…6=Saturday             |
| **$hour**   | 当前小时（24小时机制），两位数(16)              |
| **$hhour**  | 半小时机值，就是0-29分钟显示0，30-59分钟显示1。 |
| **$qhour**  | 一刻钟机值，通过0-3显示，每15分钟一截。         |
| **$minute** | 当前分钟数，两位数(57)                          |

```
$template TEMPLATE_NAME,"text %PROPERTY% more text", [OPTION]

$template DynamicFile,"/var/log/test_logs/%timegenerated%-test.log"
$template DailyPerHostLogs,"/var/log/syslog/%$YEAR%/%$MONTH%/%$DAY%/%HOSTNAME%/messages.log"

*.info ?DailyPerHostLogs
*.* ?DynamicFile
```

##### 6、输出(outputs)

输出频道为用户可能想要的输出类型提供了保护，在规则中使用前要先定义.其定义如下所示，

NAME：指定输出频道的名称；FILE_NAME：指定输出文件；MAX_SIZE指定日志文件的大小，单位是bytes； ACTION：指定日志文件到达MAX_SIZE时的操作。

$outchannel NAME, FILE_NAME, MAX_SIZE, ACTION

```
$outchannel NAME, FILE_NAME, MAX_SIZE, ACTION
```

#### 三、rsyslog传输实验

##### 1、实验准备

（1）准备一台客户端，将auth相关日志发送至rsyslog服务器，做好rsyslog的客户端配置。192.168.230.147

（2）准备一台服务器，用于接收rsyslog并保存至指定目录，做好rsyslog的服务器端配置并重启rsyslog服务。192.168.230.188

##### 2、rsyslog的配置文件

此处以192.168.230.188作为服务器端，查看以下配置文件：/etc/rsyslog.conf，另外，在/etc/rsyslog.d目录中还有单独的日志配置。

```
### MODULES ####

$ModLoad imuxsock	#提供本地系统日志支持（如通过logger命令）

$ModLoad imjournal	# 提供对systemd journal的访问
#$ModLoad imklog	# 提供内核日志支持（相当于systemd的systemd-journald.service）
#$ModLoad immark	# 提供-MARK-消息功能

#### GLOBAL DIRECTIVES ####

# Use default timestamp format 使用默认日志的时间戳格式
$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat

# Include all config files in /etc/rsyslog.d/ # 包含/etc/rsyslog.d/目录下的配置文件
$Includeconfig /etc/rsyslog.d/*.conf

### RULES ####

# Log all kernel messages to the console.	# 将所有的内核消息记录到控制台
# Logging much else clutters up the screen.
#kern.*											 /dev/console

# Log anything (except mail) of level info or higher.
# 将info或更高级别的消息送到/var/log/messages，除了mail/news/authpriv/cron之外


# Dont log private authentication messages!
# 其中*是通配符，代表任何设备：none表示不对任何级别的消息进行记录
*.info;mail.none;authpriv.none;cron.none		 	/var/log/messages

# The authpriv file has restricted access.
# 将authpriv设备的任何级别的信息记录到/var/log/secure中
authpriv.*										 /var/log/secure

# Log all the mail messages in one place.
# 将mail设备中的任何级别信息记录到/var/log/maillog文件中
mail.*											 -/var/log/maillog

# Log cron stuff
# 将cron设备的任何级别的信息记录到/var/log/cron文件
cron.*											 /var/log/cron

# Everybody gets emergency messages
# 将任何设备的emerg级别或者更高的消息发送给所有正在系统上的用户
*.*, emerg											 :omusrmsg: *

# Save news errors of level crit and higher in a special file.
# 将ucp和news设备的crit级别或者更高级别消息记录到/var/log/spooler文件中
ucp, news.crit									 /var/log/spooler

# Save boot messages also to boot.log
# 将和本地系统启动相关的信息记录到/var/log/boot.log文件中
local7.*										 /var/log/boot.log
```

##### 3、修改服务器端配置

（1）加载 UDP/TCP 的syslog接收模块，并设置监听端口，让TCP和UDP同时受到支持，也可以只开放UDP或TCP。

```
# Provides UDP syslog reception
$ModLoad imudp
$UDPServerRun 514

# Provides TCP syslog reception
$ModLoad imtcp
$InputTCPServerRun 514
```

![image-20250212000915607](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212000915607.png)

（2）增加日志记录规则

```
#### Added By ymqyyds ####
:fromhost-ip,isequal,"192.168.230.147"                     /var/log/host_192.168.230.147.log
:fromhost-ip,isequal,"192.168.230.147"                     ~
##########################
```

第一行右边的表示把该IP发送过来的日志存放到/var/log/host_192.168.230.147.log文件中，其中IP地址188是客户端IP。

第二行右边的~表示丢弃该IP发送过来的包。因为该文件内容是顺序执行的，所以上面两行就是把该IP日志存放到host_192.168.230.147.log后就丢弃该数据，防止在多个文件中存放相同的内容。

![image-20250212002137148](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212002137148.png)

至于这个第三行我不知道为什么，必须加上，不加上就无法生效，但不报错，就是用不了

（3）重启rsyslog

```
systemctl restart rsyslog
```

并执行命令`netstat -ant`确认514端口正常启动。

![image-20250212002226857](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212002226857.png)

##### 4、修改客户端配置

同样编辑/etc/rsyslog.conf，最基本的要求，添加一行内容，指定服务器端IP和端口，并重启rsyslog服务。

```
*.* @192.168.230.188:514
```

![image-20250212002725917](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212002725917.png)

##### 5、测试rsyslog是否接收成功

尝试远程登录147客户端的SSH，或发送邮件等操作，确认是否在188服务器端接收到了对应日志。

```
tail -f /var/log/host_192.168.230.147.log

ssh root@192.168.230.188
```

![image-20250212003656750](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212003656750.png)

##### 6、优化日志配置

（1）日志内容格式优化，输出日志的来源IP，并自定义列，修改服务器端配置如下。

```
$template MyLogFormat,"%timestamp% %fromhost-ip% %syslogtag% %msg%\n"
$ActionFileDefaultTemplate MyLogFormat
```

（2）将不同主机发送来的日志，保存到不同的文件或目录中，如：

```
$template RemoteLogs,"/var/log/host_%fromhost-ip%.log" 
:fromhost-ip, !isequal, "127.0.0.1" ?RemoteLogs
```

（3）综上

```
#### Added By ymqyyds ####
$template MyLogFormat,"%timestamp% %fromhost-ip% %syslogtag% %msg%\n"
$ActionFileDefaultTemplate MyLogFormat

$template RemoteLogs,"/var/log/host_%fromhost-ip%.log" 
:fromhost-ip, !isequal, "127.0.0.1" ?RemoteLogs
##########################
```

看 192.168.230.188 服务端的情况

![image-20250212004602065](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212004602065.png)

![image-20250212004653529](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212004653529.png)

再在 192.168.230.147 客户端上看看啥情况

![image-20250212004809120](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212004809120.png)

完全一致匹配，当然，服务器端还包含了其他日志中的文件