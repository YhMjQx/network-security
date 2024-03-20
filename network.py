import socket

# 定义一个客户端
def test_Client():
    # 建立与服务器的连接
    s = socket.socket()  # 以类实例的方式，默认使用TCP协议
    s.connect(('192.168.230.130',554))  # 传了一个元组作为参数，元组中的元素分别是服务器ip地址和服务器端口号

    # 传输数据（收发数据包）
    content = 'Welcome to ymq world '
    s.send(content.encode())
    # content = 'Welcome to ymq world 这是我的世界哦耶'
    # s.send(content.encode('gbk'))

    # 关闭连接
    s.close()

# 定义一个服务器端
def test_Server():
    s = socket.socket()  # 建立Socket连接对象
    s.bind(('192.168.1.178',555))  # 绑定服务器端ip地址和端口
    s.listen()  # 监听 555 端口号流量情况
    while True:
        chanel,client = s.accept()  # 接收来自客户端发送的数据
        message = chanel.recv(1024)  # 接收数据的缓冲大小设置为1024
        print(client)  # 这是客户端信息
        print(message.decode())  # 打印接收到的数据（由于该数据在发送前是被编码过的，因此接收到之后也要被解码）

test_Server()
# test_Client()
