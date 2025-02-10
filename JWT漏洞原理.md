[TOC]



# ==JWT漏洞原理==

教材内容

## JWT漏洞原理详解

### 一、JWT定义

#### 1.1 JWT 简介

 JWT 全称是Json Web Token，为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准，由服务端用加密算法对信息签名来保证其完整性和不可伪造，常用于分布式站点的单点登录（SSO）。

 JWT声明一般被用在客户端与服务端之间传递身份认证信息，便于向服务端请求资源。有了JWT服务端就无需保存任何关于用户或会话的信息，用来作身份认证、会话状态维持、信息交换。

#### 1.2 session

 为了解决http协议本身并不能记录状态问题，我们通常使用session在每一次会话开始时产生，用于存放会话信息，每个session以键值对的方式生成，然后将session_id以cookie的形式返回给客户端，客户端再次请求时携带session_id，服务端根据session_id使用对应的session作为认证信息为客户端响应对应服务，但是session在使用过程中还是会有扩展性 不佳、服务开销比较大、可能会被窃取身份信息等问题。

#### 1.3 session和JWT

 从原理上看两者是比较类似的，但session的认证信息是存储在服务端，客户端的session_id仅仅是session的标识符，而jwt本身就是携带认证信息的。token机制服务端是不存储相关认证信息的，只是对token做解密并根据解密信息查询用户信息，故对于服务端的开销更小，也更利于分布式服务器应用的扩展。

### 二、JWT的优缺点

#### 2.1 JWT的优点

1.JWT可以进行跨语言支持的，如JAVA，JavaScript，NodeJS，PHP等很多语言都可以使用。

2.JWT可以在自身存储一些其他业务逻辑所必要的非敏感信息。

3.JWT结构简单，字节占用很小，便于传输。

4.JWT不需要在服务端保存会话信息，易于应用的扩展。

5.可扩展性好， 应用程序分布式部署的情况下，session需要做多机数据共享,jwt不需要。

6.无状态的jwt不在服务端存储任何状态。

#### 2.2 JWT的缺点

1.JWT包含认证信息，因此一旦信息泄露，任何人都可以获得令牌的所有权限。

2.JWT不建议使用HTTP协议来传输代码，而是使用加密的HTTPS协议进行传输。

3.安全性低， 由于jwt的payload是使用base64url编码的，可以直接解码，因此jwt中不能存储敏感数据。而session的信息是存在服务端的，相对来说更安全。

4.性能比较差， jwt太长。由于是无状态使用JWT，所有的数据都被放到JWT里，如果还要进行一些数据交换，那载荷会更大，经过编码之后导致JWT非常长。

### 三、JWT 结构

#### 3.1 JWT的基本结构

一般是分为三个字符串的，分别为头部、载荷、签名，中间用.隔开：

（1）Header：加密算法与Token类型；

（2）Payload：用户信息和附加信息的声明，一般是Json类型的键值对；

（3）Signature：对前两个部分的签名，其中包含了base64加密后的Header、base64加密后的Payload、签名加密算法私钥。

#### 3.2 JWT的详细结构

大概的结构如下：

```
Header.Payload.Signature
```

1.Header（头部）
Header部分是一个JSON 对象，如：

```
{  "alg": "HS256",  "typ": "JWT"}
```

（1）alg表示签名的算法，默认HS256。
（2）type表示令牌的类型。

2.Payload（载荷）
Payload部分也是一个JSON 对象，其中是有7个字段的，如：

```
iss (issuer)：JWT的发行者exp (expiration time)：过期时间sub (subject)：JWT面向的主题aud (audience)：JWT的用户nbf (Not Before)：生效时间iat (Issued At)：签发时间jti (JWT ID)：JWT唯一标识
```

同时也可以自定义一些其他的字段。

3.Signature（签名）
Signature 部分是对前两部分的签名，防止数据被篡改，这里首先需要一个服务器端的秘钥secretkey，然后根据Header（头部）里面指定的签名算法，按照公式产生签名。一般的公式如：

```
data = base64urlEncode(header) + "." + base64urlEncode(payload)signature = HMAC-SHA256(data,secretkey)
```

### 四、JWT验证流程

（1）客户端提交用户名密码等信息到服务端请求登录，服务端在验证通过后前发一个具有时效性的token，将token返回给客户端。

（2）客户端收到token后会将token存储在cookie或localStorage中。

（3）随后客户端每次请求都会携带这个token，服务端收到请求后校验该token并在验证通过后返回对应资源。

如图：

