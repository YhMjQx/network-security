[TOC]



# ==AVWS和AppScan扫描器==

#### 一、AVWS安装

安装时需要设置3443端口及HTTPS证书，建议使用IP地址来绑定证书，配置后会有如下提醒。

![image-20211123161157308](https://gitee.com/ymq_typroa/typroa/raw/main/20211123161238.png)

安装后把patch.exe和patch.dat扔到主目录（C:\Program Files (x86)\Acunetix\12.0.190902105）下，管理员运行，license key 任意输入，破解完成。

#### 二、AVWS处理扫描任务

##### 1、添加Target任务

访问[Acunetix - Add Targets](https://yhmjqx:3443/#/targets/add-multiple)，登录成功后点击：Create Target

![image-20240909110341001](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240909110341001.png)

##### 2、配置站点登录

如果需要登录站点，建议提前做好登录配置，否则有些页面无法扫描。有两种选择：自动登录、提前录制，建议使用提前录制登录事件。

下图为预先录制登陆序列方法

![image-20240909110858847](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240909110858847.png)

![image-20240909110823274](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240909110823274.png)

![image-20240909111549636](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240909111549636.png)

这一页没什么限制就跳过

![image-20240909111618330](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240909111618330.png)

第三页可以用来选择使用什么方式来判断访问成功

![image-20240909111930863](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240909111930863.png)

剩余的选项按情况而论

3、查看扫描结果

![image-20240909112316819](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240909112316819.png)

![image-20240909112333666](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240909112333666.png)

4、生成报告

![image-20211129005700902](https://gitee.com/ymq_typroa/typroa/raw/main/20211129005700.png)

#### 三、AppScan安装

先安装.NET Framework运行库

![image-20211123161938439](https://gitee.com/ymq_typroa/typroa/raw/main/20211123161938.png)

在安装目录中直接使用rcl_rational.dll替换原有的文件，然后再直接导入IBM的License文件：AppScanStandard.txt，就是对应的文件就行了，不能使用HCL的License。

#### 四、AppScan主动扫描

##### 1、新建扫描任务

![image-20211129011016709](https://gitee.com/ymq_typroa/typroa/raw/main/20211129011016.png)

输入目标地址

![image-20211129011318992](https://gitee.com/ymq_typroa/typroa/raw/main/20211129011319.png)

录制登录事件

![image-20211129011532497](https://gitee.com/ymq_typroa/typroa/raw/main/20211129011532.png)

后续步骤根据需要选择即可，然后进入漫长的扫描时间

![image-20211129011927352](https://gitee.com/ymq_typroa/typroa/raw/main/20211129011927.png)

查看扫描结果

![image-20211129012326639](https://gitee.com/ymq_typroa/typroa/raw/main/20211129012326.png)

#### 五、被动扫描

AppScan支持被动扫描，用户直接可以在录制器里面操作，然后对所有操作进行漏洞扫描分析

![image-20211129013224742](https://gitee.com/ymq_typroa/typroa/raw/main/20211129013224.png)