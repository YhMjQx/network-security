# ==LAMPP基础环境==

## 一、环境组合

LAMPP：Linux + Apache + MySQL + PHP + Python

LNMP：Linux + Nginx + Mysql + PHP(Python)

Java：Linux + JDK + Tomcat + MySQL

其他：

DB：MySQL、MangoDB、Redis

服务器：Apache、Nginx、Tomcat、Weblogic、Webshpere、IIS（这个是微软开发的）

## 二、PHP应用部署

Xampp是集合了LAMPP的完整的运行环境，相对来说比较适合于开发环境和调试环境，但相对来说，安全性配置不足。

PHPStudy、Wampp，基于XAMPP讲解，然后再Xampp上部署其他应用，在PHPStudy上部署类似环境

编程语言分为：

编译型：将源代码编译为二进制，然后执行二进制指令（c，c++，java...）

解释型：解释器直接执行源代码，效率偏低（php...）



- Xampp默认启动后，Apache使用80 端口，所以要想访问需要先放通服务器80端口，其不能关闭防火墙，可以使用 `firewall-cmd --add-port=80/tcp --permanent
  ` 或者使用富规则
- [PHP 7.3.29 - phpinfo()](http://192.168.230.147/dashboard/phpinfo.php) http://192.168.230.147/dashboard/phpinfo.php该网址中展示了所有的运行环境和参数，通常情况下，建议删除该页面
- 默认情况下， /opt/lampp/htdocs 目录对应的是LAMPP应用程序的根目录（Document Root） /opt/lampp/htdocs/dashboard/phpinfo.php 相当于  /dashboard/phpinfo.php

> ![image-20240117144141518](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117144141518.png)
>
> 这个就是该应用程序的根目录，程序运行都是在这个目录下运行的
>
> ![image-20240117144527387](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117144527387.png)
>
> 这个是其中文件所包含的内部文件等等，对应于网页
>
> ![image-20240117144605515](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117144605515.png)
>
> 结合上面的信息我们做一些简单的操作熟悉一下
>
> ##### 做一做简单的对网页的操作
>
> 首先，下面这张图是原本的 htdocs 目录下的 application.html 的部分代码，对应的我网页如下下图所示
>
> ![image-20240117144845192](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117144845192.png)
>
> ![image-20240117144954467](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117144954467.png)
>
> 接下来我将在源代码中添加一句话
>
> ![image-20240117145415078](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117145415078.png)
>
> 我们试着刷新一下网页看看效果
>
> ![image-20240117145425855](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117145425855.png)
>
> 目的达成
>
> 
>
> ##### 修改phpinfo.php网页的路径
>
> ![image-20240117150213971](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117150213971.png)
>
> 原本 phinfo.php 文件存在于 /opt/lampp/htdocs/dashboard ，现在我们在/opt/lampp/htdocs 目录下写一个php文件，从而达到也可以访问phpinfo.php的目的
>
> ![image-20240117150016062](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117150016062.png)
>
> ![image-20240117150021533](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117150021533.png)
>
> ok,现在我们去网页访问 /ymqxamppinfo.php
>
> ![image-20240117150155388](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117150155388.png)
>
> 现在我们访问路径不一样，但依旧可以访问该页面，但是我在想，能不能吧把原来页面的路径删除，只留下我自己创建的页面呢。好吧至少目前我还不会，能达到以上目的，我猜应该也是利用了php函数，根本还是用的是phpinfo.php文件，只是利用函数创建了一个链接而已



- 在 /opt/lampp/htdocs 目录下，创建二级目录 xindai ，用于部署 小额信贷系统，并复制相应文件到该目录
- 在MySQL客户端环境中，导入该系统的配套数据库：类似于 数据库名称叫什么？有什么要求？编码格式是什么？这种问题请到给的系统压缩包里去找说明
- 修改配置文件，进行数据库链接，进而实现系统和数据库的融合运行



![image-20240117161258980](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117161258980.png)

PHPMyAdmin ： 是一个网页版本的MySQl管理端，可以完成跟navicat几乎类似的功能，比如：建库，建表，建对象，备份，还原，执行SQL等。但是为了安全起见，默认情况下是禁止远程访问

我们去访问，就会告诉403的错误代码，权限不够

![](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240117161958828.png)

当时在本机上就可以直接访问，但问题是本机服务器是命令行界面，除非我们将整个phpMyAdmin源码从服务器上下载下来的物理机上，否则是不可以的
