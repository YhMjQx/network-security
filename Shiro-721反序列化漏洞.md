[TOC]



# ==Shiro-721反序列化漏洞==

教材内容

## Shiro-721反序列化漏洞

### 一、漏洞简介

 Shiro-721反序列化漏洞，使用由于Shiro通过 使用AES-128-CBC 模式进行cookie中rememberMe字段的加密，于是用户可通过Padding Oracle加密生成的攻击代码来构造恶意的rememberMe字段，并重新请求网站，进行反序列化攻击，最终导致任意代码执行。

影响版本：Apache Shiro < 1.4.2

### 二、漏洞原理

#### 2.1 AES 的 CBC 模式

 AES加密算法全称是Advanced Encryption Standard（高级加密标准），是最为常见的对称加密算法之一。AES的区块长度固定为128位，密钥长度则可以是128，192或256位。分组密码在加密时明文分组的长度是固定的，而实用中待加密消息的数据量是不定的，数据格式可能是多种多样的。为了能在各种应用场合安全地使用分组密码，通常对不同的使用目的运用不同的工作模式。AES有五种工作模式：电码本模式（Electronic Codebook Book ，ECB）、密码分组链接模式（Cipher Block Chaining ，CBC）、计算器模式（Counter，CTR）、密码反馈模式（Cipher FeedBack ，CFB）、输出反馈模式（Output FeedBack ，OFB）。而在Shiro721中使用的就是CBC模式。

 密码分组链接模式（Cipher Block Chaining ，CBC），其中“分组“是指加密和解密过程都是以分组进行的。每一个分组大小为128bits(16字节)，如果明文的长度不是16字节的整数倍，需要对最后一个分组进行填充(padding)，使得最后一个分组长度为16字节。“链接”是指密文分组像链条一样相互连接在一起。

**加密过程：**

