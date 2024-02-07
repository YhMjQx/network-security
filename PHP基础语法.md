[TOC]



# ==PHP基础语法==

> 这是一个思考，经过本节课我们可以知道，在通过Apache访问php页面时，服务器端会用php脚本引擎处理我们的php源码，此时我们在页面查看源代码时，是根本看不到php代码的。而html相反，html页面的源代码和我满写的代码是完全一样的，因此我们可以试想一下，如果用php页面写html会怎么样，客户根本无法查看到我原本的php代码，相反，看到的都是html代码
>
> ```php
> <!DOCTYPE html>
> <html lang="en">
> <head>
>     <meta charset="UTF-8">
>     <meta name="viewport" content="width=device-width, initial-scale=1.0">
>     <title>lookphp</title>
> </head>
> <body>
>     <?php
>         echo '<div style="width:300px; height:200px; border:solid 3px red;">'.`date /T`.'</div>'
>     ?>
> </body>
> </html>
> ```
>
> 访问结果：
>
> ![image-20240207153546174](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240207153546174.png)
>
> 我们来查看页面源代码，会发现完全成了html语句了，说明我们就可以通过这种方式来蒙蔽客户的双眼，从而提高安全
>
> ```
> <!DOCTYPE html>
> <html lang="en">
> <head>
>     <meta charset="UTF-8">
>     <meta name="viewport" content="width=device-width, initial-scale=1.0">
>     <title>lookphp</title>
> </head>
> <body>
>     <div style="width:300px; height:200px; border:solid 3px red;">2024/02/07 ���� 
> </div></body>
> </html>
> ```
>
> 但是这种方法必须要通过php脚本引擎处理才有这样的效果。有没有一种可能访问的时候，跳过该php脚本引擎，直接窥探后台脚本代码。从而实现攻击呢？

## 一、基本结构

### 1.代码块

php代码必须要用 <?php  ?>包裹起来 。而且 .php 文件中可以写 html 语法，但是.html 文件中不能写 php代码

```php

<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    </head>
    <body>
        <?php
       		echo "你好啊，请接受我的网络攻击吧";
    	?>
    </body>
</html>
```



### 2.注释

```php
<?php
    echo "你好啊，请接受我的网络攻击吧";
    /* 该方法可以将这两个字符包裹的内容全都注释 */
    //该方法只能单独注释一行 

?>
```



### 3.内容输出

#### （1）换行问题

```php
<?php
    echo "你好啊，请接受我的网络攻击吧。\n";
    /* 该方法可以将这两个字符包裹的内容全都注释 */
    //该方法只能单独注释一行 
    print "欢迎来到牛逼的网页。";
    
?>

```

![image-20240207135943156](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240207135943156.png)

php中，浏览器无法解析 \n 作为换行符。要想换行，换行符必须为 `<br>` 或 `<br/>`

```php
<?php
    echo "你好啊，请接受我的网络攻击吧。<br>";
    /* 该方法可以将这两个字符包裹的内容全都注释 */
    //该方法只能单独注释一行 
    print "欢迎来到牛逼的网页。";
    
?>

```

![image-20240207140106361](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240207140106361.png)

#### （2）echo与print

```php
<?php
    echo "你好啊，请接受我的网络攻击吧。<br>";
    /* 该方法可以将这两个字符包裹的内容全都注释 */
    //该方法只能单独注释一行 
    print "欢迎来到牛逼的网页。<br>";

    echo '111111','22222','33333333<br>';
    // print '111111','22222','33333333';   php语法中 print输出字符串不能用 , 连接
    echo '111111'.'22222'.'33333333<br>';  
    print '111111'.'22222'.'33333333<br>';  
    // 一般情况下，我们都选择使用 . 来连接字符串
?>

```



### 4.通信过程

我们在浏览器查看php页面的源代码时，发现其代码很简洁，仿佛就是将执行好的代码结果作为页面源代码似的。这一点和HTML页面源代码就不一样了，HTML页面源代码就是整个html文件中的所有内容。这其实与php和html页面处理和通信过程有关。

