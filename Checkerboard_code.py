Checkerboard1 = []
line0 = ['A', 'B', 'C', 'D', 'E']
Checkerboard1.append(line0)
line1 = ['F', 'G', 'H', 'I', 'K']
Checkerboard1.append(line1)
line2 = ['L', 'M', 'N', 'O', 'P']
Checkerboard1.append(line2)
line3 = ['Q', 'R', 'S', 'T', 'U']
Checkerboard1.append(line3)
line4 = ['V', 'W', 'X', 'Y', 'Z']
Checkerboard1.append(line4)

Checkerboard2 = []
line0 = ['A', 'B', 'C', 'D', 'E']
Checkerboard2.append(line0)
line1 = ['F', 'G', 'H', 'J', 'K']
Checkerboard2.append(line1)
line2 = ['L', 'M', 'N', 'O', 'P']
Checkerboard2.append(line2)
line3 = ['Q', 'R', 'S', 'T', 'U']
Checkerboard2.append(line3)
line4 = ['V', 'W', 'X', 'Y', 'Z']
Checkerboard2.append(line4)

print(Checkerboard1)
# print(Checkerboard2)
# print(len(Checkerboard1))
# print(len(Checkerboard1[0]))

def encode():
    plaintext = input('请输入明文:').strip()
    print('密文为:', end='')
    def encodeplain(plaintext,Checkerboard):
        for item in plaintext: # 遍历明文字符串中的每一个字符
            for i in range(0, len(Checkerboard)):
                for j in range(0, len(Checkerboard[0])):
                    # 利用双层for循环遍历矩阵中的每一个
                    if item == Checkerboard[i][j]:  # 如果在矩阵中找到了和明文字符串中相同的字符，则输出矩阵中的该字符下标
                        print(i, end='')
                        print(j, end=' ')

    if 'I' in plaintext:
        encodeplain(plaintext, Checkerboard1)
    elif 'J' in plaintext:
        encodeplain(plaintext, Checkerboard2)
    elif ('I' not in plaintext) and ('J' not in plaintext):
        encodeplain(plaintext, Checkerboard1)

    print('')


def decode():
    ciphertext = input('请输入密文:').replace(' ','')

    def decodecipher(ciphertext,Checkerboard):
        line = []
        column = []
        groups = len(ciphertext[::2])
        # print(groups)  # 计算有多少组
        for lineitem in ciphertext[::2]:
            lineitem = int(lineitem)
            line.append(lineitem)
        # print(line)
        for columnitem in ciphertext[1::2]:
            columnitem = int(columnitem)
            column.append(columnitem)
        # print(column)
        print('明文为:',end='')
        for i in range(0,groups):
            print(Checkerboard[line[i]][column[i]],end='')
        print('')

    decodecipher(ciphertext,Checkerboard1)
    print('或')
    decodecipher(ciphertext, Checkerboard2)

encode()
decode()
