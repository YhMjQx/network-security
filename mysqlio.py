# 针对数据库的操作，一共分三步：
# 1.建立数据库连接
# 2.执行SQL语句
# 3.关闭数据库连接

# Python操作数据库（如：MySQL），Python发送能够与数据库直接通信的数据包，并获取数据库服务器的响应结果
# 这是一种典型的基于TCP/IP的通信过程，要求必须要满足数据库服务器的数据包规则。
# 在Python中，要操作MySQL，需要依赖于第三方库，P有MySQL，先安装 pip install pymsql

import pymysql
from pymysql.cursors import DictCursor
# 建立连接
conn = pymysql.connect(host='192.168.230.147',user='remote',password='p-0p-0p-0',database='woniunote',charset='utf8')
# print(conn.host_info)  # socket localhost:3306

# 操作数据库
# 定义一个游标对象，用于执行sql语句，获取结果集
# cursor = conn.cursor()  # 游标对象的返回结果默认是元组
cursor = conn.cursor(DictCursor)  #  这样是将结果集作为列表嵌套字典的方式返回
sql = "select username,password,nickname from users"
cursor.execute(sql)
result = cursor.fetchall()
# print(result)
for row in result:
    # print(row[0],row[1],row[2])
    print(row['username'],row['password'],row['nickname'])

# 关闭数据库
conn.close()

# 更新数据库，必须确认提交，两种方式：
# 1.在构造连接对象时设置autocommit （自动提交）为True
# 2.显示提交 conn.commit()
# conn = pymysql.connect(host='localhost',user='root',password='p-0p-0p-0',database='woniunote',charset='utf8',port=3306)
conn = pymysql.connect(host='localhost',user='root',password='p-0p-0p-0',database='woniunote',charset='utf8',port=3306,autocommit=True) # 给连接对象设置自动提交
cursor = conn.cursor()
sql = "update users set nickname='ymqyyds' where userid=8"
cursor.execute(sql)
# conn.commit()  # 显示提交sql语句
conn.close()
