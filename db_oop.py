import pymysql
from pymysql.cursors import DictCursor

class DB:
    def __init__(self,host='localhost',database='woniunote',user='root',password='p-0p-0p-0',charset='utf8',type='default'):
        # 构造函数定义类属性
        self.conn = pymysql.connect(user=user,password=password,host=host,database=database,charset=charset)
        self.cursor = None  # 定义一个游标属性是用来获取sql语句的执行结果的

        # 根据不同情况修改类属性
        if type == 'default':
            self.cursor = self.conn.cursor()
        elif type == 'dict':
            self.cursor = self.conn.cursor(DictCursor)
        else:
            raise Exception('参数type错误，只能为 default或dict')

    def query(self,sql):
        try:
            self.cursor.execute(sql)  # 使用游标执行sql语句，直接让cursor指向sql执行结果
            result = self.cursor.fetchall()  # 然后再用fetchall来让cursor获取结果
            return result
        except:
            print('更新操作出现异常，请确认正确后再重试')

    def update(self,sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    # db = DB()
    db = DB(type='dict')
    print(db.query('select * from users'))
