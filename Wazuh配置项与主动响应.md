[TOC]



# ==Wazuh配置项与主动响应==

教材内容

#### 一、核心配置文件

##### 1、日志级别

```xml
<alerts>    
    <log_alert_level>3</log_alert_level>    表示除过1，2级的日志，其余都会记录在alerts.log文件中
    <email_alert_level>12</email_alert_level>  表示12级以上的警告，会进行发送邮件警告
</alerts>
```

##### 2、执行命令

```xml
<localfile>    
    <log_format>command</log_format>    
    <command>df -P</command>    
    <frequency>360</frequency>
</localfile>
```

##### 3、监控文件

```xml
<localfile>    
    <log_format>syslog</log_format>    
    <location>/var/log/secure</location>
</localfile>
```

##### 4、白名单

```xml
<global>    
    <white_list>127.0.0.1</white_list>    
    <white_list>^localhost.localdomain$</white_list>    
    <white_list>192.168.112.2</white_list>
</global>
```

##### 5、主动响应

```xml
<command>    
    <name>firewall-drop</name>    
    <executable>firewall-drop</executable>    
    <timeout_allowed>yes</timeout_allowed>
</command>
<active-response>    
    <command>firewall-drop</command>    
    <location>local</location>    
    <level>9</level>    
    <timeout>600</timeout>
</active-response>
```

> 在Linux的命令行中修改配置文件相对比较麻烦，建议直接使用VSCode远程连接到Linux，在VScode中直接修改配置项。

##### 6、主动响应执行命令

```xml
<!-- Active response -->
<global>
    <white_list>127.0.0.1</white_list>
    <white_list>^localhost.localdomain$</white_list>
    <white_list>8.8.8.8</white_list>
    <white_list>144.144.144.144</white_list>
</global>

<command>
    <name>disable-account</name>  这个是主动响应执行命令定义的“昵称”
    <executable>disable-account</executable>  这个是主动响应要执行的命令的名字
    <timeout_allowed>yes</timeout_allowed>  
</command>
```

![image-20250208230858736](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250208230858736.png)

```xml
<!--
<active-response>
	active-response options here
</active-response>
-->
```

但是，默认情况下，虽然定义的命令很多，但是在 active-response 节点中，默认并没有进行调用

#### 二、主动响应

##### 1、工作原理

