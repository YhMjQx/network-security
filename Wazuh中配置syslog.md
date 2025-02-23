[TOC]



# ==Wazuh中配置syslog==

本次配置实验需要使用三台设备，分别是：

192.168.230.188 ：Wazuh 服务器  rsyslod 客户端

192.168.230.147 ：rsyslod 客户端

192.168.230.112 ：rsyslog 服务器

#### 一、wazuh中配置syslog

首先，续上文 《Linux 配置 rsyslog 日志》的配置

> 第一步：192.168.230.188 开启 rsyslog 服务，并且 wazuh 服务器也装在 192.168.230.188 上，并且 rsysload 服务配置如下：
>
> ![image-20250212153358577](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212153358577.png)
>
> ![image-20250212153434751](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212153434751.png)
>
> 表示，接收来自 ip 地址非127.0.0.1 的系统日志 并存储在 /var/log 目录下
>
> 第二步：192.168.230.147 主机作为 rsyslog 客户端 的 rsyslog 配置如下：
>
> ![image-20250212153539474](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212153539474.png)
>
> 说白了就是将 192.168.230.147 的日志信息去拿不发送给 188 服务器
>
> 此时，我们可以在 192.168.230.188 服务器上看到来自 192.168.230.147 的日志信息
>
> ![image-20250212153934923](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212153934923.png)
>
> 第三步：在 192.168.230.188 上使用 wazuh 监听 来自 非 127.0.0.1 IP地址 的主机系统日志

##### 1、监听rsyslog文件

在ossec.conf文件中，可以配置监听上述收到的日志文件，如：

```xml
<localfile>    
    <log_format>syslog</log_format>    
    <location>/var/log/host_*.log</location>
</localfile>
```

![image-20250212153736802](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212153736802.png)

确保在wazuh上启动了wazuh-manager，可以直观地在alerts.log看到相应的来自 192.168.230.147.log的预警信息，类似于以下内容。

重启 192.168.230.188 的 wazuh 服务器之后，我们来远程 ssh 登录 192.168.230.147 ，然后查看 192.168.230.188 的 alerts.log 文件

![image-20250212155128059](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212155128059.png)

##### 2、Wazuh内置syslog进程

第一个实验成功之后，我们关闭 192.168.230.188 的 rsyslog 服务器，让他不接收来自 192.168.230.147 的日志信息。

但是，我们直接使用 wazuh 来代替 rsyslog 接收192.168.230.147 的日志信息，说白了，就是配置 wazuh 自带的 rsyslog 服务

编辑ossec.conf，直接定义syslog的端口，远程日志直接发送给wazuh而不再需要通过rsyslog进程和日志文件中转

```xml
<remote>    
    <connection>syslog</connection>    
    <port>514</port>    
    <protocol>udp</protocol>    
    <allowed-ips>192.168.230.0/24</allowed-ips>
</remote>
```

> - 首先，关闭 192.168.230.188 的 rsyslog.conf 配置文件中的所有配置，也就是恢复原来的摸样
>
>   ![image-20250212160522563](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212160522563.png)
>
>   同时，删掉 192.168.230.188 的 /var/log 目录下的 host_* 文件
>
> - 其次，配置 192.168.230.188 的 wazuh 的ossec.conf 配置文件
>
>   ![image-20250212160741286](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212160741286.png)
>
>   在这里，只针对 192.168.230.0 网段的 ip 地址将日志发过来
>
> - 192.168.230.147 依旧保持 rsyslog 的配置，让他给 192.168.230.188 的 514 端口发送日志文件 
>
> - 192. 168.230.188重启 wazuh
>
> ssh 远程登录 192.168.230.147 进行测试
>
> 同时在192.168.230.188服务器上 `tail -f /var/ossec/logs/alerts/alerts.log` 文件
>
> ![image-20250212161409925](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212161409925.png)
>
> 发现确实 192.168.230.188 预警了 192.168.230.147 的日志信息
>
> - 但是，这种情况，如果没有高级别风险的日志，192.168.230.188 就会丢弃 192.168.230.147 的日志信息

##### 3、将wazuh服务器端syslog发送给远程 日志服务器

将192.168.230.188 的 wazuh的预警日志发送给`192.168.230.112` 如果日志级别超过9级，再发送给 `192.168.230.225`.

```xml
<ossec_config>  
    <syslog_output>    
        <level>9</level>    
        <server>192.168.230.225</server>    
        <port>514</port>  
    </syslog_output>  
    <syslog_output>    
        <server>192.168.230.112</server>  
    </syslog_output>
</ossec_config>

或
我们在这里使用下面的这个
<ossec_config>  
    <syslog_output>    
        <level>5</level>    
        <server>192.168.230.112</server>    
        <port>514</port>  
    </syslog_output> 
</ossec_config>
表示，当日志审计等级超过 7 级 之后，便会将日志发送给 192.168.230.112
注意 ossec_config 标签，默认 ossec.conf 文件是已经有的，我们只需要将其中的内容包裹在里面就好了
```

![image-20250212164944278](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212164944278.png)

（1）在192.168.230.112 远程日志服务器上对rsyslog.conf做如下配置。

```shell
$ModLoad imudp
$UDPServerRun 514

#### Added By ymqyyds ####
$template MyLogFormat,"%timestamp% %fromhost-ip% %syslogtag% %msg%\n"
$ActionFileDefaultTemplate MyLogFormat

$template RemoteLogs,"/var/log/host_%fromhost-ip%.log"
:fromhost-ip, !isequal, "127.0.0.1" ?RemoteLogs
##########################
```

![image-20250212161901650](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212161901650.png)

![image-20250212164133920](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212164133920.png)

（2）有alert产生时，收到的日志信息如下：

远程ssh登录 192.168.230.147 ，在 192.168.230.147 的 /var/log/secure 文件中可以看到日志

![image-20250212165745506](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212165745506.png)

在 192.168.230.188 的 wazuh 服务器中 可以看到 192.168.230.147 的日志信息

![image-20250212165820610](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212165820610.png)

此时 192.168.230.112 中便产生了 来自 192.168.230.188 的预警信息日志

![image-20250212170018128](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212170018128.png)