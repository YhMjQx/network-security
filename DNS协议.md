# ==DNS协议==

1.了解域名的结构

2.DNS的查询过程

3.在Windows server上部署DNS

4.分析流量    实施DNS欺骗    再分析

## 一、DNS

#### 1.概念

- DNS（domain name system）域名系统，作为将域名的IP地址的相互映射关系存放在一个分布式的数据库，DNS使用的是UDP的53号端口
- 域名：由ICANN机构统一管理    www.baidu.com    www.a.shifen.com    www.sina.com.cn    httpd.apache.org    等等

#### 2.域名空间

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816131608309.png" alt="image-20230816131608309" style="zoom:200%;" />

- 树状结构
  - 根域：（全世界只有13台根域服务器）
  - 顶级域：（主要用于区分域名的用途）
    - 组织类
      - .com    商业
      - .edu     教育类，学校类
      - .org      社会非营利性组织
    - 国家/地区域名
      - .cn    中国
      - .hk    香港
      - .us    美国
      - .uk    英国
  - 二级域
    - woniu.com
      - www.woniu.com     mail.woniu.com
  - FQDN（完全限定域名）    主机名.DNS后缀（二级域名）

## 二、DNS查询

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816144813831.png" alt="image-20230816144813831" style="zoom:200%;" />

- 客户机想要访问www.baidu.com，根据自己的TCP/IP参数，向自己的首选DNS服务器发送DNS请求
- 首选DNS服务器收到客户机的请求后，会去查询自己的区域文件，如果找不到www.baidu.com的IP地址信息，会将请求转发到根域服务器（需要配置根提示）；如果找到了www.baidu.com的IP地址，就直接响应给客户机
- 根域服务器收到请求后，由于根域服务器只维护顶级域服务器的信息，会向客户机响应顶级域服务器.com，首选DNS服务器根据根域服务器响应的信息，将请求转发给.com顶级域
- .com顶级域服务器收到请求后，由于.com顶级域服务器只维护二级域服务器的信息，于是将二级域服务器baidi.com的IP地址响应给首选DNS服务器，然后首选DNS服务器再根据这个信息将请求转发给baidu.com
- baidu.com二级域收到请求后，baidu.com的DNS服务器汇总所维护的是baidu.com区域中所有的主机信息，包含了www.baidu.com的信息，直接将www.baidu.com的IP地址响应给首选DNS服务器
- 首选DNS服务器再将www.baidu.com的IP地址响应给客户机

### 1.查询方式

##### 递归查询

- 当客户机请求自己的首选DNS服务器，首选DNS服务器上有域名记录信息，直接响应给客户机（如图所示第一步和第八步就是递归查询）

##### 迭代查询

- 首选DNS服务器没有域名记录信息，通过一步一步去请求根域服务器，顶级域服务器，二级域服务器，最终找到对应的域名记录信息

### 2.查询内容

- 正向：通过域名查IP
- 反向：通过IP查域名

## 三、使用Windows部署DNS服务器

#### 1.使用Linux（bind服务器） 

#### 2.DNS服务器分类

- 主要名称服务器：存放区域（二级域）中相关的设置，存放的是区域文件的正本数据
- 辅助名称服务器：存放的是副本数据，从主要名称服务器赋值过来，不能修改
- 主控名称服务器：提供数据赋值（简单可以理解为DNS服务器中的某一个角色）
- 缓存（cache-only）域名服务器：里面没有区域文件，需要转发数据（直接赚转发给外部的二级域服务器）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816164528413.png" alt="image-20230816164528413" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816164554838.png" alt="image-20230816164554838" style="zoom:200%;" />

添加DNS服务器，除了我下面专门提醒的，其他基本上都是下一步

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816164800061.png" alt="image-20230816164800061" style="zoom:200%;" />

点击空白，添加主机记录

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816165143842.png" alt="image-20230816165143842" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816205008194.png" alt="image-20230816205008194" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816205011908.png" alt="image-20230816205011908" style="zoom:200%;" />

这两张图片说明了什么，说明对于百度来说

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816205103311.png" alt="image-20230816205103311" style="zoom:200%;" />

shifem.com是他的二级域，a.是他的子域，www是他的主机头

#### 3.DNS记录

- A记录：主机记录，域名和IP地址的映射关系
- CNAME：别名记录
- SOA：全为名称服务器
- NS：名称服务器
- MX：邮件交换记录，一般有邮件服务器时使用
- SRV：正在提供特定服务的服务器
- PTR：反向指针

