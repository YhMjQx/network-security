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

![image-20231011225546184](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231011225546184.png)

```shell
awk 选项 处理逻辑 文件或文本

echo "hello woniu welcome chengdu" | awk '{print $2}' #按照空格隔开，并输出第二列的内容：woniuxy

echo "http://www.wociuxy.com/index.html" | awk '{print $2}'  #因为默认是以空格作为分隔符的，但是这个字符串中并没有空格，所以该指令的输出结果是少读没有，所以我们可以指定分隔符 使用 -F 选项

echo "http://www.wociuxy.com/index.html" | awk -F '.' '{print $2}'
输出结果：woniuxy

也可以使用 -F [/.] 表示既可以用 . 也可以用 / 分隔

查找/etc/passwd下面第一个域为root的行并将其第一个域打印出来（-F : 表示以冒号分隔域）
awk -F : '$1~/root/ {print $1}' /etc/passwd

查找/etc/passwd中不包含root的行并统计一个有多少行
awk -F : 'BEGIN {sum=0} $0!~/root/ {sum+1} END {print sum}' /etc/passwd

文件/etc/passwd中如果第一个域包含root则打印他，否则打印第三个域的值
awk -F : '{if ($1=="root") print $1;else print $3}' /etc/passwd

 
```





## 三、sed（编辑文本）
