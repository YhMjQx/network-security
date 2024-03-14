import csv
def read_csv(filepath, has_first_column = True):
    with open(filepath, 'r') as f:
        content = f.readlines()
        if not has_first_column:
            raise Exception('Your csv does not have first line be used to key')  # 抛出异常结束函数运行
            # return None
        key_line = content[0].strip().split(',')
        csv_list = []
        columnnum = len(key_line)
        for i in range(1,len(content)):
            # print(content)
            # 若 某一行数据以 # 开头，则跳过
            if content[i].startswith('#'):
                continue

            line = content[i].strip()
            # print(line)
            csv_dict = {}
            for j in range(0, columnnum):
                csv_dict[key_line[j]] = line.split(',')[j]
            csv_list.append(csv_dict)
    return csv_list

result = read_csv('./user.csv',has_first_column=True)
# result = read_csv('./user.csv',has_first_column=False)
# print(result)

# 使用 Python 的 CSV 模块进行读写

with open('./user.csv','r') as f:
    # 以列表的形式读取并遍历每一行
    # csv_list = csv.reader(f)
    # print(csv_list)  # <_csv.reader object at 0x000001D6A7A57820>
    # for item in csv_list:
    #     print(item)

    csv_result = csv.DictReader(f)  # 以字典的形式读取csv文件数据
    print(csv_result)  #  <csv.DictReader object at 0x0000018C6ED60590>
    for item in csv_result:
        # print(item)
        print(dict(item))


# f.tell()  #  告诉我文件指针的位置
# f.seek()  #  设置文件指针的位置
