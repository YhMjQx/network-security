[TOC]



# ==PHP运行管理员命令==

## Apache + PHP

**要么是管理员或root权限，要么是管理员授权给用户可执行的权限**

为什么windows中php程序就可以读取外部文件，但是linux就无法读取外部文件

> 任意一个文件或文件夹，用 `ls -l `的命令可以显示其基本信息和权限信息
>
> ```
> drwxr-xr-x. 2 root root  6 9月  15 16:40 myfolder
> -rw-r--r--. 1 root root  5 9月  15 16:42 test.txt
> 
> ```
>
> - 第一栏的10个字符，共分为4个部分
>   - 第一个字母： - 代表普通文件， d 代表目录
>   - 第2、3、4：代表当前文件或文件夹所属用户的（owner）权限，用 u 表示
>   - 第5、6、7：代表当前文件或文件夹所属用户组（group）的权限，用 g 表示
>   - 第8、9、10：代表其他用户组和其他用户（other）的权限，用 o 表示 
> - 权限的表示方法：
>   - r 读：也可以使用数字 4 来表示
>   - w 写：也可以使用数字 2 来表示
>   - x 执行：也可以使用数字 1 来表示
>   - 任何一个数都可以使用2的多少次方互加来表示，就像任何一个数字都可以使用10的多少次方来表示
>   - 用2的多少次方来表示的话，是不会有重复的
>   - user有rwx的权限，即数字为7；rw权限，即数字为6；rx权限，数字为5；wx权限，数字为3

- linux中读取文件时，需要注意每一层级的关系，比如我需要读取一个层次较深的外部文件，我需要让该外部文件所处的每一个目录都可以被其他用户和组访问，因此该文件和该文件的所有父级目录都需要 `chmod o+rx ...`

### 一、PHP运行操作系统命令

- 通过反引号包裹命令可以直接执行，但是也仅限于普通命令，涉及更高或管理员权限的命令是无法执行的

- windows和linux在php文件中都是通过 添加反引号来包裹命令进行执行的
- 查看文件或写入修改等等操作时，需要该文件支持拥有r w x 权限
  - 如果是该当前文件或文件夹所属用户（u）的文件，那就是第一个权限
  - 如果是当前文件或文件夹所属用户组（g）的文件，那就是第二个文件
  - 如果是其他用户组和其他用户（o）的文件，那就是第三个权限

- 但是执行命令就不一样了，难道执行命令时，也是给文件加上r w x 权限吗？？？不应该是执行命令的用户拥有什么权限吗 

那么我们现在使用的是xampp，此时apache+PHP的默认用户是谁呢

### 二、PHP运行只有root用户才拥有的权限

比如我们执行如下命令，在 linux 中的 xampp 中 /opt/lampp/htdocs/learn/doexec.php 文件中写入以下代码，然后通过windows来访问 192.168.230.147/learn/doexec.php 

```php
<?php
$exec = `systemctl stop filewalld`;
echo $exec;
?>
```

由于**权限不够**，访问结果就是一片白板

![image-20240220142815019](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220142815019.png)

那我们该怎么做呢？

那我们查看一下systemctl目录在哪里，去看他以及他的父目录都是否拥有对应的权限

![image-20240220145150040](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220145150040.png)

我们可以看见

- /usr/bin/systemctl 对拥有其他用户组和其他用户有rx权限
- /usr/bin 对拥有其他用户组和其他用户有rx权限
- /usr 对拥有其他用户组和其他用户有rx权限

但是通过上面的执行，我们发现，依旧无法成功执行systemctl命令，说明什么，单纯靠文件本身是否拥有权限是不行的

> 这里和访问文件是不一样的，访问文件时，只要文件拥有相对应的权限，我们就可以访问并且通过php程序也可以访问，但是执行命令就不一样了，就算该命令拥有权限，如果是普通用户也是无法执行的

**我们利用php的环境来执行 whoami ，这样就可以看见php环境到底是那个用户在执行**，单纯的在系统命令行中执行 whoami 得到的结果只是当前系统登录的用户，而不是php执行代码时所用的用户

- **系统执行 whoami** 

![image-20240220145903496](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220145903496.png)

结果是root，那如果说就是系统登录的用户在执行php的话，结合上面所说的，php代码执行 systemctl 命令是绝对没问题的，因此，php环境默认执行代码的用户和系统登录的用户是不一样的

- **php代码执行 whoami** 

```php
<?php
$exec = `whoami`;
echo $exec;
?>
```

![image-20240220150136707](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220150136707.png)

我们那可以看见，执行php环境的用户是daemon，这是一个系统用户，xampp安装时默认使用的是该用户，毫无疑问，该用户没有root权限

