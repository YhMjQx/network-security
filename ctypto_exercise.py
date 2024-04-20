import string
upper = string.ascii_uppercase
lower = string.ascii_lowercase
# 简单的可逆算法：
# 加密过程：大写变小写，小写变大写，数字+1
# 解密过程：大写变小写，小写变大写，数字-1
def easey_encode(source):
    dest = ''
    temp = ''
    for c in source:
        if ord(c) in range(65,91):
            temp = c.lower()
        elif ord(c) in range(97,123):
            temp = c.upper()
        elif ord(c) in range(48,58):
            temp = chr(ord(c)+1)
        dest += temp
    print(dest)

def easey_decode(source):
    dest = ''
    temp = ''
    for c in source:
        if ord(c) in range(65,91):
            temp = c.lower()
        elif ord(c) in range(97,123):
            temp = c.upper()
        elif ord(c) in range(48,58):
            temp = chr(ord(c)-1)
        dest += temp
    print(dest)

# 有张三和李四两个人
# 张三的加密算法是：凯撒加密，字母右移5位
# 李四的加密算法是：大小写互换
# 要求双方在不知道对方加密算法的前提下，双方实现文本传输，并且保证传输过程中文本始终是加密的
# 只考虑大小写字母，不考虑数字和其他符号
# 具体文本传输请看 ./img.png

# 可行性分析函数
def encode_shift5():
    plain = string.ascii_uppercase
    # print(plain)
    plain_list = []
    cipher_list = []
    for c in plain:
        print(c,end=' ')
    print('')
    for c in plain:
        index = plain.index(c)
        cipher_list.append(plain[(index+5)%len(plain)])
    print(cipher_list)
    for c in cipher_list:
        index = cipher_list.index(c) - 5
        plain_list.append(cipher_list[index])
    print(plain_list)


def encode_zhang(source):
    # 利用凯撒算法，对大小写右移五位
    # upper = string.ascii_uppercase
    # lower = string.ascii_lowercase
    cipher = ''
    for c in source:
        # if c in upper or c in lower:
        #     index = upper.index(c) or lower.index(c)
        #     cipher +=
        if c in upper:
            index = upper.index(c)
            cipher += upper[(index+5)%len(upper)]
        elif c in lower:
            index = lower.index(c)
            cipher += lower[(index+5)%len(lower)]
    # print(cipher)
    return  cipher

def decode_zhang(cipher):
    plain = ''
    for c in cipher:
        if c in upper:
            index = upper.index(c)
            plain += upper[index-5]
        elif c in lower:
            index = lower.index(c)
            plain += lower[index-5]
    return plain

def code_li(source):
    cipher = ''
    # upper = string.ascii_uppercase
    # lower = string.ascii_lowercase
    for c in source:
        if c in upper:
            cipher += c.lower()
        elif c in lower:
            cipher += c.upper()
    # print(cipher)
    return cipher

def code(source):
    result1 = encode_zhang(source)
    print(result1)
    result2 = code_li(result1)
    print(result2)
    result3 = decode_zhang(result2)
    print(result3)
    result4 = code_li(result3)
    print(result4)

def test():
    upper = string.ascii_uppercase
    print(upper)
    lower = string.ascii_lowercase
    print(lower)
    print(encode_zhang('YhMjQx'))
    print(code_li('YhMjQx'))

if __name__ == '__main__':
    easey_encode('YhMjQx521134')  # yHmJqX632245
    easey_decode('yHmJqX632245')  # YhMjQx521134
    print('----------------------------------------------')
    encode_shift5()
    print('----------------------------------------------')
    test()
    print('----------------------------------------------')
    source = 'HelloWorld'
    print(source)
    code(source)
