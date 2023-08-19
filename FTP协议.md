# ==FTP协议==

1.了解FTP协议

2.使用在Windows操作系统上使用serv-U软件搭建FTP服务器

3.分析FTP流量

## 一、FTP协议

1.概念

- FTP（文件传输协议），由两部分组成：客户端/服务器    C/S，应用场景：企业内部存放公司文件，开发网站时，利用FTP协议，将网页或程序传到网站服务器，网络中传输一些大文件也使用该文件
- FTP：基于传输层TCP，默认端口号（20号端口一般用于传输数据，21号端口用于传输控制信息）但是，是否使用20号端口作为传输数据端口，和FTP的传输模式有关
  - 如果采用的是主动模式，传输数据使用20号端口
  - 如果采用被动模式，传输数据时使用的端口需要服务器与客户机协商决定

- 主动模式（port方式）

  - 建立连接使用21号端口，客户端通过此通道向服务器发送port命令，服务器从20端口主动向客户端发起连接

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819134651838.png" alt="image-20230819134651838" style="zoom:200%;" />

- 被动模式（pasv（passive）方式）

  - 建立连接使用21号端口，客户端向服务器发送pasv命令，服务器收到后随机打开一个高端端口（大于1024），服务器在指定范围内的某个端口被动等待客户机连接

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819135339255.png" alt="image-20230819135339255" style="zoom:200%;" />

- 传输文件时的传输模式
  - 文本模式：ASCII模式，以文本序列传输
  - 二进制模式：binary模式，（视频，图片，程序...）

## 二、FTP的客户端和服务端

#### 1.服务端程序

- serv-U
- filezilla server（开源）
- vsftpd（Linux平台下）
- Windows server IIS（FTP发布服务）

#### 2.客户端程序

- 命令行：ftp 192.168.10.10              访问
- 资源管理器：ftp://192.168.10.10    访问
- 浏览器：ftp://192.168.10.10            访问
- 第三方工具
  - flashFXP
  - filezilla client
  - cuteftp
  - xftp

## 三、部署FTP服务器

#### 1.针对于FTP用户

- 匿名用户
  - anoymous固定名称（某些FTP的服务端软件也可以使用 FTP用户名作为匿名用户）
- 普通用户

用serv-U演示一下（要么关闭防火墙，要么在防火墙中设置端口访问权限）

现在虚拟机当中弄几个文件

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819153335317.png" alt="image-20230819153335317" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819153517620.png" alt="image-20230819153517620" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819153529693.png" alt="image-20230819153529693" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819153645438.png" alt="image-20230819153645438" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819153701686.png" alt="image-20230819153701686" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819153714740.png" alt="image-20230819153714740" style="zoom:200%;" />

 创建用户（匿名用户没有密码，填密码时直接下一步）![image-20230819153748564](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819153748564.png)

下面是zhangsan用户需要设置访问权限

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819153945509.png" alt="image-20230819153945509" style="zoom:200%;" />

然后输入这个192.168.237.131（server 2016的IP）就可以直接用物理机访问到虚拟机的文件了

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819154038148.png" alt="image-20230819154038148" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819154045268.png" alt="image-20230819154045268" style="zoom:200%;" />

然后通过抓包可以看到很多信息，先建立TCP三次握手，然后客户机发送指令，申请连接，申请好之后传输文件等等差不多就这些内容

#### 2.针对于FTP协议被动模式

- 如何使用域中其他账户登录让其访问自己的根目录

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819211148342.png" alt="image-20230819211148342" style="zoom:200%;" />

  使用上述的ftp方式登录进来之后，在界面右击点击登录，然后就直接跳转到张三用户的根目录去了，此时可以在该目录下创建新的文件夹，也可以将自己原有的文件传进去

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819211238215.png" alt="image-20230819211238215" style="zoom:200%;" />

- 如何使用虚拟路径让其他用户可以访问另一个用户的根目录

如何设置远程访问占用端口？这个方法再加上防火墙配置访问端口，可以让安全系数高一点点

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819211825236.png" alt="image-20230819211825236" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819211851376.png" alt="image-20230819211851376" style="zoom:200%;" />

