[TOC]



# ==Wazuh配置预警规则==

> 解码器的作用就是判断这到底是哪一类的日志，解析非结构化日志提取字段值

#### 一、Rule语法规则

##### 1、Rule的级别定义

https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html

| Level | Title                            | Description                                                  |
| :---- | :------------------------------- | :----------------------------------------------------------- |
| 0     | Ignored                          | No action taken. Used to avoid false positives.These rules are scanned before all the others.They include events with no security relevance. 用来避免误报，这里没有安全问题 |
| 2     | System low priority notification | System notification or status messages. They have no security relevance. 系统提示或状态信息，与安全无关的事件 |
| 3     | Successful/Authorized events     | They include successful login attempts, firewall allow events, etc. 登录成功或未违反防火墙规则的事件 |
| 4     | System low priority error        | Errors related to bad configurations or unused devices/applications.They have no security relevance and are usually caused by default installations or software testing. 无效的配置或不常用的应用程序相关的错误，没有安全风险 |
| 5     | User generated error             | They include missed passwords, denied actions, etc. By itself they have no security relevance. 在没有安全风险的前提下，出现的密码错误，某些被拒绝的操作等 |
| 6     | Low relevance attack             | They indicate a worm or a virus that have no affect to the system (like code red for apache servers, etc).They also include frequently IDS events and frequently errors. 对系统没有威胁的蠕虫或病毒(例如Linux机器上的Windows蠕虫) |
| 7     | “Bad word” matching              | They include words like “bad”, “error”, etc.These events are most of the time unclassified and may have some security relevance. 一些有风险的关键字出现在日志中，比如 bad，error之类的单词 |
| 8     | First time seen                  | Include first time seen events. First time an IDS event is fired or the first time an user logged in.It also includes security relevant actions (like the starting of a sniffer or something like that). 首次出现的事件 |
| 9     | Error from invalid source        | Include attempts to login as an unknown user or from an invalid source.May have security relevance (specially if repeated).They also include errors regarding the “admin” (root) account. 存在一定安全风险，比如以未知用户名登录，或无效的源信息等，比如可能存在爆破风险 |
| 10    | Multiple user generated errors   | They include multiple bad passwords, multiple failed logins, etc.They may indicate an attack or may just be that a user just forgot his credentials. 出现多次密码错误的尝试，或者多次登录失败的操作等，存在较高安全风险 |
| 11    | Integrity checking warning       | They include messages regarding the modification of binaries or the presence of rootkits (by Rootcheck).They may indicate a successful attack. Also included IDS events that will be ignored (high number of repetitions). 文件完整性检查不通过，可能被篡改，很有可能攻击成功，或被IDS忽略的大量重复的事件 |
| 12    | High importance event            | They include error or warning messages from the system, kernel, etc.They may indicate an attack against a specific application. 非常重要的安全风险，要引起重视 |
| 13    | Unusual error (high importance)  | Most of the times it matches a common attack pattern. 高风险，多次匹配到攻击行为 |
| 14    | High importance security event   | Most of the times done with correlation and it indicates an attack. 多个检测规则形成关联结果 |
| 15    | Severe attack                    | No chances of false positives. Immediate attention is necessary. 极其严重的安全事件，不存在误报的可能，必须立即处理 |

##### 2、规则配置字段详解

