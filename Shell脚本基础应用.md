# ==Shell脚本基础应用==

## 一、脚本运行

1.编写一个最简单的脚本并保存到 /opt/learn/shelllearn.sh 中，步骤如下

```shell
vi shelllearn.sh
```

```shell
文件编辑页面中：
#!/usr/bin/bash - 指定使用哪个壳程序来解析执行的，在这里表达的意思是下面的代码是用的bash这个壳程序来执行的
#这是Shell的注释，用#开头
echo "hello world"
```

2.使用如下命令运行shelllearn.sh

```shell
source shelllearn.sh    #通过source命令来执行该文件
或
. shelllearn.sh
或
bash shelllearn.sh    #因为这个shell脚本是在bash这个壳程序的环境中执行的
或
chmod u+x shelllearn.sh
./ shelllearn.sh


但是上面的都是命令，我可不可以直接让shelllearn这个文件直接执行？答案是可以
因为这个脚本是在bash壳程序环境下解析执行的，所以我们直接将opt这个目录放在bash环境中，不就可以了吗
```

3.传递参数给shell脚本

| 命令                        | 作用                                                         |
| --------------------------- | ------------------------------------------------------------ |
| echo "hello,12 $3"          | 程序体后面输出带三个参数的值                                 |
| sh hello.sh Denny Bill Mary | 运行时输出Hello,Denny,Bill,Mary                              |
| 1                           | 代表第一个参数                                               |
| 2                           | 代表第二个参数                                               |
| ...                         | 以此类推，但不能超过9个参数（试试看$10会输出什么：$10实际上是在$1后面追加了一个字符0） |
| 0                           | 特殊的 ，$0表示该shell脚本的名称                             |

4.引号的特殊用法
