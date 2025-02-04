[TOC]



# ==NMap扫描器进阶==

## 一、基础功能回顾

```
扫描IP地址（只做ping扫描，不做端口扫描）：nmap -sn 192.168.112.0/24  192.168.112.1-255
基于SYN包扫描端口号：nmap -sS 192.168.112.188
基于三次握手扫描端口号：nmap -sT 192.168.112.188
指定端口扫描：nmap -p10-200, -p21,22,25,80,445,3306,1521,8080,8888 192.168.112.188
扫描端口和版本：nmap -sV 192.168.112.188
扫描操作系统：nmap -O 192.168.112.188
万能开关：nmap -A 192.168.112.188
```

## 二、内置脚本扫描

可以使用内置脚本进行功能扩展，命令语法为：nmap —script=brute 192.168.112.188。

```
auth: 负责处理鉴权证书（绕开鉴权）的脚本  
broadcast: 在局域网内探查更多服务开启状况，如dhcp/dns/sqlserver等服务  
brute: 提供暴力破解方式，针对常见的应用如http/snmp等  
default: 使用-sC或-A选项扫描时候默认的脚本，提供基本脚本扫描能力  
discovery: 对网络进行更多的信息，如SMB枚举、SNMP查询等  
dos: 用于进行拒绝服务攻击  
exploit: 利用已知的漏洞入侵系统  
external: 利用第三方的数据库或资源，例如进行whois解析  
fuzzer: 模糊测试的脚本，发送异常的包到目标机，探测出潜在漏洞 
intrusive: 入侵性的脚本，此类脚本可能引发对方的IDS/IPS的记录或屏蔽  
malware: 探测目标机是否感染了病毒、开启了后门等信息  
safe: 此类与intrusive相反，属于安全性脚本  
version: 负责增强服务与版本扫描（Version Detection）功能的脚本  
vuln: 负责检查目标机是否有常见的漏洞（Vulnerability），如是否有MS08_067
```

所有扫描脚本，可以查看Kali下的目录：/usr/share/nmap/scripts，具体各个脚本的用法及参数，参考：https://nmap.org/nsedoc/

## 三、 脚本实战应用

### 1、扫描SSH登录认证情况

```
┌──(root@kaliQiang)-[/home/denny]
└─# nmap -p22 --script=auth 192.168.112.188                       
Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-28 22:23 CST
Nmap scan report for 192.168.112.188 (192.168.112.188)
Host is up (0.00044s latency).

PORT   STATE SERVICE
22/tcp open  ssh
| ssh-auth-methods: 
|   Supported authentication methods: 
|     publickey
|     gssapi-keyex
|     gssapi-with-mic
|_    password
| ssh-publickey-acceptance: 
|_  Accepted Public Keys: No public keys accepted
Nmap done: 1 IP address (1 host up) scanned in 0.35 seconds
```

### 2、扫描主机漏洞

```
┌──(root@kaliQiang)-[/home/denny]
└─# nmap --script=vuln 192.168.112.158              
Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-28 22:27 CST
Nmap scan report for 192.168.112.158 (192.168.112.158)
Host is up (0.00023s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
1025/tcp open  NFS-or-IIS
MAC Address: 00:0C:29:5E:35:7D (VMware)

Host script results:
| smb-vuln-ms08-067: 
|   VULNERABLE:
|   Microsoft Windows system vulnerable to remote code execution (MS08-067)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2008-4250
|The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,
|           Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary
|           code via a crafted RPC request that triggers the overflow during path canonicalization.
|           
|     Disclosure date: 2008-10-23
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms08-067.aspx
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: NT_STATUS_OBJECT_NAME_NOT_FOUND
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143

Nmap done: 1 IP address (1 host up) scanned in 39.55 seconds
```

### 3、爆破模块

```
nmap -p22 --script=brute 192.168.112.188
nmap -p3306 --script=brute 192.168.112.188

┌──(root@kaliQiang)-[/home/denny]
└─# nmap --script=brute 192.168.112.158                                                                                                                                   
130 ⨯
Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-28 23:06 CST
Nmap scan report for 192.168.112.158 (192.168.112.158)
Host is up (0.000092s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
1025/tcp open  NFS-or-IIS
MAC Address: 00:0C:29:5E:35:7D (VMware)

Host script results:
| smb-brute: 
|_  guest:<blank> => Valid credentials, account disabled

Nmap done: 1 IP address (1 host up) scanned in 28.48 seconds
```

### 4、指定字典爆破

```
map -p3306 --script=brute --script-args 'userdb=./usertest.txt,passdb=./password-3000.txt' 192.168.112.188
```

> 爆破频率过高，很容易导致服务器拒绝服务，所以爆破虽然技术不难，但是实际应用中还需要注意。

## 四、SNetCracker爆破工具

![image-20240908165508042](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240908165508042.png)