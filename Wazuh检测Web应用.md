[TOC]



# ==Wazuh检测Web应用==

#### 一、配置VAuditDemo环境

1、安装VAuditDemo

配置端口为81，httpd.conf中Listen 81，再Include etc/extra/httpd-vhosts.conf，在 httpd-vhosts.conf 中指定VAuditDemo的目录。

2、确保Apache的AccessLog可以正常访问

3、在ossec.conf中添加对access_log文件的检测

```xml
<localfile>    
    <log_format>syslog</log_format>    
    <location>/opt/lampp/logs/access_log</location>
</localfile>
```

#### 二、检测状态码异常

##### 1、为404和403状态码设置规则

（1）在 ruleset/decoders/0375-web-accesslog_decoders.xml 中存在以下解码器，看起来比较匹配Apache的日志

```xml
<decoder name="web-accesslog-ip">    
    <type>web-log</type>    
    <parent>web-accesslog</parent>    
    <regex>^(\S+) \S+ \S+ \.*[\S+ \S\d+] "(\w+) (\S+) HTTP\S+" (\d+) </regex>    
    <order>srcip, protocol, url, id</order>
</decoder>


192.168.112.1 - - [17/Dec/2021:02:09:17 +0800] "GET /dashboard/phpinfo.php HTTP/1.1" 200 110370
```

（2）在 ruleset/rules/0245-web_rules.xml 中未找到专门针对403和403状态码的规则，所以此处对31101规则进行修改，修改结果如下：

```xml
<rule id="31101" level="5" >    
    <if_sid>31100</if_sid>    
    <id>^404$</id>    
    <description>Web server 404 error code.</description>    
    <group>attack,pci_dss_6.5,pci_dss_11.4,gdpr_IV_35.7.d,nist_800_53_SA.11,xxxxxxx,</group>
</rule>
```

并在其下方添加一条阈值预警的规则：

```xml
<rule id="561103" level="10" frequency="5" timeframe="30">    
    <if_matched_sid>31101</if_matched_sid>    
    <same_source_ip></same_source_ip>    
    <description>同一个IP地址不停出现404状态码，疑似扫描.</description>    
    <group>attack,</group>
</rule>
```

![image-20250211012025389](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211012025389.png)

##### 2、访问不存在URL地址多次

```shell
** Alert 1639679514.43828: - web,accesslog,attack,

2021 Dec 17 02:31:54 centqiang->/opt/lampp/logs/access_log

Rule: 561103 (level 10) -> '同一个IP地址不得出现404状态码，疑似扫描.'

Src IP: 192.168.112.1

192.168.112.1 - [17/Dec/2021:02:31:53 +0800] "GET /messages.php HTTP/1.1" 404 1048
192.168.112.1 - [17/Dec/2021:02:31:51 +0800] "GET /messages.php HTTP/1.1" 404 1048
192.168.112.1 - [17/Dec/2021:02:31:49 +0800] "GET /messages.php HTTP/1.1" 404 1048
192.168.112.1 - [17/Dec/2021:02:31:48 +0800] "GET /messages.php HTTP/1.1" 404 1048
192.168.112.1 - [17/Dec/2021:02:31:37 +0800] "GET /messages.php HTTP/1.1" 404 1048
```

![image-20250211012002310](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211012002310.png)

![image-20250211012113626](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211012113626.png)

##### 3、访问PHPMyadmin多次

操作同上，设定403状态码即可，与此类似，所有的异常状态码均可以设定相应的预警规则。

#### 三、识别暴力破解登录

##### 1、暴力破解的识别标志

从access_log中识别出POST请求，并且频繁发送到 user/logCheck.php ，则可以断定为爆破。

```shell
192.168.112.1 - - [20/Dec/2021:16:29:42 +0800] "POST /user/logCheck.php HTTP/1.1" 302 -
```

##### 2、为爆破设定规则

```xml
<group name="web,accesslog,">  
    <rule id="561103" level="5">    
        <if_sid>31100</if_sid>    
        <id>^403$</id>    
        <description>Web server 403 error code.</description>    
        <group>attack,</group>  
    </rule>  
    
    <rule id="561104" level="5">    
        <if_sid>31100</if_sid>    
        <url>user/logCheck.php</url>    
        <description>某个IP地址正在登录.</description>    
        <group>attack,</group>  
    </rule>  
    
    <rule id="561105" level="10" frequency="5" timeframe="30">    
        <if_matched_sid>561104</if_matched_sid>    
        <description>相同IP地址的用户在频繁登录，疑似暴力破解.</description>    
        <group>attack,</group>  
    </rule>
</group>
```

##### 3、测试上述规则

![image-20250211013220023](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211013220023.png)

> 为什么会出现31108而不是561104呢？那是因为31108被首先匹配了，怎么办呢？要么修改为 noalert=”1”， 要么自定义规则编号设为31108，并且配置 overwrite=”yes”
> 思考：通过URL地址来进行登录和爆破检测存在什么问题？应该如何解决? 尝试解决发现，会出现混乱的情况，比如 200 的响应码，我们登录访问 user/logcheck.php 的响应码一定是 200 的，那么要想跳过 31108 就需要让他不匹配 200 ，但很显然这是不可能的 

##### 4、异常处理

如果规则文件，或配置文件，或规则编号重复等情况，均会导致wazuh-manager启动不成功，可以使用命令查看具体信息：

```shell
systemctl status wazuh-manager

Dec 17 03:06:38 centqiang env[41469]: 2021/12/17 03:06:38 wazuh-analysisd: ERROR: Duplicate rule ID:561103
Dec 17 03:06:38 centqiang env[41469]: 2021/12/17 03:06:38 wazuh-analysisd: CRITICAL: (1220): Error loading the rules: 'etc/rules...es.xml'.
```

另外，详细的错误日志也可以查看 /var/log/message，如

```shell
Dec 17 03:06:36 centqiang systemd: Starting Wazuh manager...
Dec 17 03:06:38 centqiang env: 2021/12/17 01:06:38 wazuh-analysisd: ERROR: Duplicate rule ID:561103
Dec 17 03:06:38 centqiang env: 2021/12/17 01:06:38 wazuh-analysisd: CRITICAL: (1220): Error loading the rules: 'etc/rules/local_rules.xml'.
```

#### 四、识别SQL注入

##### 1、编写一个SQL注入规则

```xml
<rule id="561301" level="8">    
    <regex>union|select|order by|and|or</regex>       
    <description>疑似SQL注入</description>
</rule>
<rule id="561302" level="10" frequency="5" timeframe="20">    
    <if_matched_sid>561301</if_matched_sid>    
    <same_source_ip ></same_source_ip>           
    <description>正在尝试连续SQL注入</description>
</rule>
```

##### 2、对于关键字进行匹配和确认

包括 updatexml, database(), user(), extract等进行匹配

##### 3、其他因素的影响

（1）由于Access Log只保存URL地址信息，也就是说只针对GET请求可以检测，POST请求正文则不行。

（2）由于正则匹配无法针对绕过WAF的一些手段进行匹配，所以检测规则也并非万能的。