| Option                                                       | Values                                                       | Description                                                  |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [rule](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#rule) | See [table](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#rule) below. | Its starts a new rule and its defining options. 创建一条新的规则字段 |
| [match](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#match) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will attempt to find a match in the log using [sregex](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html#sregex-os-match-syntax) by default, deciding if the rule should be triggered. 简单的匹配，不支持完整的正则表达式语法，通常用于包含某个字符串 |
| [regex](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#regex-rules) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It does the same as `match`, but with [regex](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html#regex-os-regex-syntax) as default. 标准的正则表达式匹配模式 |
| [decoded_as](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#decoded-as) | Any decoder’s name.                                          | It will match with logs that have been decoded by a specific decoder. 指定具体的解码器，用于快速建立解码器与规则之间的关联 |
| [category](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#category) | Any [type](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#type). | It will match with logs whose decoder’s [type](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#type) concur. 指定匹配解码器的类型 |
| [field](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#field) | Name and any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a field extracted by the decoder in [order](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/decoders.html#order) with a regular expression. 匹配解码器中正则表达式提取出来的变量的值 |
| [srcip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#srcip) | Any IP address.                                              | It will compare the IP address with the IP decoded as `srcip`. Use “!” to negate it. 攻击源IP，通常用于记录溯源或触发主动响应的参数，!srcip表示非 |
| [dstip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#dstip) | Any IP address.                                              | It will compare the IP address with the IP decoded as `dstip`. Use “!” to negate it. 攻击目标IP地址 |
| [srcport](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#srcport) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a port with a value decoded as `srcport`. 攻击源端口 |
| [dstport](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#dstport) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a port with a value decoded as `dstport`. 攻击目标商品 |
| [data](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#data) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a data with a value decoded as `data`. 匹配从解码器的正则表达式中提取的字段名，匹配成功规则才会被执行 |
| [extra_data](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#extra-data) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a extra data with a value decoded as `extra_data`. 同上，用于匹配正则表达式中提取的字段名 |
| [user](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#user) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a user with a value decoded as `user`. 同上，用一匹配user字段 |
| [system_name](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#system-name) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a system name with a value decoded as `system_name`. 同上，用于匹配system_name字段 |
| [program_name](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#program-name) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a program name with a value pre-decoded as `program_name`. 同上 |
| [protocol](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#protocol) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a protocol with a value decoded as `protocol`. 同上 |
| [hostname](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#hostname) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a hostname with a value pre-decoded as `hostname`. 同上 |
| [time](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#time) | Any time range. e.g. (hh![:mm-hh:](http://www.emoji-cheat-sheet.com/graphics/emojis/mm-hh.png)mm) | It checks if the event was generated during that time range. 确定事件产生的时间范围，如果非正确的时间范围，则规则匹配失败 |
| [weekday](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#weekday) | monday - sunday, weekdays, weekends                          | It checks whether the event was generated during certain weekdays.同上 |
| [id](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#id) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing an ID with a value decoded as `id` 同上 |
| [url](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#url) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a URL with a value decoded as `url` 同上 |
| [location](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#location) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a location with a value pre-decoded as `location`. 同上 |
| [action](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#action) | Any String or [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a string or regular expression representing an action with a value decoded as `action`. 同上 |
| [status](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#status) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a status with a value decoded as `status`. 同上 |
| [srcgeoip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#srcgeoip) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a GeoIP source with a value decoded as `srcgeoip`. 同上 |
| [dstgeoip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#dstgeoip) | Any [regular expression](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/regex.html). | It will compare a regular expression representing a GeoIP destination with a value decoded as `dstgeoip`. 同上 |
| [if_sid](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#if-sid) | A list of rule IDs separated by commas or spaces.            | It works similar to parent decoder. It will match when a rule ID on the list has previously matched. 对应的rule ID匹配成功后才会匹配该rule，与父解码器类似 |
| [if_group](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#if-group) | Any group name.                                              | It will match if the indicated group has matched before. 同上 |
| [if_level](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#if-level) | Any level from 1 to 16.                                      | It will match if that level has already been triggered by another rule. 同上 |
| [if_matched_sid](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#if-matched-sid) | Any rule ID (Number).                                        | Similar to `if_sid` but it will only match if the ID has been triggered in a period of time. 与指定if_sid类似，但是用于设定阈值预警规则用 |
| [if_matched_group](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#if-matched-group) | Any group name.                                              | Similar to `if_group` but it will only match if the group has been triggered in a period of time. 同上 |
| [same_id](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-id) | None.                                                        | The decoded `id` must be the same. 解码器的id字段必须相同才会触发预警，通常用于阈值预警 |
| [not_same_id](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#not-same-id) | None.                                                        | The decoded `id` must be different. 与上相反，新版本中不再适用 |
| [different_id](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-id) | None.                                                        | The decoded `id` must be different. 同上，适用于新版本       |
| [same_source_ip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-source-ip) | None.                                                        | The decoded `srcip` must be the same. srcip必须相同          |
| [not_same_source_ip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#not-same-source-ip) | None.                                                        | The decoded `srcip` must be different. 与上相反              |
| [same_srcip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-srcip) | None.                                                        | The decoded `srcip` must be the same.                        |
| [different_srcip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-srcip) | None.                                                        | The decoded `srcip` must be different.                       |
| [same_dstip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-dstip) | None.                                                        | The decoded `dstip` must be the same. dstip必须相同          |
| [different_dstip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-dstip) | None.                                                        | The decoded `dstip` must be different.                       |
| [same_srcport](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-srcport) | None.                                                        | The decoded `srcport` must be the same.                      |
| [different_srcport](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-srcport) | None.                                                        | The decoded `srcport` must be different.                     |
| [same_dstport](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-dstport) | None.                                                        | The decoded `dstport` must be the same.                      |
| [different_dstport](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-dstport) | None.                                                        | The decoded `dstport` must be different.                     |
| [same_location](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-location) | None.                                                        | The `location` must be the same.                             |
| [different_location](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-location) | None.                                                        | The `location` must be different.                            |
| [same_srcuser](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-srcuser) | None.                                                        | The decoded `srcuser` must be the same.                      |
| [different_srcuser](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-srcuser) | None.                                                        | The decoded `srcuser` must be different.                     |
| [same_user](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-user) | None.                                                        | The decoded `user` must be the same.                         |
| [not_same_user](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#not-same-user) | None.                                                        | The decoded `user` must be different.                        |
| [different_user](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-user) | None.                                                        | The decoded `user` must be different.                        |
| [not_same_agent](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#not-same-agent) | None.                                                        | The decoded `agent` must be different.                       |
| [same_field](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-field) | None.                                                        | The decoded `field` must be the same as the previous ones.   |
| [not_same_field](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#not-same-field) | None.                                                        | The decoded `field` must be different than the previous ones. |
| [different_field](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-field) | None.                                                        | The decoded `field` must be different than the previous ones. |
| [same_protocol](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-protocol) | None.                                                        | The decoded `protocol` must be the same.                     |
| [different_protocol](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-protocol) | None.                                                        | The decoded `protocol` must be different.                    |
| [same_action](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-action) | None.                                                        | The decoded `action` must be the same.                       |
| [different_action](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-action) | None.                                                        | The decoded `action` must be different.                      |
| [same_data](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-data) | None.                                                        | The decoded `data` must be the same.                         |
| [different_data](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-data) | None.                                                        | The decoded `data` must be different.                        |
| [same_extra_data](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-extra-data) | None.                                                        | The decoded `extra_data` must be the same.                   |
| [different_extra_data](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-extra-data) | None.                                                        | The decoded `extra_data` must be different.                  |
| [same_status](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-status) | None.                                                        | The decoded `status` must be the same.                       |
| [different_status](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-status) | None.                                                        | The decoded `status` must be different.                      |
| [same_system_name](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-system-name) | None.                                                        | The decoded `system_name` must be the same.                  |
| [different_system_name](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-system-name) | None.                                                        | The decoded `system_name` must be different.                 |
| [same_url](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-url) | None.                                                        | The decoded `url` must be the same.                          |
| [different_url](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-url) | None.                                                        | The decoded `url` must be different.                         |
| [same_srcgeoip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-srcgeoip) | None.                                                        | The decoded `srcgeoip` must the same.                        |
| [different_srcgeoip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-srcgeoip) | None.                                                        | The decoded `srcgeoip` must be different.                    |
| [same_dstgeoip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#same-dstgeoip) | None.                                                        | The decoded `dstgeoip` must the same.                        |
| [different_dstgeoip](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#different-dstgeoip) | None.                                                        | The decoded `dstgeoip` must be different.                    |
| [description](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#description) | Any String.                                                  | Provides a human-readable description to explain what is the purpose of the rule. Please, use this field when creating custom rules. |
| [list](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#list) | Path to the CDB file.                                        | Perform a CDB lookup using an ossec list.                    |
| [info](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#info) | Any String.                                                  | Extra information using certain attributes.                  |
| [options](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#options) | See the table [below.](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#options) | Additional rule options that can be used. 附加选项           |
| [check_diff](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#check-diff) | None.                                                        | Determines when the output of a command changes.             |
| [group](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#group) | Any String.                                                  | Add additional groups to the alert.                          |
| [mitre](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#mitre) | See [Mitre table](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#mitre) below. | Contains Mitre Technique IDs that fit the rule               |
| [var](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#var) | Name for the variable. Most used: [BAD_WORDS](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html#bad-words) | Defines a variable that can be used anywhere inside the same file. |

#### 二、规则的层次划分

##### 1、根规则与派生规则(Parent/Child)

（1）根规则：就是基础规则，只负责区分规则类别。

（2）派生规则：可以引用根规则去做更细节的过滤和匹配，从而派生出更具体的描述安全事件的规则。

```xml
<rule id="5700" level="0" noalert="1">
    <decoded_as>sshd</decoded_as>
    <description>SSHD messages grouped.</description>
</rule>

<rule id="5710" level="5">
    <if_sid>5700</if_sid>
    <match>illegal user|invalid user</match>
    <description>sshd: Attempt to login using a non-existent user</description>
    <mitre>
        <id>71110</id>
    </mitre>
    <group>invalid_login,authentication_failed,pcj_dss_10.2.4,xxxxx,</group>
</rule>

规则说明：
规则 ID 5700 是根规则，它代表的是与 SSHD 这个进程相关的事件。

规则 ID 5710 是 5700 的派生规则，引用根规则后，进一步进行匹配派生出更具有可描述性的事件。

派生规则引用根规则的方法，使用 if_sid 字段，与关联规则使用的 if_matched_sid 有所区别，区别在下面会进行阐述，可以重点关注下。
```

派生规则ID(5710)引用规则ID(5700)为根规则,进行条件匹配 `illegal user|invalid user`后 形成了 `sshd: Attempt to login using a non-existent user` 事件

> 1. **规则 ID 5700**：
>    - 这是一个根规则，用于分组与 SSHD 进程相关的事件。
>    - `decoded_as` 指定了解码类型为 `sshd`。
>    - `noalert="1"` 表示此规则不会生成警报。
> 2. **规则 ID 5710**：
>    - 这是一个派生规则，引用根规则 `5700`。
>    - 使用 `<if_sid>5700</if_sid>` 引用根规则。
>    - `<match>` 字段匹配日志中的关键字 `illegal user` 或 `invalid user`。
>    - 描述为 `sshd: Attempt to login using a non-existent user`，表示尝试使用不存在的用户登录。
>    - `mitre` 部分包含 Mitre ATT&CK 框架的 ID `71110`。
>    - `group` 字段定义了规则所属的组，如 `invalid_login`、`authentication_failed` 等。
>
> ### 派生规则引用说明：
>
> - 派生规则通过 `<if_sid>` 引用根规则，与 `<if_matched_sid>` 有所区别，具体区别未在内容中详细说明，但可以关注其使用场景。

##### 2、原子规则和关联规则(Atomic/Composite)

（1）原子规则：用于描述发生的个别事件，各个事件之间没有相关性，比如说发生了一次登录失败或发生了一次登录成功 但我们无从得知，发生了多少次登录失败，或者说多少次登录失败后发生了登录成功。

（2）关联规则：将一段时间内的多个事件相关联，譬如可以知道在某个时间段，同一个源地址IP发生了多少次登录失败，从而识别为暴力破解事件。

```xml
<rule id="100302" level="3">
    <if_sid>86620</if_sid>
    <field name="event_name">login_audit$</field>
    <field name="app_type">web$</field>
    <field name="http.results">failed$</field>
    <description>Suricata Rules - $(event_name). $(srcip) -> $(http.email) -> $(http.hostname) -> $(http.url) = $(http.results).</description>
    <options>no_full_log</options>
    <group>login_audit,authentication_failures,</group>
</rule>

<rule id="100401" level="7" frequency="20" timeframe="120" ignore="300">
    <if_matched_sid>100302</if_matched_sid> <!-- login_audit failed web -->
    <same_source_ip />
    <description>Nazuh Rules - Multiple login failures events from same IP ($IP_FREQ hit/$IP_TIME sec). $(srcip) -> $(http.email) -> $(http.hostname) -> $(http.url) = $(http.results).</description>
    <options>no_full_log</options>
    <group>brute_force_web,</group>
</rule>


规则说明：
规则 ID 100302 是原子规则，在这个例子里它表示登录失败的事件规则。

规则 ID 100401 是 100302 的关联规则。

关联规则 ID 100401，定义了在 120 秒的时间范围内发生次数达到 20 次，则触发该规则。

使用 if_matched_sid 字段来引用原子规则 100302，与 if_sid 的区别在于，前者需要在时间范围内发生，后者则没有时间的概念。

same_source_ip 代表同一个源地址 IP 进行的访问。

ignore="300"  表示100401触发之后的 300 秒内不会再被触发
```

规则说明：在120s为统计周期内，同一个源IP地址发生超过20次登录失败，触发告警规则

> 1. **XML 规则部分**：
>    - 规则 100302 是原子规则，用于匹配登录失败的事件。
>    - 规则 100401 是关联规则，基于 100302 的匹配结果，在 120 秒内达到 20 次登录失败时触发。
>    - 包含字段匹配、描述、选项和分组信息。
> 2. **汉字说明部分**：
>    - 解释了规则 100302 和 100401 的关系。
>    - 提到 `if_matched_sid` 的使用方法及其与 `if_sid` 的区别。
>    - 说明 `same_source_ip` 表示同一源 IP 的访问。

##### 3、关联规则的用法

（1）某个事件数目出现次数

```xml
<rule id="102399" level="10" frequency="30" timeframe="900">
    <if_matched_group>nids_phase1</if_matched_group>
    <options>no_full_log</options>
    <group>suricata_alert_phase2,nids_phase2</group>
    <description>Phase 2: Alarm - Phase 1 Alarm of occurred 60 times within 900 seconds. $(srcip) -> $(dstip) -> $(alert.signature) -> $(alert.signature_id).</description>
</rule>


字段说明：
frequency：定义事件发生的次数 >= 30 次。

timeframe：定义事件检测时间窗口在 900 秒内。
```

> 1. **XML 规则部分**：
>    - 规则 ID 102399 是一个高级规则，级别为 10。
>    - 使用 `if_matched_group` 引用组 `nids_phase1`。
>    - 在 900 秒内，如果事件发生次数达到 30 次，则触发该规则。
>    - 描述中包含了源 IP、目标 IP、警报签名和签名 ID 的信息。
>    - 规则分组为 `suricata_alert_phase2` 和 `nids_phase2`。
> 2. **汉字说明部分**：
>    - 解释了 `frequency` 和 `timeframe` 字段的含义。
>    - `frequency` 表示事件发生的次数阈值。
>    - `timeframe` 表示事件检测的时间窗口。

（2）某事件A之后发生了事件B

```xml
<rule id="100410" level="12" timeframe="900">
    <if_matched_sid>100409</if_matched_sid>  <!-- login_audit failed app -->
    <if_sid>100303</if_sid>  <!-- login_audit success app -->
    <same_field>http.device_id</same_field>
    <description>Wazuh Rules - Multiple authentication failures from same device_id, followed by a success ($BRUTE_TIME sec).</description>
</rule>

字段说明：
A 事件：login_audit failed app（登录审计失败事件）。

B 事件：login_audit success app（登录审计成功事件）。
```

> 1. **XML 规则部分**：
>    - 规则 ID 100410 是一个高级规则，级别为 12。
>    - 使用 `if_matched_sid` 引用规则 100409（登录审计失败事件）。
>    - 使用 `if_sid` 引用规则 100303（登录审计成功事件）。
>    - 通过 `same_field` 匹配 `http.device_id`，表示同一设备 ID 的事件。
>    - 描述中表示在同一设备 ID 上发生多次认证失败后，紧接着发生一次成功登录的事件。
> 2. **汉字说明部分**：
>    - 解释了 A 事件和 B 事件的含义。
>    - A 事件为登录审计失败事件。
>    - B 事件为登录审计成功事件。

（3）连续多次事件中某个字段出现不同的值，针对JSON动态字段

```xml
<rule id="100413" level="7" frequency="10" timeframe="900" ignore= "120">        
    <if_matched_sid>100411</if_matched_sid>        
    <same_field>http.device_id</same_field>        
    <diffrent_field>http.email</not_same_field>        
    <description>XXXXXXXXXXXXXX</description>
</rule>

规则说明
规则匹配事件的http.email字段值出现不同的类型
匹配事件的 json 数据中 http.device_id 的值要一样
```

定义以下规则，并对其进行测试.

```xml
<group name="json_log,">
    <!-- {"key":"value", "key2":"AAAA"} -->
    <rule id="110001" level="3">  
        <decoded_as>json</decoded_as>  
        <field name="key">value</field>  
        <description>Testing JSON alert</description>
    </rule>

    <rule id="110002" level="10" frequency="4" timeframe="60">  
        <if_matched_sid>110001</if_matched_sid>  
        <same_field>key2</same_field>  
        <description>Testing same_field option</description>
    </rule>
</group>
```

请按照以下序列进行测试

```json
{"key":"value", "key2":"AAAA"}
{"key":"value", "key2":"BBBB"}
{"key":"value", "key2":"CCCC"}
{"key":"value", "key2":"AAAA"}
{"key":"value", "key2":"AAAA"}
{"key":"value", "key2":"AAAA"}
{"key":"value", "key2":"AAAA"}
```

> 类似的，针对JSON动态字段，也可以使用<different_field>key2</different_field>
>
> 如果是针对内置的静态字段，如user字段，则使用same_user或different_user等
>
> ![image-20250211005348616](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211005348616.png)

#### 三、规则应用实例

> ![image-20250210205054982](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210205054982.png)
>
> 如果 wazuh 无法启动，报错，怎么查看完整错误信息？
>
> 在 `/var/log/message` 日志文件中存在系统所有日志信息
>
> ![image-20250210204934931](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210204934931.png)

##### 1、使用local_rules.xml覆盖原始规则

先为MySQL设置正确的解码器如下：

```xml
<decoder name="mysql_log">  
    <prematch>\d+ Connect|\d+ Query</prematch>  
    <regex offset="after_prematch">Access denied for user '(\S+)'@'(\S+)'</regex>  
    <order>user, srcip</order>
</decoder>
```

同时，将上述解码器放置于etc/decoders/local_decoder.xml文件中

![image-20250210204330427](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210204330427.png)

同时在ossec.conf中，使用以下配置禁用ruleset/decoders/0150-mysql_decoders.xml，否则，如果对wazuh的规则库进行更新时，ruleset文件夹中所有的解码器规则将会被覆盖。

```xml
<decoder_exclude>0150-mysql_decoders.xml</decoder_exclude>
```

同样的，对文件夹`/var/ossec/ruleset/rules`内的任何规则文件所做的更改也将在规则库更新过程中丢失。但是，对于rules来说，我们可以将覆盖原始规则的overwrite属性设置为yes，并将新规则写入到local_rules.xml文件中，这样旧的规则rules文件将会失败。当然，也可以像decoder一样，将对应的MySQL的规则文件进行排除，再重新写入自己的规则文件。

![image-20250210210007592](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210210007592.png)

![image-20250210205316445](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210205316445.png)

另外，请在本实验中，一并关注字段过滤和字段引用的使用方式，以及阈值设定等规则的使用。

```xml
<group name="mysql_log,">  
  <rule id="50100" level="0" overwrite="yes">    
    <decoded_as>mysql_log</decoded_as>    
    <description>MySQL messages grouped.</description>  
  </rule>  
    
  <rule id="50105" level="3" overwrite="yes">    
    <if_sid>50100</if_sid>    
    <regex>\d+ Connect</regex>    
    <description>MySQL: 用户$(dstuser)正在登录.</description>    
    <mitre>      
      <id>T1078</id>    
    </mitre>    
    <group>authentication_success,</group>  
  </rule>  
  
  <rule id="50106" level="9" overwrite="yes">    
    <if_sid>50105</if_sid>    
    <match>Access denied for user</match>    
    <description>MySQL: 用户$(dstuser)登录失败.</description>    
    <group>authentication_failed,</group>  
  </rule>  
  
  <rule id="50107" level="7" overwrite="yes">    
    <if_sid>50106</if_sid>    
    <match>Access denied for user</match>    
    <description>MySQL: 外连用户qiang登录失败.</description>    
    <user>qiang</user>    
    <group>authentication_failed,</group>  
  </rule>  
  
  <rule id="50108" level="3" overwrite="yes">    
    <if_sid>50100</if_sid>    
    <match>select @@version_comment limit 1</match>    
    <description>MySQL: 用户$(dstuser)登录成功.</description>    
    <group>authentication_success,mysql_query</group>  
  </rule>  
    
	<rule id="50109" level="7" frequency="3" timeframe="60" ignore="30">
    <if_matched_sid>50106</if_matched_sid>
    <different_user/>
    <description>MySQL: 相同IP: $(srcip)，不同User: $(dstuser)正在登录.</description>
    <group>authentication_success,mysql_query</group>
  </rule>
  
  <!-- 新增检测暴力破解 -->  
  <rule id="561002" level="12" frequency="5" timeframe="30">    
    <if_matched_sid>50106</if_matched_sid>    
    <description>多次登录失败，疑似暴力破解，用户名：$(dstuser).</description>    
    <group>attack,</group>  
  </rule>
</group>
```

我们可以发现，自己定义的这些 rules id 在 wazuh 默认的 rules 库中已经存在了，但为什么在这里还能使用呢，甚至连 overwrite都没有使用？就是因为，我们在 ossec.cnf 文件中已经将 wazuh 默认的 mysql_rules 库和 mysql-decoder 解码器屏蔽掉了，所以自己新定义的 mysql_rules 库就可以沿用原来的 id

**同时注意，我们在解码器中获取字段信息时，用户信息使用 user 来捕获，但是传到 rules 中，我们就需要使用 detuser 来接收**

> ### 规则说明：
>
> 1. **规则 50100**：
>    - 根规则，用于分组 MySQL 日志消息。
>    - `decoded_as` 指定解码类型为 `mysql_log`。
> 2. **规则 50105**：
>    - 派生规则，匹配 MySQL 连接事件。
>    - 使用正则表达式 `\d+ Connect` 匹配连接日志。
>    - 描述为“用户 $(dstuser) 正在登录”。
>    - 关联 Mitre ATT&CK 框架 ID `T1078`。
> 3. **规则 50106**：
>    - 派生规则，匹配 MySQL 登录失败事件。
>    - 匹配关键字 `Access denied for user`。
>    - 描述为“用户 $(dstuser) 登录失败”。
> 4. **规则 50107**：
>    - 派生规则，匹配特定用户 `qiang` 的登录失败事件。
>    - 描述为“外连用户 qiang 登录失败”。
> 5. **规则 50108**：
>    - 派生规则，匹配 MySQL 查询事件。
>    - 匹配关键字 `select @@version_comment limit 1`。
>    - 描述为“用户 $(dstuser) 登录成功”。
> 6. **规则 501002**：
>    - 新增规则，用于检测暴力破解行为。
>    - 在 30 秒内登录失败次数达到 5 次时触发。
>    - 描述为“多次登录失败，疑似暴力破解，用户名：$(dstuser)”。
>
> ------
>
> ### 完整内容总结：
>
> 1. **规则组**：`mysql_log` 组包含多个规则，用于处理 MySQL 日志中的连接、登录和查询事件。
> 2. **规则关系**：
>    - 规则 50100 是根规则。
>    - 规则 50105、50106、50107、50108 是派生规则，分别处理连接、登录失败、特定用户登录失败和登录成功事件。
>    - 规则 501002 是新增规则，用于检测暴力破解行为。
> 3. **字段说明**：
>    - `if_sid` 用于引用父规则。
>    - `match` 和 `regex` 用于匹配日志中的关键字或正则表达式。
>    - `description` 描述规则的作用。
>    - `group` 定义规则所属的组。

使用wazuh-logtest进行测试，并输入以下日志，看看具体的执行结果。

```shell
9 Connect	Access denied for user 'root'@'192.168.230.1' (using password: YES)
12 Connect    Access denied for user 'remote'@'192.168.230.1' (using password: YES)
211218  19:56:44        8 Connect    root@192.168.112.1 as anonymous on

持续尝试输入多次第三行的内容，确认是否触发561002规则，并同时在真实的MySQL客户端生成以上日志，确认预警规则的正确性。
```

![image-20250210212313025](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210212313025.png)

![image-20250210212538151](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210212538151.png)

![image-20250210212954352](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210212954352.png)

![image-20250210212403292](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210212403292.png)

![image-20250210212630697](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210212630697.png)

![image-20250210213042783](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210213042783.png)

##### 2、使用noalert属性忽略警告

为50105号规则设置noalert=”1”，看看会发生什么？

```xml
<rule id="50105" level="3" overwrite="yes" noalert="1">    
    <if_sid>50100</if_sid>    
    <regex>\d+ Connect</regex>    
    <description>MySQL: 用户$(dstuser)正在登录.</description>    
    <mitre>      
        <id>T1078</id>    
    </mitre>    
    <group>authentication_success,</group>
</rule>
```

此时用户 root 登录时，就不会再报 50105 的预警了只会报 50106 的预警，但是如果将 50106 使用 noalert="1" 操作了之后，啥预警都没有了，除非使用 remote 用户再登录 才会有个 50107 的预警，同理可得依次往下推

![image-20250210213605623](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210213605623.png)

如果我将 50105 和 50106 都使用 noalert="1" ，那么再使用 root 登录：

![image-20250210213804254](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250210213804254.png)

从测试结果可以看出，50105的规则将不会触发告警，但是如果50106、50107，50108任意一条规则满足，仍然不影响告警。接下来继续对50106设置noalert=”1”,继续观察对应的警告，并总结其规律。分别使用wazuh-logtest和mysql客户端进行测试。