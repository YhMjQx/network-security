[TOC]



# ==ThinkPHP框架安装==

MVC：Model View Controller

我不会将很仔细的步骤写出来，前几步比较简单因此我只是大概描述了一下

### 一、使用 xampp7.3的版本

因此我们使用的是PHP7.3的版本

### 二、配置php环境变量加入path中

![image-20240303193244875](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240303193244875.png)

### 三、安装composer

 https://getcomposer.org/Composer-Setup.exe

注意要确保所使用的 php 已经配置在环境变量中

### 四、开启xampp的配置文件httpd.conf文件中的 openssl 模块

我们打开 php 目录下的 php.ini，将 **extension=php_openssl.dll** 前面的分号去掉就可以了。然后重启xampp

### 五、配置国内镜像地址

安装好composer之后，cmd中直接运行 `composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/`

![image-20240303193602597](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240303193602597.png)

### 六、安装ThinkPHP框架 ：

 创建一个新的目录来安装ThinkPHP，并在该目录下使用cmd中运行命令即可安装 `composer create-project topthink/think TPDemo` 其中TPDemo是我们自己在文件夹下创建的项目名，最后TPDemo就在该新建的目录下

![image-20240303202026959](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240303202026959.png)



### 七、配置Xampp与TPDemo整合

修改 D:\WEB\XAMPP7.3\apache\conf 目录下的 httpd.conf，注释原来的DocumentRoot，并添加下面的内容

```php
#DocumentRoot "D:/WEB/XAMPP7.3/htdocs"
#<Directory "D:/WEB/XAMPP7.3/htdocs">

DocumentRoot "D:/PHP/ThinkPHP/TPDemo/public"
<Directory "D:/PHP/ThinkPHP/TPDemo/public">
```

![image-20240303202149372](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240303202149372.png)

### 八、开发

### 1.TPDemo/route/app.php

![image-20240303202256963](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240303202256963.png)

该文件定义的就是，**路由地址规则定义** 

其中的 `'think'` 就是路由地址，也就是URL地址

![image-20240303202548556](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240303202548556.png)

其中 `:name` 代表地址参数，访问 /hello/woniuxy 此时将转向index控制器下的 hello 方法 即 index/hello 

![image-20240303202948427](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240303202948427.png)



### 2.TPDemo/app/controller/index.php

![image-20240303204549126](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240303204549126.png)

> 发现 `Index` 类继承自 `BaseController` 类，而`BaseController`类又在 app 这个命名空间下 即 TPDemo/app/BaseController.php 
>
> 该页面代码中 `app\controller` 就是一个命名空间。 PHP命名空间，用于对不同的类进行归类管理，同时允许不同命名空间下类重名

我们可以看见，这里就有一个 hello 方法，其中有一个 name 的参数，这个参数的值就是通过前面的 `:name` 所传的值，所以最后我们在web页面看到的输出结果就是 hello,woniuxy 





