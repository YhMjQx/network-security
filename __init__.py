
# string1 = {'name':'张三','age':25,'sex':'男','phone':'192168230147'}
# print(string1['phone'])
#
# string2 = 'hello\nworld'
# string3 = '你好世界'
# print(string2)
# print(string3)
#
# print(string2,end=' ')
# print(string3)
#
# string4 = '这是我的学号：'
# # id = input("请输入学号")
# # print(string4 + id)
#
# id = 26221117
# print(string4 + str(id))
# print('%s%d' % (string4,id))
# print(f"{string4}{id}")
# print("{}{}".format(string4,id))
#
import random
#
# point = 123.456
# print("%.2f" % point)  #四舍五入
# print("{:.2f}".format(point))  #四舍五入
#
# #关于 进制 与 字符转换的运算
# #字符与ASCII码的转换
# print(ord('Y')) ; print(ord('M')) ; print(ord('Q'))
# print(ord('杨')) ; print(ord('明')) ; print(ord('强'))
# print(chr(89)) ; print(chr(77)) ; print(chr(81))
# print(chr(26472)) ; print(chr(26126)) ; print(chr(24378))
#
# #进制转换
# print(bin(99))  #0b1100011
# print(oct(99))  #0o143
# print(hex(99))  #0x63
# a = 0b00111100
# b = 0b10101010
# print(a&b)
# print(bin(a&b))  #0b101000
#
# #左移 << 相当于乘以2
# print(a)  #60
# print(a << 1)  #120  00111100 -> 1111000
# #右移 >> 相当与除以2
# print(a >> 1)  #30  00111100 -> 11110
#
# a = 10
# print(a << 1)  #1010 -> 10100
# print(a >> 1)  #1010 -> 101
# b=11
# print(b << 1)  #1011 -> 10110
# print(b >> 1)  #1011 -> 101
#
# #数值类型转换
# print(int(123.45))  #123
# print(int(123.55))  #123
# print(int(-123.456))  #-123
# print(round(123.556,2))  #124.56
# print(float(123456))  #123456.0
# print(float("123.45"))  #字符串转换为小数 123.45
# print(float('123.456'))  #字符串转换为 123.456
# print(int(float('123.45')))  #字符串转换为123.45并取整
#
# phone = 192168230147
# print('我的ip是' + str(phone))


#随机数
# r1 = random.randint(1,10)  #生成一个闭区间的随机数
# print(r1)
# r2 = random.randrange(1,10)  #左闭右开,第三个参数 step 为步长
# print(r2)
# r3 = random.randrange(1,10,2) #左闭右开且步长为2 即从 1 3 5 7 9 中进行寻找随机数
# print(r3)
# r4 = random.uniform(1.5,3.5)  #指定范围内的小数,无数个
# print(r4)
# r5 = random.choice("ABCDEFGHIJKLMNOPQRST")  #从字符串序列中随机选取一个值
# print(r5)
# r6 = random.choice([1,2,3,4,5,6,7,8,9])  #从列表序列中随机选取一个值
# print(r6)
# r7 = random.choice((1,2,3,4,5,6,7,8,9))  #从元组中随机选取一个值
# print(r7)

#字符串切片操作
# source = 'HelloWorld'
# print(source[2])  # l
# print(source[0:5])  #左闭右开 输出前5个字符  Hello
# print(source[1:])  #输出从第二个位置到最后   elloWorld
# print(source[:5])  #输出前五个字符  Hello
# print(source[-1])  #输出倒数第一个位置的字符  d
# print(source[1:-2])  #输出第二个位置到倒数第二个位置前的字符  elloWor
# print(source[0:5:2])  #从前5个位置中，以步长为2输出  Hlo
#
# #字符串内置方法
# print(source.count('l'))  #计算子字符串在源字符串中出现的次数
# print(len(source))  #计算源字符串的长度
#
# source = "zhang,san,li,si,wang,wu"
# print(source.split(','))  #按照分隔符将字符串分割，并将分割好的字符串组合为一个列表
# list = ['zhang', 'san', 'li', 'si', 'wang', 'wu']
# print('#'.join(list))  #将被分割的字符串按照给定的分隔符拼凑回来

#字符串编码和解码方法
source = "hello杨明强yyds999"
print(source)
print("UTF-8编码格式编码：",end='')
print(source.encode())  #encode方法将字符串按照指定的编码格式转换为字节类型，默认编码格式为 UTF-8
source = b'hello\xe6\x9d\xa8\xe6\x98\x8e\xe5\xbc\xbayyds999'
print("UTF-8编码格式解码：",end='')
print(source.decode())  #将字节类型按照指定编码格式转换为字符串，默认编码格式为UTF-8

source = "杨明强"
print(source)
print("gbk编码格式编码：",end='')
print(source.encode('gbk'))
source = b'\xd1\xee\xc3\xf7\xc7\xbf'
print("gbk格式解码：",end='')
print(source.decode('gbk'))

source = ' \t  woniuxy \n \n \t '
print(source.strip())  #清除字符串左右两边不可见字符，lstrip() 清除左边不可见字符 rstrip() 清除字符串右边不可见字符