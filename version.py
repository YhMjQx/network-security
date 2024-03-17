from exercise.common import *

# username = ''
# password = ''
# phone = ''

def input_username():
    # global username
    username = input('请输入用户名:')
    if check_username(username):
        if is_user_exists(username):
            print('你输入的用户名已存在')
            return input_username()
        else:
            print('用户名正确')
            return username
    else:
        print('用户名错误')
        return input_username()
# 在循环调用函数时加上 return 是为了防止再次输入密码时没有返回结果使得最终的结果变成了None

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

def do_login():
    username = input('请输入用户名：')
    password = input('请输入密码：')
    user = check_and_get_user(username)
    if user is None:
        print('用户名不存在')
        exit(0)
    elif user['password'] == password:
        print('用户名密码正确，登录成功')
    else:
        print('登录失败')

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


def draw_menu():
    print('*=*=*=*=*=*=* 欢迎使用用户管理系统 *=*=*=*=*=*=*')
    print('*=*=* 1.注册  2.登录  3.修改密码  4.退出 *=*=*=*')
    option = input('请选择您的操作[1 2 3 4]:')
    if option == '1':
        do_reg()
        draw_menu()
    elif option == '2':
        do_login()
        draw_menu()
    elif option == '3':
        do_change_password()
    elif option == '4':
        print('退出系统')
        exit(0)
    else:
        print('请输入正确的选项: ')
        draw_menu()



if __name__ == '__main__':
    # do_reg()
    # print('注册成功')
    # do_login()
    # do_change_password()
    draw_menu()
