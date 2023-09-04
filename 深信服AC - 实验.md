# ==跨三层（AF）取MAC==

实验环境：

需要在172.172.4.10上做一个不需要认证，然后认证后AC自动绑定172.172.4.10的IP和MAC地址

由于AC和172.172.4.10处于不同网络，所以AC不能自动绑定

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903171312895.png" alt="image-20230903171312895" style="zoom:200%;" />

**第一步：**

在用户管理中创建一个销售部，使得172.172.4.10可以以销售部的身份上线

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903173543760.png" alt="image-20230903173543760" style="zoom:200%;" />

然后组创建好了之后，需要添加认证策略

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903173735174.png" alt="image-20230903173735174" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903191126944.png" alt="image-20230903191126944" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903173838820.png" alt="image-20230903173838820" style="zoom:200%;" />

现在需要在AF上取MAC

**首先**，进入AF，去查询172.172.1.2这个口的MAC地址

**然后**将得到的结果放进AC的配置中

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903174731946.png" alt="image-20230903174731946" style="zoom:200%;" />

从上面我们可以知道，该操作使用的是SNMP协议，于是我们现在需要去开启SNMP协议，由于AF是与AC相连的，所以SNMP协议配置时，需要用到的是172.172.1.3的信息

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903175130886.png" alt="image-20230903175130886" style="zoom:200%;" />

然后开启接口的SNMP协议管理

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903175403415.png" alt="image-20230903175403415" style="zoom:200%;" />

**最后**，我们验证一下，是否成功开启

**第一步**：检验是不是销售部上线了

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903190533426.png" alt="image-20230903190533426" style="zoom:200%;" />

**第二步**：进入用户认证管理 -》用户管理 -》IP/MAC绑定查看

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903191300088.png" alt="image-20230903191300088" style="zoom:200%;" />

如果没有绑定成功，自己去网页中上一下网，登录一下界面应该就有了，实在不行再把浏览器中的记录清楚了之后再重新上网一下

绑定成功后就有了以下的情况

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903191437508.png" alt="image-20230903191437508" style="zoom:200%;" />













# ==邮件审计==

邮件审计时，先配置认证策略

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904144231970.png" alt="image-20230904144231970" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904163802304.png" alt="image-20230904163802304" style="zoom:200%;" />

再配置上网审计策略，适用对象。然后配置上网权限策略

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904144500325.png" alt="image-20230904144500325" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904144727454.png" alt="image-20230904144727454" style="zoom:200%;" />

一切准备就绪就可以在实时状态中的上网行为监控里查看了





# ==审计IM聊天内容==

一样的，需要有认证策略，和上面一样，如果有了就可以不用配置了

然后，进入以下界面（在上网审计策略当中）

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904162851050.png" alt="image-20230904162851050" style="zoom:200%;" />

选中这两项，然后适用对象还是IT部

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904163143398.png" alt="image-20230904163143398" style="zoom:200%;" />

现在就需要添加准入策略

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904163957980.png" alt="image-20230904163957980" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904164109530.png" alt="image-20230904164109530" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904164122315.png" alt="image-20230904164122315" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904164419429.png" alt="image-20230904164419429" style="zoom:200%;" />

这个时候客户端再去访问网页就需要安装一个插件，插件安装好了之后，才会准入AC

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904164508300.png" alt="image-20230904164508300" style="zoom:200%;" />

把这个准入插件安装好了之后再进行qq聊天的话，其中的内容就会被审计到

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904164725711.png" alt="image-20230904164725711" style="zoom:200%;" />











# ==外部AD用户认证==

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904165753015.png" alt="image-20230904165753015" style="zoom:200%;" />

由于pc想要访问公网，需要通过AC认证，但是AC认证是在外部做的AD认证，接下来，看操作

## 一、远程登录AD（账号密码在上图）

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904170008066.png" alt="image-20230904170008066" style="zoom:200%;" />

### 1.打开用户和计算机

开始菜单 -> 管理工具 

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904170207187.png" alt="image-20230904170207187" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904170420767.png" alt="image-20230904170420767" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904170541944.png" alt="image-20230904170541944" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904170653591.png" alt="image-20230904170653591" style="zoom:200%;" />

设置密码就不教了，但要符合密码复杂性要求

## 2.返回AC

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904170938913.png" alt="image-20230904170938913" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904182346118.png" alt="image-20230904182346118" style="zoom:200%;" />

## 3.服务器添加好了之后，再添加认证策略

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904182927607.png" alt="image-20230904182927607" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904182951595.png" alt="image-20230904182951595" style="zoom:200%;" />

后面不过改变，直接提交

## 4.测试

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904183254422.png" alt="image-20230904183254422" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904183436324.png" alt="image-20230904183436324" style="zoom:200%;" />

在用户认证与管理 -》用户管理 -》组/用户中，会将AD域中的数据同步到AC中

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904183558433.png" alt="image-20230904183558433" style="zoom:200%;" />









# ==AC用户自注册==

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904184309846.png" alt="image-20230904184309846" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904184705504.png" alt="image-20230904184705504" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904185938575.png" alt="image-20230904185938575" style="zoom:200%;" />

现在又需要一条认证策略

![image-20230904190141146](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904190141146.png)

![image-20230904190208894](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904190208894.png)

后面还是不变，直接提交

## 测试

使用4.0网段的进入AC

![image-20230904191239153](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904191239153.png)

![image-20230904191304366](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904191304366.png)

注册好之后，我们返回AC中区管理这个注册

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904191354550.png" alt="image-20230904191354550" style="zoom:200%;" />

最后返回去重新登陆就好了







# ==外置日志中心配置==

## 1.在AD上面下载DataCenter

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904192522335.png" alt="image-20230904192522335" style="zoom:200%;" />

![image-20230904192603963](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904192603963.png)

## 2.回到AC

![image-20230904192719868](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904192719868.png)

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904192829264.png" alt="image-20230904192829264" style="zoom:150%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904192919025.png" alt="image-20230904192919025" style="zoom:150%;" />

## 3.登录测试

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904193047534.png" alt="image-20230904193047534" style="zoom:150%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904193352766.png" alt="image-20230904193352766" style="zoom:200%;" />

外部日志中心是看不见AC系统内部的日志信息的

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230904193636708.png" alt="image-20230904193636708" style="zoom:150%;" />