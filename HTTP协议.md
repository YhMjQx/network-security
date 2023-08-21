# ==HTTP协议==

1.HTTP协议结构

2.在Windows server去搭建web服务器

3.分析HTTP流量

## 一、HTTP协议

### 1.概念

- HTTP（超文本传输协议）是用于在万维网服务器上传输超文本（HTML）到本地浏览器的传输协议
- 属于TCP/IP协议簇的一员（主要传输HTML文件，图片，查询结构等等）
- 基于传输层TCP的80端口

### 2.万维网服务

- 采用C/S架构
- 客户机通过浏览器去请求，从而在浏览器上就可以看到对应的图形界面  浏览器/服务器架构（B/S）

### 3.万维网服务的软件

- Windows server IIS（Windows平台）
- Apache（多平台）
- Tomcat（多平台）
- nginx（多平台）

- ......

## 二、HTTP工作原理

- 在客户端使用浏览器通过URL向HTTP服务器发送请求

  - URL（统一定位符），有三部分组成

  <img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230821174015676.png" alt="image-20230821174015676" style="zoom:200%;" />

- web服务器根据收到的请求直接向客户机响应信息
- 针对于HTTP默认端口号是80端口，默认端口可以改（会影响客户机的访问，如果要改建议改为非标准端口）
- 交互过程

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230821192730343.png" alt="image-20230821192730343" style="zoom:200%;" />

1.注意事项

- HTTP是无连接的：限制每次连接只处理一个请求
- HTTP是独立的：只要客户端和服务器知道如何处理数据内容，任何类型的的数据都可以通过HTTP发送，客户端以及服务器指定使用适合的MIME-type（消息内容类型）
- HTTP是无状态的：没有记忆能力，后续处理的内容需要用到前面的内容时，就必须重传，每次连接传送的数据量比较大，从另一个角度思考。服务器不需要提供先前信息，应答就比较快

**现在配置web服务器**

先做一个dhcp，让电脑获取可以联网的IP，可以手动也可以命令

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230821203211152.png" alt="image-20230821203211152" style="zoom:200%;" />

中间省略安装过程（和之前的其他服务器一样的），直接调到安装好的

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230821204212537.png" alt="image-20230821204212537" style="zoom:200%;" />

像这样在服务器中创建文件

然后再改文件下将这份代码放进下面的文件文件中

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230821204335078.png" alt="image-20230821204335078" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230821204342530.png" alt="image-20230821204342530" style="zoom:200%;" />

然就进入服务器，新建网站（把自带的默认站点关闭）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230821204422328.png" alt="image-20230821204422328" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230821204442976.png" alt="image-20230821204442976" style="zoom:200%;" />



<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230821205444474.png" alt="image-20230821205444474" style="zoom:200%;" />

报文中采用持久性连接的目的也是为了防止请求很快失效，那么有时候我就需要不停的输入账号和密码，频繁的这样不仅会很麻烦还会造成安全性问题（因为网络流量中有大量的账号和密码数据）

**HTTP协议状态码**

- 1开头的：一般情况下表示服务器收到了客户机的请求
- 2开头的：客户机请求成功，服务器给客户机想要的东西
- 3开头的：一般为重定向，如果访问页面不存在，浏览器会重定向到有效页面中去
- 4开头的：一般为用户端出错（访问的东西错误或等等）
-  5开头的：一般为服务器出错
