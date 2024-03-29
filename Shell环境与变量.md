# ==Shell环境与变量==

什么是Shell脚本呢？到底能解决什么问题，Shell脚本其实就是把一批命令集合在一起，解决一些复杂的问题，有点类似于程序设计（在Shell中，又变量，分支，循环，函数，数组等与程序设计完全类似的功能），但是本质上来说不是程序设计。

shell的程序复杂度是无法与真正的编程相提并论的，但是由于与操作系统是集成在一起的，所以能够执行一些更加底层的命令组合。且效率更高

## 一、Shell基础用法

### 1.Shell的类型

| 命令         | 作用                                                         |
| ------------ | ------------------------------------------------------------ |
| Bourne Shell | 是贝尔实验室开发的，Unix普遍使用的Shell，在编程方面比较优秀，但在用户交互方面没有其他Shell优秀 |
| Korn Shell   | 是对 Bourne Shell 的发展，在大部分内容上与 Bourne Shell 兼容，集成了 C Shell 和 Bourne Shell 优点 |
| C Shell      | 是SUN公司shell的BSD版本，语法与c语言相似，比bourne shell 更适合编程 |
| BASH         | 是GNU的Bourne Again Shell,是GNU操作系统上默认的Shell,在Bourne Shel基础上增强了很多特性，如命令补全，命令历史表 |

### 2.Shell操作

| 命令              | 作用                                 |
| ----------------- | ------------------------------------ |
| cat /etc/shells   | 列出系统中所有的shell                |
| ksh /csh/zsh/bash | 切换到其他shell                      |
| chsh qiang        | 使用命令chsh更改用户qiang的默认shell |
| cat /etc/passwd   | 查看用户使用的默认shell              |
| echo $SHELL       | 查看当前环境变量$SHELL的值           |
| wc -l             | 统计又多少行                         |

### 3.Bash基本操作

| 命令                            | 作用                         |
| ------------------------------- | ---------------------------- |
| TAB键                           | 命令补全功能（很实用）       |
| history命令或上下箭头           | 命令的历史记录               |
| allias gohome=“shutdown -h now” | 通过设定一个别名来执行长命令 |
| crontab                         | 作业控制功能                 |
| shell脚本编程                   | 非常灵活的脚本编程能力       |
| ls ; cat /etc/passwd ; mount    | 三个命令放在一起通过 ; 分离  |

### 4.echo命令

| 命令                   | 作用                                                         |
| ---------------------- | ------------------------------------------------------------ |
| echo "helloworld"      | 在屏幕上输出helloworld                                       |
| echo "hello\nworld"    | 在屏幕上输出hello\nworld                                     |
| echo -e "hello\nworld" | 在屏幕上输出<br />hello<br />world                           |
| \a                     | 蜂鸣                                                         |
| \b                     | 退格，覆盖前一个字符                                         |
| \c                     | 不带换行符打印一行                                           |
| \f                     | 换页                                                         |
| \n                     | 换行                                                         |
| \r                     | 回车                                                         |
| \t                     | 制表符                                                       |
| \v                     | 纵向制表符                                                   |
| \                      | 反斜杠                                                       |
| \0nnn                  | ASCII码是nnn（八进制）的字符                                 |
| 练习：                 | 使用echo命令输出如下格式的内容（注意对齐格式）： id name msg 01 milk "hello" 02 john "hi" echo -e "id\tname\tmsg\n01\tmilk\t"hello"\n02\tjohn\t"hi"" |
|                        |                                                              |

```shell
echo -e "id\tname\tmsg\n01\tmilk\t"hello"\n02\tjohn\t"hi"" 
输出

id name msg
01 milk "hello"
02 john "hi"
```



![image-20230927204228025](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230927204228025.png)

![image-20230927204318897](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230927204318897.png)

![image-20230927204445654](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230927204445654.png)

### 5.环境变量

环境变量是指当前操作系统预先定义好的一批全局变量，可以用于任意位置的引用。在Linux和windows中，均有环境变量的概念。

其中使用频率最高的环境变量是 PATH，PATH 中定义了一批文件夹/路径，表示只要是在这个目录下的命令。可以直接在命令行执行，不需要输入完整路径。

| 命令                | 作用                                                         |
| ------------------- | ------------------------------------------------------------ |
| set                 | 显示当前shell的变量，包括当前用户的变量                      |
| env                 | 显示当前用户的变量                                           |
| export              | 显示当前导出或用户变量的shell变量                            |
| cat /etc/profile    | 全局的环境变量，对任何用户生效                               |
| cat ~/.bash_profile | 用户主目录下的环境变量，仅对当前用户生效（本地变量定义在此） |
| export NAME=Denny   | 定义一个NAME环境变量并赋值为Denny                            |
| echo $NAME          | 输出一个环境变量的值                                         |
| unset NAME          | 删除环境变量                                                 |
| echo $USER          | 当前登录的用户名                                             |
| echo $UID           | 当前登录用户的ID号                                           |
| echo $SHELL         | 当前所使用的SHELL                                            |
| echo $HOME          | 当前用户的主目录                                             |
| echo $PED           | 当前命令行所在的目录                                         |
| echo $PATH          | 当前可执行程序的路径（设定PATH，执行命令就不用输入命令的绝对路径） |
| echo $PS1           | 命令的提示字符串（可以试一下export PS1="Welcome Linux# "）   |
| echo $PS2           | 命令一行未写完时换行提示符                                   |
|                     |                                                              |

