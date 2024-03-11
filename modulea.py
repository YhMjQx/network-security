# 定义一个模块机变量（直接隶属于当前模块，与函数和类同级，可以被其他函数直接引用）
source = '模块级变量'
list = [1, 2, 3, 4, 5, 6]

def test_01():
    print("这是一个没有参数的函数")
    source = 'Hello ymq-yyds'  # 在函数体内修改 模块级变量其实就是新定义了一个局部变量而已，事实上真正的模块级变量还没变
    print('source = %s' % source+'nb')  # 这里输出的也仅仅只是函数体内定义的局部变量

def test_02(a, b):
    result = a+b
    print(result)

    global source  # 要想在函数体内修改模块级变量并且使用修改过后的值需要定义一下该变量是 global 的局部变量
    source = 'Hello Module-variable'
    print(source)

def test_03(a, b):
    result = a+b
    list.append(777)  # 模块级变量 list 可以直接访问，可以直接修改
    print(list)
    return result

# print(__name__)  # 如果该模块被别的代码导入，则该代码输出的是该模块的真实名称，也就是 modulea

# 为了防止别的模块在导入时重复执行函数调用的代码，必须添加一个判断:
# __name__ 和 __main__ 都是魔术变量，
# 其本质就是确保该判断只会在该模块中调用和运行
if __name__ == '__main__':
    test_01()
    print(test_01.__name__)  # 该函数的__name__就是test_01
    print(__name__)  # 当在当前模块中打印 __name__ 魔术变量时，其值为 __main__

