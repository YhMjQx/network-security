# ==CronTab及定时任务==

## 一、定时任务的基本原理

```shell
# 每5秒钟向文本中输出一次时间
#for i in {1..10}; do 
while [ 1 < 2 ]; do
date "+%Y-%m-%d %H:%M:%S" >> /opt/learn/dater.txt
date "+%Y-%m-%d %H:%M:%S"
sleep 5
done
```

![image-20231005143723611](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005143723611.png)

请尝试（仅使用定时任务基本原理来解答，不使用cron）：
（1）在每个小时的20分钟执行一条指令，比如8:20,9:20,10;20 ...均会执行一次指令



（2）在指定的某个时间执行，比如23:30执行一次指令，每天晚上 23:30分执行一次指令





## 二、Cron定时任务

最简单的crontab：

```shell
crontab -e -u root

进入文本编辑器：
* * * * * command

eg:
* * * * * date >> crondate.txt
或
*/1 * * * * date >> /opt/learn/crondate.txt

这两条指令会每分钟执行一次，这个crondate.txt是默认在主目录下的，也就是在 ~ 这个目录中。当然我们也可以执行其绝对路径




```

```shell
20 * * * * date >> /opt/learn/crondate.txt
#表示每小时的第20分钟执行一次，想要控制那个时间，只需要在对应的位置进行修改就好了

20,25,30 5-8 * * 5 date >> /opt/learn/crondate.txt
#表示每周五的五点到八点期间的第20,25,30分钟分别执行一次命令
#-  表示范围
#， 表示单个隔开

*/5 * * * * date >> /opt/learn/crondate.txt
#表示每五分钟执行一次指令
#每一个单位都可以使用以上规则 数字 /数字 -范围 分隔
```



![image-20231005151331460](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005151331460.png)

OK，上面的都是别人的测试和理论，接下来我们要有自己的测试和想法

第一步：查看crond服务状态

```shell
systemctl status crond
```

![image-20231005172042679](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005172042679.png)

第二步：编辑crontab文件

```shell
crontab -e -u root	#紧接着就会进入crontab的编辑页面
```

```shell
# 编写crontab 的规则
* * * * * date >> /opt/learn/crontabtext.txt

```

第三步：查看crond进程是否执行

```shell
#由于我们将指令重定向到/opt/learn/crontatext.txt这个文件中，所以我们要想查看crontab的进程，就必须查看文件的内容
cat /opt/learn/crontabtext.txt
```

![image-20231005173156758](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005173156758.png)

我们发现最终结果确实是每一分钟指令执行一次

### 但是

如果我们的指令比较复杂呢？？？，比如我们想要将date进行格式化输出，即 `* * * * * date "+%Y-%m-%d %H:%M:%S >> /opt/learn/crontabtext.txt"` 我们看看会发生什么

第一步：将crontab 文件修改为：

![image-20231005173637586](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005173637586.png)

第二步：查看crontab进程

![image-20231005173837451](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005173837451.png)

结果发现并没有喜爱那个刚才一样正确重定向到这个文件中，法尔告诉我们有一封邮件，我们去看看怎么回事，但是由于文件太长，所以这里我们只查看文件后20行

```shell
tail -n 20 /var/spool/mail/root
```

![image-20231005174820766](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005174820766.png)

他说是 " 这个的匹配出了问题我们对应crontab 文件中的内容去看 `* * * * * date "+%Y-%m-%d %H:%M:%S >> /opt/learn/crontabtext.txt"`

那我们不用这个双引号了，我们用单引号或反引号将这个双引号和他中间的内容包含起来试试，发现还是都会报错，内容和这个错误都是一样的，只是符号改变了而已，试想：

**应该是crontab域的问题，本来只有六列，但是在这里因为空格的缘故导致系统判定出现了超过六列的规则，素以会出现这种错误，于是，我们在面对这种情况的时候就需要使用脚本作为一个列**

