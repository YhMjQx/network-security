# ==AD域服务（Active Directory活动目录）==

1.了解活动目录的相关概念

2.会在Windows服务器上部署域控制器（主/辅），将客户机加入域

3.会在域控制器上设置组策略，从而去影响域中的用户和客户机

4.扩展

- 如果将一台Windows 2003的域提升为Windows 2008的域
  - 涉及一问题：操作主机的概念
- 如何对与控制器进行备份
  - 系统状态备份

在早期的时候，所有的计算机都是独立的个体（每台计算机都有自己的用户或组），想要统一管理，在企业中，部署活动目录服务器，从而对企业中的所有用户及计算机进行集中管理

## 一、活动目录（AD）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828125219663.png" alt="image-20230828125219663" style="zoom:200%;" />

### 1.概念

- 面向Windows服务器中的目录（Windows web server）

### 2.功能

- 服务器及客户端计算机管理

- 用户服务
- 资源管理：打印机，文件共享
- 桌面配置：集中配配置置统一桌面或者对桌面策略（域策略）（gpedit.msc打开本地组策略管理器）
- 应用紫铜支撑：财务、OA，办公自动化

### 3.其他概念

- AD：是Windows中的一种服务，也是一个目录数据库
- 域：活动目录的一种体现形式，主要是由域控制器和成员计算机组成
- 域控制器：一台部署了活动目录域的服务器
- 域名空间：定位了网络资源位置
- 域中的客户机称之为对象，每一个对象都有对应的属性
  - 对象：表示了具体的事务
  - 属性：用于描述对象的数据

- 容器
  - 用于存放对象的空间，比如说域就是一个容器
- 域的组策略

## 二、域的结构

1.物理结构

2.逻辑结构

- 单域：网络中只建立了一个域

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828133549316.png" alt="image-20230828133549316" style="zoom:200%;" />

- 域树：具有连续域名空间的多个域
- 域林：由一个或多个没有形成连续域名空间的域树组成

服务器上配置

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828134003249.png" alt="image-20230828134003249" style="zoom:200%;" />

林功能级别要小于等于域功能级别，目的是为了让多个域都可以接受林功能（高版本可以兼容低版本，但是低版本不能兼容高版本）

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828134716862.png" alt="image-20230828134716862" style="zoom:200%;" />

全局编录（GC）：全局目录数据库

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828153910792.png" alt="image-20230828153910792" style="zoom:200%;" />

目录还原模式密码这个是对系统状态备份还原时需要的密码

然后将这个安装好之后，需要重启这时打卡计算机管理我们会发现此时的本地用户和组不见了，是因为现在的用户和组都升级成了域用户和组，此时他们被存放在了Active Directory中，而且本机还自动装好了DNS服务器

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828154851547.png" alt="image-20230828154851547" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828154532454.png" alt="image-20230828154532454" style="zoom:200%;" />

我们来看如何将客户机添加进域中

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828155225200.png" alt="image-20230828155225200" style="zoom:200%;" />

在可以适用DNS服务（可以解析域名）的前提下我们将客户机加入域中

步骤：系电脑-》右击属性-》高级系统设置-》计算机名-》更改

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828155529765.png" alt="image-20230828155529765" style="zoom:200%;" />

可以适用管理员将该客户机加入域中

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230828155648266.png" alt="image-20230828155648266" style="zoom:200%;" />

然后重启就好了