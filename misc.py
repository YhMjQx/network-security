import pymysql
from pymysql.cursors import DictCursor
import json
from exercise.common import query_mysql

# 针对不同异常，抛出不同错误信息
# try:
#     conn = pymysql.connect(host='localhost',user='root',password='p-0p-0p-0',database='woniunote',port=3306,charset='utf8')
#     cursor = conn.cursor(DictCursor)
#     sql = "select username,password,nickname from users"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print(result)
# except pymysql.err.OperationalError:
#     print('数据库连接失败')
# except pymysql.err.ProgrammingError:
#     print('SQL语句执行失败')
#     conn.close()
# except:
#     print('代码本身存在问题')
#     conn.close()
# finally:
#     pass
#     # print('数据库连接关闭')

# 将python对象序列化为json字符串
# row_tuple = query_mysql("select username,password,nickname from users")
# print(row_tuple)
# print(type(row_tuple))
#
# jsonstr = json.dumps(row_tuple)
# print(jsonstr)
# print(type(jsonstr))
#
# # 将json字符串反序列化为python对象
# source = '[{"username": "woniu@woniuxy.com", "password": "e10adc3949ba59abbe56e057f20f883e", "nickname": "\u8717\u725b"}, {"username": "qiang@woniuxy.com", "password": "e10adc3949ba59abbe56e057f20f883e", "nickname": "\u5f3a\u54e5"}]'
# # source = '[{"username": "woniu@woniuxy.com", "password": "e10adc3949ba59abbe56e057f20f883e", "nickname": "\u8717\u725b"},{"username": "qiang@woniuxy.com", "password": "e10adc3949ba59abbe56e057f20f883e", "nickname": "\u5f3a\u54e5"}]'
# jsonobj = json.loads(source)
# print(jsonobj)
# print(type(jsonobj))
#
# # json库还有 json.dump 和 json.load ，用于操作文件
# with open('./jsonstr.json', mode='w') as f:
#     json.dump(row_tuple,f)
# with open('./jsonstr.json',mode='r') as f:
#     result = json.load(f)
#     print(result)
#     print(type(result))

import time
# 装饰器
# 在函数或方法或类的前面，使用 @ 符号惊醒声明的特殊操作，可以改变程序的执行顺序
# 例如：统计某段代码的执行时间
# 装饰器函数内部再定义一个函数，称之为内部函数（闭包）
# 装饰器函数自带一个参数，func，用于获取被装饰函数的地址
# 内部函数运行结束后，必须要返回其函数名（地址）
#

def stat(func):
    def inner():
        start = time.time()
        func()  # 调用被装饰的函数
        end = time.time()
        print(end - start)
    return inner

@stat
def calc():
    a = 9999
    for i in range(0,3000):
        a = a + i - a * 15
    print(a)

calc()