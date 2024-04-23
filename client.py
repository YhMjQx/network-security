import socket,string
from Crypto.Cipher import AES
from binascii import b2a_hex
from network.experiment.common import *
upper = string.ascii_uppercase
lower = string.ascii_lowercase

def enc_ase(source):
    # AES加密要对消息进行分组，AES支持分组长度为128 192 256 bit位，分别对应十六进制长度16 24 32
    # 但如果分组完之后最后一组长度不够就需要进行 补位
    # print(len(source.encode()))
    # print(source.encode())
    length = len(source.encode())
    if length % 16 == 0:
        add = 0
    else:
        add = 16 - length % 16
    source += ('\0' * add)

    # 定义密钥和偏移量，必须是16个字节，24个字节或32个字节
    # key = 'todayiswonderful'.encode()
    key = 'todayiswonderful-123456789ABCDEF'.encode()
    # 定义加密模式
    mode = AES.MODE_CBC
    # 定义偏移量
    iv = b'0123456789ABCDEF'  # 确保相同明文，相同密钥的加密结果也是不同的 16字节
    # 创实例化AES加密对象
    cryptos = AES.new(key=key,mode=mode,iv=iv)
    cipher = cryptos.encrypt(source.encode())  # 将source使用AES加密
    result = b2a_hex(cipher).decode()
    return result


def input_username():
    # global username
    username = input('请输入用户名:')
    if check_username(username):
        if is_user_exists(username):
            print('你输入的用户名已存在')
            return input_username()
        else:
            print('用户名校验正确')
            return username
    else:
        print('用户名校验错误')
        return input_username()
# 在循环调用函数时加上 return 是为了防止再次输入时没有返回结果使得最终的结果变成了None

def input_password():
    # global password
    password = input('请输入密码:')
    if check_password(password):
        print('密码输入正确')
        return password
    else:
        print('密码输入错误')
        return input_password()

def input_phone():
    # global phone
    phone = input('请输入电话号码:')
    if check_phone(phone):
        print('电话号码输入正确')
        return phone
    else:
        print('电话号码输入错误')
        return input_phone()

def do_reg():
    username = input_username()
    password = input_password()
    phone = input_phone()

    with open('./user.csv','a') as f:

        f.write(f"\n{username},{password},{phone}")
        print('恭喜你，注册成功')

def do_login(username=None, password=None):
    if username == None and password == None:
        username = input('请输入用户名：')
        password = input('请输入密码：')
    user = check_and_get_user(username)
    if user is None:
        print('用户名不存在')
        return False
    elif user['password'] == password:
        print('用户名密码正确，登录成功')
        return True
    else:
        print('登录失败')
        return False

def do_change_password():
    username = input('请输入用户名：')
    password = input('请输入旧密码：')
    user = check_and_get_user(username)
    if user is None:
        print('用户名不存在')
        exit(0)
    elif user['password'] == password:
        print('用户名密码正确',end=' ')
        newpass = input('请输入新密码：')
        if check_password(newpass):
            newpassword = newpass
            change_password(username,newpassword)
            print('密码修改成功')
    else:
        print('旧密码校验失败，请重新尝试')
        do_change_password()
        exit(0)


def code_net_talk():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 6666))
    try:
        while True:
            message = input('请输入要发送的消息：')
            cipher = enc_ase(message)
            client_socket.send(cipher.encode())

            receive = client_socket.recv(1024)
            print(f'收到来自服务器的消息：{receive.decode()}')
            if '不允许登录' == receive.decode():
                print('不允许登录')
    except:
        client_socket.close()

def reg_log_talk():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 6666))
    try:
        while True:
            print('*=*=*=*=*=*=* 欢迎使用用户管理系统 *=*=*=*=*=*=*')
            print('*=*=* 1.注册  2.登录  3.修改密码  4.修改密码 *=*=*=*')
            option = input('请选择您的操作[1 2 3 4]:')
            client_socket.send(option.encode())
            receive = client_socket.recv(1024).decode()
            print(f'收到来自服务器的消息：{receive}')
            if '注册' == receive:
                do_reg()
            elif '登录' == receive:
                do_login()
            elif '修改密码' == receive:
                do_change_password()
            elif '退出' == receive:
                print('退出系统')
                exit(0)
            else:
                print('请重新操作: ')
            if '不允许登录' == receive:
                print('不允许登录')
    except:
        client_socket.close()

def force():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 6666))
    try:
        while True:
            option = '2'
            client_socket.send(option.encode())
            receive = client_socket.recv(1024).decode()
            if '登录' == receive:
                with open('./usertest.txt',mode='r') as file:
                    user_list = file.readlines()
                with open('./passtest.txt',mode='r') as file:
                    pass_list = file.readlines()
                for username in user_list:
                    print(f'正在破解{username.strip()}')
                    for password in pass_list:
                        # print(password.strip())
                        if do_login(username.strip(),password.strip()):
                            print(f'疑似破解成功。用户名为{username.strip()},密码为{password.strip()}')
                            return True

    except:
        print('出错了')
        client_socket.close()
        force()


if __name__ == '__main__':
    # draw_menu()
    code_net_talk()
    # reg_log_talk()
    # force()