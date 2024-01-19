# ==PHPMyAdmin及权限配置==

PHPMyAdmin是一个网页版本的MySQL管理端，可以完成和navicat几乎类似的功能：建库，建表，建对象，备份，执行SQL语句等，但是为了安全起见，默认情况下，是禁止远程访问的。

![image-20240119140933994](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119140933994.png)



## 所用知识点

### 1.DocumentRoot

我们去看他这个网址，http://192.168.230.147/phpmyadmin/ 访问的时候明显是在htdocs这个根目录下面去了，但是实际上他的真实目录却是在 /opt/lampp 下

![image-20240119141248218](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119141248218.png)

这是为什么呢，实际上这就是 **虚拟目录** 的作用

指定Web服务器的主目录，那么如果不配置虚拟目录的情况下，所有Web应用都应该放在该目录下。

```
DocumentRoot "/opt/lampp/htdocs"
<Directory "/opt/lampp/htdocs">

```

如果让 DocumentRoot "/opt/lampp/lampp/htdocs/xindai " 则访问时，直接访问 http://192.168.230.147/ 即可访问到信贷系统

>  其实我们访问xindai系统也可以做到类似这样的效果，只需要在Apache的配置文件中修改一下DocumentRoot即可 /opt/lampp/etc/httpd.conf ，一般情况下，有关网址访问都是和Apache有关的，这些配置的相关文件都在 /opt/lampp/etc 目录下
>
> 将![image-20240119142305258](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119142305258.png)
>
> 修改为
>
> ![image-20240119144108565](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119144108565.png)
>
> (修改Directory的原因是Directory涉及到一些访问控制的权限)  然后 /opt/lampp/lampp restart
>
> 那么访问的情况就会由
>
> ![image-20240119142442986](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119142442986.png)
>
> 变为
>
> ![image-20240119143828179](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119143828179.png)

### 2.虚拟目录

即便Web应用没有放置于DocumentRoot 目录下，只要通过配置虚拟目录，也可以实现访问，比如 PHPMyAdmin应用程序就没有放到 DocumentRoot 目录下，也是实现访问，那是因为系统为PHPMyAdmin 配置了虚拟目录，其配置文件在 /opt/lampp/etc/extra/http-xampp.conf 中。

我们进入 /opt/lampp/etc/httpd.cong 文件查找 xampp可以看见如下情况

![image-20240119150931613](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119150931613.png)

这里使用了很多的include文件。虽说之后httpd.conf才是Apache的核心文件，但是我们也不能将所有的配置信息全部揉进这一个文件当中，这样会显得非常繁琐，且文件也较大，因此我们将一些其他的配置信息写到其他的文件当中去，然后使用include包含进 httpd.conf 中来

这里面include的最重要的就是这个 etc/extra/httpd-xampp.conf

![image-20240119151401322](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119151401322.png)

我们可以看到，这个目录下的文件基本上全都是和httpd有关的，现在进入 httpd-xampp.conf 查看

打开之后可以看到这么一段话

```
Alias /phpmyadmin "/opt/lampp/phpmyadmin"


# since XAMPP 1.4.3
<Directory "/opt/lampp/phpmyadmin">
    AllowOverride AuthConfig Limit
    Require local
    ErrorDocument 403 /error/XAMPP_FORBIDDEN.html.var
</Directory>

```

这段话的效果就是配置了一个新的虚拟目录。 `Alias /phpmyadmin "/opt/lampp/phpmyadmin"` 意思是起了一个别名叫 /phpmyadmin 对应的是 /opt/lampp/phpmyadmin。就可以使得我们通过访问 http://192.168.230.147/phpmyadmin 就相当于直接访问到了 /opt/lampp/phpmyadmin

其中 ` AllowOverride AuthConfig Limit
    Require local` 属于Apache的访问控制权限模块的指令等，一般情况下应用系统中会有一个 .htaccess文件 其中就写的是这些模块的指令。其中 `Require local` 表示只有本机可以访问，为了实现远程连接控制，就要将其修改为 `Require all granted`

### 3.配置远程访问权限









### 5.Require

Apache2.4中开始使用mod_authz_host这个新的模块来进行访问控制和其他的授权检查。原来在Apache2.2版本下用以实现网站访问控制的Order，Allow，Deny指令需要替换为新的Require访问控制指令

```
允许所有：Require all granted
拒绝所有：Require all denied
只允许特定域名主机的访问请求：Require host google.com
允许匹配环境变量中的任意一个：Require env env-var [env-var] ...
允许特定的HTTP方法（GET/POST/HEAD/OPTIONS）: Require method http-method [http-method] ...
允许，表达式为true：Require expr expression
允许特定用户：Require user userid [userid] ...
允许特定用户组：Require group group-name [group-name] ...
允许，有效用户：Require valid-user
允许特定IP或IP网段，多个IP或IP网段间使用空格分隔： Require ip 192.100 192.168.100 192.168.100.5
```

