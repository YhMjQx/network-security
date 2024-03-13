# 文件的读写，所有的I/O操作主要分为三步：打开资源，操作资源，关闭资源

# # 基本操作，读取文件内容并输出
# f = open('./PHP.yml',mode='r')
# content = f.read()
# print(content)
# f.close()
#
# # 写入文件内容,以追加的方式
# f = open('./PHP.yml',mode='a')
# f.write('\nHELLOWONIU !!!')
# f.close()
#
# # 写入新文件，并使用gbk编码
# f = open('./Temp.txt',mode='w',encoding='GBK')
# f.write('我真牛逼\n道不同不相为谋\n孤独才是强者的代名词\n牛羊成群，唯猛虎独行')
# f.close()

# 读取的操作
# f = open('./Temp.txt','r',encoding='GBK')
# content = f.read()  # 正常读取
# content = f.read(13)  # 读取 13 个字符
# content = f.readline()  # 按行读取，默认读取第一行
# content = f.readlines()  # 读取全部内容，并放在列表中，且每一行作为列表的一个元素
# content = f.read()
# contentlist = content.split('\n')  # 读取所有内容，然后以 \n 为分隔符分割开来放在列表中
# print(contentlist)


# CSV 文件的读取和修改
# CSV 文件，逗号分隔符文件，用于表示二维表的数据结构
# 将 CSV 文件变成Python列表+字典的格式 [{},{},{}]
f = open('user.csv', 'r')
content = f.readlines()  # 只有这样，读出来的len(content)才是真正的行数
# print(content)
# print(len(content))
# 从第二行开始读
# line = content[1].strip()  # 利用 strip() 函数清除每一行中多余的符号
# print(line)
user_list = []
# 循环外定义列表，一个循环内定义一个字典，然后每个字典追加在列表后
for i in range(1,len(content)):
    # 我们已知列名，但是又该如何动态读取并获取列名
    # username = content[i].split(',')[0]
    # password = content[i].split(',')[1]
    # phone = content[i].split(',')[2]

    line = content[i].strip()
    username = line.split(',')[0]
    password = line.split(',')[1]
    phone = line.split(',')[2]

    user_dict = {}
    user_dict['username'] = username
    user_dict['password'] = password
    user_dict['phone'] = phone

    user_list.append(user_dict)

f.close()
# print(user_list)


# 使用 with 自动 处理资源
# with open('./Temp.txt','r') as f:
#     content = f.read()
# print(content)

