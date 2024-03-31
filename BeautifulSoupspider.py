from bs4 import BeautifulSoup
import requests

# 第一步发出请求
resp = requests.get('http://woniunote.com/')

# 第二步初始化解析器
htmldom = BeautifulSoup(resp.text,'lxml')

# 查找页面元素
print(htmldom.head.title)  # 根据标签的层次找页面标题
print(type(htmldom.head.title))  # <class 'bs4.element.Tag'>
print(htmldom.head.title.string)  # 获取页面标题的文本内容，python中的string相当于js中的innerhtml
print(htmldom.div.div['class'])  # 查找页面的第一个div容器中的第一个div容器的class属性
print(type(htmldom.div.div['class']))  # <class 'list'>

# 查找页面中的所有超连接
links = htmldom.find_all('a')
for link in links:
    print(link['href'])

# 查找页面中的所有图片链接
images = htmldom.find_all('img')
for image in images:
    print(image['src'])

# 根据id或class等属性查找
key = htmldom.find(id="loginmenu")
print(key)

titles = htmldom.find_all(class_="nav-item nav-link")  # 因为class作为python的关键字，因此在这里使用class查找时，需要将class变为class_
for title in titles:
    print(title)
    print(title.string)
    print(title['href'])

print("")
title = htmldom.find(string='以蜗牛之名, 行学习之实')
print(title)
print(title.parent)
print(title.parent.parent)
print("")


# find_all根据xpath的风格进行查找
titles = htmldom.find_all('div',{'class':'title'})  # 意思是查找htmldom下的class属性为title的div
for title in titles:
    print(title)
    print(title.a)
    print(title.a.string)
    print(title.a['href'])

# CSS 选择器
# 类选择器
# titles = htmldom.select('div.title') # 查找class属性为title的div 和 htmldom.find_all('div',{'class':'title'}) 是一个意思
titles = htmldom.select('.title')  # 相当于 htmldom.find_all(class_="title")
for title in titles:
    print(title)
#
# # id选择器
keyword = htmldom.select('#keyword')  # 查找id属性为keyword的元素，相当于 htmldom.find_all(id="keyword")
print(keyword)
print(type(keyword))

# 层次选择器
lis = htmldom.select('ul li')  # 查找 ul 标签下的li标签
for li in lis:
    print(li)