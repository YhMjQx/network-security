[TOC]



# ==Wazuh处理MySQL预警==

教材内容

#### 一、MySQL基础配置

##### 1、确保启用了MySQL的日志文件

> 查找 mysql 配置文件在哪
>
> ```shell
> find /opt/lampp/ -name *my.cnf*
> ```
>
> ![image-20250209192634607](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209192634607.png)

```shell
编辑：/opt/lampp/etc/my.cnf

# Enable MySQL Log
general_log = ON
general_log_file = /opt/lampp/logs/mysql.log
log_output = file

chmod o+w /opt/lampp/logs
需要chmod的原因是，xampp默认安装使用的user是daemon，要想让 mysql 这个user可以操作，就需要对该文件夹赋予一个其他人可写的权限

重启lampp 
```

![image-20250209193014787](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209193014787.png)

![image-20250209193507062](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209193507062.png)

MySQL的日志文件内容如下：

![image-20250209193947062](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209193947062.png)

##### 2、为MySQL添加远程访问权限

```sql
GRANT ALL PRIVILEGES ON *.* TO 'qiang'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;

flush privileges;
```

##### 3、添加mysql.log到ossec的配置文件中

```xml
vi /var/ossec/etc/ossec.conf

<localfile>
    <log_format>syslog</log_format>
    <location>/opt/lampp/logs/mysql.log</location>
</localfile>
```

重启Wazuh，并尝试读一读 ruleset/rules/0295-mysql_rules.xml 中定义的规则。

##### 4、基于已有规则进行MySQL登录

```xml
<rule id="50100" level="0">
    <decoded_as>mysql_log</decoded_as>
    <description>MySQL messages grouped.</description>
</rule>

<rule id="50105" level="3">
    <if_sid>50100</if_sid>
    <regex>^MySQL log: \d+ \S+ \d+ Connect</regex>
    <description>MySQL: authentication success.</description>
    <mitre>
        <id>T1078</id>
    </mitre>
    <group>authentication_success,pci_dss_10.2.5,pci_dss_8.7,pgp13_7.1,XXXXXX</group>
</rule>

<rule id="50106" level="9">
    <if_sid>50105</if_sid>
    <match>Access denied for user</match>
    <description>MySQL: authentication failure.</description>
    <group>authentication_failed,pci_dss_10.2.4,pci_dss_10.2.5,pci_dss_8.7,XXXXXX</group>
</rule>
```

从上述规则中可以看到，当登录MySQL失败后，会出现一条9级预警。尝试使用错误的密码远程登录MySQL，在mysql.log中新增日志：

```shell
211216 1:50:43     4 Connect     qiang@192.168.112.1 as anonymous on
     4 Connect     Access denied for user 'qiang'@'192.168.112.1' (using password: YES)
```

上述这一条日志，是完全匹配 ID 为 50106 的规则的，但是系统却不会出现预警信息。

也就是说，此时我们的确满足 50106 的错误信息，并且 在 mysql.log 的日志文件当中确实已经记录了日志信息，但是，在 wazuh 的alerts.log 文件中并没有出现预警，最终发现，原因竟然是 解码器的问题，解码器的匹配规则和 mysql.log 日志文件的文件内容无法正确匹配，导致出现这样的问题

/var/ossec/logs/alerts/alerts.log 文件与响应内容如下

![image-20250209201807664](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209201807664.png)

/opt/lampp/logs/mysql.cnf 文件与响应内容如下：

![image-20250209201942043](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209201942043.png)

我们可以看到 alerts.log 文件中确实没有对 mysql 登录信息没有预警

#### 二、解决无法预警的问题

##### 1、分析问题的原因

从 0295-mysql_rules.xml 规则中可以看到，50106依赖于50105，而50105依赖于50100，但是在50105和 mysql decoder 中，存在的正则表达式`^MySQL log: \d+ \S+ \d+ Connect` 和 `^MySQL log:`，这两条正则表达式无法成功匹配mysql.log中的信息：

![image-20250209201700873](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209201700873.png)

从规则中可以看出，规则应该是较早期的版本，而新版本的MySQL日志并不是以MySQL开头的，所以匹配不成功，无法预警。

