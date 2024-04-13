# 面向对象的核心特点：
# 1、类与实例：类有属性和方法，是利用与调用属性和方法
# 2、封装：可以决定哪些属性和方法是公有的（public），私有的（private），受保护的（protected）
# 3、继承：子类继承父类所有可访问的方法和属性
# 4、多态：通常只有强类型编程语言（C#，C++，JAVA）才严格具备多态性，弱类型编程语言本身就体现为多态

from basic.db_oop import DB

# 类名建议大驼峰规则 StudyNetWork
class People:
    # 定义类属性
    subject = 'network_security'
    # name = ''
    # age = ''
    # addr = ''
    # nation = ''
    # degree = ''
    # subject = ''

    # 使用构造函数定义类属性并初始化实例
    def __init__(self,name='woniu',age='11',addr='chengdu',nation='china',degree='undergraduate',subject='network_security'):
        print('构造函数调用')
        self.name = 'ymq'
        self.age = 20
        self.addr = 'shaanxixian'
        self.nation = 'china'
        self.degree = 'undergraduate'
        self.subject = 'network_security'

    # 使用析构函数释放内存空间
    def __del__(self):
        print(f'{self.name}的析构函数调用')

    # 定义类方法
    def study(self):
        print(f'{self.name} is studying {self.subject}')

    def work(self):
        print(f'{self.name} is working {self.subject}')

    def tech(self,type):
        print(f'{self.name} is teching {type} subject')

    # 定义受保护的方法
    def _hello(self):
        print('hello by protacted')

    # 定义私有方法
    def __welcome(self):
        print('welcome is pricate')

    # 定义类魔术方法 - 比如当打印类时，变自动调用返回内容
    def __str__(self):
        return f'当前类的实例正在被打印，其内存地址为{hex(id(self))}'

    # 定义静态方法，直接使用类名而非实力调用的方法，静态方法常驻类的内存空间
    @classmethod
    def make_money(cls):
        print(f'{cls.__name__} by {cls.subject} make money')  # cls代表对类的本身的引用，self表示对实例的引用

class Man(People):
    name = 'woniu'
    # 也可重写父类的方法
    def study(self):
        print(f'{self.name} 正在学习')

    # 也可扩展父类没有的方法
    def drive(self):
        print(f'{self.name} 会开车')


if __name__ == '__main__':
    p1 = People(name='ymq',age='20',addr='xianyoudian',nation='汉',degree='undergraduate',subject='network_security')

    print(f'class People in {hex(id(People))}')
    print(f'p1 in {hex(id(p1))}')
    print(p1)  # 当前类的实例正在被打印，其内存地址为0x1cc658a1c50
    print(People)  # <class '__main__.People'>
    p1.study()
    p1.work()
    p1.tech('network_security')
    People.make_money()  #虽然p1也可以调用类的静态方法，但不建议，应该直接使用类直接调用
    p1._hello()  # 受保护的方法本类实例化可以调用
    #p1.__welcome()  # 私有方法本类实例化也无法调用

    m = Man()
    m.name='woniu'
    m.work()
    m._hello()  # 受保护的方法子类可以调用
    # m.__welcome() # 私有方法子类更没法调用
    m.study()
    m.drive()

    # db = DB()
    db = DB(type='dict')
    print(db.query('select username from users'))
