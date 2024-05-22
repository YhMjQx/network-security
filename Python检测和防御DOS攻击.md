[TOC]



# ==Python检测和防御DOS攻击==

利用Python编程实现对wrk的泛洪攻击检测，并让程序触发调用Linux命令实现防御：

1、泛洪攻击的检测，可以考虑使用的命令，这些命令可以通过Pytho调用和分析。

- `netstat -ant | wc -l`
- `netstat -ant | grep SYN_RECV`
- `netstat -s | grep overflowed`
- `netstat -s | grep dropped`
- `top -n` 获取CPU使用率

以上操作过程的命令，允许使用管道和AWK提取数据，也可以直接使用Python进行数据提取

2、防御措施可以选择一下几种：

- 修改系统配置参数，来增强系统的TCP连接数
- 直接结束某些消耗CPU的进程，或者停止Apache的服务（不得已而为之）
- 开启防火墙，将目标IP地址进行封锁（首选）
- 自行查阅资料，进行其他可以执行的操作
- 上述Python代码实现的狠心就是调用系统指令，再通过Python 进行分析，触发命令的执行等。建议在Linux上安装Pyotn3.x及以上的版本



基本步骤：

1、确保在Linux上可以正常运行Python3.x，而Centos内置的是python2.7版本

![image-20240517192044187](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240517192044187.png)

2、做基本的调研，明确对于DOS的入侵检测，需要使用那些方法或命令

3、将可以使用的命令通过Python来运行，并进行调试，确保 Python+命令 可以正常运行

4、想办法找到连接数最多的攻击源IP地址，驱动Linux的防火墙进行入侵防御

5、最后进行整合，测试，再模拟攻击，确保脚本可以正常检测

## 一、在CentOS上安装Python3