比如，在opt目录下，正常情况我是无法补全xampp这个安装程序的，需要使用命令 `./xampp....`才可以运行，但是如果我将这个opt目录添加到PATH这个环境变量中，我就可以直接补全。

![image-20230928191435273](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230928191435273.png)

但是如果只是这样配置环境的话，当主机重启就消失了，要想永久配置环境变量就行哟啊在配置文件中修改，就比如对所有用户都成立的 `/etc/profile` 和 仅对当前用户成立生效的 `~/.bash_profile` 



![image-20230928192718394](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230928192718394.png)

将其修改为

![image-20230928192835772](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230928192835772.png)

这样就可以对本用户永久生效了

对于 PS1 这个环境变量 其值对应的就是我们这个主机的名字，用图说话

![image-20230928193115764](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230928193115764.png)



### 6.普通变量



| read NAME     Bill Gates                                    | 从终端将值读入并赋值给变量NAME                               |
| ----------------------------------------------------------- | ------------------------------------------------------------ |
| 命令                                                        | 作用                                                         |
| echo $NAME                                                  | 将变量NAME的值输出                                           |
| read NAME SURNAME    Bill Gates                             | 此时会将Bill赋值给NAME，而将Gates赋值给SURNAME               |
| cat ~/.bash_profile                                         | 本地变量在此定义，将只对本用户生效                           |
| NAME=Denny echo $NAME                                       | 在命令行定义变量NAME并取得其值，注意: 在shell中定义变量时，不能在=号两边加空格，否则会将变量名处理为一个命令，=是命令的第一个参数 |
| SOURCE=/etc/passwd<br />DEST=/opt/learn<br />cp SOURCE DEST | 利用变是代替对应值进行操作                                   |

![image-20230927214630830](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230927214630830.png)

![image-20230927214607747](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230927214607747.png)

![image-20230927214509501](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230927214509501.png)

![image-20230927214519450](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230927214519450.png)

在shell中定义变量时，不能在 = 两边加空格，否则会将变量名处理为一个命令， = 为命令的第一个参数

![image-20230927215806258](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230927215806258.png)

### 7.管道及重定向

| 命令                               | 作用                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| set \| grep USER                   | 从set的输出中查找包含USER的行                                |
| ls \|wc -l                         | 根据 ls 输出的行数来统计该文件夹下的文件数量                 |
| head /etc passwd >> passwd.txt     | 将 /etc/passwd 文件的输出重定向到文件passwd.txt中            |
| tail /etc/passwd >> passwd.txt     | 在文件passwd.txt 后面累加                                    |
| cat < /etc/passwd                  | 将 /etc/passwd 文件作为cat的输入                             |
| cat < /etc/passwd > passwd2.txt    | 将 /etc/passwd 文件作为cat的输入，并将输出结果重定向到passwd2.txt中 |
| ifconfig \| tee ifconfig.tee       | 将ifconfig的内容输出到屏幕上同时输出到文件ifconfig.tee中     |
| ifconfig \| tee -a ifconfig.tee    | 以追加的方式输出到文件ifconfig.tee中                         |
| ifconfig 1> ifconfig.out           | 标准输出重定向到文件ifconfig.out中                           |
| ifconfige 1> ifconfig.error        | 将标准输出重定向到文件ifconfig.error中，此处由于不存在命令ifconfige，所以ifconfig.error中将没有内容 |
| ifconfig 2> ifconfig.error         | 标准输出重定向到文件ifconfig.error中，由于此处没有错误，所以ifconfig.error 文件中将没有内容 |
| ifconfige 2> ifconfig.error        | 标准错误重定向到文件ifconfig.error中                         |
| ls /opt/optt 2> cat.error          | 将标准输出输出到屏幕而将标准错误重定向到cat.error            |
| ls /opt/optt 1> cat.error 2>&1     | 标准输出和标准错误一起重定向到一个文件                       |
| ls /opt/optt 2> /dev/null          | 标准错误信息回输送到系统垃圾箱，而不会输送到屏幕，也不会输出到任何地方 |
| ls /opt /optt 1> ls.out 2>ls.error | 将正确的输出和错误的输出分别重定向到文件不同的文件中去       |
| 命令1 && 命令2                     | 命令1执行成功后才执行命令2                                   |
| 命令1 \|\| 命令2                   | 命令1执行失败后才执行命令2                                   |
| tty                                | 查看当前终端设备编号                                         |
| 1>                                 | 将正常的标准输出重定向，意思就是只有正确的命令执行成功了，才会将执行成功的信息重定向 |
| 2>                                 | 如果有错，那么将错误的信息重定向                             |

![image-20230928221735123](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230928221735123.png)
