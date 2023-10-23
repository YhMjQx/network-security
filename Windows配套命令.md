# ==Windows配套命令==

## 一、文件与文件夹

```
查看命令的帮助: command /?
在任意盘符下切换到D盘: D:
切换到D:\Testing目录: cd D:\Testing
显示当前目录下的内容:dir
显示指定目录下的内容:dir D:\Testing
创建目录: mkdir He11o	或者 md He11o
强制删除目录及下级内容:rmdir /S /Q folder
新建一个文本文件: echo He11o woniu > temp.txt
查看一个文本文件:type temp.txt
在文本文件后面新增内容: echo Welcome to chengdu >> temp.txt
复制文件: copy temp.txt temp.log
复制文件夹: xcopy folder folder2 /T
重命名一个文件或文件夹:rename temp.txt test.txt，也可以使用ren
移动一个文件或文件夹:move
删除一个文件: del temp.xt
```



## 二、文本内容处理

```shell
默认情况下，windows下的findstr与Linux上的grep功能类似
ipconfig > ip.txt
findstr 192 ip.txt
findstr /v 192 ip.txt
type ip.txt l findstr 192

在windows中，也可以使用awk、grep和sed，需要先安装
grep: http://www.interlog.com/~tcharron/grep.html
awk: https://sourceforge.net/projects/gnuwin32/files/gawk/3.1.6-1/gawk-3.1.6-1-bin.zip/download
sed: https://sourceforge.net/projects/gnuwin32/files/sed/4.2.1/

在下载的文件中找到grep.exe，awk,exe，sed,exe，将其安装在某个目录中，将该目录设定在环境变量Path中即可随时使用
type ip.txt | grep 192
type ip.txt | awk "{print $1}"
type ip.txt | sed "s/192/199/g"
需要注意的是，在awk和sed的windows版本中，请使用英文半角状态下的双引号，不支持单引号

在power shel1命令窗口中，可以使用 gc 命令和select命令组合来实现 head 和 tail  的能
gc ip.txt l select -first 10 	# head
gc ip,txt l select -last 10 	# tail
```



## 三、进程与服务处理

```
启动某个服务: net start/stop/restart service
查询服务状态或者删除服务等:sc
直换用命令打开网质: C:\Users\YhMjQx\AppData\local\Google\Chrome\Application\chrome.exe http://www.woniuxy.com
列出当前所有进程信息: tasklist，当然也可以过滤

结束某个进程:
taskki11 /F/IM 进程名  相当于Linux中的pkill
taskki11 /F /PID 进程ID  相当于Linux中的kill
/F 表示强制结束进程
/IM 表示印象名称
/PID 就是进程的ID

创建一个用户:net user ymq /add，详情请使用 net user /? 查看具体帮助
```

 

## 四、网络相关命令

```
ping命令: ping woniuxy.com 或 ping -n 10 woniuxy.com
路由跟踪: tracert woniuxy.com

修改静态IP:
netsh interface ip set address "本地连接" static 192.168.10.125 255.255.255.0 192.168.10.1 1
netsh interface ip set dns"本地连接”static 202.106.0.20
netsh interface ip add dns "本地连接”8.8.8.8
修改为DHCP:
netsh interface ip set address "本地连接”dhcp
netsh interface ip set dns "本地连接"dhcp
本地连接就是网卡的名称

为防火墙添加入站允许的程序:
netsh advfirewall firewall add rule name="f.exe" dir=in program="e:\f.exe" action=allow
netsh advfirewa1 firewal1 delete rule name="f.exe"

为防火墙添加入站允许的端口:
netsh advfirewal1 firewall add rule name="HTp" protocol=TCp dir=in localport-8080 action=allow
netsh advfirewal] firewall delete rule name="HTp" protocol=TCP dir=in localport=8080

使用SSH登录远程Linux，使用SCP与Linux进行文件传输
ssh root@192.168.112.225
scp D:\test.htm] root@192.168.112.225:/opt

查看当前系统的端口： netstat 或 netstat -ano
```

 