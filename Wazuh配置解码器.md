[TOC]



# ==Wazuh配置解码器==

教材内容

#### 一、解码器与规则库目录

##### 1、decoders目录

定义了不同类型的解码器，在获取到日志记录后，Wazuh将首先通过解码器来确定日志的类型

##### 2、rules目录

确定了日志类型后，再进入rules目录下寻找同类型规则进行匹配

##### 3、sca目录

定义了常规的安全配置项的要求，如CentOS操作系统、MySQL数据库、PHP配置项等。

##### 4、自定义解码器

位于/etc/rules目录中，并确保在ossec.conf全局配置文件中已经包含该目录。

#### 二、解码器语法

##### 1、解码器语法

https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html

| Option                                                       | Values                                                       | Description                                                  |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [decoder](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#decoder) | Name of the decoder                                          | This attribute defines the decoder. 解码器根节点的名称       |
| [parent](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#parent) | Any decoder’s name                                           | It will reference a parent decoder and the current one will become a child decoder. 指定父解码器 |
| [program_name](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#program-name) | Any [regex](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html#regex-os-regex-syntax), [sregex](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html#sregex-os-match-syntax) or [pcre2](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html#pcre2-syntax) expression. | It defines the name of the program associated with the decoder. 定义解码器关联的程序 |
| [prematch](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#prematch) | Any [regex](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html#regex-os-regex-syntax) or [pcre2](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html#pcre2-syntax) expression. | It will look for a match in the log, in case it does, the decoder will be used. 从日志中去匹配一个解码器，匹配到后就会停止其他解码器的匹配 |
| [regex](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#regex-decoders) | Any [regex](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html#regex-os-regex-syntax) or [pcre2](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html#pcre2-syntax) expression. | The decoder will use this option to find fields of interest and extract them. 正则表达式，用于匹配或提取值 |
| [order](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#order) | See [order table](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#order) | The values that [regex](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#regex-decoders) will extract, will be stored in these groups. 从正则表达式中提取的值，保存于该字段定义的变量名中，变量名包含预定义的字段名，或自定义字段名 |
| [fts](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#fts) | See [fts table](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#fts) | First time seen. 首次出现，用于标志一个变量名，并在规则的 if_fts 中使用 |
| [ftscomment](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#ftscomment) | Any String                                                   | Adds a comment to fts. 对fts字段的解释说明，不常用           |
| [plugin_decoder](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#plugin-decoder) | See [below](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#plugin-decoder) | Specifies a plugin that will do the decoding. Useful when extraction with regex is not feasible. 当正则表达式无法提取变量值时，指定使用某个插件来提取值 |
| [use_own_name](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#use-own-name) | True                                                         | Only for child decoders. 对于子解码器，是否支持使用自身的名称而非父解码器的名称 |
| [json_null_field](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#json-null-field) | String                                                       | Adds the option of deciding how a null value from a JSON will be stored. 针对JSON解码器，如果匹配到空值后，以何种方式存储这个空值，默认为String，表示以 NULL（字符串型）来存储 |
| [json_array_structure](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#json-array-structure) | String                                                       | Adds the option of deciding how an array structure from a JSON will be stored. 针对JSON解码器，如果匹配到数组类型后，以何种方式存储这个数组 |
| [var](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#var) | Name for the variable.                                       | Defines variables that can be reused inside the same file. 定义一个在当前解码器的其他位置可以引用的变量名 |
| [type](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#type) | See [type table](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#type) | It will set the type of log that the decoder is going to match. 设定解码器对应日志的类型 |

##### 2、JSON Decorder

Wazuh内置了对JSON日志良好的支持，也就是说，无论是否是由Wazuh产生的预警日志，只要是JSON格式，通过JSON解码器均可以识别出对应的类型，只需要定义好相应的规则即可，比如利用Wazuh+Elastic来对Suricata的NIDS预警信息进行展示处理。

```xml
<decoder name="json">  
    <prematch>^{\s*"</prematch>  
    <plugin_decoder>JSON_Decoder</plugin_decoder>
</decoder>
```

查看规则：ruleset/rules/0475-suricata_rules.xml

```xml
<group name="ids,suricata,">
    <rule id="86600" level="0">
        <decoded_as>json</decoded_as>
        <field name="timestamp">\\.+</field>
        <field name="event_type">\\.+</field>
        <description>suricata messages.</description>
        <options>no_full_log</options>
    </rule>

    <rule id="86601" level="3">
        <if_sid>86600</if_sid>
        <field name="event_type">alert$</field>
        <description>Suricata: Alert - $(alert.signature)</description>
        <options>no_full_log</options>
    </rule>

    <rule id="86602" level="0">
        <if_sid>86600</if_sid>
        <field name="event_type">http$</field>
        <description>Suricata: HTTP.</description>
        <options>no_full_log</options>
    </rule>

    <rule id="86603" level="0">
        <if_sid>86600</if_sid>
        <field name="event_type">dns$</field>
        <description>Suricata: DNS.</description>
        <options>no_full_log</options>
    </rule>

    <rule id="86604" level="0">
        <if_sid>86600</if_sid>
        <field name="event_type">tls$</field>
        <description>Suricata: TLS.</description>
        <options>no_full_log</options>
    </rule>
</group>
```

##### 3、对JSON Decoder进行测试

```shell
运行命令：
/var/ossec/bin/wazuh-logtest

在提示符下输入一段日志：

{"timestamp":"2016-05-02T17:46:48.515262+0000","flow_id":1234,"in_iface":"etho","event_type":"alert","src_jp":"16.10.10.10","src_port":5555,"dest_jp":"16.10.10.11","dest_port":80,"proto":"TCP","alert":{"action":"allowed","gid":1,"signature_id":2019236,"rev":3,"signature":"ET WEB_SERVER Possible CVE-2014-6271 Attempt in HTTP Version Number","category":"Attempted Administrator Privilege Gain","severity":1},"payload":"21YW5KX8tgdwSZIGR1cHJY2FQQgVWI","payload_printable":"this_is_an_example","stream":0,"host":"suricata.com"}

输出结果如下：
**Phase 1: Completed pre-decoding.

**Phase 2: Completed decoding.
name: 'json'
alert.action: 'allowed'
alert.category: 'Attempted Administrator Privilege Gain'
alert.gid: '1'
alert.rev: '3'
alert.severity: '1'
alert.signature: 'ET WEB_SERVER Possible CVE-2014-6271 Attempt in HTTP Version Number'
alert.signature_id: '2019236'
dest_jp: '16.10.10.11'
dest_port: '80'
event_type: 'alert'
flow_id: '1234'
host: 'suricata.com'
in_iface: 'etho'
payload: '21YW5KX8tgdwSZIGR1cHJY2FQQgVWI'
payload_printable: 'this_is_an_example'
proto: 'TCP'
src_jp: '16.10.10.10'
src_port: '5555'
stream: '0'
timestamp: '2016-05-02T17:46:48.515262+0000'

**Phase 3: Completed filtering (rules).
id: '86601'
level: '3'
description: 'Suricata: Alert - ET WEB_SERVER Possible CVE-2014-6271 Attempt in HTTP Version Number'
groups: ['ids', 'suricata']
firedtimes: '1'
mail: 'False'
**Alert to be generated.
```

通过上述日志测试，可以更好地确认规则是否被正常触发

![image-20250210120859500](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210120859500.png)

##### 4、同级Sibling解码器

假设有以下一段日志：

```shell
Apr 12 14:31:38 hostname1 securityapp: INFO: srcuser="Bob" action="called" dstusr="Alice"
```

根据上述日志格式编写的解码器如下：

```xml
<decoder name="securityapp">  
    <program_name>securityapp</program_name>  
    <regex>(\w+): srcuser="(\.+)" action="(\.+)" dstusr="(\.+)"</regex>  
    <order>type,srcuser,action,dstuser</order>
</decoder>
```

运行日志测试，输出正常：

![image-20250210134057511](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210134057511.png)

但是，如果日志格式发生了顺序上的变化，则无法成功执行解码器。

测试如下日志：

```shell
Apr 12 14:31:38 hostname1 securityapp: INFO: action="called" srcuser="Bob"
```

![image-20250210134229119](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210134229119.png)

此时，使用Sibling解码器规范，便可以有效解决上述由于顺序不同导致的问题。

```xml
<decoder name="securityapp">
    <program_name>securityapp</program_name>
</decoder>

<decoder name="securityapp">
    <parent>securityapp</parent>
    <regex>(\w+):</regex>
    <order>type</order>
</decoder>

<decoder name="securityapp">
    <parent>securityapp</parent>
    <regex>srcuser="(\.+)"</regex>
    <order>srcuser</order>
</decoder>

<decoder name="securityapp">
    <parent>securityapp</parent>
    <regex>action="(\.+)"</regex>
    <order>action</order>
</decoder>

<decoder name="securityapp">
    <parent>securityapp</parent>
    <regex>dstusr="(\.+)"</regex>
    <order>dstuser</order>
</decoder>
```

测试成功

![image-20250210140647158](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210140647158.png)

##### 5、自定义解码器

（1）先设定一个日志文件的格式

```shell
Dec 25 20:45:02 MyHost example[12345]: User 'admin' logged from '192.168.1.100'
```

（2）编辑/var/ossec/etc/decoders/local_decoder.xml，该文件用于添加用户自定义解码器

```xml
<decoder name="example">  
    <program_name>^example</program_name>
</decoder>

<decoder name="example">  
    <parent>example</parent>  
    <regex>User '(\w+)' logged from '(\d+.\d+.\d+.\d+)'</regex>  
    <order>user, srcip</order>
</decoder>
```

（3）再编辑/var/ossec/etc/rules/local_rules.xml，添加一条用户自定义规则

```xml
<rule id="100010" level="0">  
    <program_name>example</program_name>  
    <description>User logged</description>
</rule>
```

（4）运行wazuh-logtest，确认基于正确的解码器触发正确的规则

![image-20250210141217575](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210141217575.png)

#### 三、解码器实战应用

##### 1、自定义解码器和规则

针对以下日志格式，定义解码器：

```shell
Feb 19 13:25:04 ip-10-200-102-138 ttops: WSCA 10.200.100.200 ip-10-200-102-138.us-west-2.compute.internal 10.200.102.138 2021-02-19T13:24:48 21951 pts/1 ttops root /home/ttops  1256  2021-02-19_13:25:04 vim conf.txt
```

在etc/decoders/local_decoder.xml中定义解码器如下：

```xml
<decoder name="command-audit">  
    <program_name>^tt</program_name> 
</decoder>


<decoder name="command-audit-field">  
    <parent>command-audit</parent>  
    <regex>^(WSCA) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\s+\S+\s+\S+ (\.*)</regex>
    <order>tag,ssh.client.ip,server.name,server.ip,login.time,ssh.pid,tty,login_user,sudo.user,pwd,command</order> 
</decoder>

配置说明
❶ 由于原始日志头部属于标准syslog头，Wazuh内置解码器识别到program_name为ttops
❷ 子解码规则引用父解码规则
❸ 使用OSSEC正则提取字段值
❹ 定义字段名称
```

在etc/rules/local_rules.xml中定义如下规则

```xml
<rule id="100002" level="7">    
    <field name="tag">^WSCA$</field>    
    <options>no_full_log</options>    
    <description>安全命令审计-执行命令 $(command)</description>
</rule>
```

执行/var/ossec/bin/wazuh-logtest对上述日志进行测试，实现预警：

![image-20250210143238771](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210143238771.png)

##### 2、定义解码器获取MySQL的登录srcip以触发主动响应

> 总的来说，就是解码器对日志信息进行解码，并获取其中正则表达所捕获的内容，然后这些内容可以在 rules 中和 active response 中进行引用，使用 $(parametername) 进行引用
>
> 当然 rules 也是可以根据自己的 <regex> 对消息日志进行解码的 ，成功匹配rules 的 <regex> 的消息日志，就会发出对应的预警，等级就是 rule id

在MySQL的日志检测中，存在以下规则，将会触发9级预警

```xml
<rule id="50106" level="9">    
    <if_sid>50105</if_sid>    
    <match>Access denied for user</match>    
    <description>MySQL: authentication failure.</description>    
    <group>authentication_failed,pci_dss_10.2.4,pci_dss_10.2.5,pci_dss_8.7,xxxxxxx </group>
</rule>
```

但是我们设定的Active Response的级别为9级，将会触发封锁IP的firewall-drop命令：

```xml
<active-response>    
    <command>firewall-drop</command>    
    <location>local</location>    
    <level>7</level>    
    <timeout>600</timeout>
</active-response>
```

但是主动响应时获取不到IP地址，无法完成封锁，在active-response.log中出现以下错误：

```shell
2021/12/16 22:05:32 active-response/bin/firewall-drop: Cannot read 'srcip' from data
```

分析其原因，这是因为在解码器中没有正确定义获取srcip地址导致firewall-drop无法知道封锁哪个IP，虽然触发了该主动响应指令，但是IP地址并不会被封锁。修改MySQL的解码器为：

```xml
<decoder name="mysql_log">  
    <prematch>\d+ Connect</prematch>  
    <regex offset="after_prematch">Access denied for user '(\S+)'@'(\S+)' </regex>  
    <order>user, srcip</order>
</decoder>
```

执行，firewall-drop生效，发现此时已经无法在Xshell等终端访问到系统，查看iptables -nL，也可以看到IP地址被封锁。

![image-20250209220655257](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209220655257.png)

##### 3、尝试使用firewalld-drop触发firewall-cmd命令完成IP封锁

（1）修改ossec.conf，添加命令执行规则

```xml
<command>    
    <name>firewalld-drop</name>    
    <executable>firewalld-drop</executable>    
    <timeout_allowed>no</timeout_allowed>
</command>
```

（2）修改ossec.conf，配置主动响应的执行命令

```xml
<active-response>    
    <command>firewalld-drop</command>    
    <location>local</location>    
    <level>9</level>
</active-response>
```

（3）重启wazuh-manager并进行测试，尝试触发50106规则，确认IP地址是否被封锁

（4）运行命令 firewall-cmd —list-all，查看是否存在一条DROP的富规则。

```shell
  rich rules:     
  	rule family="ipv4" source address="192.168.112.1" drop
```

firewall-cmd并不会断开现有SSH连接，但是新建SSH连接将会被阻挡。另外，如果firewalld进程没有启动或者配置不正确，也许会在active-response.log中发现类似以下信息

![image-20250209220735970](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209220735970.png)

正确的active-response.log日志应该类似以下输出：

![image-20250209220749779](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209220749779.png)

> Wazuh源代码：https://github.com/wazuh/wazuh