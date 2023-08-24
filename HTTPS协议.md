# ==HTTPS协议==

HTTPS = HTTP + SSL/TLS

**1.加密算法**

**2.PKI体系（公钥基础设施）**

3.证书

**4.部署HTTPS服务器**

- 部署CA证书服务器

**5.分析HTTPS流量**

- 分析TLS交互过程

## 一、HTTPS协议

- 在HTTP的通道上增加了安全性，传输过程中，通过加密和身份认证来确保传输的安全性

### 1.TLS

- 传输层安全协议，SSL和TLS其实是一个协议，SSL2.0 版本，自SSL3..0 版本后，更名为TLS1.0，目前最高版本TLS1.3，使用最为广泛的是TLS1.2 版本
- 设计目标
  - 保密性：所有信息都加密传输
  - 完整性：校验机制
  - 认证：双方都配备证书，防止冒充
  - 互操作，通用性
  - 可扩展
  - 高效率

- 发展史
  - SSL2.0    SSL3.0    TLS1.0    TLS1.1    TLS1.2     TLS1.3

### 2.HTTP的缺陷

- 明文传输
- 只对传输数据的长度进行完整性校验，数据是否有被篡改是不做确认的

### 3.HTTPS好处

- 在传输数据之前，客户端会和服务器去协商数据在传输过程中的加密算法，包含自己的非对称加密的密钥交换算法（RSA/DH），数据签名摘要算法（MD5/SHA），加密传输数据的对称加密算法（DES/3DES/AES）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230823124854811.png" alt="image-20230823124854811" style="zoom:200%;" />

- 客户端会随机生成一段字符串，通过协商好的非对称加密算法，使用服务端的公钥对该字符串进行加密，然后发送给服务端。服务端接收到之后，使用自己的私钥解密得到该字符串，在随后的数据传输当中，使用这个字符串作为密钥进行对称加密

## 二、加密算法

1.对称加密算法

- 加密和解密的密钥相同（公共密钥）
  - 密钥如何传输问题
  - 密钥多，难管理
- 常见的对称加密算法
  - DES/3DES
  - AES
  - RC
  - IDEA

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230823133342752.png" alt="image-20230823133342752" style="zoom:200%;" />

2.非对称加密算法

- 加密秘钥和解密密钥使用的是不同的密钥（公（公开）钥和私钥），每个用户都可以有自己的公钥和私钥，公钥是公开的，私钥是由自己保存的，只要一个密钥加密就需要另一个密钥解密
  - 加密算法比较复杂，对于大规模的数据进行加密，比较影响效率
- 常见的算法
  - Elgamai：基于DH密钥交换算法来的
  - RSA
  - ECC
  - Rabin

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230823133818515.png" alt="image-20230823133818515" style="zoom:200%;" />

## 三、PKI体系

### 1.基本概念

- 公钥基础设施
  - 通过使用公钥技术（非对称加密算法）和数字签名来确保信息安全
  - 该体系由公钥加密技术（非对称加密算法）、数字证书、CA（证书颁发机构）、RA（证书注册机构）组成
- 实现的功能
  - 身份认证
  - 数据完整性
  - 数据机密性
  - 操作不可否认性
- 身份验证和完整性验证
  - 发送方Alice首先将原始数据通过摘要算法（SHA）算出数据的摘要值，并用自己的私钥对摘要值进行签名得到数字签名，将数字签名和原始数据发送给接收方bob
  - 接收方bob收到Alice发来的原始数据和数字签名之后，用相同的摘要算法（SHA）对原始数据进行计算得出接收到之后的摘要值，再利用Alice的公钥解开数字签名得到发送之前的摘要值（这里就完成了Alice的身份认证），将两个摘要值进行比对，如果一致，说明数据在传输过程中没有被修改

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824133055429.png" alt="image-20230824133055429" style="zoom:200%;" />

- 数字证书
  - 保证密钥的合法性
  - 证书的主体可以是用户，计算机，服务等
  - 证书包含的信息
    - 使用者的公钥
    - 使用者的标识
    - 有效期
    - 颁发者的标识信息
    - 颁发者的数字签名

### 2.数据安全传输案例

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824142441379.png" alt="image-20230824142441379" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824140946865.png" alt="image-20230824140946865" style="zoom:200%;" />

### 3.数字证书颁发机构

- CA主要是进行颁发和管理数字证书
- CA作用

### 4.证书服务器（HTTPS服务器）

#### 1.部署证书服务器

- Windows    active directory证书服务：基于域，这里用独立
- Linux           open ssl

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824152721444.png" alt="image-20230824152721444" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824152741775.png" alt="image-20230824152741775" style="zoom:200%;" />

装好之后

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824153121978.png" alt="image-20230824153121978" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824153231486.png" alt="image-20230824153231486" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824153248556.png" alt="image-20230824153248556" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824153458061.png" alt="image-20230824153458061" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824153531853.png" alt="image-20230824153531853" style="zoom:200%;" />

反正像这后面的步骤都是点击下一步

然后证书是可以复制导出私钥的（双击点开，这里就有）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824154617358.png" alt="image-20230824154617358" style="zoom:200%;" />

现在服务器上已经有两个证书了

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824154730090.png" alt="image-20230824154730090" style="zoom:200%;" />

那么，如何建立这第三个证书呢

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824180547868.png" alt="image-20230824180547868" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824180848686.png" alt="image-20230824180848686" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190129335.png" alt="image-20230824190129335" style="zoom:200%;" />

然后就可以得到一个证书申请码

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190211426.png" alt="image-20230824190211426" style="zoom:200%;" />

进入CA注册页面

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190319034.png" alt="image-20230824190319034" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190403834.png" alt="image-20230824190403834" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190420525.png" alt="image-20230824190420525" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190510203.png" alt="image-20230824190510203" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824155717254.png" alt="image-20230824155717254" style="zoom:200%;" />

然后现在可以将证书下下来

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190654360.png" alt="image-20230824190654360" style="zoom:200%;" />

会进入下面的页面

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190709302.png" alt="image-20230824190709302" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190734255.png" alt="image-20230824190734255" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190751224.png" alt="image-20230824190751224" style="zoom:200%;" />

这个就是CA颁发给web的了，可以导入服务器

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824190938756.png" alt="image-20230824190938756" style="zoom:200%;" />

现在才可以开启443端口

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824191208983.png" alt="image-20230824191208983" style="zoom:200%;" />

要想让我的网站只可以通过443端口（https）访问而不能通过80端口（HTTP）访问，我们可以开启ssl设置

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230824191728920.png" alt="image-20230824191728920" style="zoom:200%;" />

## 五、https流量

