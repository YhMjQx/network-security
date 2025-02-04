[TOC]

# ==Nessus主机扫描器==

#### 一、安装Nessus

Nessus号称是世界上最流行的漏洞扫描程序，全世界有超过75000个组织在使用它。该工具提供完整的电脑漏洞扫描服务，并随时更新其漏洞数据库。Nessus不同于传统的漏洞扫描软件，Nessus可同时在本机或远端上遥控，进行系统的漏洞分析扫描。Nessus也是渗透测试重要工具之一。

安装过程相对比较简单，直接安装于Windows环境下即可，下面的安装过程基于Nessus 10.0.1-64位版本。安装完成后，需要去指定站点注册一个邮箱，收到激活码即可完成免费授权使用。

##### 1、完成安装配置

安装完成后，需要等待很长一段时间进行初始化配置。

![20211124013440](https://gitee.com/ymq_typroa/typroa/raw/main/20211124013440.png)

##### 2、登录确认

访问 https://192.168.112.160:8834/#/ 并使用注册账号进行登录。

![image-20211128232836359](https://gitee.com/ymq_typroa/typroa/raw/main/20211128232836.png)

#### 二、使用Nessus

##### 1、新建扫描任务

在首页右上角点击“New Scan”开始创建一个全新的扫描任务，进入选择扫描模板页面，如下：

![image-20211128233239807](https://gitee.com/ymq_typroa/typroa/raw/main/20211128233239.png)

##### 2、Host Descovery

用于扫描给定网段内的主机及端口，配置扫描器名称和对应的网段即可开始扫描。

![image-20211128235436072](https://gitee.com/ymq_typroa/typroa/raw/main/20211128235436.png)

扫描完成后，在首页上点击扫描器名称，可以查看结果。

![image-20211129000339165](https://gitee.com/ymq_typroa/typroa/raw/main/20211129000339.png)

##### 3、Advanced Scan

可以自行配置扫描策略和扫描选项。

![image-20211129001304134](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20211129001304.png)

##### 4、Web Application

除了常规的主机扫描外，Nessus也同样支持Web扫描，在配置好对应的扫描策略（通常默认即可）

![image-20211130163631170](https://gitee.com/ymq_typroa/typroa/raw/main/20211130163631.png)

![image-20211130163949833](https://gitee.com/ymq_typroa/typroa/raw/main/20211130163949.png)

##### 5、登录扫描

直接登录到系统进行扫描，可以更加准确进进行扫描，但是并不适用于未知密码的情况下（通常此类场景用于安全基线检查）。

![image-20211130165039902](https://gitee.com/ymq_typroa/typroa/raw/main/20211130165039.png)

![image-20211130164928322](https://gitee.com/ymq_typroa/typroa/raw/main/20211130164928.png)

##### 6、导出测试报告为HTML

![image-20211129002551418](https://gitee.com/ymq_typroa/typroa/raw/main/20211129002551.png)

> Nesssus提供的扫描类型相对还是比较全面的，并且也具备一些专项漏洞的扫描能力，也可以登录后扫描进行安全检查，将Nessus与NMap进行配合，是一种比较不错的选择，也能覆盖大部分应用场景。
