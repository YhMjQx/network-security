[TOC]

# ==Wazuh检测木马与配置==

课程目标

理解如何在Wazuh中对RootKit、木马和系统安全配置项进行检测。1、检测RootKit病毒文件
2、检测WebShell木马程序
3、使用System Audit审计安全配置项
4、使用SCA进行安全配置项审计
无

教材内容

#### 一、RootCheck

就是对Rootkit进行检测，包括各类病毒、木马、恶意程序等。检测的依据主要是：文件名、文件内容。

##### 1、ossec.conf配置

```xml
<rootcheck>    
    <disabled>no</disabled>    
    <check_files>yes</check_files>    
    <check_trojans>yes</check_trojans>    
    <check_dev>yes</check_dev>    
    <check_sys>yes</check_sys>    
    <check_pids>yes</check_pids>    
    <check_ports>yes</check_ports>    
    <check_if>yes</check_if>    
    
    <frequency>30</frequency>    
    
    <rootkit_files>etc/rootcheck/rootkit_files.txt</rootkit_files>    
    <rootkit_trojans>etc/rootcheck/rootkit_trojans.txt</rootkit_trojans>   
    
    <skip_nfs>yes</skip_nfs>
</rootcheck>
```

##### 2、检测文件名

在 etc/rootcheck/rootkit_files.txt 中定义恶意文件名，如：

```shell
tmp/mcliZokhb               ! Bash door ::/rootkits/bashdoor.php
tmp/mclzaKmfa               ! Bash door ::/rootkits/bashdoor.php

proc/kset                   ! Suspicious file ::rootkits/Suspicious.php
usr/bin/gib                 ! Suspicious file ::rootkits/Suspicious.php
usr/bin/snick               ! Suspicious file ::rootkits/Suspicious.php
usr/bin/kfl                 ! Suspicious file ::rootkits/Suspicious.php
tmp/.dump                   ! Suspicious file ::rootkits/Suspicious.php
var/.x                      ! Suspicious file ::rootkits/Suspicious.php
var/.x/psotnic              ! Suspicious file ::rootkits/Suspicious.php
```

测试过程：

在/tmp目录下创建普通文件 mclzaKmfa（使用touch命令或者echo等命令均可）

预警信息：

![image-20250214134631903](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250214134631903.png)

或创建一个.dump的文件，也是同样的效果。

##### 3、检测文件内容

在 etc/rootcheck/rootkit_trojans.txt 中定义文件内容（二进制文件或文本文件），如：

```shell
grep        !bash|givemer!
egrep       !bash|^/bin/sh|file\.h|proc\.h|/dev/|^/bin/.*sh!
find        !bash|/dev/[^tnlcs]|/prof|/home/virus|file\.h!

/etc/hosts  !^[^#]*mcafee\.com! Anti-virus site on the hosts file
/etc/hosts  !^[^#]*microsoft\.com! Anti-virus site on the hosts file
/etc/hosts  !^[^#]*f-secure\.com! Anti-virus site on the hosts file
```

在/etc/hosts文件中添加：

```
192.168.112.123 mcafee.com
```

得到的预警信息为：

![image-20250214134714225](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250214134714225.png)

#### 二、System Audit

##### 1、修改配置信息

```xml
在 etc/rootcheck 目录下添加一个 system_audit_woniu.txt文件，并引入到主配置文件中 

<rootcheck>    
    ……………………………………    
    <frequency>30</frequency>    
    
    <rootkit_files>etc/rootcheck/rootkit_files.txt</rootkit_files>    
    <rootkit_trojans>etc/rootcheck/rootkit_trojans.txt</rootkit_trojans>    
    
    <system_audit>etc/rootcheck/system_audit_woniu.txt</system_audit>    
    
    <skip_nfs>yes</skip_nfs> 
</rootcheck>
```

##### 2、添加配置规则

在 etc/rootcheck 下新增文件 system_audit_woniu.txt，内容如下：

```shell
# 可以定义路径或文件名为变量、也可以不定义直接引用
$php.ini=/opt/lampp/etc/php.ini;
$web_dirs=/opt/lampp/htdocs;

# 规则分为三个部分：
# 第一个部分是解释说明注释（可不写）
# 第二个部分是必须写，有[规则描述] [触发条件] [参考引用]
# 第三个部分是规则本身：方向箭头的左边位置：f:代表文件，d:代表目录，p:代表进程，c:代表命令，r:代表注册表
# 方向箭头的右边位置，可以直接写普通文件，代表模糊匹配，也可以写r:代表正则匹配，也可以使用 && 进行多条件匹配
# 如果是目录，则需要定义一个中间箭头，用于确认查询当前目录下的哪些文件

# PHP Checks
[PHP - 远程文件包含是否开启] [any] []
f:$php.ini -> r:^allow_url_include=Off;

# Web Shell Checks
[PHP - 是否存在一句话木马] [any] []
d:$web_dirs -> .jpg$ -> eval;
d:/opt/lampp/htdocs -> .php$ -> r:eval\(\$_POST;
```

> 触发条件解释如下：
> all：只有当下面的所有规则均匹配成功时才会预警，不太适用于多条件情况
> any：当其中任意一个规则满足时就会预警，较适用于多个配置同时开启的情况，所以配置项应该设置为不安全配置
> none：当没有任何一条规则满足时预警（全部不一样，不常用）

3、查看预警信息

![image-20250214134904394](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250214134904394.png)

#### 三、SCA

##### 1、添加一个自定义SCA文件

SCA的规则目录在 ruleset/sca 目录下，是yml文件格式

```shell
policy:  
	id: "custom_woniu_sca"  
	file: "custom_woniu_sca.yml"  
	name: "System audit for CentOS based systems"  
	description: "针对当前CentOS的核心配置进行检查"  
	references:    
		- https://www.woniuxy.com
		
checks:  
	- id: 561501    
	title: "PHP的核心配置文件"    
	description: "PHP核心配置文件是否篡改"    
	condition: none    
	rules:      
		- 'f:/opt/lampp/etc/php.ini -> r:allow_url_include=On'
```

2、添加sca主配置文件

```xml
  <sca>    
      <enabled>yes</enabled>    
      <scan_on_start>no</scan_on_start>    
      <interval>1m</interval>    
      <skip_nfs>yes</skip_nfs>    
      <policies>      
          <policy>ruleset/sca/custom_woniu_sca.yml</policy>    
      </policies>  
</sca>
```

3、查看预警信息

![image-20250214135037704](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250214135037704.png)

需要注意的是，只有配置文件被修改过或配置规则被修改过，导致两次结果不一样，才会触发。否则会导致频繁触发，意义不大。

```
sca.check.result: failed
sca.check.previous_result: passed
```

4、某个SCA配置文件的整体得分

![image-20250214135117173](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250214135117173.png)