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

### 1.物理结构

- 站点：可以将高速连接的网络中多台域控制器放入一个站点（一个站点中，至少有一台全局编录服务器）

![image-20230829191754528](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230829191754528.png)

- 域控制器
  - 当创建了一个新的用户，这个新的用户需要同步到其他所有域控制器上

![image-20230829191302673](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230829191302673.png)

![image-20230829191318391](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230829191318391.png)

![image-20230829191325141](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230829191325141.png)



### 2.逻辑结构

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

## 三、对象管理

### 1.用户

### 2.组

- 组的作用域
  - 本地域组：针对本地域，使用范围是本域
  - 全局组：管理日常维护的目录对象，使用范围整个林及信任域
    - 如果有两个不同域的用的，例如zhangsan在woniu林，lisi在woniuxy林，要相通过lisi用户登录进woniu林，只需要将lisi放进woniu和woniuxy两个林的全局组就好了
  - 通用组：身份信息记录在全局编录中，查询速度快（使用范围整个林及信任域）
  - 同林都是信任的，父域和子域默认信任关系
- 组的类型
  - 安全组：用来设置访问权限
  - 通讯组：用于电子邮件通信

### 3.组织单位（OU）

- OU是AD中的容器（对象（容器是用来存放用户或计算机的））

- 创建：部门，地理位置，对象类型


- 针对用户实施策略时使用

组织单位一般情况下是默认无法删除的，要想删除，需要在查看-》高级功能勾选了之后才有删除权限

## 四、组策略应用

**1.策略只能应用到对应的容器中**

2.策略应用

- 整个域
- 组织单位（OU）
- 站点

域中的**组策略**称为**GPO**（group policy object）：组策略对象

比如在一个域中创建组策略应用，然后将一台客户机加入该域，该客户机就会默认使用该组策略应用

3.组策略规则

- 策略的继承与阻止
  - 下级容器默认会继承来自上级的GPO
  - 子容器可以阻止来自上级容器的GPO
- 策略的强制生效和筛选
  - 强制生效
    - 强制生效会覆盖组织继承设置
  - 筛选
    - 可以针对单个特定的计算机或用户配置GPO权限（直接在OU内选定进入高级设置将权限设置为拒绝）

![image-20230830185745492](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830185745492.png)

策略的优先级问题

本地组策略    L

组策略           D

站点策略        S

OU策略          OU

L S D OU策略的应用程序，这是策略运用的顺序，当发生则略冲突时，OU的优先级最高
