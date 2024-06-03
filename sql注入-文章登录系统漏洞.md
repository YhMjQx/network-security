[TOC]



# ==文章登录系统漏洞==

## 一、构建测试系统

```python
#login.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ymqyyds</title>
    <style>

        div {
            width: 310px;
            height: 75px;
            margin: auto;
        }

        .title {
            color: rgb(6, 255, 52);
            font-size: 30px;
            text-align: center;
            margin-top: 200px;
            padding-bottom: 10px;  /*和底部下一个容器相隔一点距离*/
            font-weight: bold;  /*加粗*/
            font-style: italic;  /*斜体*/
            
        }

        input {
            width: 300px;
            height: 50px;
            background-color: antiquewhite;
            border-radius: 5px;  /*让边框看起来圆润一点*/
            text-align: center;
            margin: auto;
        }

        button {
            width: 310px;
            height: 50px;
            background-color: fuchsia;
            color: chartreuse;
            font-size: 20px;
            font-weight: bold;  /*加粗*/
            font-style: italic;  /*斜体*/
            border-radius: 5px;  /*让边框看起来圆润一点*/
        }

        .footer {
            width: 500px;
            height: 50px;
            border: solid 0px blue;
            margin: auto;
            text-align: center;
            color: aliceblue;
        }

    </style>
</head>

<body background="./image/code.png" style="background-repeat: repeat;background-attachment:fixed;background-size:100%">

    <div class="title top-100 font-30">登 录</div>

    <form action="./login.php" method="post">
        <div class="login">
            <input type="text" name="username" />
        </div>
        <div class="login" >
            <input  type="password" name="password" />
        </div>
        <div class="login">
            <input type="text" name="vericode" />
        </div>
        <div class="login" >
            <button type="submit">登 录</button>
        </div>
    </form>

    <div class="footer top-100"> 
        版权所有@华明网络安全科技有限公司
    </div>

</body>
</html>
```

```php
# login.php
<?php
     //POST请求
    //需要将对应的html页面的请求方式method也改为post

    // 该登录操作没有进行爆破的防护，违背了OWASP-认证和授权失败
    $username = $_POST["username"];
    $password = $_POST["password"];
    $vcode = $_POST["vericode"]; 
    

    // 验证码登录 启用了万能验证码，存在安全漏洞 OWASP-认证和授权失败
    if ($vcode === '0000') {

        // 连接到数据库
        $conn = mysqli_connect('127.0.0.1','root','','woniunote',3306) or die("数据库连接失败");

        mysqli_set_charset($conn,'utf8');

        //拼接sql语句并执行
        $sql = "select * from users where username='$username' and password='$password'";
        $result = mysqli_query($conn,$sql);
        if (mysqli_num_rows($result) == 1) {

            echo "login-pass";
            echo '<script>location.href="./welcome.php"</script>';
        }
        else {
            echo "login-fail";
        }

        //关闭数据库
        mysqli_close($conn);

    }
    else {
        die("vericode-error");
    }

?>
```

```php
<?php

// 以下代码违背了 OWASP-失效的访问控制
echo '欢迎来到安全测试平台'

?>
```

## 二、系统存在漏洞

以上代码的漏洞漏洞：

- 登录操作没有进行爆破的防护，违背了OWASP-认证和授权失败（中）
- 验证码登录 启用了万能验证码，存在安全漏洞 OWASP-认证和授权失败（中）
- 登录页面可以进行SQL注入，进而轻易实现登录（高）
- welcome.php 违背了 OWASP-失效的访问控制 （中）
- ' 单引号测试中，数据库报错同时显示了 页面的绝对路径（低）
- 保存用户信息的数据表中，密码字段是明文保存的，不安全（中）

```
在登录页面输入一个单引号[']作为用户名,密码123456，验证码0000，响应如下:

<br />
<b>Warning</b>:  mysqli_num_rows() expects parameter 1 to be mysqli_result, bool given in <b>/opt/lampp/htdocs/security/login.php</b> on line <b>22</b><br />

<script>location.href="./welcome.php"</script>

上述报错信息隐含两个可能存在的漏洞：
1、' 可以成功引起SQL语句报错，说明后台没有专门对单引号进行处理
select * from users where username='$username' and password='$password'
正常情况：select * from users where username=''' and password='123456'
试探情况：select * from users where username=''' and password='123456'
攻击Payload：
username: x' or userid=1#
攻击情况：select * from users where username='x' or userid=1#' and password='123456'

2、在报错信息中暴露了敏感信息
/opt/lampp/htdocs/security/login.php 这是我们访问的界面在服务器中的绝对路径
```