以下示例：允许所有访问请求，但拒绝来自特定IP或IP网段的访问请求（阻止恶意IP或网络爬虫网段的访问）

```
<Directory xxx/www/yoursite>
	<RequireAll>
		Require all granted
		Require not ip 192.168.1.1
		Require not ip 192.120 192.168.100
	</RequireAll>
</Direcory>
```

### 6..ACL

从网络的角度来说，举例网路入口（边境）越近，所能防御到的攻击越多越广，童谣，要考虑的通用性也需要越强

![image-20240119154238208](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119154238208.png)

比如有PHP WAF ，Python WAF https://www.cnglogs.com/nul1/p/8835264.html 

## PHPMyAdmin开始配置

### 1.配置远程访问

进入 /opt/lampp/etc/extra/httpd-xampp.conf 文件中，

将

![image-20240119160831972](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20240119160831972.png)

修改为

![image-20240119160904912](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119160904912.png)

因为 Require local 只允许本地访问

OK，然后重启xampp

![image-20240119161003192](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119161003192.png)

可以进入这个页面了，但是依旧还有些小错误

我们仔细看错误是什么 `mysqli_real_connect(): (HY000/1045): Access denied for user 'root'@'localhost' (using password: NO)` 熟不熟悉？？？我就问你熟不熟悉。

一看我靠，这是不是mysql登录时，不使用密码不允许登录的时候报的错吗，OK看来是需要我们去修改PHPMyAdmin登录MySQL时所需的用户密码

### 2.配置PHPMyAdmin密码

修改文件 /opt/lampp/phpmyadmin/config.inc.php

![image-20240119163929304](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119163929304.png)

```
我们修改信息，使用root@localhost或者remote@192.168.230.147都可以

/**
 * First server
 */
$i++;
/* Authentication type */
$cfg['Servers'][$i]['auth_type'] = 'config';
$cfg['Servers'][$i]['user'] = 'root';
$cfg['Servers'][$i]['password'] = 'p-0p-0p-0';
/* Server parameters */
//$cfg['Servers'][$i]['host'] = 'localhost';
$cfg['Servers'][$i]['compress'] = false;
$cfg['Servers'][$i]['AllowNoPassword'] = true;


```

![image-20240119164356907](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119164356907.png)

这样才算进来了，我试过了，配置文件使用其他用户是无法登陆的

但是现在还有一个问题就是，不管在那台机器上访问都可以进入PHPMyAdmin这个页面，非常危险，所以还需要解决这个问题：

解决方案如下：

- 为PHPMyAdmin设置访问密码
- 禁用PHPMyAdmin，注释掉在 httpd-xampp.conf 的包含文件，并删除 PHPMyAdmin 目录
- 管理数据库，使用数据库，为什么一定需要再同一个应用或同一个Apache里面呢？
- 使用 Knock 进行端口管理，并且只在需要的时候短暂打开端口，用完就关闭。



## 其他注意事项

（1）任何一个URL地址，一定要指定到具体的文件才可以访问，如果没有指定，则会访问默认文件，默认首页。

例如小额信贷系统，在/opt/lampp/htdocs/xindai目录下的index.php文件，就是该系统的默认文件，默认访问页面

如果将该文件名字改一下会遇见什么情况？

![image-20240119191318015](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119191318015.png)

现在我们再去访问一下xindai

![image-20240119191300129](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119191300129.png)

就会变成这样

（2）默认情况下，任何一个目录，如果只输入目录名而不输入文件名就去访问，该目录必须要有一个默认文件。比如 index.php index.html index.jsp 或 default.php main.php等，否则将无法访问到系统页面反而给出来的就是该目录下的所有文件，就和上图一样。

而系统的默认文件配置信息，就在 /opt/lampp/etc/httpd.conf中，这是Apache的核心配置文件

![image-20240119191937544](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119191937544.png)

但是，我们是不允许用户直接这样访问到目录页面的，这算是一个很大的漏洞，一旦讲这些暴露在外，就危险了，那么该如何处理解决呢？

（3）取消OPTIONS的权限，依旧是在 `/opt/lampp/ect/httpd.conf` 文件中修改，添加红色框中部分，并注释掉上面那句Options Index Follow...话

![image-20240119192824498](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119192824498.png)

然后由于修改了核心配置文件，需要重启 `/opt/lampp/lampp restart`  

![image-20240119193037433](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240119193037433.png)

现在再去访问就不会有这种情况了





任务：

1.完成PHPMyAdmin的登录密码配置

2.在 Xampp 7.3 上配置 woniunote系统：DocumentRoot需要指定到public目录下，直接放在根目录htdocs是有问题的

3.在Windows上完成上述任意环境配置

