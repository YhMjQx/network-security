# ==VI的使用==

##  一、文本的创建于查看

| 功能项   | 命令实例                        | 作用                                                         |
| -------- | ------------------------------- | ------------------------------------------------------------ |
| 文本创建 | vi /opt/learn/helo.txt          | 在目录/opt/learn下创建文件hello.txt并进入vi编辑界面          |
|          | touch /opt/learn/test           | 在目录/opt/learn下创建空白文件test                           |
|          | cat > /opt/learn/catfile << EOF | 创建文件catflle并在屏幕上输入内容，最后输入EOF结束，如果不使用<<EOF，则输入结束时直接按 Ctrl+D也可以 |
|          |                                 |                                                              |
| 文件查看 | vi /etc/password                | 在vi编辑器中输出文本内容                                     |
|          | cat /etc/password               | 在屏幕上输出文本内容                                         |
|          | more /etc/password              | 分屏输出文本内容                                             |
|          | less /etc/password              | 分屏输出文本内容并按需加载文件(适用于大文件的查看)           |
|          | head -n 10 /etc/password        | 只输出文件的头10行,不加参数默认输出前10行内容                |
|          | tail -n 20 /etc/password        | 只输出文件未尾的20行，不加参数默认输出后10行内容             |
|          | tail -f 文本文件                | 标识铜鼓哦留的方式实时查看最新的文件内容                     |
|          | string /bin/ls                  | 查看二进制文件中的可打印字符                                 |
|          |                                 |                                                              |

![image-20230912153556735](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230912153556735.png)

![image-20230912155300352](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230912155300352.png)

![image-20230912155304079](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230912155304079.png)

**`tail -f` **的方式可以做到实时查看文本内容变化

more，也就是将一个比较大的文件分屏输出，可以通过回车进行加载文本信息查看下面每一行的文本信息

less和more的功能是一样的，但是不同点在于，more是将文本信息一次性全都加载到内存当中，而 less 是回车一行再加载一行，也就是说 less 可以让内存消耗少一点

more和 less一般不糊用户XShell，因为IE我现在接触的东西还很少XShell是支持使用鼠标滚轮上下查看的，但是CentOS命令行界面就不行了，此时才需要使用 

## 二、文本内容的编辑

编辑一段文本，在命令模式下，vi是默认的编辑器，进入vi界面后，由两种处理模式：命令模式和编辑模式。默认命令模式进入，按 i 或者 a 进入编辑模式，在编辑模式下 按 ESC 进入命令模式

| 命令实例    | 作用                                            |
| ----------- | ----------------------------------------------- |
| vi filename | 生成新文件或者编辑查看文件                      |
| i 或者 a    | 从命令模式进入编辑模式,i为插入文本，a为追加文本 |
| Esc         | 从编辑模式进入命令模式                          |
| :w          | 保存文本                                        |
| :wq         | 保存并退出                                      |
| :wq!        | 保存并强制退出                                  |
| :q          | 退出                                            |
| :q!         | 强制退出                                        |
| o           | 光标下添加一行并进入编辑模式                    |
| O           | 在光标所在行的上方添加一行                      |
| dd          | 删除一行文字                                    |
| D           | 删除从当前光标到行尾的内容                      |
| x           | 删除一个字符                                    |
| s           | 删除一个字符并切换到编辑模式                    |
| S           | 删除一行并切换到编辑模式                        |
| :n          | 光标移至文本第n行                               |
| $           | 光标移到文本的行尾                              |
| A           | 光标移到文本的行尾并切换到编辑模式              |
| ^           | 光标移到文本的行首                              |
| G           | 光标移到文本的末尾                              |
| gg          | 光标移到文本的首行                              |
| ZZ          | 存盘退出                                        |
| /字符串     | 查找某个字符串                                  |
| n           | 继续查找                                        |
| :u          | 撤消(同标准编辑器中的Ctrl+Z)                    |
| :redo       | 重做(同标准编辑器中的Ctrl+Y)                    |

## 三、修改ip地址为静态IP

默认情况下，linux的IPIP地址为DHCP动态分配，而面向服务器应用场景，通常建议设置为静态IP，操作步骤如下：

### 1.查看默认网关，运行 route 命令

```
[root@centqiang /]# route
Kernel Ip routing table
Destination     Gateway        Genmask        Flags Metric Ref    Use Iface
defau7t         192.168.112.2  0.0.0.0        UG    100    0      0   ens33
192.168.112.0   0.0.0.0        255.255.255.0  U     100    0      0   ens33
```

以上命令确认网关地址为：192.168.112.2

### 2.确认动态IP地址及网段等信息

运行命令：vi /etc/sysconfig/network-scripts/ifcfg-ens33，其中ens33与IP addr看到的网上编号一致，并修改网上的IP地址信息如下：

```
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER ONLY="no"
#BOOTPROTO="dhcp"   # 此处注释DHCP
BOOTPROTO="static"  #设置为静态IP
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
NAME="ens33"
UUID="4930fb4c-c9cc-4fd1-97e9-49198099403c"
DEVICE="ens33"
ONB00T="yes"


#下面手工指定静态IP地址，包括IP地址，子网掩码，网关，DNS服务器，广播地址（可不指定）
IPADDR="192.168.112.188"
NETMASK="255.255.255.0"
GATEWAY="192.168.112.2"
DNS1="192.168.112.12"

#下面两个可以不用输入使用默认值
DNS2="114.114.114.114"
BROADCAST="192.168.112.255"

```

可以通过ping和 `curl 网址`来判断你是否可以上网，也就是是否改成功了