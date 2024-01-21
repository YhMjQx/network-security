

# ==Tomcat下配置HTTPS==

Tomcat核心功能还是作为Java的容器来运行Java后端代码，虽然内置了对HTTP请求的支持，但并不是最优选择，通常部署时，会在Tomcat前面加一个专用的Http服务器，例如Nginx或Apache 

## 一、关键目录信息

### 1.logs目录

#### （1）catalina.out

Tomcat运行过程中的终端输出，可以看到错误信息从而定位问题

当Tomcat启动之后占用了后台进程，其过程中遇到的报错或请求信息输出都会在本文件中存储

我们可以使用 `tail -f catalina.out` 进行实时查看文件信息变更

#### （2）localhost_access_log.2024-01-20.txt

该文件是Tomcat中的访问日志存储文件，其中存储的全都是外部访问的信息。在Linux上 Tomcat 8.0 默认是打开的，可以手工关闭，但不建议关闭，可用于取证溯源

![image-20240121144441065](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121144441065.png)

其中内容大致如图所示，记录了来访客户端的IP地址，以及该客户端都访问了那些内容

我们可以使用 `tail -f localhost_access_log.2024-01-20.txt` 来实时观测文件信息变更

![image-20240121144854476](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121144854476.png)

#### （3）/opt/apache-tomcat-8.0.53/conf/server.xml

该文件属于Tomcat的核心配置文件，其中当然也包含了日志配置信息

按下shift+G即可到达文本最后

![image-20240121153215532](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121153215532.png)

```
 <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="localhost_access_log" suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" />
```

### 2./opt/apache-tomcat-8.0.53/conf/server.xml

这是Tomcat的核心配置文件

```
<Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />

```

这是http服务开启的端口配置，8080是http的默认端口，8443是https的默认端口

```
<!--
    <Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
               clientAuth="false" sslProtocol="TLS" />
    -->

```

配置 HTTPS 的基本信息，在互联网上，HTTP必须是80，HTTPS必须是443，这样才不需要再URL地址中加端口号，其他的都需要明确指定

```
<!-- Define an AJP 1.3 Connector on port 8009 -->
    <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />
```

这是当在Tomcat前另加一个处理HTTP请求的Apache服务器时所用的配置

其中AJP表示用于将HTTP的请求需要Tomcat容器（Java）处理的部分，交给Java来处理

## 二、Tomcat配置HTTPS

### 1.基础

- HTTP协议是全程明文，所以非常不安全
- HTTP（应用层）+ TCP（传输层） 之间加了一层 SSL（TLS），将HTTP协议进行加密再传输
- HTTPS的公网上传输：公钥+私钥进行加密，客户端或浏览器可信证书（CA机构颁发）
- 安全和性能不可得兼
- 局域网内部配置：（无法取得公网浏览器的信任，现实情况不可用）

#### （1）HTTP协议明文传输

全过程都是明文，没有一点秘密可言

![image-20240121160125430](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121160125430.png)

#### （2）HTTPS对称加密传输

一般情况下HTTPS协议使用的是对称密钥加密传输，当然，这个对称也不是言语上的对称

![image-20240121160257940](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121160257940.png)

事实上，客户端会生成一个随机秘钥，然后利用该随机秘钥对所要传输的数据进行加密，然后客户端利用自己的公钥对随机秘钥进行加密，然后client将加密后的随机秘钥和数据一起发送给服务器，服务器利用client的证书可以解开随机秘钥，然后再利用随机秘钥解开数据信息

#### （3）HTTPS非对称加密传输

![image-20240121160610466](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121160610466.png)

在这里我们将程度比作client，上海比作服务器，传输数据比作发快递

客户端对要发送的数据进行加密，发送给服务器。此时服务器无法解密，于是服务器自己也加密一次又发送给客户端。此时客户端对自己的加密解开然后再发送给服务器，此时数据上就只剩下上海自己的加密了

这只是大致的意思，具体信息还没学到...

### 2.配置

- 进入jdk执行目录，如果应将jdk环境变量添加好了就可以不需用这一步

`cd /usr/java/jdk/bin`

- 输入指令： `keytool -genkeypair -alias "tomcat" -keyalg "RSA" -keystore "/opt/tomcat.keystore"` 

执行之后会出现以下信息，跟着问题做就行了

```
输入密钥库口令:  
再次输入新口令: 
您的名字与姓氏是什么?
  [Unknown]:  ymq
您的组织单位名称是什么?
  [Unknown]:  youdian
您的组织名称是什么?
  [Unknown]:  youdian
您所在的城市或区域名称是什么?
  [Unknown]:  xian
您所在的省/市/自治区名称是什么?
  [Unknown]:  shanxi
该单位的双字母国家/地区代码是什么?
  [Unknown]:  cn
CN=ymq, OU=youdian, O=youdian, L=xian, ST=shanxi, C=cn是否正确?
  [否]:  y

输入 <tomcat> 的密钥口令
	(如果和密钥库口令相同, 按回车):  
再次输入新口令: 

Warning:
JKS 密钥库使用专用格式。建议使用 "keytool -importkeystore -srckeystore /opt/tomcat.keystore -destkeystore /opt/tomcat.keystore -deststoretype pkcs12" 迁移到行业标准格式 PKCS12。
```

![image-20240121163824289](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121163824289.png)

此时我们就可以看到该目录下多了一个证书文件

但是上述信息给出了warning，我们看看，他说要我们使用这条命令来迁移什么什么，ok

![image-20240121164033872](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121164033872.png)

也就是再执行一次，然后备份了一下证书文件

- 进入 /opt/apache-tomcat-8.0.53/conf/server.xml 

取消https配置的注释，并且在下面添上两个配置 `keystorefile="/opt/tomcat.keystore" keystorePass="p-0p-0p-0"` 使得完整信息如下



```
<Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
               clientAuth="false" sslProtocol="TLS" 
               keystorefile="/opt/tomcat.keystore" keystorePass="p-0p-0p-0" />
```

由![image-20240121164801434](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121164801434.png)

变为

![image-20240121164851604](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121164851604.png)

- 重启Tomcat

/opt/apache-tomcat-8.0.53/bin/shutdown.sh

/opt/apache-tomcat-8.0.53/bin/startup.sh



现在我们去尝试使用https访问woniusales 

好家伙还是访问不了，想想问题，防火墙开没开，端口访问改没改

```
firewall-cmd --add-port=8443/tcp --permanent
firewall-cmd --add-service=https --permanent
systemctl restart firewalld
```

![image-20240121165932441](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240121165932441.png)

虽然我们电脑上还是访问不了（大概率是因为现在浏览器都比较高级，非权威机构发行的证书是不被浏览器允许的），但是Tomcat上配置HTTPS基本流程就是这样

## 三、公网

1.公网需要一个固定的IP地址：购买一台云服务器，即可获得一个固定IP

2.建议最好注册一个域名，然后去通管局备案（否则不允许用域名访问）

3.将该域名解析到IP地址，即可实现域名访问，否则只能使用IP访问