#### 修改xampp用户为root

##### 此路暂时不通

xampp7.3版本在 /opt/lampp/etc/httpd.conf 中查找user信息，发现根本没有root用户可选项

![image-20240220151120248](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220151120248.png)

xampp5.6版本是有root用户可选项的，但是就算有，修改完重新启动xampp发现，无法奏效，甚至连apache服务都无法停止，这是怎么回事。apache默认是不允许root用户执行的，为了确保安全（当然一切都是人做的，也是可以修改的）。

如果一定需要这种办法，那么就单独 源码安装 apache 和 php ，并重新编译和配置，很繁琐

#### 授权daemon用户可执行权限

通过 sudo 进行设置，我们可以编辑 sudo来对不同的用户进行权限授权

```
visudo 或 vi /etc/sudoers  编辑sudo文件信息
```

 ```
 sudo 是一个运行授权指令的命令 （super user do - 超级用户做的事）
 su 用于切换用户 （switch user）
 su - username 也是切换用户
 ```

- `su username` 只是将用户替换为username，但环境变量都还没变，还是原来账户的配置
- `su - username` 是将整个操作系统均由username登录

```php
passwd username 是用来给用户修改密码的
```

##### 切换用户

**1.将用户 /sbin/nologin 改成 /bin/bash** 

![image-20240220173708302](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220173708302.png)

![image-20240220173834353](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220173834353.png)

##### **2.给用户daemon设置密码**

```php
passwd username 即可
```

![image-20240220173943818](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220173943818.png)

**3.切换用户**

```php
su - daemon
```

![image-20240220174018151](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220174018151.png)

**4.执行指令 发现报错**

```
systemctl stop firewalld
```

![image-20240220175123523](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220175123523.png)

执行命令，输入root用户密码，才可以正确执行，但是一般情况下谁会知道root密码

替换使用sudo + 指令进行执行

![image-20240220174136311](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220174136311.png)

即使sudo之后输入了daemon的密码，还是报错被拒绝

**5.修改sudo文件，允许daemon用户执行root权限或部分权限**

```
vi /etc/sudoers
或
visudo
```

在文件末尾添加如下daemon的信息

![image-20240220211931181](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220211931181.png)

或

![image-20240220175507497](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220175507497.png)

第一栏表示 哪个账户

第二栏代表 从哪一台机器来的授权

第三栏表示 想要模拟为哪个账户

第四栏表示 该命令在执行sudo 命令 时不需要输密码

此时再使用daemon用户执行 授权的两个命令就不会出问题了

![image-20240220212121096](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220212121096.png)

![image-20240220212149319](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220212149319.png)

**6.linux中/opt/lampp/htdocs/learn/doexec.php 中书写php代码**

```php
<?php
#$exec = `systemctl stop filewalld`;
#$exec = `ip addr`;
#$exec = `whoami`;
$status = `sudo systemctl status firewalld`;
#$status = system("sudo systemctl status firewalld");
echo $status;
echo "<br>";
echo "</p>";
$exec = `sudo firewall-cmd --list-all`;
echo $exec;
?>
```

在windows中访问 192.168.230.147/learn/doexec.php 

![image-20240220213116458](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220213116458.png)

## Nginx + PHP

### 1.进入nginx默认首页

```
cd /usr/local/nginx/html
```

在该目录下创建一个页面

```php
<?php
#$exec = `systemctl stop filewalld`;
#$exec = `ip addr`;
$exec = `whoami`;
$status = `sudo systemctl status firewalld`;
#$status = system("sudo systemctl status firewalld");
echo $status;
echo "<br>";
echo "</p>";
$exec = `sudo firewall-cmd --list-all`;
echo $exec;
?>
```



默认情况下，我们是无法读取 /etc/firewalld/zones/public.xml 文件的，该文件存储的是firewall-cmd --list-all的信息

那么我们该如何在nginx中对普通用户授权呢

### 2.启动php和nginx服务

```
/usr/local/php/sbin/php-fpm
/usr/local/nginx/sbin/nginx
```

### 3.访问nginx首页

```
192.168.230.147/index.php
```

结果发现只输出了 用户名称，其他什么都没输出，这也正是说明了该用户作为普通用户没有额外的权限，那么我们该如何授权呢

### 4.给普通用户授权

- **修改php配置文件**

```
cd /usr/local/php/etc/php-fpm.d/
修改 username.conf
```

将用户和组修改为如下信息

![image-20240220220249106](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240220220249106.png)

- 重启 php-fpm

注意替换 serviceid

```
ps -ef | grep php-fpm
kill serviceid
/usr/local/php/sbin/php-fpm -R
```

**重启时使用参数 -R ，表示以root用户执行**