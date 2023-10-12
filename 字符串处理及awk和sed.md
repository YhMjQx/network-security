# ==字符串处理及awk和sed==

## 一.字符串处理

```shell
假设有变量 url="http://www.woniuxy.com/index.html"，以下用法及结果输出

*// - 从左边开始删除第一个  // 号及左边的所有字符（从左往右删掉第一个//及后面的内容）：
echo ${url#*//}  （//是可替换的内容）输出结果：www.woniuxy.com/index.html 

##*/ - 表示从左边开始删除最后（最右边）一个 / 号及左边的所有字符（换句话说也就是留下最后一个 / 后面的内容）：
echo ${url##*/}  （ / 是可替换内容）输出结果： index.html

%/* - 表示从右边开始删除最后（最右边一个） / 号及右边的所有字符：
echo ${url%/*}  （ / 是可替换内容）输出结果：http://www.woniuxy.com

%%/* - 表示从右边开始，删除最后（最左边）一个 /号及右边的字符串：
echo ${url%%/*}  （ / 是可替换内容）输出结果：http:

 # 号代表从左边开始最左边的最后一个匹配项，然后 * 号在哪一侧就删掉哪一侧的内容， ## 号代表 从左边开始最右边的匹配项匹配，然后看 * 号在哪一侧就删掉哪一侧的内容
eg:
echo ${url#*/} - 从左边开始删除最左边的/的左边的内容
echo ${url##*/} - 从最左边开始删除最右边的/的左侧的所有内容


 % 号代表从最右边开始的最右边一个匹配项开始，删除匹配项 * 所在一侧的内容； %% 号表示从最右边开始删除最左边的匹配项的 * 号所在一侧的内容
其实和 # 的意思是一样的，只是 # 和 % 的方向是相反的

假设有变量：phone="18812345678"，利用 ： 进行字符穿截取
echo ${phone:0:5}  从第一个位置开始往后截取5个字符，输出为：188123
echo ${phone:6}  从第7个位置开始往后直到结束，输出为：45678 
echo ${phone:0-7:5}  从右边第7个字符开始，截取5个输出为：23456
echo ${phone:0-7}  从右边第7个字符开始，直到结束，输出为：2345678
echo ${#phone}  取得phone字符串的数量，即字符串长度

```



## 二、AWK（对文件或字符串进行格式化输出）

对文本进行逐行处理的编程语言，它来源于3个创作者的名字：Aho、（Peter）Weinberg和（Brain）Kernighan，与sed和grep很相似，awk是一种样式扫描与处理工具，但其功能却强于sed和grep

下面是一个最简单的awk的用法

![image-20231011225236998](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231011225236998.png)

![image-20231012181419904](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231012181419904.png)

由上可见，从awk处理视角来看，任意一段文本局可以按照行列（二维表）的形式理解

```shell
awk 选项 处理逻辑 文件或文本
#如果要针对命令执行结果进行过滤，则必须要使用管道符

$0 代表整个字符串

echo "hello woniu welcome chengdu" | awk '{print $2}' #默认情况下awk会按照空格隔开，并输出第二列的内容：woniuxy

echo "http://www.wociuxy.com/index.html" | awk '{print $2}'  #因为默认是以空格作为分隔符的，但是这个字符串中并没有空格，所以该指令的输出结果是少读没有，所以我们可以指定分隔符 使用 -F 选项

echo "http://www.wociuxy.com/index.html" | awk -F '.' '{print $2}'
- F '.' 意思是以斜线作为分隔符
输出结果：woniuxy

也可以使用 -F [/.] 表示既可以用 . 也可以用 / 作为分隔符

查找/etc/passwd下面第一个域为root的行并将其第一个域打印出来（-F : 表示以冒号分隔域）
awk -F : '$1~/root/ {print $0}' /etc/passwd
#匹配 以冒号分隔 第一栏中是root的一行并输出，$1~是用来匹配第一栏的 $0 是用来打印一整行的 /xxx/ 是一个正则表达式

查找/etc/passwd中不包含root的行并统计一个有多少行
awk -F : 'BEGIN {sum=0} $0!~/root/ {sum+1} END {print sum}' /etc/passwd

文件/etc/passwd中如果第一个域包含root则打印他，否则打印第三个域的值
awk -F : '{if ($1=="root") print $1;else print $3}' /etc/passwd

打印文件中不包含bin或者root的行（特别的$0表示整行）
awk -F : '$0!~/(bin|root)' /etc/passwd

查找进程中包含yes的进程并打印出CPU使用率
top -d 1 | awk '$0~/yes/ {print $10}'

ps -aux|sort -k 3 -r|head -n 5|awk '{print "%-10s %-10s\n", $2, $3}'

cpu=`top -n 1 | grep "^%Cpu" | awk -F " " '{print int($8)}'`
```