```php
```

如下图，左边是html页面的访问，右边是php页面的访问

![image-20240207134750984](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240207134750984.png)

### 5.引号问题

```php
<?php  
	// 引号的问题
    /**
     * 1、双引号，可以包裹字符串和变量，变量会自行替换
     * 2、单引号，只能包裹字符串
     * 3、反引号，用于执行操作系统命令并返回结果
     */
    $name = "ymqyyds";
    echo "$name 为事实<br>";
    echo '$name 为事实<br>';
    echo `ipconfig`;
?>
```

![image-20240207142808304](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240207142808304.png)

### 6.编码格式

（1）header

这种方式虽然可以修改编码格式，但是会导致整个页面的编码格式全都被改变，从而导致其他内容又变成了乱码

```php
<?php
    $name = "ymqyyds";
    echo "$name 为事实<br>";
    echo '$name 为事实<br>';

    header("Content-type:text/html; charset='GBK'");
    echo `ipconfig`;
?>
```

![image-20240207143500107](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240207143500107.png)

（2）iconv

这种方法就可以在有需要的时候，对有需要的字符串进行转码就好了。

**传递参数：**

原本字符串的编码格式，想要转为哪一种编码格式，对那个字符串进行转码

```php
<?php
	$output = `ipconfig`;
    $output = iconv("GBK","UTF-8",$output);
    echo $output;
?>
```

![image-20240207144249364](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240207144249364.png)

## 二、变量

### 1.数据类型

```
String(字符串): "成都" "He11o"
Integer(整型):  12345  -200
Float(浮点型):  123.45  -12345.678
Boolean(布尔型):true    false
Array(数组):一组数据的集合
object(对象):
NULL(空值):
```



### 2.命名规范

```
变量以$符号开始，后面跟着变量的名称
变量名必须以字母或者下划线字符开始
变量名只能包含字母、数字以及下划线(A-z、0-9和)
变量名不能包含空格
变量名是区分大小写的(sy 和 sY 是两个不同的变量)
变量名不能用中文全拼，最好使用英文单词
变量名不能用无意义的简写，WB，XY，但是常规的简写是可以的，htm1，css，js，mp4
的数名必须使用动词或动名词形式
变量名或函数或等，首字母小写，如果有多个单词，第二单词的首字母建议大写:checkNumber，check_number
```



## 三、运算符

### 1.算数运算符

| 运算符 | 名称             | 描述                                                         | 实例                         | 结果  |
| :----- | :--------------- | :----------------------------------------------------------- | :--------------------------- | :---- |
| x + y  | 加               | x 和 y 的和                                                  | 2 + 2                        | 4     |
| x - y  | 减               | x 和 y 的差                                                  | 5 - 2                        | 3     |
| x * y  | 乘               | x 和 y 的积                                                  | 5 * 2                        | 10    |
| x / y  | 除               | x 和 y 的商                                                  | 15 / 5                       | 3     |
| x % y  | 模（除法的余数） | x 除以 y 的余数                                              | 5 % 2 10 % 8 10 % 2          | 1 2 0 |
| -x     | 设置负数         | 取 x 的相反符号                                              | `<?php $x = 2; echo -$x; ?>` | -2    |
| ~x     | 取反             | x 取反，按二进制位进行"取反"运算。运算规则：`~1=-2;    ~0=-1;` | `<?php $x = 2; echo ~$x; ?>` | -3    |
| a . b  | 并置             | 连接两个字符串                                               | "Hi" . "Ha"                  | HiHa  |

### 2.比较运算符

比较操作符可以让您比较两个值：

