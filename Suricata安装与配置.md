[TOC]



# ==Suricata安装与配置==

教材内容

#### 一、功能介绍

##### 1、概述

Suricata来源于经典的NIDS系统Snort，是一套基于网络流量的威胁检测引擎. 整合了intrusion detection (IDS)、intrusion prevention (IPS)、network security monitoring (NSM) 和PCAP processing等功能。

![image-20211222230530425](https://gitee.com/ymq_typroa/typroa/raw/main/20211222230530.png)

##### 2、IDS功能

通过监听网卡流量并匹配规则引擎进行入侵实时检测和预警，检测手段上也Wazuh比较类似。

##### 3、IPS功能

与Wazuh的主动响应的功能并不完全一样，IPS功能并不需要对防火墙进行调用，而是直接通过将流量引入到 iptables的队列中，再根据特征进行检测，满足规则的流量会直接被Suricata丢弃或拒绝，导致整个流量根本无法到达目标服务器。而Wazuh的主动响应机制则是在攻击行为已经发生或正在发生的情况下，通过日志信息进行检测，再调用iptables或firewall-cmd进行处理，实时性和准确性方面相对于Suricata更延后一些。

##### 4、支持的协议

Suricata来源于Snort，但是比Snort更加实用也增强了更多的功能，同时，Snort只支持传输层和网络层协议，而Suricata还支持应用层的协议进行解析和规则匹配。

#### 二、安装Suricata

##### 1、二进制安装（推荐）

```shell
yum install epel-release yum-plugin-copr
yum copr enable @oisf/suricata-6.0
yum install suricata

# 安装完成后，对应的路径如下：
Suricata主程序路径：/usr/sbin/suricata
Suricata核心配置目录：/etc/suricata/
Suricata日志目录：/var/log/suricata/
Suricata附属程序目录：/usr/bin

# 日志目录下的4个文件的功能
eve.json：以JSON格式存储预警信息或附加信息
fast.log：预警核心文件，只用于存储警告信息，非结构化数据
stats.log：Suricata的统计信息
suricata.log：Suricata程序的运行日志
```

##### 2、源码安装

（1）在Linux上安装

```shell
# yum install libjansson, libpcap, libpcre2, libmagic, zlib, libyaml, gcc, pkg-config,libgeoip, liblua5.1, libhiredis, libevent

# tar xzvf suricata-6.0.0.tar.gz
# cd suricata-6.0.0

# ./configure --prefix=/var/suricata/ --sysconfdir=/var/suricata/config --localstatedir=/var/suricata/ --enable-lua  --enable-geoip --enable-nfqueue

# make
# make install
```

安装完成后，运行/usr/sbin/suricata —build-info，确认是否安装成功

```shell
This is Suricata version 6.0.4 RELEASE
Features: NFQ PCAP_SET_BUFF AF_PACKET HAVE_PACKET_FANOUT LIBCAP_NG LIBNET1.1 HAVE_HTP_URI_NORMALIZE_HOOK PCRE_JIT HAVE_NSS HAVE_LUA HAVE_LIBJANSSON TLS TLS_GNU MAGIC RUST 
SIMD support: none
Atomic intrinsics: 1 2 4 8 byte(s)64-bits, Little-endian architecture
……………………………………
```

（2）在Windows上安装

安装之前，需要先安装npcap库用于捕获网络流量：https://nmap.org/download.html

> 安装包下载地址：https://suricata.io/download/

#### 三、首次运行Suricata

##### 1、修改基础配置信息

直接编辑/etc/suricata/suricata.yaml

```shell
vars:  
	# more specific is better for alert accuracy and performance  
	address-groups:    
	#HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"    
	#HOME_NET: "[192.168.0.0/16]"    
	#HOME_NET: "[10.0.0.0/8]"    
	#HOME_NET: "[172.16.0.0/12]"    
	#HOME_NET: "any"    
	HOME_NET: "[192.168.112.0/24]"     # 指定192.168.112.0/24网段属于本地网络    
	
	#EXTERNAL_NET: "!$HOME_NET"           # 指定非HOME_NET的IP为外部网络    
	EXTERNAL_NET: "any"                   # 指定任意IP地址，只要是源IP，均视为外部网络
```

![image-20250215005843646](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215005843646.png)

完成上述配置后， 尝试使用以下命令来启动Suricata： cd /etc/suricata && suricata -c suricata.yaml -i ens33 ，会得到以下错误：

![image-20250215010330451](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215010330451.png)

错误消息显示，/etc/suricata/rules/suricata.rules （不同版本也可能是：/var/lib/suricata/rules/suricata.rules ） 规则文件不存在，导致无法正常启动，事实上默认的suricata.yml配置文件中是明确指定了默认加载该规则文件，而Suricata的发行版本中默认该规则文件并不存在，所以要正常启动，还需要手工创建一个规则文件。

![image-20250215010347412](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215010347412.png)

将

![image-20250215010406351](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215010406351.png)

修改为

![image-20250215010421798](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215010421798.png)

因为

![image-20250215010458313](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215010458313.png)

```shell
touch /etc/suricata/rules/suricata.rules
再指定 default-rule-path: /etc/suricata/rules  或   /var/lib/suricata/rules 均可
```

再次启动，会报以下错误：

![image-20250214232416828](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250214232416828.png)

错误显示，规则文件已经存在，但是没有指定规则，所以要让Suricata成功启动，还必须为它创建一条规则才行。此时，我们先为其创建一条最简单的规则，基于ICMP协议。

```shell
alert http $EXTERNAL_NET any <> $HOME_NET 80 (msg:"出现404错误"; content: "404"; http_stat_code; sid:561001;)
```

![image-20250215010810866](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215010810866.png)

![image-20250215010524771](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215010524771.png)

##### 2、查看预警信息

（1）启动Xampp或任意Web服务器，访问一个不存在的页面，使其产生404错误。

（2）运行 tail -f /var/log/suricata/fast.log 查看文件型预警信息

```shell
12/22/2021-23:36:54.329363  [**] [1:561001:0] 出现404错误 [**] [Classification: (null)] [Priority: 3] {TCP} 192.168.112.195:80 -> 192.168.112.1:1403
```

![image-20250215010626396](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215010626396.png)

（3）运行 tail -f /var/log/suricata/eve.json，查看JSON格式的预警信息

```json
{"timestamp":"2025-02-15T01:06:51.718153+0800","flow_id":1081272915109526,"in_iface":"ens32","event_type":"alert","src_ip":"192.168.230.188","src_port":80,"dest_ip":"192.168.230.1","dest_port":37829,"proto":"TCP","tx_id":0,"alert":{"action":"allowed","gid":1,"signature_id":561001,"rev":0,"signature":"出现404错误","category":"","severity":3},"http":{"hostname":"192.168.230.188","url":"/dashboard/phpinfcxcxcxo.php","http_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0","http_content_type":"text/html","http_method":"GET","protocol":"HTTP/1.1","status":404,"length":1139},"files":[{"filename":"/dashboard/phpinfcxcxcxo.php","sid":[],"gaps":false,"state":"CLOSED","stored":false,"size":1036,"tx_id":0}],"app_proto":"http","flow":{"pkts_toserver":5,"pkts_toclient":6,"bytes_toserver":819,"bytes_toclient":1849,"start":"2025-02-15T01:06:10.829078+0800"}}
```

同时我们还看到eve.json文件中，相对于fast.log多了很多其他信息，有很多信息并非预警信息，如果不需要关心，可以用以下命令过滤：

```shell
grep 'event_type":"alert' /var/log/suricata/eve.json
```

![image-20250215010758320](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215010758320.png)

（4）如果不想要eve.json产生过多无用信息，需要在suricata.yaml的配置文件中对各种类型的输出进行禁用，比如：

```shell
在核心配置文件中，找到outputs -> eve-log -> types 节点
- anomaly:  
	enabled: no
- http:  
	extended: no
可以大量减少无效信息，当然这也取决于我们是否需要对此类日志进行收集
```

Suricata的配置文件特别多，功能也很丰富，后续学习过程中再逐步介绍。https://suricata.readthedocs.io/en/latest/output/eve/eve-json-output.html

##### 3、让Suricata后台启动

```
suricata -c suricata.yaml -i ens33 -D
```

##### 4、一些参考资料

> 官方网站：https://suricata.io/
>
> 在线文档：https://suricata.readthedocs.io/en/latest/
>
> 中文文档：https://www.osgeo.cn/suricata/
>
> 特性介绍：https://suricata.io/features/