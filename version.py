from exerciseRegister.checkregcommon import check_username,check_password,check_phone

# username = ''
# password = ''
# phone = ''

def input_username():
    # global username
    username = input('请输入用户名:')
    if check_username(username):
        print('用户名正确')
        return username
    else:
        print('用户名错误')
        input_username()

def input_password():
    # global password
    password = input('请输入密码:')
    if check_password(password):
        print('密码输入正确')
        return password
    else:
        print('密码输入错误')
        input_password()

def input_phone():

    # global phone
    phone = input('请输入电话号码:')
    if check_phone(phone):
        print('电话号码输入正确')
        return phone
    else:
        print('电话号码输入错误')
        input_phone()

def do_reg():
    username = input_username()
    password = input_password()
    phone = input_phone()

    userlist = []
    user = {'username': username, 'password': password, 'phone': phone}
    userlist.append(user)
    print(user)


if __name__ == '__main__':
    do_reg()
    print('登录成功')