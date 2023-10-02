# ==Shell脚本基础应用==

## 一、脚本运行

### 1.编写一个最简单的脚本并保存到 /opt/learn/shelllearn.sh 中，步骤如下

```shell
vi shelllearn.sh
```

```shell
文件编辑页面中：
#!/usr/bin/bash - 指定使用哪个壳程序来解析执行的，在这里表达的意思是下面的代码是用的bash这个壳程序来执行的
#这是Shell的注释，用#开头
echo "hello world"
```

### 2.使用如下命令来运行shelllearn.sh

```shell
source shelllearn.sh    #通过source命令来执行该文件
或
. shelllearn.sh
或
bash shelllearn.sh    #因为这个shell脚本是在bash这个壳程序的环境中执行的
或
sh shelllearn.sh
或
chmod u+x shelllearn.sh
./ shelllearn.sh


但是上面的都是命令，我可不可以直接让shelllearn这个文件直接执行？答案是可以
因为这个脚本是在bash壳程序环境下解析执行的，所以我们直接将opt这个目录放在bash环境中，不就可以了吗
```

### 3.传递参数给shell脚本

| 命令                        | 作用                                                         |
| --------------------------- | ------------------------------------------------------------ |
| echo "hello,12 $3"          | 程序体后面输出带三个参数的值                                 |
| sh hello.sh Denny Bill Mary | 运行时输出Hello,Denny,Bill,Mary                              |
| 1                           | 代表第一个参数                                               |
| 2                           | 代表第二个参数                                               |
| ...                         | 以此类推，但不能超过9个参数（试试看$10会输出什么：$10实际上是在$1后面追加了一个字符0） |
| 0                           | 特殊的 ，$0表示该shell脚本的名称                             |

```shell
#!usr/bin/bash
# 这是shell的注释，用#开头
echo "hello world"
echo "一共有 $# 个参数"
echo "参数一的值为：$1"
echo "参数二的值为：$2"
#在shell中，最多只接受9个参数
echo "参数九的值为：$9"
echo "参数十的值为：$10"
```

![image-20231001173434897](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231001173434897.png)

![image-20231001173558214](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231001173558214.png)

看到了吗，这就是参数的情况，不管参数十你自己输入的是多少，它总会是在 $1 的后面加上一个字符 0

### 4.引号的特殊用法

| 命令                          | 作用                                                         |
| ----------------------------- | ------------------------------------------------------------ |
| echo "$1"                     | 输出第一个参数的值                                           |
| echo '$2'                     | 输出$1                                                       |
| echo 'date'                   | 输出date                                                     |
| echo `date`                   | 输出当前时间（注意这里使用的是~下面的那个反引号而不是单引号,在这里由于markdown的格式转换成了代码的格式） |
| now=date "=%Y-%m-%d %H:%M:%S" | 格式化输出时间，同时赋值                                     |

```shell
# 在shell中，有三个引号：单引号 ‘ ，双引号 “ ，反引号 `
echo "此环境变量的路径为 $PATH"
echo '此环境变量的路径为 $PATH'
echo 'date "+%Y-%m-%d %H:%M:%S"'
echo `date "+%Y-%M-%d %H:%M:%S"` #date命令的执行结果赋值给变量now，也需要使用 反引号
echo $now
```

只有双引号和反引号的命令才会正确执行，单引号包括的对于命令来说只是字符串

![image-20231001174305875](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231001174305875.png)

![image-20231001174639588](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231001174639588.png)

我们会发现，被单引号包裹的两条代码都是原封原样的输出的，说明在shell中用单引号包裹的都属于常量字符串，会被直接输出

- 如果参数超过了10个，就会在参数没超过10个的参数之后加上后面对应的参数。比如$10 = $1的后面添加一个字符0  

- 请完善以下脚本，明确提醒用户，如果输入参数错误，则给予中文提示，如果参数中给定的文件不存在，给与中文不存在的提示。

  文件名：filter.sh

  - ```shell
    #!usr/bin/bash
    #通过参数来决定对某个文件进行查找，并输出相应行数和行号，只接受一个参数
    filename=$1
    grep -n root $filename
    ```

  - 运行方法

    ```shell
    source filter.sh /etc/passwd
    ```

## 二、特定用法

### 1.特殊变量

| 命令 | 作用                                                         |
| ---- | ------------------------------------------------------------ |
| $#   | 传递到脚本的参数个数                                         |
| $0   | 脚本名称                                                     |
| $*   | 以一个单字符串的形式显示所有向脚本传递的参数与位置变量不同，此项参数可超过9个 |
| $$   | 脚本运行的当前进程id号                                       |
| $!   | 后台运行的最后一个进程的进程id号                             |
| $@   | 与 $* 相同，但是使用时加引号，并在引号中返回每个参数         |
| $?   | 显示最后命令的退出状态，0表示正确，其他任何值表示错误，特别的：在脚本中可定义0~255的退出状态码 |
| $_   | 代表上一个命令的最后一个参数                                 |

![image-20231001220030364](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231001220030364.png)

然后第三个 echo $? 结果为0表示上一个 echo $? 命令执行成功并退出

![image-20231001232627054](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231001232627054.png)

我们看这张图 2> 只会将错误的命令执行进行重定向，而由于 ipconfig 这条命令是正确的，于是导致 2> 重定向失败，，所以导致整条命令实际上是失败的，所以最后的 $? 才会输出127这个非0的数字。而下面的因为 ifconfig 这条命令在Linux中不存在，所以是错误的，于是 2> 重定向才是成功的，最后的 $? 才会是 0

理解*和@的区别：

```shell
脚本：
echo "使用 $ * 的结果是：$*"
echo "使用 $ @ 的结果是：$@"
```

```shell
传递参数：
11 22 33 44 55 66

