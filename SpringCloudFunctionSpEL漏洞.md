[TOC]



# ==SpringCloudFunctionSpEL漏洞==

![image-20250202224156216](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202224156216.png)![image-20250202224233382](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202224233382.png)

![image-20250202231131848](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202231131848.png)

![image-20250202230551412](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202230551412.png)

![image-20250202230705742](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202230705742.png)![image-20250202230837891](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202230837891.png)![image-20250202230919348](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202230919348.png)![image-20250202231048620](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202231048620.png)![image-20250202231252966](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202231252966.png)![image-20250202231340169](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202231340169.png)![image-20250202231810035](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202231810035.png) 

![image-20250202231829990](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202231829990.png)

## 漏洞复现：

- 下载JDK15安装并配置环境变量

- 下载 SpringCloud-Function-0.0.1-SNAPSHOT.jar 并运行 java -ajr SpringCloud-Function-0.0.1-SNAPSHOT.jar

  ![image-20250205215957993](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250205215957993.png)

- 浏览器访问 运行 SpringCloud-Function-0.0.1-SNAPSHOT.jar 的ip地址的 9000 端口

  ![image-20250205220053651](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250205220053651.png)

  ![image-20250205220335549](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250205220335549.png)

- 下载 Spel_RCE_Bash_EXP.py  Spel_RCE_POC.py 两个 exp工具

  ![image-20250205220351849](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250205220351849.png)

- 攻击机kali监听 6666 端口

  ![image-20250205220503542](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250205220503542.png)

- 攻击机kali 执行 如图所示的代码来扫描目标，看谁存在漏洞

![image-20250205220804978](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250205220804978.png)

- 存在漏洞之后，执行 exp 进行漏洞利用

  ![image-20250205221242469](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250205221242469.png)