> 以上payload其实只是遵循了注入类攻击的两个核心原则：
>
> 1、拼接为有效的语句或代码
>
> 2、确保完成了闭合，并且可以改变原有执行逻辑
>
> 由于通常情况下并不知道真实地字段名或者密等，需要不断尝试，但是手动尝试很慢，所以建议写一个python+字典脚本自动拼接进行快速处理

## 三、修复漏洞

### 1、sql注入payload测试

```python
import requests
# 利用python对php的登录页面进行Fuzz测试

def loginfuzz(target_url,fuzz_dict):

    fuzzdata = {'username':"'", 'password':'p-0p-0p-0', 'vericode':'0000'}
    resp = requests.post(target_url,fuzzdata)
    # print(resp.text)
    if 'Warning' in resp.text:
        print('本系统可能存在SQL注入漏洞，可以一试')
    with open(fuzz_dict,mode='r') as file:
        data = file.readlines()
        for fuzz_data in data:
            payload = {f'username':fuzz_data.strip(), 'password':'p-0p-0p-0', 'vericode':'0000'}
            resp = requests.post(target_url,payload)
            if 'login-fail' not in resp.text:
                print(f'登录成功，payload为{payload}')


if __name__ == '__main__':
    target_url = 'http://192.168.230.147/security/login.php'
    fuzz_dict = './sqldict.txt'
    loginfuzz(target_url,fuzz_dict)
```

### 2、修复welcome.php，防止任意登录

- 设置common.php，在该页面中开启session和函数create_dbconn

```php
<?php

session_start();

function create_dbcon() {
    $conn = mysqli_connect('127.0.0.1','root','','woniunote',3306) or die("数据库连接失败");

    mysqli_set_charset($conn,'utf8');

    return $conn;
}

function login_result($result) {
    echo '<script>window.alert("'.$result.'")</script>';
    echo '<script>location.href="./login.html"</script>';
}

?>
```

- **在login.php和welcome.php中include "common.php"**

```php
#在login.php页面中，当用户成功登录之后记录用户session信息
include "common.php"
if (mysqli_num_rows($result) == 1) {

    echo "login-pass";
    // 登录成功，则记录用户session信息
    $_SESSION['username'] = $username;
    $_SESSION['islogin'] = TRUE;

    echo '<script>location.href="./welcome.php"</script>';
}
#在welcom.php页面中，判断访问该页面的用户的session信息是否已经登录过
<?php

// 以下代码违背了 OWASP-失效的访问控制


include "common.php";

// 由于$_SESSION['islogin']变量没设置过，所以在部分情况下这种问题会报错，因此使用 isset()来判断该变量是否存在，如果该变量存在，再判断用户是否登录过
// isset() 判断变量是否存在，如果存在返回真，如果不存在返回假
if(!isset($_SESSION['islogin']) or $_SESSION['islogin'] != TRUE) {
    die('你还没有登录，无法访问本页面');
}

echo '欢迎来到安全测试平台</br>';
?>
```

### 3、修复报错信息中包含文件绝对路径

- 首先，搞明白暴露原因是因为sql语句拼接错误，然后在执行过程中暴露了错误
- 因此，我们可以采取解决办法，让SQL语句执行错误时按照我们在自己的想法输出错误信息，就类似于python中的 try + except，在js中我们使用die

```php
$sql = "select * from users where username='$username' and password='$password'";
$result = mysqli_query($conn,$sql) or die('SQL语句执行失败');
```

### 4、修复数据表中的用户信息，确保以密文的形式存储

**主要依据为php内置的md5()函数**

- 确保用户表中password字段的长度为32位，用以容纳md5哈希值

![image-20240531174926303](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240531174926303.png)

- 在插入用户信息时，先md5处理之后再插入用户信息

```php
$md5_password = md5($password);
$sql = "select * from users where username='$username' and password='$md5_password'";
```

### 5、修复SQL注入漏洞

#### 方案一：处理逻辑问题，**分开查询和判断用户名与密码**

> 用户名和密码的对比放在同一条SQL语句中存在很严重的逻辑问题
>
> 应先通过对用户名查询user表，如果确实找到一条记录（用户名唯一的情况下），找到记录后在进行密码的单独对比

