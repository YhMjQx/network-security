[TOC]



# ==MSF框架初始化问题解决==

1.登录kali系统，编辑软件源文件配置

```
vim /etc/apt/sources.list
#中科大
deb http://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
deb-src http://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
#阿里云
#deb http://mirrors.aliyun.com/kali kali-rolling main non-free contrib
#deb-src http://mirrors.aliyun.com/kali kali-rolling main non-free contrib
#清华大学
#deb http://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free
#deb-src https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free
 这是几个国内的源
```

把源插入后，想使用哪个源就把注释符号#去掉

按”ESC“退出编辑，再shift+冒号键   --->注入wq（保存并退出）

2.更新
更新软件列表(非root权限在命令行前加“sudo”)

```
apt-get update 更新索引

apt-get upgrade 更新软件

apt-get dist-upgrade 升级

apt-get clean 删除缓存包

apt-get autoclean 删除未安装的deb包
apt-get install dsniff  安装dsniff软件包

最后
msfdb reinit
```

> 问题出现原因，我怀疑是因为kali自身的版本与msf框架的版本不兼容导致的，而msf版本的更新又是通过 包管理器进行更新的，故此直接更新包管理器，然后利用更新后的包管理器进行msf数据库的初始化，就可以初始化出于kali版本相对应的msf数据库
