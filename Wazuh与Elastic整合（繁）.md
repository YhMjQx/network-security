[TOC]



# ==Wazuh与Elastic整合（简）==

![image-20250213163637395](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213163637395.png)

![image-20250213161435764](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213161435764.png)

> 由于 elastic 不能以 root 身份运行，所以我们可以先 创建一个普通用户ymqyyds，然后将压缩包，放在 普通用户ymqyyds的目录下，然后以普通用户ymqyyds的身份进行解压，得到的就是普通用户权限的文件夹
>
> ![image-20250213164214098](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164214098.png)

![image-20250213164252056](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164252056.png)

> ![image-20250213164357278](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164357278.png)
>
> ![image-20250213164442005](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164442005.png)
>
> ![image-20250213164500138](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164500138.png)
>
> ![image-20250213164529467](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164529467.png)

![image-20250213164547949](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164547949.png)

> ![image-20250213164604198](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164604198.png)
>
> ![image-20250213164617434](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164617434.png)
>
> ![image-20250213164644233](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164644233.png)

> 如果以 root 身份运行了怎么办
>
> ![image-20250213164710751](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164710751.png)
>
> ![image-20250213164733677](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164733677.png)
>
> ![image-20250213164808210](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164808210.png)
>
> ![image-20250213164835231](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164835231.png)
>
> ![image-20250213164851853](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164851853.png)
>
> ![image-20250213164902827](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164902827.png)

![image-20250213164916228](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164916228.png)

![image-20250213164925256](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164925256.png)

![image-20250213165026995](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165026995.png)

> ![image-20250213164947477](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213164947477.png)
>
> 如果访问结果如上所示，则表示 elastic 配置成功.

![image-20250213165200013](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165200013.png)

> ![image-20250213165055931](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165055931.png)
>
> ![image-20250213165116409](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165116409.png)
>
> ![image-20250213165121918](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165121918.png)
>
> ![image-20250213165216120](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165216120.png)

 ![image-20250213165243634](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165243634.png)

![image-20250213165307394](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165307394.png)

此时 elastic 和 kibana 连接好了

接下来 kibana 安装 wazuh 插件 在 wazuh 服务器 安装 filebeta 并配置连接 elasticsearch

![image-20250213165458039](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165458039.png)

![image-20250213165516160](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165516160.png)

> wazuh 插件的版本也一定要和 kibana 版本高度一致
>
> ![image-20250213222520501](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213222520501.png)
>
> ![image-20250213222543718](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213222543718.png)
>
> wazuh  提供 两个用户名和密码 分别是 wazuh/wazuh 还有 wazuh-wui/wazuh-wui 

![image-20250213165527112](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165527112.png)

![image-20250213165534783](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165534783.png)

> 解压的模块如下：
>
> ![image-20250213223431750](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213223431750.png)

![image-20250213165553519](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165553519.png)

> ![image-20250213223025583](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213223025583.png)
>
> ![image-20250213223047458](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213223047458.png)

![image-20250213165600626](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165600626.png)

> ![image-20250213223650088](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213223650088.png)
>
> ![image-20250213165614114](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250213165614114.png)