下载地址：[Python 版本 Python 3.10.14 |Python.org](https://www.python.org/downloads/release/python-31014/)

安装教程：

[CentOS 7 安装 Python 3.10_yum python3.10-CSDN博客](https://blog.csdn.net/zltliqi/article/details/126449120)

[服务器Centos7部署安装Python3的完整过程（3.10.1） - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/654585535)

```
cd ~

sudo yum -y update

sudo yum -y install openssl-devel libffi-devel bzip2-devel

sudo yum -y groupinstall "Development Tools"

wget https://www.openssl.org/source/openssl-1.1.1q.tar.gz --no-check-certificate

tar zxf openssl-1.1.1q.tar.gz

cd openssl-1.1.1q

./config --prefix=/usr/local/openssl-1.1.1

sudo make && sudo make install

mkdir /usr/local/python3

wget https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tgz

tar zxf Python-3.10.5.tgz 

cd Python-3.10.5

./configure --enable-optimizations --with-openssl=/usr/local/openssl-1.1.1 --with-openssl-rpath=auto --prefix=/usr/local/python3

sudo make altinstall

#make

#make install

# 配置环境变量

vi ~/.bash_profile

export PYTHON_HOME=/usr/local/python3

PATH=$PATH:$HOME/bin:$PYTHON_HOME/bin

export PATH

退出编辑
source ~/.bash_profile
```

## 二、理解各个命令的含义

### 1、uptime

`uptime` 命令用户查看主机的开机时长，用户连接数量，以及**在 1、5、15分钟 三个时间段内，CPU的负载情况**。

![uptime](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240519154030013.png)

[每周一个linux命令之---uptime详解 - vinter_he - 博客园 (cnblogs.com)](https://www.cnblogs.com/vinter/p/9668896.html)

### 2、netstat

`netstat` 命令用来打印Linux中网络系统的状态信息，可让你得知整个Linux操作系统的网络情况，需要注意的是在windows和Linux上的参数会略有不同。

```
-a或--all 显示所有连线中的Socket
-n或--numeric 直接使用IP地址，而不通过域名服务器。意思就是以数字的形式代替服务
-l或--listening 显示监控中的服务器的Socket。
-t或--tcp 显示TCP传输协议的连线状况
-u或--udp 显示UDP传输协议的连线状况。
-s或--statistics 显示网络工作信息统计表
-r或--route 显示Routing Table。
-p或--programs 显示正在使用Socket的程序识别码和程序名称。

以数字方式列出所有TCP连接情况: netstat -ant
以数字方式列出所有UDP连接情况: netstat -anu
以数字方式列出所有TCP和UDP处理监听状态的情况: netstat -anult
显示所有端口的统计信息: netstat-s
显示TCP端口的统计信息: netstat-st
显示核心路由信息: netstat -r
显示所有连接的进程信息: netstat -ap
```

[Linux netstat命令 |菜鸟教程 (runoob.com)](https://www.runoob.com/linux/linux-comm-netstat.html)

### 3、ss

`ss` 用来显示处于活动状态的套接字信息。他可以显示和netstat类似的内容，但ss的优势在于它能够显示更多更详细的有关TCP和连接状态的信息，而且比netstat更快速高效。

```
显示监听状态下的队列情况: ss -lnt
显示非监听状态下的连接详情: ss -nt
显示socket摘要信息: ss -s  注意其结果的IPv6的变化
```

LISTEN 状态: Recv-Q 表示的当前等待服务端调用 accept 完成三次握手的 listen backlog 数值，也就是说，当客户端通过 connect() 去连接正在 listen() 的服务端时，这些连接会一直处于这个 queue 里面直到被服务端accept() ; Send-Q 表示的则是最大的 listen backlog 数值，这就就是上面提到的 min(backlog,somaxconn)的值

非 LISTEN 状态: Recv-Q 表示 receive queue 中的 bytes 数量;Send-Q 表示 send queue 中的 bytes 数值该数值意义不大，更多关注连接的数量和状态即可

### 4、firewall-cmd

```
关闭防火墙:systemctl stop firewalld

添加允许端口:firewall-cmd --add-port=80/tcp

列出防火墙规则:firewall-cmd --list-all

禁止IP地址访问80端口:firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.112.148" port port="80" protocol="tcp" reject'

让配置永久生效:添加允许端口:firewall-cmd --add-port=80/tcp --permanent

允许http服务通过1分钟:firewall-cmd --zone=public --add-service=http --timeout=1m，这个 timeout 选项是一个以秒(s)、分(m)或小时(h)为单位的时间值。
```

### 5、sysctl

sysctl命令用于运行时配置内核参数，这些参数位于/proc/sys目录下。sysctl配置与显示在/proc/sys目录中的内核参数，可以用sysctl来设置或重新设置联网功能，如IP转发、IP碎片去除以及源路由检查等。用户只需要编辑/etc/sysctl.con文件，即可手工或自动执行由sysctl控制的功能。

```
显示所有系统参数:sysctl -a

使用cat查看指定参数:cat /proc/sys/net/ipv4/ip_forward，除/proc/sys外，后面的路径与参数名称一致换成 / 即可

临时改变某个指定参数的值，如:sysctl -w net.ipv4.ip forward=1，也可以:echo 1 > /proc/sys/netipv4/ip forward

如果想永久保留配置，可以修改/etc/sysctl.con文件
```

快速修改部分参数，优化性能：

```
net/ipv4/tcp_syn_cookies   是否打开SYN COOKIES的功能，"1”为打开，“2”关闭。

net/ipv4/tcp_max_syn_backlog	SYN队列的长度，加大队列长度可以容纳更多等待连接的网络连接数。

net/ipv4/tcp_synack_retries和net/ipv4/tcp_syn_retries	定义SYN重试次数，默认为5，建议为2

net/ipv4/sack=0
```

> 其他参数的说明:https://www.cnblogs.com/feiyun126/p/8646989.html
>
> 一些优化方案:https://blog.csdn.net/wangshuminjava/article/details/80935792

## 三、利用python实现DOS入侵检测

### 采集TCP连接数据

#### 采集跟DOS攻击关联度较高的数据 

##### uptime

- >  19:51:11 up 5 days,  8:40,  3 users,  load average: 0.00, 0.02, 0.05  **->**  [' 19:51:11 up 5 days', '  8:40', '  3 users', '  load average: 0.00', ' 0.02', ' 0.05\n']  **->**    load average: 0.00  **->**  ['', '', 'load', 'average:', '0.00']  ->  0.00

```python
import os,time

# 可采用 split和awk进行修改得到前1分钟的CPU平均负载
import time,os

def get_cpu_01():
    uptime = os.popen('uptime').read()
    #print(type(uptime))
    #print(uptime)
    cpu_load = float(uptime.split(',')[3].split(' ')[4])
    #print(cpu_load)
    return cpu_load

```

- >  20:07:30 up 5 days,  8:56,  3 users,  load average: 0.00, 0.01, 0.05  **-->>**   20:07:30 up 5 days,  8:56,  3 users,  load average,0.00, 0.01, 0.05  **-->> ** [' 20:07:48 up 5 days', '  8:56', '  3 users', '  load average', '0.00', ' 0.01', ' 0.05\n']  **-->>**  0.00

```python
def get_cpu_02():
    uptime = os.popen('uptime').read()
    #print(type(uptime))
    #print(uptime)
    cpu_load = float(uptime.replace(': ',',').split(',')[4])
    #print(cpu_load)
    return cpu_load
```

- >  20:16:56 up 5 days,  9:05,  3 users,  load average: 0.00, 0.01, 0.05  **-->>**  0.00, 0.01, 0.05  **-->>**  0.00

```python
def get_cpu_03():
    uptime = os.popen('uptime').read()
    #print(type(uptime))
    #print(uptime)
    cpu_load = float(os.popen("uptime | awk -F ': ' '{print$2}' | awk -F ',' '{print$1}'").read())
    #print(cpu_load)
    return cpu_load
```

##### netstat -ant 连接数量

正常 `netstat -ant` 展示情况，一般是不会迅猛增加

![image-20240521174617885](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240521174617885.png)

```python
def get_TCP_conn():
    netstat = int(os.popen('netstat -ant | wc -l').read())
    return netstat
```

##### ss -lnt  读取队列情况

![image-20240522201335571](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240522201335571.png)

```python
def get_queue_size():
    queue = os.popen('ss -lnt | grep :80').read()
    recv_q = int(queue.split()[1])
    send_q = int(queue.split()[2])
    return recv_q,send_q
```

##### 主调函数

```python
if __name__ == '__main__':
    while True:
        #cpu_load = get_cpu_load_01()
        #cpu_load = get_cpu_load_02()
        cpu_load = get_cpu_load_03()

        TCP_conn = get_TCP_conn()

        recv_q,send_q = get_queue_size()

        print(f"cpu_load:{cpu_load} TCP_conn:{TCP_conn} TCP_Queue:{recv_q,send_q}")
        time.sleep(2)
        #print(type())
        if cpu_load > 33.3 or TCP_conn > 2000 or recv_q > send_q -10:
            print("CPU 负载过高或TCP连接数太多，可能遭遇DOS攻击，请注意！！！")
```