![image-20220624111031803](https://gitee.com/ymq_typroa/typroa/raw/main/20220624111031.png)

1. 发送方将明文（Plaintext）分成若干分组（Plaintext[1]，…，Plaintext[n]），每个分组16个字节，不够则填充。
2. 生成一个跟分组长度一致（16个字节）的IV（Initialization Vector，初始向量），用于后续的异或运算。
3. 将IV与第一个明文分组（Plaintext[1]）进行异或得到m1（可以看做一个中间值）。
4. 将m1使用密钥Key进行加密得到第一个密文分组（Ciphertext[1]）。
5. 将上一步得到的密文与下一个明文分组进行异或，得到一个新的中间值，再将这个中间值使用Key进行加密得到后续的一个密文分组。接着重复这个过程直到所有明文分组被加密。
6. 为了接收方能够成功解密，还需要将 IV 也发送给接收方。为描述方便，这里把将 IV 当成Ciphertext[0]，发送时会将IV作为密文的第一个分组，最后将后续密文分组按顺序拼接即可得到最终的密文（Ciphertext）。

**解密过程：**

![image-20220624110317251](https://gitee.com/ymq_typroa/typroa/raw/main/20220624110317.png)

1. 接收方将密文（Ciphertext）分成若干分组（Ciphertext[1]，…，Ciphertext[n]）。
2. 将第一个密文分组（Ciphertext[1]）使用密钥Key进行解密，得到中间值m1。
3. 将IV（Ciphertext[0]）与m1进行异或运算得到第一个明文分组（Plaintext[1]）。
4. 将下一个密文分组使用Key进行解密得到一个新的中间值，而再将上一个密文分组与该中间值进行异或即可得到后续的一个明文分组。重复这个过程直到所有密文分组被解密。
5. 最后将所有明文分组组合在一起即可获取到完整的明文（Plaintext）。

#### 2.2 Padding Oracle 攻击原理

 Padding的含义是“填充”，在解密时，如果算法发现解密后得到的结果，它的填充方式不符合规则，那么表示输入数据有问题，对于解密的类库来说，往往便会抛出一个异常，提示Padding不正确。Oracle在这里便是“提示”的意思，和甲骨文公司没有任何关系。

##### 2.2.1 分组填充方式（PKCS5Padding,PKCS7Padding）

 因为分组加密方式只能使用一个固定大小的密钥加密相同字节长度的明文（一般长度为8个字节或16个字节），所以需要将加密的明文按照密钥大小拆分为多块（所以也叫块加密），如果拆分后最后一个块明文长度不够，就需要填充字节来补齐长度。按照常见的PKCS#5或PKCS#7公钥加密标准，最后需要填充几个字节，那么每个填充字节的值就用所需填充的字节数，若最后一个明文刚好符合固定长度，就需填充一个完整分组。

 通过下图我们可以更好的进行理解：

![image-20220624143435943](https://gitee.com/ymq_typroa/typroa/raw/main/20220624143435.png)

 我们假设每个分组8个字节，当最后一个分组为8个字节长度时，就再填充8个字节，且每个字节的值都为16进制的“8”，即0x08。若最后一个分组为7个字节，则需要填充1个字节，该字节的值为0x01。以此类推，6个字节就需填充两个字节，都为0x02。

 那么它如何判断填充是否错误？当将密文解密后，其会检查明文最后的一个字节，若发现其为0x02，则继续检查倒数第二个字节是否为0x02，若倒数第二个字节不是0x02，则判断出填充错误。其判断方式就是通过去读明文最后一个字节填充的字节，根据该字节的值，继续向前检查。

##### 2.2.2 异或运算（xor）

 异或（xor）是一个数学运算符。它应用于逻辑运算。异或的数学符号为“⊕”，计算机符号为“xor”。其运算规则为：若a、b两个值不相同，则异或结果为1。如果a、b两个值相同，异或结果为0。

有以下运算规律：

```
1. 若a xor b = c, 则b xor c = a, a xor c = b
2. a xor 0 = a
3. a xor a =0
4. 若a xor b = c，
则a xor b xor c = 0, c xor c xor d = d
```

##### 2.2.3 Padding Oracle

 当我们知晓IV与密文，输入点可控（能够任意输入IV与任意密文交由解密器解密），且当密文解密出错时，能够判断出是否是由于填充错误造成的，就能在不知道对称密钥的情况下，通过构造明文分组中不同的填充值，再利用填充时的错误回显或是时间延迟，进行爆破，推测出密文解密后的中间值，进而可以推测出原始明文，或是利用中间值结合特定的IV构造出想要的明文。而这个利用错误回显或是时间延迟做判断的过程就称为oracle。

 接下分析该攻击的具体实现流程，前面我们知道了分组的填充方式以及如何判断填充是否错误，这里我们可以从第一个分组开始进行分析。

- 关键词说明：
  - Plaintext：明文，Plaintext[-n]：明文分组中最后第n个字节
  - m：中间值，由IV与Plaintext进行异或运算得到，m[-n]：中间值的最后第n个字节
  - IV：初始向量，IV[-n] : 初始向量的最后第n个字节
  - G_IV：构造的IV，G_IV[-n]：构造的IV的最后第n个字节

 **采用CBC模式进行解密时，其会将密文分组解密为一个中间值m，而后再将m与IV进行异或得到最后的明文分组。当我们可以控制输入的IV与密文时，我们可以先只输入第一个密文分组，而将其解密后得到的就是完整的明文，是没有填充字节的，这必定会触发填充错误。于是我们可以尝试构造一个G_IV，使得中间值m与G_IV进行异或后得到的明文的最后一个字节Plaintext[-1]为0x01，这样就不会出现填充错误。**

 那么如何找到这个G_IV呢？我们可以将G_IV的前面7个字节全部设置为0（这样不会改变明文中的前七个字节），而最后一个字节G_IV[-1]从0x00开始到0xFF（一个字节为8位，最多为256种可能）进行尝试，当解出明文的最后一个字节不为0x01就会发生填充错误，由此进行判断，最后我们必然找的到一个GIV[-1]使得“G_IV[-1] xor m[-1]=0x01”。 

 找到这个G_IV[-1]后，我们可以有以下推论：

```
G_IV[-1] xor m[-1] = 0x01      
# 找到一个G_IV[-1]与m[-1]异或为0x01

G_IV[-1] xor 0x01 = m[-1]     
# G_IV[-1]与0x01异或得到解密后的m[-1]

IV[-1] xor m[-1] = Plaintext[-1]     
# 将m[-1]与原本的IV[-1]异或就会得到明文的最后一个字节
```

 知道了m[-1]，这个同理我们可以继续构造G_IV[-1] xor m[-1] = 0x02，G_IV[-2] xor m[-2] = 0x02。因为m[-1]知道所以很容易得到G_IV[-1]，而后我们就可以将G_IV[-2]从0x00开始到0xFF，必定会找到GIV[-2] 使得“GIV[-2] xor m[-2] = 0x02”，此时不会发生填充错误。

```
GIV[-2] xor m[-2] = 0x02 
G_IV[-2] xor 0x02 = m[-2]     
IV[-2] xor m[-2] = Plaintext[-2]
```

 于是可以继续构造G_IV[-3]…G_IV[-8]，我们就可以得到该明文分组的所有字节。接下来我们就可以在后续的分组中使用该方法来获取所有明文分组，但是后续的明文分组是使用上一个密文分组来进行异或，所以我们需要修改的是前一个密文分组。

 注意：当对最后一个密文分组的中间值进行猜解的时候，会遇到明文本身最后一个字节为填充字节，如0x02，可能会得出不同的两个结果。我们将最后一个字节构造成0x01时，无论前面字节是什么都不会触发填充错误，而将最后一个字节构造成0x02同样也不会报错。这时我们可以在最后一个填充字节判断成功的情况下，构造倒数第二字节为任意值都不出现填充错误，则明文最后一个字节就构造成了 0x01。

##### 2.2.4 CBC 翻转攻击

 我们了解了如何猜解出中间值，并进一步通过中间值来得到明文。当我们知道其解密后的中间值，就可以构造一个IV使得二者异或得到的明文为我们想要的明文，从而完成攻击。

![image-20220628120803605](https://gitee.com/ymq_typroa/typroa/raw/main/20220628120803.png)

 具体攻击细节我们通过上图来了解，如上图所示，我们需要修改明文分组3的内容，就可以修改密文分组2的内容，让其与中间值3异或运算得到我们想要的结果。但是修改了密文分组2会让其解密后的中间值乱码（损坏），最后得到的明文会是乱码，所以我们需要通过前面的填充攻击的方式猜解出损坏的中间值，再通过修改密文分组来还原该明文分组。同理密文分组1对应的明文分组1也可通过修改IV来还原，最终我们就修改了明文分组3，而且其他明文不变。使用这种方法我们也可以修改整个明文以及添加新的明文。

#### 2.3 Shiro 721漏洞原理

 Shiro 721与Shiro 550对应的shiro版本加解密过程基本一致，只是在shiro 550之后，AES加密密钥都使用动态获取的方式。

![image-20220629105231787](https://gitee.com/ymq_typroa/typroa/raw/main/20220629105238.png)

 这里对解密过程就不多赘述，只看关键部分，将rememberMe字段进行base64解码及其他相关操作后，会调用AbstractRememberMeManager.class中的decrypt()方法对密文进行解密，而其使用的加解密算法任是AES的CBC模式，使用的填充方法是PKCS5Padding。

![image-20220630092332711](https://gitee.com/ymq_typroa/typroa/raw/main/20220630092339.png)

 接着来到cipherServer的decrypt()方法，这里会取出密文首部的16个字节赋值给iv，并将后续的密文，密钥，iv交由另一个decrypt()方法处理。![image-20220629150313740](https://gitee.com/ymq_typroa/typroa/raw/main/20220629150313.png)

 在该decrypt()方法中就直接调用crypt()方法出处理。

![image-20220629150354416](https://gitee.com/ymq_typroa/typroa/raw/main/20220629150354.png)

 接着看crypt()方法，这里会将密文解密，并检测明文的填充是否正确，若不正确，则会报错。

![image-20220629150537268](https://gitee.com/ymq_typroa/typroa/raw/main/20220629150537.png)

 后续也会在响应中重新设置cookie，设置rememberMe=deleteMe，所以我们可以使用该字段来判断。如下图我们使用Brup拦截登录成功后刷新页面的请求，修改rememberMe字段的最后一个字符，使得其发生填充错误。

![image-20220629145607125](https://gitee.com/ymq_typroa/typroa/raw/main/20220629145607.png)

 注意：我们需要登录以获取一个合法用户的rememberMe，因为Shiro会获取用户信息，若不是合法用户也会返回异常从而返回rememberMe=deleteMe。

 若填充正确，则会解密后的字节数组返回。最后交由AbstractRememberMeManager.class的convertBytesToPrincipals()方法处理，其会抵用deserialize()方法将解密后的字节数组进行反序列化处理，其中就会调用readObject方法进行反序列化。于是攻击者可以先构建执行命令的恶意对象，将其序列化，然后修改rememberMe字段中的IV与密文分组，通过CBC翻转攻击将明文构造成序列化后的恶意对象，最后让其进行反序列化操作，从而执行恶意命令。

### 三、漏洞复现

#### 3.1 实验环境

- 被攻击主机


 主机：Centos7.9 （IP：192.168.219.206）

 漏洞环境：shiro1.41（https://github.com/inspiringz/Shiro-721）

- 攻击主机


 主机：kali （IP：192.168.219.134）

 漏洞利用工具：shiro_exp.py（https://github.com/inspiringz/Shiro-721）

环境搭建：

1. 在Docker中拉取镜像

   ```
    docker pull vulfocus/shiro-721
   ```

   > ```
   > cd /opt/Shiro-721-master/Docker/
   > docker build -t shiro-721
   > ```

2. 利用镜像创建容器并运行。

   ```
    docker run -itd --name=shiro-721 -p 8080:8080 vulfocus/shiro-721s
   ```

3. 访问 [http://192.168.219.206:8080](http://192.168.219.206:8080/) ，如下：

   ![image-20220627172345818](https://gitee.com/ymq_typroa/typroa/raw/main/20220627172345.png)

#### 3.2 复现过程

1.使用ysoserial.jar 的 CommonsBeanutils1 生成对应的payload，此处执行的命令为在/tmp目录下创建一个shiro721的文件。

```
java -jar ysoserial.jar CommonsBeanutils1 "touch /tmp/shiro721" > payload.class
```

![image-20220627165226120](https://gitee.com/ymq_typroa/typroa/raw/main/20220627165233.png)

2.下载漏洞利用工具，解压后，将上面生成得payload.class放于exp目录下。

```
unzip Shiro-721-master.zip
mv payload.class Shiro-721-master/exp/
cd Shiro-721-master/exp/
```

3.打开Brup Suite，在浏览器中访问目标网址，使用任一账户登录并勾选“Remember Me”，登录完成后刷新页面并使用Brup拦截请求，从中获取到rememberMe字段。

![image-20220628102505445](https://gitee.com/ymq_typroa/typroa/raw/main/20220628102505.png)

4.在exp目录下执行shiro_exp.py生成恶意rememberMe 字段，格式为

`python shiro_exp.py url地址 rememberMe的值 paylaod.class`。

（此处需要使用Python2运行，可以在Kali中运行Python2命令）

```
python2 shiro_exp.py http://192.168.219.206:8080/login.jsp nwMZjaJG3xgP+zR8PJ2aaT6D2wz3ZRChx2vAfIACpUywYLi0ivQxsZ+nrtHjO37B9zHC1m9C/957U01sH5MJStSQpF1EDrh/uKc6A8xrO6/t1834TfiY0YN+6QaQ16ZnB/o5ATYDiQWyQ6VGwBGN4WiQgY7IMZtqtZJCRz26fSrICKe81frHFwg24Z0igvLgb1/Xnje5HSe5hfPp3uOR0fwdQe0VlD6EyQ5+N2/XrZ23yfI+c5iyOE0nXAAq1IVGgoTTpoF+hAaV1tE4e3X1H1NNDg3TgFmuBqlVZvVV1Rv2pejAXAkZBZYnHOjlQmxlBJjE1HUdIYN5IUNDBOA73g/f/0qJhkIqiPcdgVVW/6V/DDdlS8GfYB/7P03Ru8F0X1yOtiouy67CdlIC73DzhMs3sbG7stKYAwGJjIefMS87EKZ6maieY2iLIwcgwxrGxS2Ls6gMPp/c6RRvZEkI3Yb55kRyMGvH5dpWzwuV+UXLB2l0xMSy4mG1iNWKXzbM payload.class
```

![image-20220628103046484](https://gitee.com/ymq_typroa/typroa/raw/main/20220628103046.png)

此过程会很长，可能20分钟左右或者更久，生成的payload.class内容越多时间就越长，所以尽量选择较短的命令执行来复现漏洞即可。最终会生成如下rememberMe cookies。

![image-20220628102724639](https://gitee.com/ymq_typroa/typroa/raw/main/20220628102724.png)

5.将刚才拦截的请求放于repeater模块中，将rememberMe字段替换成我们生成的恶意rememberMe。

![image-20220628103243145](https://gitee.com/ymq_typroa/typroa/raw/main/20220628103243.png)

发送请求，而后查看容器中的tmp目录中的文件，发现成功创建了shiro721。

![image-20220628103443374](https://gitee.com/ymq_typroa/typroa/raw/main/20220628103443.png)

### 四、修复建议

1. 将shiro升级至安全的版本。
2. 关闭rememberMe持久化登录功能。

### 五、参考文章

1. 【现代密码学入门】31. CBC模式 (1)：工作原理（https://www.bilibili.com/read/cv11392532/）
2. padding oracle原理深度解析（[http://blog.topsec.com.cn/padding-oracle%e5%8e%9f%e7%90%86%e6%b7%b1%e5%ba%a6%e8%a7%a3%e6%9e%90/）](http://blog.topsec.com.cn/padding-oracle原理深度解析/）)
3. PaddingOracle攻击原理（http://cn-sec.com/archives/536995.html）
4. Shiro反序列化漏洞复现分析（Shiro-721）（https://www.roaing.com/shiro721.html）
5. Shiro 721 Padding Oracle攻击漏洞分析（https://www.anquanke.com/post/id/193165）