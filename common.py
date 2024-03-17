import re
'''
用户名的规则:
长度为5-12位，使用 len 函数进行判断
且不能以数字开头 username[0] 不能是 0-9 的范围
只能是大小写字母或数字
'''

def check_username(username):
    if len(username) < 5 or len(username) > 12:
        return False

    if username[0] >= '0' and username[0] <= '9':
        return False

    for char in username:
        if not ((ord(char) in range(65,91)) or (ord(char) in range(97, 123)) or (ord(char) in range(48,58))):
        # if not ((char >= 'A' and char <= 'Z') or (char >= 'a' and char <= 'z') or (char >= '0' and char <= '9')):
            return False

    return True

# 使用半自动测试代码进行用户名单元测试
# print(check_username('ymqyyds'))  # True
# print(check_username('ymq6'))  # False
# print(check_username('6aymqyyds'))  # False

'''
密码的规则：
密码必须且只能由字母大小写和数字组成：至少有一位是大写，至少一位小写，至少一位数字   
长度为6~15位
'''
def check_password(password):
    if not (len(password) >= 6 and len(password) <= 15):
        return False

    lower = 0
    upper = 0
    digital = 0
    other = 0
    for char in password:
        if ord(char) in range(65,91):  #  A - Z
            upper += 1
        elif ord(char) in range(97,123):  # a - z
            lower += 1
        elif ord(char) in range(48,58):  # 0 - 9
            digital += 1
        else:  # 其他特殊字符
            other += 1


    if lower < 1 or upper < 1 or digital < 1 or other >= 1:
        return False

    return True

'''
电话的规则：
1.必须以 1 开头
2.第二位必须是 3-9 
3.后面九位数都是数字
'''
def check_phone(phone):
    pattern = '^1[3-9]\d{9}$'
    if re.match(pattern,phone):
        return True
    else:
        return False



#使用全自动测试代码进行单元测试
def test_driver(func, expectarg, *args):
    actual = func(*args)
    if actual == expectarg:
        print("测试 %s 成功" % func.__name__)
    else:
        print("测试 %s 失败" % func.__name__)

# 动态读取csv文件，并将第一行作为key值
def read_csv(filepath, has_first_column = True):
    with open(filepath, 'r') as f:
        content = f.readlines()  # readlines() 将每一行作为一个字符串读出来并作为列表中的一个元素
        if not has_first_column:
            raise Exception('Your csv does not have first line be used to key')  # 抛出异常结束函数运行
            # return None
        key_line = content[0].strip().split(',')
        csv_list = []
        columnnum = len(key_line)
        for i in range(1,len(content)):
            line = content[i].strip()
            csv_dict = {}
            for j in range(0, columnnum):
                csv_dict[key_line[j]] = line.split(',')[j]
            csv_list.append(csv_dict)
    return csv_list

# 读取csv文件，并检查用户是否存在
def is_user_exists(username):
    user_list = read_csv('./user.csv')
    # print(user_list)
    # for i in range(0,len(user_list)):
    for user in user_list:
        if user['username'] == username:
            return True
    return  False

# 读取csv文件，并检查用户是否存在，如果存在则以字典形式返回该用户信息
def check_and_get_user(username):
    user_list = read_csv('./user.csv')
    # print(user_list)
    # for i in range(0,len(user_list)):
    for user in user_list:
        if user['username'] == username:
            return user
    return None

# 修改用户密码，修改一个CSV文件中的某一行中的某一列，不能直接使用文件（python中不存在直接使用文件爱你）
def change_password(username,newpassword):
    csv_list = read_csv('./user.csv')
    # print(csv_list)
    index = 0
    for user in csv_list:
        # print(user)
        if user['username'] == username:
            index = csv_list.index(user)
            break
    csv_list[index]['password'] = newpassword
    # print(csv_list)
    with open('./user.csv', mode='w') as f:
        f.write("username,password,phone\n")
        for user in csv_list:
            line = ''
            # print(user)
            line = f"{user['username']},{user['password']},{user['phone']}\n"
            line = line.replace(' ','').replace("'","")
            f.write(line)
            # for v in user.values():
            #
            #     print(v)



if __name__ == '__main__':  # 直接 main 然后回车就可以自动弹出这一行
    pass
    # change_password('hellosb','Ymq123yyds')
    # 用户名规则单元测试
    # test_driver(check_username, True, 'ymqyyds')
    # test_driver(check_username, False, 'ymq6')
    # test_driver(check_username, True, 'aymqyyd')
    # test_driver(check_username, True, 'yhmjqx')
    # test_driver(check_username, False, 'ymqyyds666ymq')
    # test_driver(check_username, False, 'sigeman*nre')

    #密码规则单元测试
    # test_driver(check_password, True, 'Woniu123')
    # test_driver(check_password, True, 'YhMjQx521134')
    # test_driver(check_password, False, 'nishizhensb')
    # test_driver(check_password, False, 'Woniu12345678978945613')
    # test_driver(check_password, False, 'Woniuxy')
    # test_driver(check_password, True, 'Woniu123')
    # test_driver(check_password, False, 'woniu123')
    # test_driver(check_password, False, 'Won#iu123')
    # test_driver(check_password, False, 'Won$iu123')

    # 电话规则单元测试
    # test_driver(check_phone, True, '13892696338')
    # test_driver(check_phone, False, '13892696')
    # test_driver(check_phone, False, '13892696338666')
    # test_driver(check_phone, True, '18710666870')
    # test_driver(check_phone, True, '13772816626')
    # test_driver(check_phone, False, '12892696338')
    # test_driver(check_phone, False, '53892696338')

    # print(is_user_exists('ymqyy'))
    # print(check_and_get_user('ymqyy'))
    # print(read_csv('./user.csv'))
    # with open('./user.csv','r') as f:
    #     content = f.readlines()
    #     print(content)
    # read_csv('./user.csv',has_first_column=True)