| 运算符  | 名称       | 描述                                           | 实例               |
| :------ | :--------- | :--------------------------------------------- | :----------------- |
| x == y  | 等于       | 如果 x 等于 y，则返回 true                     | 5==8 返回 false    |
| x === y | 绝对等于   | 如果 x 等于 y，且它们类型相同，则返回 true     | 5==="5" 返回 false |
| x != y  | 不等于     | 如果 x 不等于 y，则返回 true                   | 5!=8 返回 true     |
| x <> y  | 不等于     | 如果 x 不等于 y，则返回 true                   | 5<>8 返回 true     |
| x !== y | 不绝对等于 | 如果 x 不等于 y，或它们类型不相同，则返回 true | 5!=="5" 返回 true  |
| x > y   | 大于       | 如果 x 大于 y，则返回 true                     | 5>8 返回 false     |
| x < y   | 小于       | 如果 x 小于 y，则返回 true                     | 5<8 返回 true      |
| x >= y  | 大于等于   | 如果 x 大于或者等于 y，则返回 true             | 5>=8 返回 false    |
| x <= y  | 小于等于   | 如果 x 小于或者等于 y，则返回 true             | 5<=8 返回 true     |

### 3.逻辑运算符

| 运算符   | 名称 | 描述                                         | 实例                                 |
| :------- | :--- | :------------------------------------------- | :----------------------------------- |
| x and y  | 与   | 如果 x 和 y 都为 true，则返回 true           | x=6 y=3 (x < 10 and y > 1) 返回 true |
| x or y   | 或   | 如果 x 和 y 至少有一个为 true，则返回 true   | x=6 y=3 (x==6 or y==5) 返回 true     |
| x xor y  | 异或 | 如果 x 和 y 有且仅有一个为 true，则返回 true | x=6 y=3 (x==6 xor y==3) 返回 false   |
| x && y   | 与   | 如果 x 和 y 都为 true，则返回 true           | x=6 y=3 (x < 10 && y > 1) 返回 true  |
| x \|\| y | 或   | 如果 x 和 y 至少有一个为 true，则返回 true   | x=6 y=3 (x==5 \|\| y==5) 返回 false  |
| ! x      | 非   | 如果 x 不为 true，则返回 true                | x=6 y=3 !(x==y) 返回 true            |

### 4.赋值运算符

在 PHP 中，基本的赋值运算符是 **=**。它意味着左操作数被设置为右侧表达式的值。也就是说，**$x = 5** 的值是 5。

| 运算符 | 等同于    | 描述                           |
| :----- | :-------- | :----------------------------- |
| x = y  | x = y     | 左操作数被设置为右侧表达式的值 |
| x += y | x = x + y | 加                             |
| x -= y | x = x - y | 减                             |
| x *= y | x = x * y | 乘                             |
| x /= y | x = x / y | 除                             |
| x %= y | x = x % y | 模（除法的余数）               |
| a .= b | a = a . b | 连接两个字符串                 |



## 四、分支语句

### 1.if...else...

和C语言是一样的

```php
<?php
$t=date("H");
if ($t<"20") {
   echo "Have a good day!";
   }
else {
   echo "Have a good night!";
   }
?>
//判断当前时间的小时数是否在晚上八点以前或之后
```



### 2.多重分支

```php
<?php 
$t=date("H"); 
if ($t<"10") { 
    echo "Have a good morning!"; 
} 
elseif ($t<"20") { 
    echo "Have a good day!"; 
} 
else { 
    echo "Have a good night!"; 
} 
?> 
// 判断当前时间的小时数
// else if 的判断是要基于上一条判断结果不满足的前提才行
```



### 3.switch...case

```php
<?php
$favcolor="red";
switch ($favcolor)
{
case "red":
    echo "你喜欢的颜色是红色!";
    break;
case "blue":
    echo "你喜欢的颜色是蓝色!";
    break;
case "green":
    echo "你喜欢的颜色是绿色!";
    break;
default:
    echo "你喜欢的颜色不是 红, 蓝, 或绿色!";
}
?>
```



## 五、循环语句

### 1.for循环

```php
for (初始值; 条件; 增量)
{
    要执行的代码;
}
初始值：主要是初始化一个变量值，用于设置一个计数器（但可以是任何在循环的开始被执行一次的代码）。
条件：循环执行的限制条件。如果为 TRUE，则循环继续。如果为 FALSE，则循环结束。
增量：主要用于递增计数器（但可以是任何在循环的结束被执行的代码）。
```

