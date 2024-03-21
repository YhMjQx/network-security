import socket

client_socket = socket.socket()
client_socket.connect(('192.168.230.130',6666))
while True:
    message = input('请输入要发送的消息：').encode()
    client_socket.send(message)

    recieve = client_socket.recv(10240).decode()
    print(f"收到来自服务器的回复：{recieve}")

# client_socket.close()
