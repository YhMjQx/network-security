# ==TCPDump==

## 一、流量监控概述

对于一个通信过程的分析，首先需要把5个最基本的数据

```
源IP：谁发起请求，谁就是源，任意一端都可能是源，也可能是目标
源端口：通常情况下，第一次发起请求的，可以称之为客户端，第一次的目标机，称之为服务器
目标IP：通常情况下，目标IP是确定的，并且目标端口是确定的。
目标端口：对于服务器来说，通常是固定的
协议：实现约定好的规则  http HTTPS ssh是最为流行的应用层协议
然后具体查看内容（payload：载荷）


访问过程中，ip和端口缺少其中一个都无法访问成功
```

在网络数据交互中中哪怕只是一串数字 `510123199812157859`我们都可以从中得到很多信息

## 二、安装tcpdump

```
yum install -y tcpdump


已安装:
  tcpdump.x86_64 14:4.9.2-4.el7_7.1                                                                            
作为依赖被安装:
  libpcap.x86_64 14:1.5.3-13.el7_9 
  
libpacp是Linux上标准的流量监控的库，大多数流量监控工具都是基于这个底层库进行开发的，在windows上，比较知名的是WinPcap和npacp
目前市面上主流的防火墙，IDS，IPS，包过滤工具，只要涉及到流量的产品或系统，底层均基于以上这些库
```

## 三、tcpdump的使用

```
tcpdump -i ens32  监控ens32网卡上的流量，并输出到终端
tcpdump tcp and dst port 80 -i ens32 #只监控当前服务器端的80端口的流量

tcpdump tcp and dst port 80 -i ens32 -c 100 #只捕获100条数据库就自动结束

tcpdump tcp and dst port 80 -i ens32 -w ./target.cap #将监控到的流量下载到target.cap这个流量包中

```

我们可以做一个实验，使用命令  `systemctl stop firewalld.service` `/opt/lampp/lampp start` ,开启这个应用的web服务，然后用windows去访问，在Linux终端去已检测流量