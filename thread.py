# 并发操作，如果一个单核的CPU，是不存在严格意义的并发，只是因为处理时间极短，所以感觉上是并发操作的
# 针对多核CPU。比如 四核CPU。严格意义上的并发处理就是四个

# 线程和进程
# 1、每一个应用程序都至少会有一个进程，并且有PID和独立的内存空间
# 2、每一个进程至少拥有一个线程，而线程并没有独立的内存空间

# 要使用线程就引用模板库 threading
import threading,time,requests,random

session = requests.session()

# 定义一个装饰器，查看每一个线程的时间
def performance(fun):
    def inner():
        start = time.time()
        fun()
        end = time.time()
        print(f'执行{fun.__name__}所使用的时间为：{end-start}')
    return inner

# 这一个函数就对应了一个线程

def test_01():
    print(threading.current_thread().name)
    for i in range(0,5):
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(1)


def test_02():
    print(threading.current_thread().name)  # 获取线程对象的name属性
    print(time.strftime('%Y-%m-%d %H:%M:%S'))  # 格式化输出时间
    time.sleep(1)

@performance
def home():
    resp = session.get("http://192.168.230.147:8080/woniusales/")
    if '成都蜗牛创想科技' in resp.text:
        print('首页访问成功')
    else:
        print('首页访问失败')

@performance
def login():
    data = {'username': 'admin', 'password': 'admin123', 'verifycode': '0000'}
    resp = session.post(url="http://192.168.230.147:8080/woniusales/user/login", data=data)
    if resp.text =='login-pass':
        print('登录系统成功')
    else:
        print('登录系统失败')

@performance
def add_vipuser():
    # random.randint(300000000,900000000) 的意思是从 300000000 到 900000000 中选取一个整数
    data = {'customername':'你爸爸','customerphone':f'13{random.randint(300000000,900000000)}','childsex':'男','childdate':'2024-04-01','creditkids':'9','creditcloth':'9'}
    resp = session.post(url='http://192.168.230.147:8080/woniusales/customer/add',data=data)
    if resp.text == 'add-successful':
        print('添加用户成功')
    else:
        print('添加用户失败')

# 基于HTTP协议，进行流量泛洪，压力测试，性能测试
# @performance
def woniusales_flood_01():
    for i in range(0,1000):
        home()
        login()
        add_vipuser()

if __name__ == '__main__':
    # 的那个python执行时，虽然没有手工启动线程，默认python会启动一个主线程。
    # test_01()  # 单次调用就相当于只开启了一个线程
    # for i in range(0,5):
    #     test_02()  # 但是即使只是这样多次调用同一个函数，他们使用的线程还是一样的，都是 MainThread
    # 那我们该如何开启多线程呢，看下面的for循环
    # for i in range(0,5):
    #     # 实例化一个线程，并且制定调用test_02这个函数，然后启动线程
    #     t = threading.Thread(target=test_02)  # threading.Thread(target=test_02,args=()) 通过args元组可以给test_02这个函数传参
    #     t.start()

    for i in range(0,1000):
        threading.Thread(target=woniusales_flood_01).start()