```php
//拼接sql语句并执行
$md5_password = md5($password);
$sql = "select * from users where username='$username'";
$result = mysqli_query($conn,$sql) or die('SQL语句执行失败');
if (mysqli_num_rows($result) == 1) {

    $row = mysqli_fetch_assoc($result);
    if($md5_password == $row['password']) {
        // echo "login-pass";
        echo '<script>window.alert("login-pass")</script>';
        // 登录成功，则记录用户session信息
        $_SESSION['username'] = $username;
        $_SESSION['islogin'] = TRUE;

        echo '<script>location.href="./welcome.php"</script>';
    }
    else {
        $_SESSION['islogin'] = FALSE ;
        login_result('login-fail');
    }

}
else {
    // echo "login-fail";
    $_SESSION['islogin'] = FALSE ;
    login_result('login-fail');
}
```

> 我们来看一下，`mysqli_fetch_assoc`，`mysqli_fetch_all`，`mysqli_fetch_row` 三者的区别
>
> - `$row = mysqli_fetch_assoc($result); var_dump($row);`
>   - 对SQL查询的结果集处理之后的结果，是关联数组
>
> ![image-20240602153033714](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20240602153033714.png)
>
> - `$row = mysqli_fetch_all($result); var_dump($row);`
>   - 对SQL查询的结果集处理之后的结果，默认是索引数组，参数MYSQLI_NUM代表的也是这个
>
> ![image-20240602153526149](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20240602153526149.png)
>
> - `$row = mysqli_fetch_all($result,MYSQLI_ASSOC); var_dump($row);`
>   - 对SQL查询的结果集处理之后的结果乃是索引 + 关联数组
>
> ![image-20240602153739572](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20240602153739572.png)
>
> - `$row = mysqli_fetch_row($result); var_dump($row);`
>   - 对SQL查询的结果集处理之后的结果是索引数组
>
> ![image-20240602154156697](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20240602154156697.png)

#### 方案二：函数 `addslashes()` 

**可以将字符串中的单引号、双引号、反斜杠、NULL值自动添加转义符，从而防止SQL注入中对单引号和双引号的预防。**

```php
$username = addslashes($_POST["username"]);
```

> ```
> 原始SQL语句如下:
> $sgl = "select * from user where username='$username' and password='$password'";
> 如果用户输入 x'or userid=1#' 则SQL语句变成:
> $sgl = "select * from user where username='x' or userid=1#" and password='$password'";
> 如果使用addslashes强制为用户输入添加转义符，则变成:
> $sgl = "select * from user where username='x' or userid=1#\" and password='$password'";
> 上述SQL语句的用户名为:x\' or userid=1#\'，密码为$password，逻辑上保持不变
> 如果直接输入 \ ，则如下：
> $sgl= "select * from user where username='\' and password='$password"
> ```

## 四、mysqli面向对象的与处理方式修复SQL注入

- **面向过程方式**

```php
# 面向过程创建数据库连接
function create_dbcon() {
    $conn = mysqli_connect('127.0.0.1','root','','woniunote',3306) or die("数据库连接失败");
    mysqli_set_charset($conn,'utf8');
    return $conn;
}

# 面向过程执行和处理SQL查询
$sql = "select * from users where username='$username'";
$result = mysqli_query($conn,$sql) or die('SQL语句执行失败'); 
$row = mysqli_fetch_assoc($result);
```

- **面向对象方式**

```php
// 面向对象创建数据库连接
function create_dbconn_oop() {
    $conn = new mysqli('192.168.230.147','root','p-0p-0p-0','woniunote',3306) or die("数据库连接失败");
    // $conn->query('set names utf8');
    $conn->set_charset('utf8');
    return $conn;
}

// 执行SQL语句
function exec_sql_oop($sql) {
    $conn = create_dbconn_oop();
    $result = $conn->query($sql);
    // 获取行数
    // echo $result->num_rows;

    $rows = $result->fetch_all(MYSQLI_ASSOC);
    // var_dump($rows);  // 展示所有处理后的结果集内容

    foreach ($rows as $row) {
        echo "username : " . $row['username'] . " , password : " . $row['password'] . "</br>";
    }
}

exec_sql_oop('select * from users where userid < 6;');
```

### 1、mysqli预处理功能

