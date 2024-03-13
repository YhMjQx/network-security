# CSV 文件的读取和修改
# CSV 文件，逗号分隔符文件，用于表示二维表的数据结构
# 将 CSV 文件变成Python列表+字典的格式 [{},{},{}]
f = open('user.csv', 'r')
content = f.readlines()  # 只有这样，读出来的len(content)才是真正的行数,因为readlines读出来的结果会将每一行作为一个元素
# print(content)
# print(len(content))
first_line = content[0].strip().split(',')  # ['username', 'password', 'phone']
# print(first_line)
# first_line[0]  # 这是username标题
# first_line[0]  # 这是password标题
# first_line[0]  # 这是phone标题
# 从第二行开始读
# line = content[1].strip()  # 利用 strip() 函数清除每一行中多余的符号
# print(line)
user_list = []
for i in range(1,len(content)):
    # 我们已知列名，但是又该如何动态读取并获取列名
    # username = content[i].split(',')[0]
    # password = content[i].split(',')[1]
    # phone = content[i].split(',')[2]

    # 利用 strip() 函数清除每一行中多余的符号 例如 \n
    line = content[i].strip()
    username = line.split(',')[0]
    password = line.split(',')[1]
    phone = line.split(',')[2]

    user_dict = {}
    user_dict[first_line[0]] = username
    user_dict[first_line[1]] = password
    user_dict[first_line[2]] = phone

    user_list.append(user_dict)

f.close()
print(user_list)

# 使用 with 自动 处理资源
# with open('./Temp.txt','r') as f:
#     content = f.read()
# print(content)

