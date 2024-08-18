[TOC]



# ==VAuditDemo审计思路==

## 一、Xampp安装VAditDemo

### 第一步：

**解压VAuditDemo**

先上传好zip文件，然后解压

```
[root@mycentos htdocs]# unzip VAuditDemo-master.zip 
[root@mycentos htdocs]# mkdir vaudit-release
[root@mycentos htdocs]# mkdir vaudit-debug
[root@mycentos htdocs]# cp -r VAuditDemo-master/VAuditDemo_Release/* ./vaudit-release/
[root@mycentos htdocs]# cp -r VAuditDemo-master/VAuditDemo_Debug/* ./vaudit-debug/
```

### 第二步：

给对应的目录和文件赋予写权限

```
[root@mycentos vaudit-release]# chmod o+w sys
[root@mycentos vaudit-release]# mkdir uploads
[root@mycentos vaudit-release]# chmod o+w uploads/

[root@mycentos sys]# chmod o+w config.php
```

![image-20240818130508529](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818130508529.png)

![image-20240818130659522](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818130659522.png)

```
[root@mycentos vaudit-debug]# chmod o+w sys
[root@mycentos vaudit-debug]# chmod o+w uploads/

[root@mycentos sys]# chmod o+w config.php
```

![image-20240818130440680](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818130440680.png)

![image-20240818130746500](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818130746500.png)

### 第三步：

**修改 /opt/lampp/etc/extra/httpd-vhosts.conf 文件，配置虚拟根目录**

![image-20240818120644966](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818120644966.png)

其中 ServerAdmin 代表服务器管理员的邮箱地址，不是必选项

DocumentRoot和ServerName 是必选项

ErrorLog可以指定路径也可以不指定，不指定时使用xamppapache默认日志文件

CustomLog 定义自己的访问日志

### 第四步：

**确保 /opt/lampp/etc/httpd.conf 文件 包含 /opt/lampp/etc/extra/httpd-vhosts.conf**

vi /opt/lampp/etc/httpd.conf 

![image-20240818121626031](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818121626031.png)

### 第五步：

**开启监听端口，监听虚拟根目录对应的端口**

vi /opt/lampp/etc/httpd.conf 

![image-20240818121832110](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818121832110.png)

### 第六步：

**重启xampp并开放防火墙端口**

```shell
/opt/lampp/lampp restart

[root@mycentos etc]# firewall-cmd --add-port=81/tcp --permanent
success
[root@mycentos etc]# firewall-cmd --add-port=82/tcp --permanent
success
[root@mycentos etc]# firewall-cmd --reload
success
```

此时，基本的安装配置已经完成，可以访问并安装，但依旧存在些许问题

### 第七步：

访问 192.168.230.147:82 就会直接跳转到 http://192.168.230.147:82/install/install.php

![image-20240818162836452](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818162836452.png)

输入正确的mysql数据库用户名和密码就可以安装成功

### 第八步：

但是进去之后会发现留言功能是存在问题的，这是因为作者的疏忽

![image-20240818153640443](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818153640443.png)

![image-20240818153943974](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818153943974.png)

修改这个文件的第十行代码

再次访问就好了

## 二、代码审计思路

![image-20240818164531348](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240818164531348.png)

