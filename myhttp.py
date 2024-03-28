import requests

# 发送GET请求
# resp = requests.get("http://192.168.230.147:8080/woniusales/")
# resp.encoding = 'utf-8'
# print(resp.content)  # 得到的是响应的二进制流
# print(resp.text)  # 所访问页面的源代码，就是响应的文本型数据
# print(resp.encoding)  # utf-8
# print(resp.cookies)  # <RequestsCookieJar[]>
# print(resp.headers)  # 服务器响应头，其中包含的是服务器配置信息
# print(resp.history)  # []


# 发送post请求
# data = {'username':'admin','password':'admin123','verifycode':'0000'}
# resp = requests.post("http://192.168.230.147:8080/woniusales/user/login",data=data)
# # print(resp.text)
# # print(resp.cookies)
# if resp.text == 'login-pass':
#     print('登录成功')
#
# else:
#     print('登录失败')
#
# # 登录成功后获取响应的Cookie，用于在后续请求中使用
# cookies = resp.cookies

# # 下载图片
# # resp = requests.get('http://woniunote.com/img/banner-1.jpg')
# # # print(resp.text)
# # with open('./woniunote.jpg',mode='wb') as f:
# #     f.write(resp.content)


# # 文件上传
# file = {'batchfile':open('filepath','rb')}  # 具体情况去看 ./img.png,filepath也是自己电脑中的具体情况
# data = {'batchname':'GB20240327'}  # 这两部分的内容都需要去抓包进行查看
# resp = requests.post(url='http://192.168.230.147:8080/woniusales/goods/upload',data=data,files=file,cookies=cookies)
# print(resp.text)

# # 第二种维持Cookie的用法
# session = requests.session()  # 创建一个session对象，用这个session对象来发送请求，就可以自动帮我们维持和发送session和cookie
# data = {'username':'admin','password':'admin123','verifycode':'0000'}
# post_resp = session.post(url='http://192.168.230.147:8080/woniusales/user/login',data=data)
#
# data = {'batchname':'GB20240327'}  # 这两部分的内容都需要去抓包进行查看
# file = {'batchfile':open('filepath','rb')}  # 具体情况去看 ./img.png,filepath也是自己电脑中的具体情况
# file_resp = session.post(url='http://192.168.230.147:8080/woniusales/goods/upload',data=data,files=file,cookies=cookies)
# print(file_resp.text)  # 根据我请求的网站，这个响应是json字符串

# # 利用python直接处理JSON
# import json
#
# salelist = json.loads(file_resp.text)  # 将响应结果反序列化为list+dict对象


# 处理HTTPS请求
# 由于HTTPS请求还要验证证书，但我们没有，所以直接忽略证书进行访问就好了
resp = requests.get('https://www.woniuxy.com',verify=False)  # verify=False 忽略证书验证
print(resp.text)