##### 2、处理无法解析MySQL日志的问题

```xml
# 使用正则表达式
<rule id="50106" level="9">
    <if_sid>50105</if_sid>
    <regex>Access denied for user</regex>
    <description>Database authentication failure.</description>
    <group>authentication_failed,</group>
</rule>

# 将50105规则：
<rule id="50105" level="3">
    <if_sid>50100</if_sid>
    <regex>^MySQL log: \d+ \S+ \d+ Connect</regex>
    <description>Database authentication success.</description>
    <group>authentication_success,</group>
</rule>

# 修改为如下：
<rule id="50105" level="3">
    <if_sid>50100</if_sid>
    <regex>\d+ Connect</regex>
    <description>Database authentication success.</description>
    <group>authentication_success,</group>
</rule>

# 而50105又依赖于50100：
<rule id="50100" level="0">
    <decoded_as>mysql_log</decoded_as>
    <description>MySQL messages grouped.</description>
</rule>

50100 需要执行解码器：<decoded_as>mysql_log</decoded_as>，修改ruleset/decoders/0150-mysql_decoder.xml为：
<decoder name="mysql_log">
    <prematch>\d+ Connect</prematch>
</decoder>
```

![image-20250209201545029](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209201545029.png)

![image-20250209201428315](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209201428315.png)

重启 wazuh，测试成功

![image-20250209202243731](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209202243731.png)

##### 3、MySQL爆破检测

30秒内触发50106达到5次及以上，提升预警至12级

```xml
<rule id="561001" level="12" frequency="5" timeframe="30">
    <if_matched_sid>50106</if_matched_sid>
    <description>MySQL: Too Many Fails to Login, Maybe Force Crack.</description>
    <group>attack,</group>
</rule>
```

![image-20250209210151658](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209210151658.png)

##### 4、触发主动响应

目前虽然已经触发规则，但是主动响应获取不到IP地址，无法完成封锁，请解决。

> 为神马 ssh 的主动响应就可以封锁，但是 mysql 的主动响应就无法封锁？区别是在于 decoder 的问题
>
> 我们先看 ssh 的 decoder
>
> ![image-20250209211629455](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209211629455.png)
>
> 其中，利用这样的正则表达式可以实现正确匹配到对应的用户名和ip地址，并且将其值传递出去给主动响应
>
> 但是我们看 mysql 的decoder
>
> ![image-20250209211739018](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209211739018.png)
>
> 这还是我们刚刚改过的，否则根本都检测不到预警，我们可以看到，并没有对ip地址及逆行正则匹配并且传参，因此无法实现主动响应

因此，我们修改 mysql 的 decoder 如下

```xml
<decoder name="mysql_log">
    <prematch>\d+ Connect</prematch>
    <regex offset="after_prematch">Access denied for user '(\S+)'@'(\S+)' </regex>
    <order>user, srcip</order>
</decoder>
```

>针对 主动响应 我们有两种方式
>
>```xml
>  <active-response>
>    <command>firewall-drop</command>
>    <location>local</location>
>    <level>7</level>
>    <timeout>600</timeout>
>  </active-response>
>
>  <active-response>  
>    <command>firewall-drop</command>  
>    <location>local</location>  
>    <rules_id>5712</rules_id>
>    <rules_id>561001</rules_id>  
>    <timeout>600</timeout>
>  </active-response>
>```
>
>分别是
>
> `<level>7</level>` 表示任意预警达到 7 级，则进行 IP 封锁
>
> `<rules_id>561001</rules_id>` 表示触发预警 id=561001 则进行 ip 封锁

执行，firewall-drop生效，发现此时已经无法在Xshell等终端访问到系统，查看iptables -nL，也可以看到IP地址被封锁。

```shell
Chain INPUT (policy ACCEPT)
target     prot opt source               destination
DROP       all  --  192.168.112.1        0.0.0.0/0

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
DROP       all  --  192.168.112.1        0.0.0.0/0

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```

如果发现没有封锁IP地址成功，那么可以查看一下active-response.log文件，是否出现了以下错误，如果出现，说明解码器设置不正确。

```shell
2021/12/16 22:05:32 active-response/bin/firewall-drop: Cannot read 'srcip' from data
```