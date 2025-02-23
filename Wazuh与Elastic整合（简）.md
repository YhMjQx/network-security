[TOC]



# ==Wazuh与Elastic整合==

教材内容

#### 一、Elastic Stack介绍

##### 1、Elastic Search

Elasticsearch 是一个分布式、RESTful 风格的搜索和数据分析引擎，能够解决不断涌现出的各种用例。 作为 Elastic Stack 的核心，它集中存储您的数据，帮助您发现意料之中以及意料之外的情况。数字、文本、地理位置、结构化数据、非结构化数据。适用于所有数据类型。

![image-20211215111055479](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20211215111055.png)

##### 2、Kibana

Kibana 是一个免费且开放的用户界面，能够让您对 Elasticsearch 数据进行可视化，并让您在 Elastic Stack 中进行导航。您可以进行各种操作，从跟踪查询负载，到理解请求如何流经您的整个应用，都能轻松完成。

![image-20211215111223293](https://gitee.com/ymq_typroa/typroa/raw/main/20211215111223.png)

##### 3、Beats

Beats 是一个免费且开放的平台，集合了多种单一用途数据采集器。它们从成百上千或成千上万台机器和系统向 Logstash 或 Elasticsearch 发送数据。

![image-20211215111342929](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20211215111342.png)

#### 二、安装与配置

##### 1、一键安装

Wazuh与Elastic的整合和配置过程相对是比较麻烦的，所以Wazuh在较新的版本中很好的解决了这一问题，只需要运行一个脚本，就可以完成所有安装和配置，完全的一键安装使用。

```shell
curl -sO https://packages.wazuh.com/4.10/wazuh-install.sh && sudo bash ./wazuh-install.sh -a
```

安装过程输出如下：

```
[root@centqiang ~]# curl -sO https://packages.wazuh.com/4.3/wazuh-install.sh && sudo bash ./wazuh-install.sh -a
06/03/2023 00:50:06 INFO: Starting Wazuh installation assistant. Wazuh version: 4.3.1006/03/2023 00:50:06 INFO: Verbose logging redirected to /var/log/wazuh-install.log06/03/2023 00:50:11 INFO: Wazuh repository added.06/03/2023 00:50:11 INFO: --- Configuration files ---06/03/2023 00:50:11 INFO: Generating configuration files.06/03/2023 00:50:12 INFO: Created wazuh-install-files.tar. It contains the Wazuh cluster key, certificates, and passwords necessary for installation.06/03/2023 00:50:12 INFO: --- Wazuh indexer ---06/03/2023 00:50:12 INFO: Starting Wazuh indexer installation.06/03/2023 00:51:27 INFO: Wazuh indexer installation finished.06/03/2023 00:51:28 INFO: Wazuh indexer post-install configuration finished.06/03/2023 00:51:28 INFO: Starting service wazuh-indexer.06/03/2023 00:52:38 INFO: wazuh-indexer service started.06/03/2023 00:52:38 INFO: Initializing Wazuh indexer cluster security settings.06/03/2023 00:52:59 INFO: Wazuh indexer cluster initialized.06/03/2023 00:52:59 INFO: --- Wazuh server ---06/03/2023 00:52:59 INFO: Starting the Wazuh manager installation.06/03/2023 00:53:40 INFO: Wazuh manager installation finished.06/03/2023 00:53:40 INFO: Starting service wazuh-manager.06/03/2023 00:53:53 INFO: wazuh-manager service started.06/03/2023 00:53:53 INFO: Starting Filebeat installation.06/03/2023 00:53:58 INFO: Filebeat installation finished.06/03/2023 00:54:00 INFO: Filebeat post-install configuration finished.06/03/2023 00:54:00 INFO: Starting service filebeat.06/03/2023 00:54:00 INFO: filebeat service started.06/03/2023 00:54:00 INFO: --- Wazuh dashboard ---06/03/2023 00:54:00 INFO: Starting Wazuh dashboard installation.06/03/2023 00:54:58 INFO: Wazuh dashboard installation finished.06/03/2023 00:54:59 INFO: Wazuh dashboard post-install configuration finished.06/03/2023 00:54:59 INFO: Starting service wazuh-dashboard.06/03/2023 00:54:59 INFO: wazuh-dashboard service started.06/03/2023 00:55:49 INFO: Initializing Wazuh dashboard web application.06/03/2023 00:55:49 INFO: Wazuh dashboard web application initialized.06/03/2023 00:55:49 INFO: --- Summary ---06/03/2023 00:55:49 INFO: You can access the web interface https://<wazuh-dashboard-ip>    User: admin    Password: .2vP6B2JUFq2ukkWd8G+uhOqlco0Z?Hx06/03/2023 00:55:49 INFO: Installation finished.
```

待上述安装完成后，直接访问` https://Wazuh-IP，（确保防火墙放行443端口），输入用户名：admin(https://xn--wazuh-ip,(443),:admin-8487a03torpd4aq87fqs1d1yrr87e8y3a5gvjkso67h8y6bxo8b/) `和对应生成的密码即可访问 Elastic的Kibana页面。如图所示：

![image-20230306010656105](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20230306010656.png)

##### 2、查看密码

直接在当前安装目录中会存在一个文件名为：wazuh-install-files.tar，使用以下命令可查看到保存于该文件中的密码文件：

```
sudo tar -O -xvf wazuh-install-files.tar wazuh-install-files/wazuh-passwords.txt
```

> 如果无法成功执行上述命令，则直接将tar文件下载到Windows环境中打开访问即可。

##### 3、确认服务

```
[root@centqiang ~]# systemctl list-unit-files | grep wazuhwazuh-dashboard.service                       enabled wazuh-indexer-performance-analyzer.service    disabledwazuh-indexer.service                         enabled wazuh-manager.service                         enabled
```

##### 4、内存消耗

```
[root@centqiang ~]# free              total        used        free      shared  buff/cache   availableMem:        7990068     5500364      344272       12068     2145432     2171828Swap:       8257532           0     8257532
```

一台全新服务器环境，安装完上述套件后，消耗内存5.5G左右。

#### 三、各模块功能介绍

针对Wazuh的所有操作，均可以在Kibana中完成，比如配置Wauzh客户端、管理账户信息、查看安全预警事件、查看系统审计报告、管理规则库和解码库等，也包括更多可视化操作的功能。

![image-20230306011226817](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20230306011226.png)