![image-20221209172243357](https://gitee.com/ymq_typroa/typroa/raw/main/202212091722437.png)

### 五、涉及到的算法

#### 5.1 Base64URL

 Base64URL算法是base64的修改版，是为了方便在web中传输使用了不同的编码表，不会在末尾填充=号，并将+和/分别改为-和_。

#### 5.2HMAC

 HMAC算法是密钥相关的哈希运算消息认证码（Hash-based Message Authentication Code）的缩写，它是一种对称加密算法，使用相同的密钥对传输信息进行加解密。

#### 5.3 RSA算法

 RSA算法则是一种非对称加密算法，使用私钥加密明文，公钥解密密文。
在HMAC和RSA算法中，都是使用私钥对signature字段进行签名，只有拿到了加密时使用的私钥，才有可能伪造token。

#### 5.4 RS256

 RS256 (采用SHA-256 的 RSA 签名) 是一种非对称算法, 它使用公共/私钥对: 标识提供方采用私钥生成签名, JWT 的使用方获取公钥以验证签名。由于公钥 (与私钥相比) 不需要保护, 因此大多数标识提供方使其易于使用方获取和使用 (通常通过一个元数据URL)。

#### 5.5 HS256

 HS256 (带有 SHA-256 的 HMAC 是一种对称算法, 双方之间仅共享一个 密钥。由于使用相同的密钥生成签名和验证签名, 因此必须注意确保密钥不被泄密。

### 六、JWT漏洞

#### 6.1 漏洞利用工具

1.https://jwt.io/ JWT专用的解码网站

![image-20221209172909517](https://gitee.com/ymq_typroa/typroa/raw/main/202212091729633.png)

2.https://tooltt.com/jwt-decode/ JWT Token解析解码工具

![image-20221209172948744](https://gitee.com/ymq_typroa/typroa/raw/main/202212091729869.png)

3.https://github.com/brendan-rius/c-jwt-cracker jwt爆破工具

4.https://github.com/ticarpi/jwt_tool jwt综合工具

5.python的pyjwt库

#### 6.2 攻击的思路

找到需要JWT鉴权之后的才能访问的界面，将请求重放进行测试

1.未授权访问

删除Token后仍然可以正常响应对应页面。

2.敏感信息泄露

通过JWt.io解密出Payload后查看其中是否包含敏感信息，如弱加密的密码等。

3.破解密钥+越权访问

 通过JWT.io解密出Payload部分内容，通过空加密算法或密钥爆破等方式实现重新签发Token并修改Payload部分内容，重放请求包，观察响应包是否能够越权查看其他用户资料。

4.检查Token的时效性

 解密查看payload中是否有exp字段键值对（Token过期时间），等待过期时间后再次使用该Token发送请求，若正常响应则存在Token不过期。

5.看页面的回显，进行探测

 如修改Payload中键值对后页面报错信息是否存在注入，payload中kid字段的目录遍历问题与sql注入问题。

6.没有校验签名

 某些服务端没有校验JWT签名，可以尝试修改signature或者直接删除signature看JWT是否还有效。

7.签名算法改为none

 head中的alg值改为none，有的可以绕过签名，这样服务端收到token会将其认定为无加密的算法，就可以随意修改payload的部分伪造token

#### 6.3 实例

使用 Authentication Lab的几个靶场进行尝试

```
https://authlab.digi.ninja/
```

##### 6.3.1 敏感信息泄露（Leaky JWT）

![image-20221207121858574](https://gitee.com/ymq_typroa/typroa/raw/main/202212091743020.png)

上边提供的是加密的JWT的token，开发者如果把不必要的信息放在payload里边，那么解密的时候就可能获得用户的用户名和密码。我们将token放到解密的网站进行解密

```
https://tooltt.com/jwt-decode/
```

![image-20221207140807593](https://gitee.com/ymq_typroa/typroa/raw/main/202212091744319.png)

 可以看到用户名是admin，密码是经过md5加密的，就可以尝试使用解密网站进行解密2ac9cb7dc02b3c0083eb70898e549b63

```
https://www.cmd5.com/
```

![image-20221207141005487](https://gitee.com/ymq_typroa/typroa/raw/main/202212091745924.png)

找到用户名和密码

```
joe / Password1
```

![image-20221207141148974](https://gitee.com/ymq_typroa/typroa/raw/main/202212091749760.png)

登陆成功

##### 6.3.2 空加密算法破解JWT（JWT None Algorithm）

![image-20221207141245807](https://gitee.com/ymq_typroa/typroa/raw/main/202212091750343.png)

 JWT一般是几种加密算法进行签名，但是有的服务端也可以接受none（空加密算法）进行加密，在burp里边有一个Json Token Attacker插件，可以使用空加密算法

![image-20221207143454412](https://gitee.com/ymq_typroa/typroa/raw/main/202212091751493.png)

看一下token抓包，可以看到使用user登陆成功了

![image-20221207144446668](https://gitee.com/ymq_typroa/typroa/raw/main/202212091752226.png)

可以看到用户名和等级为robin，user

![image-20221207144738003](https://gitee.com/ymq_typroa/typroa/raw/main/202212091753500.png)

修改了用户发现是不允许的认证方式

![image-20221207144824329](https://gitee.com/ymq_typroa/typroa/raw/main/202212091753014.png)

![image-20221207144932427](https://gitee.com/ymq_typroa/typroa/raw/main/202212091753897.png)

可以在插件里边设置算法为None然后update更新，再放包发现admin权限登陆成功

![image-20221207155322327](https://gitee.com/ymq_typroa/typroa/raw/main/202212091754631.png)

### 七、安全建议

1.要保证密钥不在网站的根目录下，不会被其他方式泄露

2.JWT中不放用户名、密码等敏感信息

3.限制JWT的有效时间，避免被恶意利用
