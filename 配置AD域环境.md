[TOC]



# ==配置AD域环境==

课程目标

1. 了解Windows AD域相关概念
2. 掌握在Windows server 上部署AD域控制器和辅助域控制器，并将客户机加入域完成主域控和辅助域控搭建，并将客户机加入域

教材内容

## 部署AD域环境（Win2008）

### 一、工作组和域

1、为什么需要域

在早期Windows主机都是属于工作组网络，单独的个体，在企业环境中，针对于工作组网络的计算机要达到统一管理相当麻烦，为实现将一个企业中所有的用户和计算机进行集中管理（如域安全策略、软件集中安装部署、统一登录认证等），在Windows server操作系统上部署AD来实现这一需求。

工作组主机（独立操作，适用于个人电脑）

![image-20230814005454922](https://gitee.com/ymq_typroa/typroa/raw/main/202308140054953.png)

域主机（统一操作，适用于工作环境）

![image-20230814005412762](https://gitee.com/ymq_typroa/typroa/raw/main/202308140054806.png)

#### 二、Active Directory基本概念

##### 1、概述

- 活动目录（Active Directory）是面向Windows Standard Server、Windows Enterprise Server以及 Windows Datacenter Server的目录服务。
- Active Directory不能运行在Windows Web Server上，但是可以通过它对运行Windows Web Server的计算机进行管理。
- Active Directory存储了有关网络对象的信息，并且让管理员和用户能够轻松地查找和使用这些信息。
- Active Directory使用了一种结构化的数据存储方式，并以此作为基础对目录信息进行合乎逻辑的分层组织

##### 2、功能

- 服务器及客户端计算机管理：管理服务器及客户端计算机账户，所有服务器及客户端计算机加入域管理并实施组策略。
- 用户服务：管理用户域账户、用户信息、企业通讯录（与电子邮件系统集成）、用户组管理、用户身份认证、用户授权管理等，按省实施组管理策略。
- 资源管理：管理打印机、文件共享服务等网络资源。
- 桌面配置：系统管理员可以集中的配置各种桌面配置策略，如：用户使用域中资源权限限制、界面功能的限制、应用程序执行特征限制、网络连接限制、安全配置限制等。
- 应用系统支撑：支持财务、人事、电子邮件、企业信息门户、办公自动化、补丁管理、防病毒系统等各种应用系统
- 主要将网络中的计算机逻辑上组织到一起集中管理

#### 三、Active Directory相关概念

##### 1、Active Directory

- AD是Windows server的一种服务
- AD是一个目录数据库，被用来存储用户账户、计算机账户、打印机与共享文件夹等对象，而提供目录服务的组件就是AD域服务器，它负责目录数据库的存储、添加、删除、修改与查询等工作

##### 2、域

- 活动目录的一种实现形式。
- 域是Windows网络中独立运行的单位，域之间相互访问则需要建立信任关系(即Trust Relation)。
- 当一个域与其他域建立了信任关系后，两个域之间不但可以按需要相互进行管理，还可以跨网分配文件和打印机等设备资源，使不同的域之间实现网络资源的共享与管理，以及相互通信和数据传输

##### 3、域控制器（DC，Domain Controller）

- 安装了活动目录的一台计算机（一般为Windows server）
- 一个域可以有多台域控制器

##### 4、名称空间（DNS域名空间）

- 是一个区域的名字（在DNS上新建的一个区域）
- 定位了网络资源（域名资源）的位置

##### 5、对象和属性

- 对象由一组属性组成，它代表的是具体的事物
- 属性就是用来描述对象的数据

##### 6、容器（组织单位、域）

- 是一种特殊的活动目录对象
- 作用是存放对象的空间

##### 7、LDAP协议及相关名词

- 轻量级目录访问协议，它基于X.500标准，是一个开放的、中立的、工业标准的应用协议。

- 可以查询与更新活动目录数据库，活动目录利用LDAP名称路径来描述对象在活动目录内的位置。

- 域中一个活动目录的例子，“CN=zhangsan,OU=网络安全,DC=woniuxy,DC=com”

  含义：zhangsan这个对象位于 woniuxy.com 这个域的网络安全组织单位(OU)中

  部分关键词说明：

  - DC（Domain Component，域组件）：表示使用 DNS 来定义其名称空间的 LDAP 树的顶部，用 . 分开的每个单元都可以看成是一个DC域组件，上述的 woniuxy.com 就被分成了两个。

  - OU（Organization Unit，组织单位）：组织单位中包含对象、容器，还可以包含其他组织单位。

  - CN（Common Name，通用名称） ：对象的名称，如 zhangsan。

  - DN（Distinguished Name，可分辨名称）：AD 域中每个对象都有唯一的 DN，DN 有三个属性，就上述的 DC、OU、CN。

  - UPN（User Principal Name，用户辨别名称）：用于用户身份标识，如在域 woniuxy.com 中的 zhangsan 用户，它的UPN为：[zhangsan@woniuxy.com](mailto:zhangsan@woniuxy.com)。

  - FQDN（Fully Qualified Domain Name，全限定域名）：同时带有主机名和域名的名称。如上述的zhangsan的 FQDN 为 zhangsan.woniuxy.com。

    ![image-20230227111222401](https://gitee.com/ymq_typroa/typroa/raw/main/202302271113986.png)

##### 8、域组策略（GPO对象）

- 若干策略的集合
- 应用到容器会影响容器内所有的计算机和用户

#### 四、域部署结构

##### 1、物理结构

- 站点：可以将高速连接的网络中多台域控制放入一个站点

  - 一个域的域控制器分布在不同的站点中，而站点之间是慢速连接，由于不同站点的域控制器之间会互相复制AD DS数据库，因此要谨慎规划执行复制的时段，尽量在离峰时段执行复制工作，频率不要过高，避免复制时占用站点之间的连接带宽，影响站点之间其他数据的传输效率
  - 同一个站点内的域控制器之间是通过快速链路连接在一起的，在复制AD DS数据时，可以实现快速复制。AD DS会设置让同一个站点内、隶属于同一个域的域控制器之间自动执行复制操作，默认的复制频率也要高于不同站点之间的域控制器。

- 域控制器

  ![image-20220320232705431](https://gitee.com/ymq_typroa/typroa/raw/main/202203202327499.png)

##### 2、逻辑结构

- 单域：网络中只建立了一个域

- 域树：具有连续的名称空间的多个域

- 域林：由一个或多个没有形成连续名称空间的域树组成

- 组织单位：域内部的一种容器（用于存放对象）

  ![image-20220320232359841](https://gitee.com/ymq_typroa/typroa/raw/main/202203202323906.png)

#### 五、域功能级别和林功能级别

**AD DS将域与林划分为不同的功能级别，每个级别各有不同的功能与限制**

##### 1、域功能级别

- 会受早期域控制器（操作系统）版本影响
- 只会影响到该域，不会影响到其他域

##### 2、林功能级别

- 会受域功能级别影响
- 会影响到该林的所有域

![image-20220320235036372](https://gitee.com/ymq_typroa/typroa/raw/main/202203202350445.png)

#### 六、部署Windows域

##### 1、配置Windows Server 2008 主域控

（1）域控Server最好配置为固定IP

![image-20220320235737747](https://gitee.com/ymq_typroa/typroa/raw/main/202203202357800.png)

（2）添加服务器角色（Active Directory域服务）

![image-20230815120308111](https://gitee.com/ymq_typroa/typroa/raw/main/202308151203254.png)

![image-20230815120502462](https://gitee.com/ymq_typroa/typroa/raw/main/202308151205516.png)

一路下一步，进行AD域服务的安装。

![image-20230815120547647](https://gitee.com/ymq_typroa/typroa/raw/main/202308151205696.png)

（3）开始配置域服务器

![image-20230815120717988](https://gitee.com/ymq_typroa/typroa/raw/main/202308151207043.png)

![image-20230815120808737](https://gitee.com/ymq_typroa/typroa/raw/main/202308151208786.png)

![image-20230815120934171](C:/Users/Denny/AppData/Roaming/Typora/typora-user-images/image-20230815120934171.png)

输入根域名：woniuxy.com

![image-20230815121128603](https://gitee.com/ymq_typroa/typroa/raw/main/202308151211643.png)

选择成为DNS服务器

![image-20230815121428586](https://gitee.com/ymq_typroa/typroa/raw/main/202308151214631.png)

选择存储位置，建议保持默认：

![image-20230815121519912](https://gitee.com/ymq_typroa/typroa/raw/main/202308151215952.png)

输入密码：Woniu123等，满足密码强度要求：

![image-20230815121629949](https://gitee.com/ymq_typroa/typroa/raw/main/202308151216987.png)

确认配置没有问题后进入下一步，开始配置：

![image-20230815121720858](https://gitee.com/ymq_typroa/typroa/raw/main/202308151217904.png)

- 部署配置：添加新林（网络中没有林也没有域）
- 域控制选项：域功能级别和林功能级别设定，域控制功能（一般情况下第一台域控制器都会安装DNS服务器，网络中第一台域控制一定是全局编录服务器（GC），目录服务器还原模式密码用于恢复活动目录数据时使用）
- 其他选项：NetBIOS域名一般为二级域名称（使用默认）
- 路径：活动目录数据库及日志存放位置
- 检查：无错误项即可安装

（5）在域控服务器上添加一个账号用于登录

##### 2、配置一台Windows 7的客户机

（1）将客户机加入域

为客户机配置正确的DNS服务器（输入的DNS服务器的IP，而不是域控制器的IP）这里域控制器和DNS为同一台

![image-20220321001913456](https://gitee.com/ymq_typroa/typroa/raw/main/202203210019532.png)

根据提示，需要输入一个有权限加入该域的帐户的名称和密码（域用户，普通用户或域管理员都可）

![image-20220321002323094](https://gitee.com/ymq_typroa/typroa/raw/main/202203210023200.png)

（2）测试是否可以使用域账户登录Windows7, 如果可以，则说明域环境配置成功。

![image-20241101152243863](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241101152243863.png)

![image-20241101152439633](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241101152439633.png)

![image-20241101152622270](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241101152622270.png)

大小写字母，数字

课程小结

针对于AD域环境需要了解的相关概念，通过部署主域控和额外域控来充分理解域的相关内容

1. 如何在现有林中创建新域（域树）
2. 如何创建新林
3. 理解AD域中的相关概念
4. 完成本节部署域环境实验（主要域控和辅助域控）