![image-20211212035658191](https://gitee.com/ymq_typroa/typroa/raw/main/20211212035658.png)

##### 2、location参数

Each active response specifies where its associated command will be executed: on the agent that triggered the alert, on the manager, on another specified agent or on all agents, which also includes the manager(s). The `location` options are:

- `Local`. It runs the script on the agent that generated the alert.
- `Server`. It runs the script on the Wazuh manager.
- `Defined agent`. It specifies the IDs of the agents that run the script regardless of where the event has been observed.
- `All`. Every agent in the environment will run the script. Use with caution.

##### 3、执行的命令

（1）在Linux操作系统中，内置的脚本如下：

| Script name                                                  | Description                                                  |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| [disable-account](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/disable-account.c) | Disables an account by setting `passwd-l`                    |
| [firewall-drop](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/firewalls/default-firewall-drop.c) | Adds an IP to the iptables deny list                         |
| [firewalld-drop](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/firewalld-drop.c) | Adds an IP to the firewalld drop list                        |
| [host-deny](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/host-deny.c) | Adds an IP to the /etc/hosts.deny file                       |
| [ip-customblock](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/ip-customblock.c) | Custom OSSEC block, easily modifiable for custom response    |
| [ipfw](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/firewalls/ipfw.c) | Firewall-drop response script created for ipfw               |
| [npf](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/firewalls/npf.c) | Firewall-drop response script created for npf                |
| [wazuh-slack](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/wazuh-slack.c) | Posts modifications on Slack                                 |
| [pf](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/firewalls/pf.c) | Firewall-drop response script created for pf                 |
| [restart-wazuh](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/restart-wazuh.c) | Automatically restarts Wazuh when ossec.conf has been changed |
| [route-null](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/route-null.c) | Adds an IP to null route                                     |

（2）在Windows操作系统中，内置以下脚本：

| Script name                                                  | Description              |
| :----------------------------------------------------------- | :----------------------- |
| [netsh.exe](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/netsh.c) | Blocks an ip using netsh |
| [restart-wazuh.exe](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/restart-wazuh.c) | Restarts wazuh agent     |
| [route-null.exe](https://github.com/wazuh/wazuh/blob/4.2/src/active-response/route-null.c) | Adds an IP to null route |

##### 4、SSH连续登录失败后封锁IP地址

（1）确认SSH规则文件中存在连续登录失败的规则，如果不存在，则需要手工创建

```xml
<rule id="5712" level="10" frequency="8" timeframe="120" ignore="60">    
    <if_matched_sid>5710</if_matched_sid>    
    <description>sshd: brute force trying to get access to </description>    
    <description>the system.</description>    
    <mitre>    
        <id>T1110</id>    
    </mitre>    
    <same_source_ip ></same_source_ip>                     
    <group>authentication_failures,pci_dss_11.4,pci_dss_10.2.4,pci_dss_10.2.5,gdpr_IV_35.7.d,         gdpr_IV_32.2,hipaa_164.312.b,nist_800_53_SI.4,nist_800_53_AU.14,nist_800_53_AC.7,tsc_CC6.1,         tsc_CC6.8,tsc_CC7.2,tsc_CC7.3,    
    </group>
</rule>
```

> 上述规则是指：如果在120秒的时间内，同一个IP地址连续触发了5710的预警8次，则产生5712的预警，级别为10级。

（2）为ossec.conf添加主动响应配置

```xml
<active-response>  
    <command>firewall-drop</command>  
    <location>local</location>  
    <rules_id>5712</rules_id>  
    <timeout>1800</timeout>
</active-response>
```

> 上述配置是指：如果系统触发了5712号规则，直接直接调用firewall-drop对应的命令封锁客户端IP地址

（3）触发防火墙Drop规则

```shell
parameters.alert.previous_output: Dec 12 04:42:33 centqiang sshd[18817]: Invalid user qiang from 192.168.112.1 port 2102
Dec 12 04:42:32 centqiang sshd[18815]: Failed password for invalid user qiang from 192.168.112.1 port 2076 ssh2
Dec 12 04:42:29 centqiang sshd[18815]: Failed password for invalid user qiang from 192.168.112.1 port 2076 ssh2
Dec 12 04:42:25 centqiang sshd[18815]: Failed password for invalid user qiang from 192.168.112.1 port 2076 ssh2
Dec 12 04:42:21 centqiang sshd[18815]: Invalid user qiang from 192.168.112.1 port 2076
parameters.alert.full_log: Dec 12 04:42:36 centqiang sshd[18817]: Failed password for invalid user qiang from 192.168.112.1 port 2102 ssh2
parameters.alert.predecoder.program_name: sshd
parameters.alert.predecoder.timestamp: Dec 12 04:42:36
parameters.alert.predecoder.hostname: centqiang
parameters.alert.decoder.parent: sshdparameters.alert.decoder.name: sshd
parameters.alert.data.srcip: 192.168.112.1
parameters.alert.data.srcuser: qiang
parameters.alert.location: /var/log/secure
parameters.program: active-response/bin/firewall-drop
```

> 一旦触发Action-Response，可以在logs目录下查看action-response.log日志文件。

（4）重启防火墙恢复，或使用iptables -F清空规则。

> active-response 测试
>
> - 第一步：去 wazuh 官网查询 [How to configure Active Response](https://documentation.wazuh.com/current/user-manual/capabilities/active-response/how-to-configure.html?highlight=active&highlight=response) 然后看他给的教程
>
> - 第二步：配置 wazuh 文件 ossec.conf
>
>   比如，在这里我需要测试 firewall-drop 这个主动响应的功能如何，我需要在 ossec.conf 中找到他，然后进行调用
>
>   ```xml
>     <!-- Active response -->
>     <global>
>       <white_list>127.0.0.1</white_list>
>       <white_list>^localhost.localdomain$</white_list>
>       <white_list>8.8.8.8</white_list>
>       <white_list>144.144.144.144</white_list>
>     </global>
>   
>     <command>
>       <name>firewall-drop</name>
>       <executable>firewall-drop</executable>
>       <timeout_allowed>yes</timeout_allowed>
>     </command>
>   
>     <!--
>     <active-response>
>       active-response options here
>     </active-response>
>     -->
>   
>     <active-response>
>       <command>firewall-drop</command>
>       <location>local</location>
>       <level>7</level>  表示预警等级达到7级就执行
>       <timeout>600</timeout>  表示这条指令有效期限为600秒（阻挡 ip 十分钟）
>     </active-response>
>   ```
>
>   比如，修改成这样，记得需要编写 <active-response> 节点
>
>   ![image-20250208235503491](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250208235503491.png)
>
>   每一个参数的含义都有介绍，比如这里的 local 意思就是，执行这个主动响应脚本的设备的 location
>
>   然后重启 wazuh-manager 服务
>
> - 选择一个合适的 rule id 进行测试，这里选择 id=5712 的主动响应进行测试
>
>   ```xml
>     <rule id="5710" level="5">
>       <if_sid>5700</if_sid>
>       <match>illegal user|invalid user</match>
>       <description>sshd: Attempt to login using a non-existent user</description>
>       <mitre>
>         <id>T1110.001</id>
>         <id>T1021.004</id>
>       </mitre>
>       <group>authentication_failed,gdpr_IV_35.7.d,gdpr_IV_32.2,gpg13_7.1,hipaa_164.312.b,invalid_login,nist_800_53_AU.14,nist_800_53_AC.7,nist_800_53_AU.6,pci_dss_10.2.4,pci_dss_10.2.5,pci_dss_10.6.1,tsc_CC6.1,tsc_CC6.8,tsc_CC7.2,tsc_CC7.3,</group>
>     </rule>
>   
>     <rule id="5712" level="10" frequency="8" timeframe="120" ignore="60">
>       <if_matched_sid>5710</if_matched_sid>
>       <same_source_ip />
>       <description>sshd: brute force trying to get access to the system. Non existent user.</description>
>       <mitre>
>         <id>T1110</id>
>       </mitre>
>       <group>authentication_failures,gdpr_IV_35.7.d,gdpr_IV_32.2,hipaa_164.312.b,nist_800_53_SI.4,nist_800_53_AU.14,nist_800_53_AC.7,pci_dss_11.4,pci_dss_10.2.4,pci_dss_10.2.5,tsc_CC6.1,tsc_CC6.8,tsc_CC7.2,tsc_CC7.3,</group>
>     </rule>
>   ```
>
> - 要想触发 5712 这个主动响应，我们需要在120秒内触发5710  8次
>
>   5710的评判标准是匹配到 `illegal user|invalid user`
>
>   接下来我们试试看
>
>   ![image-20250209001411605](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209001411605.png)
>
>   ![image-20250209001623719](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209001623719.png)
>
>   ![image-20250209001640559](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209001640559.png)
>
>   直接给我强制断线
>
> - 使用 `iptables -F` 直接清空 iptables 配置
>
>   ![image-20250209003058295](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209003058295.png)
>
>   重连成功
>
> - ![image-20250209003500893](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209003500893.png)

> 我们可以使用 `ls /var/ossec/ruleset/rules | xargs grep 2502` 这样的命令 来查找 /var/ossec/logs/alerts/alerts.log 文件中出现的 不知名的 id 号
>
> ![image-20250209003709755](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209003709755.png)
>
> 然后进入相对应的文件去看，该预警信息配置是怎样的
>
> ![image-20250209003918467](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250209003918467.png)
