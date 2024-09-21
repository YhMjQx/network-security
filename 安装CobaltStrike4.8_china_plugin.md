第一步：安装jdk1.8以上的版本

[2022 年超详细过程步骤讲解 CentOS 7 安装jdk1.8-阿里云开发者社区 (aliyun.com)](https://developer.aliyun.com/article/1589599#:~:text=2022 年超详细过程步骤讲解 CentOS 7 安装jdk1.8 1 1、卸载系统自带jdk 1.1,7 7、将环境变量设置生效、同时查看是否安装成功 配置的环境生效： ... 8 8、后语 如果需要jdk的安装包、请加下方博主联系方式 )

第二步：

安装cs

[CobaltStrike4.8汉化版带插件-CSDN博客](https://blog.csdn.net/m0_60571842/article/details/132920672)

注意文件的权限，还有java版本

就是开启的这个过程非常慢

![image-20240913231820027](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913231820027.png)

注意报错

```
[*] Starting teamserver
keytool -importkeystore -srckeystore ./cobaltstrike.store -destkeystore ./cobaltstrike.store -deststoretype pkcs12
^C
[root@mycentos Server]# keytool -importkeystore -srckeystore ./cobaltstrike.store -destkeystore ./cobaltstrike.store -deststoretype pkcs12
输入源密钥库口令:  
keytool 错误: java.io.IOException: Keystore was tampered with, or password was incorrect
[root@mycentos Server]# keytool -importkeystore -srckeystore ./cobaltstrike.store -destkeystore ./cobaltstrike.store -deststoretype pkcs12
输入源密钥库口令:  

*****************  WARNING WARNING WARNING  *****************
* 存储在 srckeystore 中的信息的完整性*
* 尚未经过验证!  为了验证其完整性, *
* 必须提供源密钥库口令。                  *
*****************  WARNING WARNING WARNING  *****************

输入目标密钥库口令:  
再次输入新口令: 
输入 <cobaltstrike> 的密钥口令
输入 <cobaltstrike> 的密钥口令
输入 <cobaltstrike> 的密钥口令
keytool 错误: java.security.UnrecoverableKeyException: Cannot recover key
[root@mycentos Server]# keytool -importkeystore -srckeystore ./cobaltstrike.store -destkeystore ./cobaltstrike.store -deststoretype pkcs12
输入源密钥库口令:  
keytool 错误: java.io.IOException: Keystore was tampered with, or password was incorrect
[root@mycentos Server]# keytool -importkeystore -srckeystore ./cobaltstrike.store -destkeystore ./cobaltstrike.store -deststoretype pkcs12
输入源密钥库口令:  
已成功导入别名 cobaltstrike 的条目。
已完成导入命令: 1 个条目成功导入, 0 个条目失败或取消

Warning:
已将 "./cobaltstrike.store" 迁移到 Non JKS/JCEKS。将 JKS 密钥库作为 "./cobaltstrike.store.old" 进行了备份。
[root@mycentos Server]# ls

```

他让我设置密钥库口令，我设置了，但是结果不起作用，最终密钥库口令竟然是123456

然后开启服务器，客户端链接就好

![image-20240913232055829](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913232055829.png)

![image-20240913232104925](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913232104925.png)



### java 1.8 安装

```
cd /usr/local/
mkdir java
cd java/
cp /opt/jdk-8u301-linux-x64.tar.gz ./
tar -zxvf jdk-8u301-linux-x64.tar.gz
vi /etc/profile
source /etc/profile
[root@mycentos java]# java -version
java version "1.8.0_301"
Java(TM) SE Runtime Environment (build 1.8.0_301-b09)
Java HotSpot(TM) 64-Bit Server VM (build 25.301-b09, mixed mode)
```

> ```
> #java environment
> export JAVA_HOME=/usr/local/java/jdk1.8.0_301
> export CLASSPATH=.:${JAVA_HOME}/jre/lib/rt.jar:${JAVA_HOME}/lib/dt.jar:${JAVA_HOME}/lib/tools.jar
> export PATH=$PATH:${JAVA_HOME}/bin
> ```
>
> 将这些内容写进 /etc/profile 文件中
>
> ![image-20240913235305390](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240913235305390.png)

### CobalStrike安装

该zip文件的解压密码是 mht

```
mv CobaltStrike4.8汉化版带插件.zip CobaltStrike4.8.zip
unzip CobaltStrike4.8.zip
cd CobaltStrike4.8汉化版/
chmod -R 777 Server/
cd Server/
./teamserver 192.168.230.150 p-0p-0p-0
keytool -importkeystore -srckeystore ./cobaltstrike.store -destkeystore ./cobaltstrike.store -deststoretype pkcs12
chmod 777 cobaltstrike.store
chmod 777 cobaltstrike.store.old
firewall-cmd --add-port=50050/tcp --permanent
firewall-cmd --reload
```

![image-20240914000301875](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240914000301875.png)

```
./teamserver 192.168.230.150 p-0p-0p-0
```

![image-20240914002701298](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240914002701298.png)

yes就好了

经过测试 

192.168.230.147

192.168.230.150

192.168.230.188

三台CentOS上都成功可以开启cs并使用物理机链接



#### 粗略使用

```
服务器端：
cd /opt/CobaltStrike4.8/Server
./teamserver 192.168.230.147 p-0p-0p-0
```

![image-20240914175726403](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240914175726403.png)

![image-20240914175737969](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240914175737969.png)
