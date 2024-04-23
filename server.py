import socket,requests,string
from Crypto.Cipher import AES
from binascii import a2b_hex
upper = string.ascii_uppercase
lower = string.ascii_lowercase

def decode_aes(source):
    key = 'todayiswonderful-123456789ABCDEF'.encode()
    mode = AES.MODE_CBC
    iv = b'0123456789ABCDEF'
    cryptos = AES.new(key=key,mode=mode,iv=iv)
    plain = cryptos.decrypt(a2b_hex(source))
    return plain.decode().strip()



def code_net_talk(ip):
    try:
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 6666))
        server_socket.listen()
        chanel, client = server_socket.accept()
        while True:
            print(client)

            if client[0] == ip:
                chanel.send('不允许登录'.encode())
                # print('不允许登录')
                server_socket.close()
                return False

            message = chanel.recv(1024).decode()
            print(f'收到来自客户端的消息：{message}')
            plain = decode_aes(message)
            print(f'解密之后结果为：{plain}')

            chanel.send('收到'.encode())
    except:
        print('出错了')
        server_socket.close()
        code_net_talk(ip)

def perform_operation(option):
    if option == '1':
        return "注册"
    elif option == '2':
        return "登录"
    elif option == '3':
        return "修改密码"
    elif option == '4':
        return "退出"
    else:
        return "你好"

def reg_log_talk():
    try:
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 6666))
        server_socket.listen()
        chanel, client = server_socket.accept()
        while True:
            print(client)

            if client[0] == ip:
                # chanel.send('不允许登录'.encode())
                print('不允许登录')
                server_socket.close()
                return False
            option = chanel.recv(1024).decode()
            print(option)
            result = perform_operation(option)
            print(f'客户端将进行{result}操作')
            chanel.send(result.encode())

    except:
        server_socket.close()
        reg_log_talk()

if __name__ == '__main__':
    ip = '10.0.0.1'
    code_net_talk(ip)
    # reg_log_talk()