| 命令实例                            | 作用                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| crontab                             | 每个用户都可以有一个crontab文件来保存调度信息，通过该命令运行任意一个shell脚本或者命令 |
| /var/spool/cron                     | 保存所有用户的crontab文件                                    |
| /etc/cron.deny<br />/etc/cron.allow | 系统管理员可以通过cron.deny和cron.allow这两个文件来禁止或允许用户拥有自己的crontab文件（cron.allow需要自己新建） |
| crontab的域                         | 第一列 分钟0~59  <br />第二列 小时0~23（0表示子夜）  <br />第三列 日1~31   <br />第四列 月1~12   <br />第五列  星期0~6（0表示星期天） <br /> 第六列  要运行的命令 |
| 常用规则                            | * ： 匹配任何值<br />*/n ：匹配每n个单位（从起始值算起的每n个单位）<br />x ：匹配 x  <br />x-y：匹配从x-y的值<br />x,y,z：只匹配x,y,z三个值 |
| crontab [ -u user ] -e -l -r        | -u 用户名<br />-e 编辑crontab文件<br />-l 列出crontab文件中的内容<br />-r 删除crontab文件 |
| systemctl start/stop crond          | 启动或停止crond进程，如crond进程停止，则不会有任务被自动执行 |
| 不发送邮件                          | 在crontab -e 中有编辑任务时，在第一行添加：MAILTO="",则不会发送邮件。可以通过 、var/log/cron 查看执行的日志 |
|                                     |                                                              |

> 提示：编写定时任务时，确定好定时规则后，要执行的指令建议直接卸载shell脚本中（为了方便起见，我们可以选择给该脚本文件添加可执行权限），让cron直接执行改脚本即可，尽量避免在定时规则文件中直接调用命令
>
> 类似于：* * * * * /opt/learn/crontabtext.sh
>
> 这样的形式（这种形式需要确保脚本具有可执行权限，并且指定绝对路径）（如果不想执行绝对路径就将/opt/learn/这个目录放在bash环境变量当中，但并不是很建议这样使用）

书接上回：要想在crontab中添加较为复杂的规则，我们需要使用脚本来实现，我们来看

第一步：完成crontabtext.sh的编辑

![image-20231005180947327](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005180947327.png)

第二步：给crontext.sh脚本添加可执行权限，然后直接在列中放置脚本的绝对路径即可（如果不添加可执行权限我们也可以猜crontab中使用 `sh 绝对路径` 来使用）

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005181129671.png" alt="image-20231005181129671" style="zoom:150%;" />

第三步：在crontab添加脚本

![image-20231005181328188](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005181328188.png)

第四步：查看crontext.txt中的crontab输出信息

![image-20231005181613874](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005181613874.png)

结果是成功。



## 三、其他补充命令

| 命令实例           | 作用                                                         |
| ------------------ | ------------------------------------------------------------ |
| at                 | 单次定时任务， yum install at -y; systemctl start atd;       |
| at 时间            | 指定某一特定的时间去做某件事情                               |
| at HH:MM           | at 16:00                                                     |
| at now + 5 minutes | 从现在开始的5分钟后                                          |
| 如何退出at编辑模式 | Ctrl + D                                                     |
| atq                | 查询现有任务，即待定的任务                                   |
| atrm id            | 删除某任务，这个id在atq的结果中可以看见                      |
|                    |                                                              |
| command &          | 后台运行，如有输出，则会输出到前台                           |
| nohup command &    | 后台运行 ，所有输出将会转存到nohup.out文件中                 |
|                    |                                                              |
| sleep n            | 让shell脚本暂停n秒                                           |
| usleep n           | 让shell脚本沉睡n纳秒，10的-9次方                             |
|                    |                                                              |
| time command       | 计算某一个命令或脚本运行时花的时间（精确到毫秒）：如：time ls (ls这个命令所花的时间) <br />time sh myshell.sh （运行myshell.sh这个脚本所花的时间） |
|                    |                                                              |

![image-20231005211929901](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005211929901.png)

![image-20231005212024776](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231005212024776.png)

使用`sh timer.sh &` 该命令可以将脚本放在后台运行，但是要输出到命令行中的数据还是会依旧输出

平常如果我们想要将一个运行的程序转到后台运行可以使用 Ctrl + Z

使用 `nohub sh timer.sh &`该命令将timer.sh脚本在后台运行，并且timer.sh中要输出到命令中的数据也都会自动重定向到nohub.out文件中去
