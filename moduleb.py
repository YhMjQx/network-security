import modulea
# 需要注意的是，注意不要循环导入，不要在A中导入B，在B中导入A

# 导入到 模块级 ，调用时使用 模块.函数 的方式进行调用
modulea.test_01()  # 这是一个没有参数的函数 source = Hello ymq-yyds
print('')

print('source = %s' % modulea.source)  # 模块级变量在模块被导入之后直接使用  输出 source = 模块级变量
print('')

modulea.test_02(1,2)  # 3  Hello Module-variable
print('')

print(modulea.source)  # Hello Module-variable
print('')

modulea.test_03(1, 2)
print('')

# 导入模块的方法
# 当导入一个模块时，事实上是将模块的源代码执行了一遍

# 通过 from...import...导入到函数级，那么直接在代码中调用函数即可
from modulea import test_01
test_01()
from random import choice
print(choice([1,2,3,4,5]))
print('')

# 通常情况下，在同一个包下，可以不需要在导入时明确声明包名，但是，建议在任何时候都把包名加上
# 直接使用 import 只能导入到模块级，不能到函数或类级,使用方法如下
import basic.modulea
print(basic.modulea.source)
print('')

from basic import modulea
print(modulea.source)
print('')

#如果要直接导入到函数级或类级，则必须使用 from...import...
from basic.modulea import test_01
test_01()
print('')