运行结果：
使用 $ * 的结果是：11 22 33 44 55 66    #该结果是所有参数构成一个字符串"11 22 33 44 55 66"
使用 $ @ 的结果是：11 22 33 44 55 66    #该结果是给每一个参数都加上引号作为字符串输出"11" "22" "33" "44" "55" "66"

#下面是通过函数+参数的方式进行验证
function testargs
{
	echo "There is $# args"
	echo "$10"
}
testargs "$*"
testargs "$@"
```

![image-20231002140247423](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231002140247423.png)

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20231002140327935.png" alt="image-20231002140327935" style="zoom:150%;" />

### ![image-20231002140622450](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231002140622450.png)2.expr表达式  

| 命令                   | 作用                                                         |
| ---------------------- | ------------------------------------------------------------ |
| expr 10 + 10           | expr是一个手工计算器，此处会输出20（注意空格）               |
| expr 10+10             | 此处会输出10+10                                              |
| expr 10.1 + 1          | expr不能处理小数                                             |
| expr "hello" = "hello" | 成功返回1，失败返回0                                         |
| 练习：                 | 使用echo命令输出一句话：300/56+360，其中360由运算得来：echo "300/56=`expr 300 / 5 \* 6 `" |

注意空格：

![image-20231002144703870](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231002144703870.png)

expr不能处理非整数：

![image-20231002145130274](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231002145130274.png)

expr对字符判断：

![image-20231002145521183](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231002145521183.png)

## 三、test命令

| 命令                | 作用                                                        |
| ------------------- | ----------------------------------------------------------- |
| test -e /etc/passwd | 测试文件/etc/passwd是否存在，存在则 $? 返回0，不存在则返回1 |
| [ -e /etc/passwd ]  | 与 test -e /etc/passwd 作用一样，注意空格                   |
| -d file             | 如果该文件是一个目录，则结果为真                            |
| -e file             | 如果文件存在，结果为真                                      |
| -f file             | 如果文件是一个普通文件，结果为真                            |
| -r file             | 如果文件可读，则为真                                        |
| -w file             | 如果文件可写，结果为真                                      |
| -x file             | 如果文件可执行，结果为真                                    |
| -s file             | 如果文件长度不为0，结果为真，即 $? 结果为0                  |
| -L file             | 如果文件为符号文件（判断是不是链接文件），结果为真          |

![image-20231002152731956](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231002152731956.png)

![image-20231002152902558](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231002152902558.png)

`注意 空格 该命令的作用和 teat -e 是一样的`

### 2.逻辑处理

| 命令                                 | 作用                                            |
| ------------------------------------ | ----------------------------------------------- |
| [ -e /etc/passwd -a -r /etc/passwd ] | -a 逻辑与，操作符两边均为真，结果为真，否则为假 |
| [ -e /etc/passwd -o -r /etc/passwd ] | 逻辑或，操作符两边一遍为真，结果为真，否则为假  |
| [ ! -e /etc/passwd ]                 | 逻辑否，条件为假，结果为真                      |

### 3.test字符串

| 命令                 | 作用           |
| -------------------- | -------------- |
| [ $USER = "root" ]   | 字符串比较     |
| [ "$USER" = "root" ] | 建议使用此方式 |
| =                    | 等于           |
| !=                   | 不等于         |
| -z                   | 为空字符串     |
| -n                   | 非空字符串     |

### 4.test数值

| 命令             | 作用                         |
| ---------------- | ---------------------------- |
| [ $$ -eq 18646 ] | 对数值的测试                 |
| -eq              | 数值相等  =                  |
| -ne              | 数值不相等  !=               |
| -le              | 第一个数小于等于第二个数  <= |
| -ge              | 第一个数大于等于第二个数  >= |
| -gt              | 第一个数大于第二个数  >      |
| -lt              | 第一个数小于第二个数  <      |

## 课后思考

1.如果参数超过了10个或者像ping -c 5 woniuxy.com。该如何处理？

要想让脚本你可以传递超过9个参数，我们只需要在脚本中对超过的参数形式进行修改就好了

```shell
#!usr/bin/bash
echo $*
echo $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14}
```

我们来看结果：

![image-20231002165032429](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231002165032429.png)

这样就可以正确输出超过9个的参数了

2.请完善以下脚本，明确提醒用户，如果输入参数错误，则给予中文提示，如果参数中给定的文件不存在，基于中文不存在的提示。

```shell
#!usr/bin/bash
# 通过参数来决定对某个文件进行查找，并输出响应行号和行数，只接受一个参数
filename=$1

grep -n root $filename
```



3.在shell中，如何对小数进行运算

这里有两个我觉得较容易理解的文章：

[Shell中小数计算的两种方式_shell中三种小数运算方式-CSDN博客](https://blog.csdn.net/Jerry_1126/article/details/85331404)

> 在Shell中，不能用计算整数的方式来计算小数。要借助bc命令，可以说bc是一个计算器，也可以说bc是个微型编程语言，反正当作工具来用，还是很方便，特别是小数计算。必须借助bc命令。
>
> ```shell
> linux:~# var1=5
> linux:~# var2=35.14
> linux:~# var3=$(echo "scale=4; $var2 / $var1" | bc)
> linux:~# echo $var3
> 7.0280
> 
> #其中 scale=4 表示保留小数点后四位
> ```
>
> ```shell
> linux:~# var3=$(bc <<EOF
> >scale = 4
> >var1 = 5
> >var2 = 35.14
> >var2 / var1
> >EOF)
> linux:~# echo $var3
> ```
>
> 

[shell脚本中的小数运算 - lnlvinso - 博客园 (cnblogs.com)](https://www.cnblogs.com/lnlvinso/p/13460810.html)

4.SSH相关的配置和日志