```php
// MySQLi的预处理功能
// 主要思想：先用 ? 代替要传的参数，然后绑定参数时传入参数，随后执行
// 更新类操作：直接执行即可，无需后续操作
function myself_mysqli_prepare_update() {
    // 首先创建数据库连接对象
    $conn = create_dbconn_oop();
    // 创建预处理语句
    $updatesql = "update users set username = ? where userid = ?;";
    // 实例化预处理对象
    $stmt = $conn->prepare($updatesql);
    // 设置执行参数
    $username = '??????';
    $userid = 9;
    // 绑定结果参数
    $stmt->bind_param('si',$username,$userid);
    // 正式执行SQL语句
    $stmt->execute(); // execute()方法返回一个布尔类型，表示执行成功与否
    // $conn->commit(); // 默认情况下，更新类操作会自动提交

}

// 查询类操作：查询完成后需绑定结果参数，即：查询的什么列名，结果参数就是什么，数量一定要对上
function myself_mysqli_prepare_query() {
    // 创建数据库连接对象
    $conn = create_dbconn_oop();
    // 创建预处理语句
    $querysql = "select * from users where userid < ?;";
    // 实例化预处理对象
    $stmt = $conn->prepare($querysql);
    // 设置执行参数
    $userid = 6;
    // 绑定参数
    $stmt->bind_param("i", $userid);
    // 绑定结果参数
    $stmt->bind_result($userid,$username,$password,$nickname,$avatar,$qq,$role,$credit,$createtime,$updatetime);
    // 执行查询语句
    $stmt->execute();
    // 调用结果并进行处理
    $stmt->store_result();
    // 输出行数
    // $stmt->affected_rows();
    $stmt->num_rows()."</br>";
    // 遍历结果
    while ($stmt->fetch()) {
        echo $userid . ' ',$username . ' ',$password . '</br>';
    }

}
```

### 2、mysqli修复SQL注入漏洞

```php
<?php

    include "common.php";
     //POST请求
    //需要将对应的html页面的请求方式method也改为post

    // 该登录操作没有进行爆破的防护，违背了OWASP-认证和授权失败
    $username = $_POST["username"];
    $password = $_POST["password"];
    $vcode = $_POST["vericode"]; 
    

    // 验证码登录 启用了万能验证码，存在安全漏洞 OWASP-认证和授权失败
    if ($vcode === '0000') {

        // 连接到数据库
        $conn = create_dbconn_oop();
        $sql = 'select userid,username,password,role from users where username = ?;';
        $stmt = $conn->prepare($sql);
        $stmt->bind_param('s',$username);
        $stmt->bind_result($userid,$username2,$password2,$role);
        $stmt->execute() or die('SQL语句执行失败');
        $stmt->store_result();
        
        if ($stmt->num_rows == 1) {
            $md5_password = md5($password);
            $stmt->fetch();
            if($md5_password == $password2) {
                // echo "login-pass";
                echo '<script>window.alert("login-pass")</script>';
                // 登录成功，则记录用户session信息
                $_SESSION['username'] = $username;
                $_SESSION['islogin'] = TRUE;

                echo '<script>location.href="./welcome.php"</script>';
            }
            else {
                $_SESSION['islogin'] = FALSE ;
                login_result('login-fail');
            }

        }
        else {
            // echo "login-fail";
            $_SESSION['islogin'] = FALSE ;
            login_result('login-fail');
        }

        //关闭数据库
        mysqli_close($conn);

    }
    else { 
        // die("vericode-error");
        login_result('vericode-error');

    }
     
?>
```


配置MySQL临时日志查看预处理之后的SQL语句

在MySQL数据库中运行以下语句，开启临时日志，将日志信息保存到表格MySQL数据库的general_log表中

```sql
#开启
USE mysql;
SET GLOBAL log_output = 'TABLE';
SET GLOBAL general_log = 'ON';
#确认
SHOW VARIABLES LIKE "general_log";
```

并通过执行以下语句进行查询确认

```sql
SELECT * FROM general_log WHERE argument LIKE '%username%' ORDER BY thread_id DESC LIMIT 10;
```

> 正常情况下，general_log是默认关闭的
>
> ![image-20240602163253585](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240602163253585.png)
>
> 然后执行对应的SQL语句开启
>
> ![image-20240602163857085](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240602163857085.png)
>
> database : mysql ; table : general_log ;

**MySQLi的与处理功能同样支持面向过程和面向对象**

在处理mysql连接过程中遇到两个问题

```
$conn = mysqli_connect('localhost','root','','woniunote',3306) or die("数据库连接失败");
和
$conn = mysqli_connect('127.0.0.1','root','','woniunote',3306) or die("数据库连接失败");
和
$conn = mysqli_connect('192.168.230.147','root','p-0p-0p-0','woniunote',3306) or die("数据库连接失败");
三者可以正确连接数据库
但是
$conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote',3306) or die("数据库连接失败");
和
$conn = mysqli_connect('127.0.0.1','root','','woniunote',3306) or die("数据库连接失败");
和
$conn = mysqli_connect('192.168.230.147','root','p-0p-0p-0','woniunote',3306) or die("数据库连接失败");
三者无法正确连接数据库

意思是本地连接不能用密码（这个我不理解），远程连接数据库必须要用密码（这个我理解）
```