```php
<?php
    for($a=1;$a<=10;++$a) {
        echo date("Y-m-d H:i:s")."<br>";
    }
?>
```





### 2.while循环

- **while** - 只要指定的条件成立，则循环执行代码块

- **do...while** - 首先执行一次代码块，然后在指定的条件成立时重复这个循环

  - ```php
    $i=10;
    do {
        echo date("Y-m-d H:i:s")."<br>";
    } while ($i>5) {
        echo date("Y-m-d H:i:s")."<br>";
        --$i;
    }
    ```

- **for** - 循环执行代码块指定的次数

- **foreach** - 根据数组中每个元素来循环代码块

循环中的break和continue用法和效果和C语言是一样的

```php
<?php
    $a = 1;
    while($a < 10) {
        echo "<br>";
        echo date("Y-m-d H:i:s");
        $a++;
    }
?>
```

这里有一个问题，下面代码是有bug的

```php
<?php
    $s = date("s");
	while($s < 30) {
        echo date("Y-m-d H:i:s")."<br>";
        $s = date("s");
        sleep(1);
}
?>
//为什么该代码最终无法得到我们想要的结果，即每一秒输出一次,而是知道循环结束，才将所有结果输出
```

> 这段代码之所以无法实现每秒输出一次的目标，而是等到循环结束后一次性输出所有结果，是由于输出被缓冲导致的。
>
> PHP默认情况下会对输出进行缓冲，即将所有输出先存储在缓冲区中，等到达到一定条件（如缓冲区满、脚本结束）时再将缓冲区的内容一次性输出。这就是为什么在循环结束之前，你看不到任何输出。
>
> 要解决这个问题，你可以使用`ob_flush()`和`flush()`函数来立即刷新缓冲区并将内容输出到浏览器。修改后的代码如下：
>
> ```php
> <?php
>     $s = date("s");
>     while($s < 30) {
>         echo date("Y-m-d H:i:s")."<br>";
>         $s = date("s");
>         ob_flush();
>         flush();
>         sleep(1);
>     }
> ?>
> ```
>
> 使用`ob_flush()`和`flush()`函数会立即将缓冲区中的内容输出到浏览器，使得每一次循环的结果可以立即显示。
>
> 请注意，有些服务器环境可能会关掉缓冲机制，这样就不需要额外的刷新方法。此外，由于使用`flush()`函数会将缓冲区的内容强制输出到浏览器，因此可能会影响性能。所以，请谨慎使用这些方法并根据实际情况进行选择。
>
> > `ob_flush()` 是 PHP 中的一个输出缓冲区函数，它用于立即将输出缓冲区中的内容发送到客户端。具体来说，`ob_flush()` 函数会清空当前输出缓冲区并立即发送其中的内容到浏览器。
> >
> > 在默认情况下，PHP 会将输出（例如 `echo` 或者 `print` 语句）存储在一个输出缓冲区中，直到缓冲区满、脚本结束或者通过调用 `ob_flush()` 来手动刷新，并将缓冲区中的内容发送给客户端。这样可以提高性能和整体响应时间。
> >
> > `ob_flush()` 函数在很多情况下都非常有用，特别是在需要确保即时显示输出内容时。例如，当需要在循环中逐步输出结果或者长时间运行脚本时，使用 `ob_flush()` 可以确保部分输出内容及时显示在浏览器中。
> >
> > 需要注意的是，`ob_flush()` 函数只会刷新当前输出缓冲区，如果有多个输出缓冲区（通过 `ob_start()` 函数进行的配置），你可能需要在每个缓冲区上分别调用 `ob_flush()` 来进行刷新。
> >
> > 总之，`ob_flush()` 函数在需要立即将输出发送到浏览器，确保结果尽快显示给用户的情况下非常有用。



具体信息还请看[PHP 教程 |菜鸟教程 (runoob.com)](https://www.runoob.com/php/php-tutorial.html)