![image-20231012203634124](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231012203634124.png)

![image-20231012204359999](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231012204359999.png)

```shell
如何通过结合ping 和 awk 等其他命令来获得一个域名的IP地址（不能有其他内容）？

我们看上图可以发现 `ping www.woniuxy.com -c 1` 该命令的执行结果有两行，我们分别从两行的特征入手

方法一（从第一行入手）：
注意 以特殊符号作为分隔符的时候要进行转义
ping www.woniuxy.com -c 1 | grep ^PING | awk -F [\(\)] `{print $2}` 

方法二（从第二行入手）：
ping www.woniuxy.com -c 1 | grep icmp_sec | awk `{print $4}`

方法三（正则表达式）：
ping www.woniuxy.com -c 1 | awk `$4~/^[0-9]*\.[0-9]*\./ {print $4}`

方法四（如果没有规则可以grep的情况下，则使用head和tail联合使用来定位具体的行）：
ping www.woniuxy.com -c 1 | head -n 2 | tail -n 1
#先取前两行，然后在前两行的基础上取最后一行
```

```shell
wc -l /etc/passwd 
#计算整个文件的行数

grep root /etc/passwd
#输出文件中有root的行

grep -v root /etc/passwd
#输出文件中没有root的行

grep -v root /etc/passwd | wc -l
#统计文件中不包含root的行数
```





## 三、sed（编辑文本）

### 1.sed的基本用法

常用的三个选项：

（1）-e	指定脚本 或 进行多点编辑

（2）-n	显示处理后的结果

（3）-i	永久将编辑保存到指定文件中

常用的6个动作：

（1）a：新增，a 的后面可以接字符串，而这些字符串会在新的一行出现（目前的下一行）

（2）c：取代，c的后面可以接字符串，这些字符串可以取代n1,n2 之间的行

（3）d：删除，因为是删除，所以 d 后面通常不会接任何字符串

（4）i：插入，i的后面可以接字符串，二这些字符串会在新的一行出现（目前的上一行）

（5）P：打印，将某个选择的数据印出。通常 p 会与参数 sed -n 一起运行

（6）s：取代，可以直接进行取代工作，通常这个 s 的动作可以搭配正则表达式进行

2.示例：

```shell
head /etc/passwd > test.txt 	#先准备一份简单的文本文件

sed '5a Hello woniu' test.txt 	#在第5行后面添加 Hello woniu 的新行。即：原新增的作为新的第6行

sed '5i Hello Chengdu' test.txt 	#在第5行前面添加 Hello Chengdu 的新行，即：原地5行就变为第6行

sed '2d' test.txt 	#删除第2行

sed '2,5d' test.txt 	#删除第2行到第5行

sed '3,$d' test.txt 	#删除第3行到最后

sed '2,5c Goooooood' text.txt 	#将第2行到第5行的内容替换为 Goooooood

sed -n '/root/p' test.txt 	#搜索包含root的行并打印出来

sed -n '/root/d' test.txt 	#搜索包含root的行并删除

sed 's/要替换的字符串/新的字符串/g' 	#搜索并进行替换，支持正则表达式，其中 g 代表全局替换，可以不加但结果是按行找第一个
# 带有 g 参数，表示在整个文本中将所有的要替换的字符串替换为新的字符串，如果不带 g 就表名在每一行中匹配第一个找到的字符串并替换

sed -e '' -e '' ie '' 	#多点编辑，即一次使用多个规则

sed -i '4a Hello woniu' test.txt

```

事实上， `sed '5a Hello woniu' test.txt ` 这条命令只会临时的在第5行后面新添加一行 `Hello woniu` 同时并输出到屏幕上，当再一次`cat test.txt`的时候内容就消失了，如果要永久插入的话就要在 sed 的后面加上参数 -i 此时就可以永久插入，但不会同时自动显示在屏幕上 
