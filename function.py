# Python中的函数和参数的用法
# 函数的构成
# 1.函数名（必须有，且在同一作用范围中不允许重复）
# 2.参数（可以没有），遵守标准的命名规范
# 3.返回值（可以没有），如果没有返回值，则返回为None

def test_01():
    print("这是一个没有参数的函数")

def test_02(a, b):
    result = a+b
    print(result)

def test_03(a, b):
    result = a+b
    return result

def test_04(fun, a, b):
    print(fun(a, b))
    print('helloymqyyds')

# test_01()  #这是一个没有参数的函数
# print(test_01())  #这是一个没有参数的函数  None

# test_02(1, 2)  # 3
# print(test_03(4, 5))  # 9

# x = test_04  #将 test_04 这个函数的内存地址赋值给 x
# print(x)  #输出test_04的内存地址  <function test_04 at 0x0000026EA53E5A80>
# print(type(x))  # 输出x的类型 <class 'function'> 表明是函数类型
# x()  # 调用 test_04 这个函数   helloymqyyds

# test_04(test_03, 4, 5)  # 函数作为参数传参

# source = "helloymqyyds"
# print(type(source))  # <class 'str'>
# print(id(source))  # 2984262554032
# print(hex(id(source)))  # 0x1685ed8d1b0  这就是这个字符串在python运行环境中的内存地址，每次运行的结果都是不一样的

'''
Python里面的参数分为以下四种：
1.必须参数（位置参数：positional argument）
2.默认值参数（定义形参时，可以设置一个默认值）
3.可变长参数，可选参数，必须加 * 号说明
4.字典参数，关键字参数，在可变长参数之后，还可以定义字典参数，必须加 ** 说明
# 函数定义和传参时的顺序，按照给定的 1 2 3 4 顺序传参
'''
def test_argus_01(a, b, c=100):
    result = a * b + c
    print(result)
#
# test_argus_01(10,10)  # 200
# test_argus_01(10,10,200)  #300
# test_argus_01(c=100, a=10, b=20)  #在传参时，直接指定参数名称和值，可以不用考虑参数位置（推荐该用法）

def test_args_02(a, b, c=10, d=20, *args):
    result = a * b + c * d
    print(result)
    print(args)  #可变长参数，是以元组的形式存在
    print(*args)  #在元组或列表前添加 * ，表示将数据展开
#
# test_args_02(10, 20)  # 400 () 这玩意看着挺像元组的
# test_args_02(10, 20, 5, 5)  # 225 ()
# test_args_02(10, 20, 5, 5, 6)  # 225 (6,)  6
# test_args_02(10, 20, 5, 5, 6, 7, 8)  # 225   (6, 7, 8)    6 7 8
# 从上面我们清楚的看到，传参是严格按照顺序传参的，且可变长参数args原来是一个元组，我们传参时就相当于是把数字传给了 *args 然后这个原本就是元组的展开形式，去掉 * 之后又恢复成了元组

def test_args_03(a, b, c=10, d=20, *args, **kwargs):
    result = a * b + c * d
    print(result)
    print(args)
    print(kwargs)


# test_args_03(10, 20, 6, 6, 7, 8, 9)  # 236   (7, 8, 9)  {}
# test_args_03(10, 20, 6, 6, 7, 8, 9, name='ymq',age=20)  # 236   (7, 8, 9)  {'name': 'ymq', 'age': 20}
# 从上面可以看出，多出的数字参数依旧是传给了可变长参数（即元组），只有真正字典型的参数才会传给 **kwargs,而且在后面的参数中千万不要会和前面的参数名重复

# 通常情况下，自定义函数，并且不需要交由第三方调用时，或者不考虑各类复杂场景时，位置参数和默认参数足够了
# 如果需要将函数交由其他用户调用，或开发的是一套框架，需要考虑各种复杂调用的情况或参数不确定，此时加上可变参数和字典参数