![image-20230816205753150](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816205753150.png)

创建一个反向查找区域，这里的网段是根据下面这个对应的<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816205919808.png" alt="image-20230816205919808" style="zoom:200%;" />

#### 4.区域传送

- 将主要名称服务器的区域文件传送到辅助名称服务器上
- 区域文件传送使用的是TCP协议

要想做到区域传送，就要先配置好区域传送

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816211812120.png" alt="image-20230816211812120" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816211920732.png" alt="image-20230816211920732" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816211952194.png" alt="image-20230816211952194" style="zoom:200%;" />

于是在辅助区域中也能看到主区域中的文件了

下面是在辅助DNS下配置反向

![image-20230816212319938](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816212319938.png)

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230816212312974.png" alt="image-20230816212312974" style="zoom:200%;" />

## 四、分析DNS流量

#### 1.DNS报文字段

- ID

- flags（标志位） 

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230817225549641.png" alt="image-20230817225549641" style="zoom:200%;" />

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230817225614067.png" alt="image-20230817225614067" style="zoom:200%;" />

  - 第一位：标识报文类型（0是请求，1是响应）
  - 第2-5位：opcode（查询种类）
  - 第6位：是否是权威应答（响应报文中存在）
  - 第7位：一个UDP报文为512字节，指示是否截断超过的部分
  - 第8位：是否请求递归
  - 第9位：允许递归标识
  - 第10-12位：保留位
  - 第13-16位：应答码（响应报文中存在）
    - 0    没有错误
    - 1    格式错误
    - 2    服务器错误
    - 3    名字错误
    - 4    服务器不支持
    - 5    拒绝
    - 6-15    保留

- Questions： 请求段中的问题记录数

- Answer RRs：回答段中的应答记录数

- Authority RRs：授权段中的授权记录数

- Addition RRs：附加段总的附加记录数

- 


 

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818194018683.png" alt="image-20230818194018683" style="zoom:200%;" />

这个是在DNS服务器上配置转发器的情况，为了更加快速的完成DNS服务，黑色的线（win10向DNS服务器发送请求，服务器去找到外部的二级域名DNS，从外部二级域名DNS服务器上获取到win10想要的域名信息，然后外部二级域名DNS服务器发送给server2016，server2016会先将域名信息缓存在自己的服务器中，再由server2016发送给win10），红色的线（win10向server2016发送DNS请求，server2016发现自己有该域名的数据信息，直接响应给win10）

## 五、DNS欺骗

实验：在server上安装web服务器，让kali（使用ettercap工具）欺骗win10，使得win10访问其他网页时，会被跳转到该服务器上

1.在server上安装web服务器

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818203027962.png" alt="image-20230818203027962" style="zoom:200%;" />

并开启https的443端口（证书去网上随便搞一个）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818204743704.png" alt="image-20230818204743704" style="zoom:200%;" />

2.修改ettercap中的文件，

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818203224452.png" alt="image-20230818203224452" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818203405308.png" alt="image-20230818203405308" style="zoom:200%;" />

这里101.37.65.91是www.woniuxy.com的IP地址，意思是访问www.sohu.com是让其跳转到www.woniuxy.com上去，其中一个A是代表了IPv4的意思

3.开始执行欺骗

- 首先，这是服务器的IP和网关

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818203900073.png" alt="image-20230818203900073" style="zoom:200%;" />

- 接下来是ettercap的操作，我们的目的是欺骗win10（192.168.19.66）的访问，我们需要先进行ARP欺骗，然后再进行DNS欺骗
  - ARP欺骗

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818203938669.png" alt="image-20230818203938669" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818204046380.png" alt="image-20230818204046380" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818204209098.png" alt="image-20230818204209098" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818204243638.png" alt="image-20230818204243638" style="zoom:200%;" />

DNS欺骗

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818204517663.png" alt="image-20230818204517663" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818204541618.png" alt="image-20230818204541618" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818204611463.png" alt="image-20230818204611463" style="zoom:200%;" />

上面的操作和命令的操作效果是一样的

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818205047990.png" alt="image-20230818205047990" style="zoom:200%;" />

4.效果

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818205146524.png" alt="image-20230818205146524" style="zoom:200%;" />

如果此时我进行登录，而有人对我进行抓包，我的账号和密码就会被别人知道

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818205249666.png" alt="image-20230818205249666" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230818205413023.png" alt="image-20230818205413023" style="zoom:200%;" />
