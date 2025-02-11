[TOC]



# ==Shiro-550反序列化漏洞==

教材内容

> shiro-root 这个环境该如何配置
>
> - 第一步：去把 shiro-root 源码的包下载下来
>
> - 第二步：就是在 IDEA 中打开源码包
>
> - 第三步：修改 如下图所示位置的 pom.xml 文件的某个依赖的版本号
>
>   ![image-20250122151106241](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250122151106241.png)
>
>   将 jstl 的版本号修改为 1.2
>
> - 第四步：配置 tomcat
>
>   ![image-20250122151227333](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250122151227333.png)
>
>   ![image-20250122151307942](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250122151307942.png)
>
>   ![image-20250122151758104](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250122151758104.png)
>
>   ![image-20250122151806879](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250122151806879.png)

## Shiro-550反序列化漏洞

### 一、前置知识

#### 1.1 Shiro简介

 Apache Shiro 是一个强大易用的 Java 安全框架，提供了认证、授权、加密和会话管理等功能，对于任何一个应用程序，Shiro 都可以提供全面的安全管理服务。

![image-20220621160129969](https://gitee.com/ymq_typroa/typroa/raw/main/20220621160137.png)

Primary Cocnerns（基本关注点）:

- Authentication（认证）：经常和登录挂钩，是证明用户说他们是谁的一个工作
- Authorization（授权）：访问控制的过程，即，决定‘谁’可以访问‘什么
- Session Management（会话管理）：管理用户特定的会话，即使在非web或是EJB的应用中
- Crytography（加密）：通过加密算法保证数据的安全，且易于使用

Supporting Features（辅助特性）:

- Web Support（网络支持）:web support API可以帮助在web应用中方便的使用shiro
- Caching（缓存）:保证安全操作使用快速有效
- Concurrency（并发）:支持多线程应用
- Testing（测试）：支持集成单元测试
- Run As（以..运行）：可以假定用户为另一个用户
- Remeber Me:记住用户，无需再次登录·

#### 1.2 Shiro服务器端识别身份加解密处理cookie的流程

##### 1.2.1 加密

1. 用户使用账号密码进行登录，并勾选”Remember Me“。
2. Shiro验证用户登录信息，通过后，查看用户是否勾选了”Remember Me“。
3. 若勾选，则将用户身份序列化，并将序列化后的内容进行AES加密，再使用base64编码。
4. 最后将处理好的内容放于cookie中的rememberMe字段。

##### 1.2.2 解密

1. 当服务端收到来自未经身份验证的用户的请求时，会在客户端发送请求中的cookie中获取rememberMe字段内容。
2. 将获取到的rememberMe字段进行base64解码，再使用AES解密。
3. 最后将解密的内容进行反序列化，获取到用户身份。

### 二、Shiro-550

#### 2.1 漏洞简介

 shiro-550主要是由shiro的rememberMe内容反序列化导致的命令执行漏洞，造成的原因是默认加密密钥是硬编码在shiro源码中，任何有权访问源代码的人都可以知道默认加密密钥。于是攻击者可以创建一个恶意对象，对其进行序列化、编码，然后将其作为cookie的rememberMe字段内容发送，Shiro 将对其解码和反序列化，导致服务器运行一些恶意代码。

影响版本：shiro <= 1.2.4

特征：

1. cookie中含有rememberMe字段，如："rememberMe=JV+gEljeMVBj3EFY22otzX……"
2. cookie中含有"rememberMe=delete"

#### 2.2 漏洞分析

##### 2.2.1 环境搭建

Shiro安装包：shiro-root-1.2.4（https://codeload.github.com/apache/shiro/zip/shiro-root-1.2.4）

调试环境：Tomcat 9.0.22 + idea 2022.2 + jdk 1.8 + maven 3.6

##### 2.2.2 加密过程分析

访问http://localhost:8080/samples-web/login.jsp，使用其提供的root用户登录，并勾选“Remember Me” 。

![image-20220622151011796](https://gitee.com/ymq_typroa/typroa/raw/main/20220622151011.png)

将断点放于AbstractShiroFilter.class中的doFilterInternal()方法处，会创建subject对象，并使用请求信息。

![image-20220622101941000](https://gitee.com/ymq_typroa/typroa/raw/main/20220622101941.png)

而后进行一些处理，会调用AuthenticatingFilter.class中的executeLogin()方法对用户输入的登录信息进行验证，该方法会生成一个用于身份验证的token并进行相关验证。

![image-20220622102934978](https://gitee.com/ymq_typroa/typroa/raw/main/20220622102935.png)

验证通过后返回后续需要的相关登录信息，而后继续跟进到DefaultSecurityManager.class的rememberMeSuccess()方法。此方法会获取RememberMeManager，若该对象不为空，则使用onSuccessfulLogin()方法处理传入的登录相关的信息（subject、token、info）。

![image-20220622104408212](https://gitee.com/ymq_typroa/typroa/raw/main/20220622104408.png)

跟进到AbstractRememberMeManager.class的onSuccessfulLogin()方法，其首先会调用forgetIdentity()方法处理subject对象。

![image-20220622104543777](https://gitee.com/ymq_typroa/typroa/raw/main/20220622104543.png)

继续查看CookieRememberMeManager.class的forgetIdentity()方法，该方法取出了subject对象中的request与response交由另一个forgetIdentity()方法处理。

![image-20220622105054884](https://gitee.com/ymq_typroa/typroa/raw/main/20220622105054.png)

跟进另一个forgetIdentity()方法，其调用了removeFrom()方法来处理cookie。

![image-20220622105139033](https://gitee.com/ymq_typroa/typroa/raw/main/20220622105139.png)

来到SimpleCookie.class，removeFrom()方法获取相关信息（rememberMe字段及其值deleteMe，路径等），并将相关信息使用addCookieHeader()方法添加至cookie中。

![image-20220622105441671](https://gitee.com/ymq_typroa/typroa/raw/main/20220622105441.png)

回到AbstractRememberMeManager.class的onSuccessfulLogin()方法，接着这里判断用户是否勾选了”Remember Me“ ，若是，则使用rememberIdentity()方法继续处理登录的相关信息。

![image-20220622105607728](https://gitee.com/ymq_typroa/typroa/raw/main/20220622105607.png)

在rememberIdentity()方法中，取出对应用户的身份验证信息（如这里的root）并生成一个principals对象来存放，而后再交由另一个rememberIdentity()方法进行处理。

![image-20220622150655344](https://gitee.com/ymq_typroa/typroa/raw/main/20220622150655.png)

查看该rememberIdentity()方法，其调用了convertPrincipalsToBytes()方法来处理这个principals对象。convertPrincipalsToBytes()方法将principals对象进行序列化操作并用byte数组存放，判断是否启用加密服务，启用则将序列化的数据使用encrypt()方法进行加密。

![image-20220622110946822](https://gitee.com/ymq_typroa/typroa/raw/main/20220622110946.png)

跟进到encrypt()方法，其使用cipherService（生成的加密服务对象）的encrypt()方法将序列化数据进行加密，而加密方式AES加密，模式为CBC，密钥为128位（16个字节），填充方式为PKCS5Padding。

![image-20220622111812322](https://gitee.com/ymq_typroa/typroa/raw/main/20220622111812.png)

而其使用getEncryptionCipherKey()方法获取encryptionCipherKey用于加密的密钥。

![image-20220622111859207](https://gitee.com/ymq_typroa/typroa/raw/main/20220622111859.png)

其中用于加密的encryptionCipherKey与解密的decryptionCipherKey都是通过setCipherKey()方法来设置。

![image-20220622120529764](https://gitee.com/ymq_typroa/typroa/raw/main/20220622120529.png)

而该类的构造方法就调用了setCipherKey()方法设置为DEFAULT_CIPHER_KEY_BYTES，而这个默认的加密密钥就硬编码于代码中。

![image-20220622120633676](https://gitee.com/ymq_typroa/typroa/raw/main/20220622120633.png)

继续跟进到JcaChipherService的encrypt()方法，定义了一个ivBytes变量（CBC模式的初始化向量，用于每次AES加密之前或者解密之后，使用初始化向量与明文或密文异或），是随机生成的16个字节组成的字节数组。接着调用另一个encrypt()方法，并传入相关数据（plaintext：序列化数据，key： DEFAULT_CIPHER_KEY_BYTES，iv：随机生成的16个字节）

![image-20220622112817327](https://gitee.com/ymq_typroa/typroa/raw/main/20220622112817.png)

在这个encrypt()方法中主要有以下操作：

1. 调用AES的加密方法crypt()，将身份验证对象的序列化内容使用默认的密钥进行加密。
2. 生成一个用于存放输出值的byte数组output。
3. 将iv与encrypted放于output中。

最后将output返回。

![image-20220622114657382](https://gitee.com/ymq_typroa/typroa/raw/main/20220622114657.png)

而后回到AbstractRememberMeManager.class的rememberIdentity()方法，其接着调用了rememberSerializedIdentity()方法，将前面的output（iv变量与加密后的内容）进行base64编码，并将最终结果放于cookie中。

![image-20220622113327849](https://gitee.com/ymq_typroa/typroa/raw/main/20220622113327.png)

##### 2.2.3 解密过程分析

勾选“Remember Me”进行登录后，进行调试，刷新页面。

将断点打在DefaultSecurityManager.class的第二个createSubject()方法处，该方法用于获取cookie中的rememberMe字段，并利用其生成subject对象。

![image-20220622165022157](https://gitee.com/ymq_typroa/typroa/raw/main/20220622165022.png)

我们单步进入resolvePrincipals()方法，其调用了getRememberedIdentity()方法去获取rememberMe中的身份信息。

![image-20220622165349981](https://gitee.com/ymq_typroa/typroa/raw/main/20220622165350.png)

getRememberedIdentity()方法中，其又调用了getRememberedPrincipals()方法。

![image-20220622165625290](https://gitee.com/ymq_typroa/typroa/raw/main/20220622165625.png)

跟进到AbstractRememberMeManager.class中的getRememberedPrincipals()方法，其先调用了getRememberedSerializedIdentity()，判断获取的值不为空后，又使用convertBytesToPrincipals()方法来获取用于身份验证的principals对象。

![image-20220622165817364](https://gitee.com/ymq_typroa/typroa/raw/main/20220622165817.png)

先看CookieRememberMeManager.class的getRememberedSerializedIdentity()方法，先获取cookie中的值，然后base64解码，返回解码后的数据。

![image-20220622170543238](https://gitee.com/ymq_typroa/typroa/raw/main/20220622170543.png)

接着查看convertBytesToPrincipals()方法，该方法调用了deserialize()方法进行反序列化操作。

![image-20220622170656928](https://gitee.com/ymq_typroa/typroa/raw/main/20220622170656.png)

跟进到DefaultSerializer.calss的deserialize()方法，发现其没有对传入的序列化数据做任何过滤，直接调用了ObjectInputStream的readObject()方法进行反序列化操作，从而使得可以利用该方法触发Apache Commons Collections链的反序列化漏洞。

![image-20220622170859697](https://gitee.com/ymq_typroa/typroa/raw/main/20220622170859.png)

后续就是成功生成用于身份验证的对象，用户获取到权限进行访问。

#### 2.3 漏洞复现

> 用户登录时，启用RememberMe，服务器会用AES加密序列化的用户信息，生成cookie。如果密钥是默认的，攻击者可以构造恶意对象，序列化后加密，替换cookie，服务器解密时触发反序列化漏洞，执行任意代码。
>
> Shiro使用AES-CBC模式加密，并且密钥是硬编码的，攻击者可以利用已知密钥构造恶意cookie。
>
> - **核心问题：默认密钥 + 不安全的反序列化**
>   Apache Shiro的“记住我”（RememberMe）功能会生成一个加密的Cookie，用于用户下次自动登录。
>   但早期版本中，Shiro**默认使用硬编码的AES加密密钥**（如`kPH+bIxk5D2deZiIxcaaaA==`）。攻击者一旦知道密钥，就能伪造恶意Cookie。
> - **漏洞利用流程：**
>   - **加密逻辑缺陷**：Shiro将用户信息序列化后，用AES加密生成Cookie，但**未对数据完整性做签名验证**。
>   - **构造恶意数据**：攻击者利用已知密钥，加密一个精心构造的**恶意序列化数据**（包含攻击代码）。
>   - **触发反序列化**：服务器解密Cookie时，直接反序列化数据。若环境中存在可利用的第三方库（如Commons BeanUtils），会触发**远程代码执行（RCE）**，比如反弹Shell。
> - **关键点总结：**
>   - **默认密钥**：开发若不主动修改密钥，系统如同“门锁钥匙藏在门口地毯下”。
>   - **无验签机制**：加密不防篡改，攻击者无需破解AES，直接伪造合法格式的恶意数据。
>   - **反序列化漏洞**：Java反序列化时，若加载了恶意类，会直接执行攻击代码。
> - **防御思路：**
>   - 修改Shiro的AES密钥（随机生成强密钥）。
>   - 升级Shiro到安全版本（≥1.2.6），禁用危险的反序列化类。
>   - 关闭RememberMe功能（若无需使用）。
>
> **类比**：
> 好比快递员（Shiro）用固定密码的箱子（AES加密）送货，但密码是公开的。攻击者调包箱子里的物品（恶意代码），快递员直接拆箱使用，导致家中被入侵。

##### 2.3.1 实验环境

- 被攻击主机


主机：Centos7.9 （IP：192.168.219.206）

漏洞环境：vulhub/shiro:1.2.4

- 攻击主机


 主机：Windows10（IP：192.168.219.1）

 漏洞利用工具：ShiroExploit by 飞鸿（https://github.com/feihong-cs/ShiroExploit-Deprecated），netcat-win32-1.12（https://eternallybored.org/misc/netcat/）



##### 2.3.2 环境搭建

本次实验使用docker进行环境搭建。

1.拉取镜像

```
docker pull vulhub/shiro:1.2.4
```

2.创建容器

```
docker run -itd --name shiro550 -p 8080:8080 vulhub/shiro:1.2.4
```

3.临时开放端口

```
firewall-cmd --add-port=8080/tcp
```

成功搭建后访问http://192.168.219.206:8080/，如下：

![image-20220623094150165](https://gitee.com/ymq_typroa/typroa/raw/main/20220623094157.png)

##### 2.3.4 复现过程

在攻击主机打开shiro反序列化利用工具，选择漏洞类型为shiro550，地址栏中填入对应的地址，http://192.168.219.206:8080/

![image-20220623110154367](https://gitee.com/ymq_typroa/typroa/raw/main/20220623110154.png)

而后选择ceye.io进行漏洞检测（CEYE是一个用于检测带外数据（Out-of-Band）的监控平台，例如DNS查询和HTTP请求。它可以帮助安全研究人员在测试漏洞时收集信息，例如SSRF/ XXE/ RCE等）。

![image-20220623110429395](https://gitee.com/ymq_typroa/typroa/raw/main/20220623110429.png)

当扫描完后，会告诉我们可以使用哪些利用链进行命令执行。

![image-20220623111159816](https://gitee.com/ymq_typroa/typroa/raw/main/20220623111159.png)

使用netcat监控5555端口。

![image-20220623111353203](https://gitee.com/ymq_typroa/typroa/raw/main/20220623111353.png)

使用其简便操作进行反弹shell，指定反弹shell的连接地址为192.168.219.1:5555后，进行反弹shell的连接。

![image-20220623112315113](https://gitee.com/ymq_typroa/typroa/raw/main/20220623112315.png)

成功连接。

![image-20220623112147160](https://gitee.com/ymq_typroa/typroa/raw/main/20220623112147.png)

#### 2.4 修复建议

1. 更新shiro到1.2.4以上的版本。
2. 不使用默认的加密密钥，改为随机生成密钥。

### 三、参考文章

1. Shiro（一）:Shiro介绍及主要流程 （https://www.cnblogs.com/insaneXs/p/10999384.html）
2. Shiro反序列化漏洞详细分析（https://www.anquanke.com/post/id/228889）
3. Shiro反序列化分析带思路及组件检测笔记（https://xz.aliyun.com/t/8997）