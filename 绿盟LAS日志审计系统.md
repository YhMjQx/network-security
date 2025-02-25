[TOC]



# ==绿盟LAS日志审计系统==



#### 一、基础配置

1、LAS系统默认IP：192.168.17.100，账户密码：admin/woniu123，登录界面

![image-20230513140523788](https://gitee.com/ymq_typroa/typroa/raw/main/20230513140523.png)

2、在首页右上角进入数据采集菜单，配置日志客户端进行日志采集。

![image-20230513141113149](https://gitee.com/ymq_typroa/typroa/raw/main/20230513141113.png)

3、先下载Windows和Linux的Agent端，并安装于目标系统上。在两个操作系统中，都将安装一个名为nsfocusagent的服务，并确认服务已经正常启动。最小化接入网络结构图如下（全部主机位于192.168.17.0网段）：

![image-20230513151047201](https://gitee.com/ymq_typroa/typroa/raw/main/20230513151047.png)

4、进行日志接入：

（1）选择系统日志类型，此处以Linux为例（Windows同）

（2）选择要接入的采集器，保持默认值：192.168.17.100（CU:192.168.17.100）

（3）配置接入方式，默认建议选择Agent，当然也可以选择适用于Linux系统的Rsyslog。

![image-20230513143857484](https://gitee.com/ymq_typroa/typroa/raw/main/20230513143857.png)

如果要使用Rsyslog接入，则只需要编辑 /etc/rsyslog.conf中，在末尾添加：`*.* @@192.168.17.100:514` 即可

（5）完成接入

![image-20230513144004207](https://gitee.com/ymq_typroa/typroa/raw/main/20230513144004.png)

5、以下图中接入了三台设备，一台Windows，两台Linux（分别使用Agent和Rsyslog），并且在右边可以看到已处理的日志数量。

![image-20230513144106041](https://gitee.com/ymq_typroa/typroa/raw/main/20230513144106.png)

6、以上，日志接入完成，也可以在Agent中看到代理端的连接情况，并进行进一步的配置。

![image-20230513145142950](https://gitee.com/ymq_typroa/typroa/raw/main/20230513145143.png)

#### 二、查看日志和事件告警

##### 1、日志分析

利用SSH客户端远程登录Linux操作系统，IP地址为192.168.17.60，获得一条系统日志，查询如下：

![image-20230513145939644](https://gitee.com/ymq_typroa/typroa/raw/main/20230513145939.png)

上述只是对Agent采集到的日志进行查询，将日志进行格式化输出而已，并不是安全告警，仅用于事后审计。

##### 2、事件告警

日志审计系统通过配置告警规则，也可以对日志进行告警，类似于HIDS系统的安全预警，如：

![image-20230513150557205](https://gitee.com/ymq_typroa/typroa/raw/main/20230513150557.png)

#### 三、配置告警规则

##### 1、添加日志文件

进入采集终端下的Agent节点，为目标IP配置数据采集

![image-20230513161716560](https://gitee.com/ymq_typroa/typroa/raw/main/20230513161716.png)

指定日志文件路径（监控指定日志，与Wazuh类似），也可以指定要进行审计的目录（类似于Wazuh的文件完整性监控）。

![image-20230513162029735](https://gitee.com/ymq_typroa/typroa/raw/main/20230513162029.png)

目前该设备无法采集应用服务日志，只能进行目录审核。如果要进行日志分析和预警，需要手工添加日志文件，在Linux

系统中，编辑：“/etc/.nsfmhp/syslog.conf”，将需要进行分析的日志手工添加即可。

```
/root/apache-tomcat-8.0.47/logs/localhost_access_log.2023-05-13.txt;/var/log/messages;/var/log/audit/audit.log;/var/log/secure;............
```

并重启Agent服务

```
systemctl restart nsfocusagent
```

##### 2、配置事件规则

（1）配置404状态码规则

第一步：在分类中创建规则

![image-20230513165432107](https://gitee.com/ymq_typroa/typroa/raw/main/20230513165432.png)

第二步：为规则设置名称和过滤条件

![image-20230513165325538](https://gitee.com/ymq_typroa/typroa/raw/main/20230513165325.png)

（2）配置SQL注入规则（在Web入侵事件中）

![image-20230513165606379](https://gitee.com/ymq_typroa/typroa/raw/main/20230513165606.png)

（3）配置SSH登录失败规则（在Linux嫌疑事件中）

![image-20230513165901171](https://gitee.com/ymq_typroa/typroa/raw/main/20230513165901.png)

单纯在设置中配置事件规则，还不能进行告警，所以还需要继续为事件规则配置告警规则。

##### 3、配置告警规则

（1）配置404状态码基础告警

![image-20230513170502632](https://gitee.com/ymq_typroa/typroa/raw/main/20230513170502.png)

（2）为404状态码配置阈值告警

![image-20230513170619085](https://gitee.com/ymq_typroa/typroa/raw/main/20230513170619.png)

当触发阈值预警时，会有高风险告警提示：

![image-20230513171731546](https://gitee.com/ymq_typroa/typroa/raw/main/20230513171731.png)

（3）其他的SQL注入和SSH登录，也可以进行相同的设置。告警规则列表如下：

![image-20230513170907197](https://gitee.com/ymq_typroa/typroa/raw/main/20230513170907.png)

（4）最后看到的告警信息如下：

![image-20230513172612028](https://gitee.com/ymq_typroa/typroa/raw/main/20230513172612.png)

#### 四、其他配置

##### 1、修改设备IP地址

![image-20230513151337709](https://gitee.com/ymq_typroa/typroa/raw/main/20230513151337.png)

##### 2、通知配置

![image-20230513151435486](https://gitee.com/ymq_typroa/typroa/raw/main/20230513151435.png)

##### 3、添加数据库审计源

（1）选择数据库源

![image-20230513161301060](https://gitee.com/ymq_typroa/typroa/raw/main/20230513161301.png)

（2）输入数据库信息

![image-20230513161241166](https://gitee.com/ymq_typroa/typroa/raw/main/20230513161241.png)

（3）输入数据库账密

![image-20230513161338993](https://gitee.com/ymq_typroa/typroa/raw/main/20230513161339.png)

（4）对指定的数据表进行新增操作，查看日志如下：

![image-20230513161437256](https://gitee.com/ymq_typroa/typroa/raw/main/20230513161437.png)