在防火墙高级设置当中

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819212515593.png" alt="image-20230819212515593" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819212542234.png" alt="image-20230819212542234" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819212601046.png" alt="image-20230819212601046" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819212622278.png" alt="image-20230819212622278" style="zoom:200%;" />

此时才能更安全一点访问，那么虚拟路径是个怎么回事呢？看下面

我们在C盘下新建一个lisi用户的根目录，那么我们尝试用zhangsan的用户文件（在D盘）来访问lisi的文件

首先需要给zhangsan用户添加lisi文件的访问权限

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819213509843.png" alt="image-20230819213509843" style="zoom:200%;" />

然后在zhangsan用户属性中配置虚拟路径

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819213721934.png" alt="image-20230819213721934" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819213735392.png" alt="image-20230819213735392" style="zoom:200%;" />

此时就会在zhangsan的根目录中产生一个虚拟的文件路径叫做李四的文件夹，点进去就会直接跳转到lisi的根目录中（相当于是将lisi的根目录中的文件映射到了zhangsan的根目录中以一个虚拟目录的方式存在）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230819213854096.png" alt="image-20230819213854096" style="zoom:200%;" />

#### 3.FTP状态码

| 状态码       | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| **1xx**      | 肯定初步答复，指示某一项操作已经成功开始，但客户端希望在继续操作新的命令前得到另一个答复 |
| **110**<br/> | **重新启动标记答复**                                         |
| 120          | 服务已就绪<br/>                                              |
| 125 ****     | 数据连接已打开，正在开始传输<br/>                            |
| **150 **     | **文件状态正常，准备打开数据连接 ftp，使用两个端口：21发送命令，20发送数据，150表示服务器准备在20端口上打开连接，发送数据。** |
| **2xx**      | **肯定完成答复，某一项操作已经成功完成，客户端可以执行新的命令** |
| **200**      | **确定**                                                     |
| 202          | 未执行命令，命令过多                                         |
| 211          | 系统状态，或系统帮助答复                                     |
| 212          | 目录状态                                                     |
| 213          | 文件状态                                                     |
| 214          | 帮助消息                                                     |
| 215          | name系统类型，name是Assigned Numbers文档所列的正式名称       |
| **220**      | **服务就绪，可以执行新用户请求**                             |
| 221          | 服务关闭控制连接。如果适当，请注销。                         |
| 225          | 数据连接打开，没有进行中的传输                               |
| **226**      | **关闭数据连接**                                             |
| **227**      | **进入被动模式**                                             |
| **230**      | **用户已登录，继续**                                         |
| **250**      | **请求的文件操作正确，完成**                                 |
| 257          | 已创建“PATHNAME”                                             |
| 3xx          | 肯定中间答复，此命令已经成功，但服务器需要更多客户端的信息以完成对请求的处理 |
| **331**      | **用户名正确，输入密码**                                     |
| **332**      | **需要登录账号**                                             |
| 350          | 请求的文件操作正在等待进一步的信息                           |
| 4xx          | 瞬时否定答复，此命令不成功，但错误是暂时的。如果重试，有可能会成功 |
| 421          | 服务不可用，正在关闭控制连接                                 |
| **425**      | **无法打开数据连接**                                         |
| 426          | Connection closed                                            |
| 450          | 未执行请求的文件操作。文件不可用                             |
| 451          | 请求的操作异常终止                                           |
| 452          | 未执行请求的操作，系统存储空间不够                           |
| 5xx          | 永久性否定的答复，此命令不成功。                             |
| 500          | 语法错误，无法识别。可能包括命令过长之类的                   |
| 501          | 在参数中有语法错误                                           |
| 502          | 未执行命令                                                   |
| 503          | 错误的命令序列                                               |
| 504          | 未执行该参数的命令                                           |
| **530**      | **未登录**                                                   |
| 532          | 存储文件需要账户                                             |
| **550**      | **未执行请求的操作，文件不可用、无权限的操作**               |
| 551          | 请求的操作异常终止                                           |
| 552          | 请求的文件操作异常终止                                       |
| 553          | 未执行请求的操作，不允许的文件名                             |

