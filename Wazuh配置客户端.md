[TOC]



# ==Wazuh配置客户端==

> 实验配置：
>
> Wazuh 服务器 ：192.168.230.188 
>
> Linux Wazuh 客户端 ：192.168.230.147
>
> Windows Wazuh 客户端 ：192.168.230.

#### 一、安装Agent客户端

##### 1、在Wazuh服务器端生成Authentication Key

在Manager端运行/var/ossec/bin/manage_agents命令

根据客户端的IP地址添加Agent，并生成相应的Key备用。

![image-20250212233306983](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212233306983.png)

![image-20250212233358143](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212233358143.png)

![image-20250212233412793](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212233412793.png)

![image-20250212233626590](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212233626590.png)

需要注意的是：我们在服务器端需要打开 1514 端口，原因如下：

![image-20250212233827871](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212233827871.png)

这是 192.168.230.188 服务器端的配置，客户端与服务器端连接时，默认使用的是这个端口。

##### 2、在Windows上安装Agent

（1）保持默认安装，并勾选Run Agent configuration interface

![image-20211220233900600](https://gitee.com/ymq_typroa/typroa/raw/main/20211220233900.png)

（2）输入Manager IP地址和对应的Authentication key。并在Manager菜单中选择重启服务。

![image-20250212234545157](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250212234545157.png)

![image-20250213000449940](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213000449940.png)

（3）在Manager端运行/var/ossec/bin/manage_agents -l，可以看到以下输出，表示连接成功

经过我的测试，就算不出现 any 也是可以的，只要确保 netstat -ant 的结果中由而这相关联的显示结果就好了

```
Available agents:    
	ID: 001, Name: winseven, IP: any
```

在Windows操作系统上，wazuh-agent将被安装为系统服务。

![image-20211221000229146](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20211221000229.png)

（4）重启agent服务，并运行命令确认已经成功连接到manager

```
netstat -ano
```

![image-20250213001203808](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213001203808.png)

##### 3、在Linux上安装Agent

（1）在客户端电脑上写入repo文件

```shell
rpm --import https://packages.wazuh.com/key/GPG-KEY-WAZUH
cat > /etc/yum.repos.d/wazuh.repo << EOF
[wazuh]
gpgcheck=1
gpgkey=https://packages.wazuh.com/key/GPG-KEY-WAZUH
enabled=1
name=EL-\$releasever - Wazuh
baseurl=https://packages.wazuh.com/4.x/yum/
protect=1
EOF
```

（2）安装wazuh-agent

```
yum install wazuh-agent
```

（3）设置Agent为自启动

```
systemctl enable wazuh-agent
```

（4）修改配置文件指定Manager IP

在Agent客户端编辑 /var/ossec/etc/ossec.conf 文件

```xml
<server>    
    <address>192.168.112.188</address>    
    <port>1514</port>    
    <protocol>tcp</protocol>
</server>
```

（5）启动wazuh-agent服务

```
systemctl start wazuh-agent
```

（6）在Linux的Agent端同样运行manage_agents命令，导入Key

![image-20250213002840130](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213002840130.png)

（7）重启wazuh-agent服务，并运行netstat命令确认连接成功建立。

![image-20250213002956402](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213002956402.png)

![image-20250213003023147](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213003023147.png)

（8）在服务器端确认代理端是否正常上线：

![image-20250213003044270](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213003044270.png)

#### 二、测试Agent与Manager

##### 1、Windows

（1）在C:\Program Files\ossec-agent文件夹中找到安装目录，并尝试修改ossec.conf

（2）在Windows上添加一个新的账号

（3）在%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Startup文件夹中添加一个新的文件

（4）在ossec.conf文件中添加对Apache访问日志的监听，并构造404错误

```xml
<localfile>    
    <location>C:\Xampp\apache\logs\access.log</location>    
    <log_format>syslog</log_format>
</localfile>


<localfile>    
    <location>C:\phpStudy\PHPTutorial\Apache\logs\error.log</location>    
    <log_format>syslog</log_format>
</localfile>
```

![image-20250213001904622](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213001904622.png)

![image-20250213002302527](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213002302527.png)

（5）如果上述测试完全通过，则其他操作完全一致。

##### 2、Linux

（1）添加一个新的账号，然后删除它

在 192.168.230.147 上操作如下指令

![image-20250213003325079](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213003325079.png)

在 192.168.230.188 服务器上查看

![image-20250213003315774](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213003315774.png)

（2）在/etc/目录下创建一个新的文件

（3）启动Xampp服务

（4）访问Xampp页面并产生404错误

给 192.168.230.147 agent 添加 xampp 日志文件审计

```xml
<localfile>
    <log_format>syslog</log_format>
    <location>/opt/lampp/logs/access_log</location>
</localfile>
```

![image-20250213003809747](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213003809747.png)

重启 wazuh-agent

尝试访问 192.168.230.147 并造成 404

![image-20250213004010095](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213004010095.png)

查看 192.168.230.188 服务器日志

![image-20250213004110658](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213004110658.png)

#### 三、Agentless无代理配置

在Agentless的配置场景下，可以用于检测目标系统的文件完整性，功能相对较少。

##### 1、使用SSH输入密码登录远程目标

```
/var/ossec/agentless/register_host.sh add root@example_address.com example_password [enablepass]
```

##### 2、使用公钥登录远程目标

```
sudo -u ossec ssh-keygen
```

> https://documentation.wazuh.com/current/user-manual/capabilities/agentless-monitoring/index.html