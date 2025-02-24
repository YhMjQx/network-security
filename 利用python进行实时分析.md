[TOC]



# ==利用python进行实时分析==

教材内容

#### 一、实时分析的思路

对于Wazuh内置的JSON日志格式，其字段较多，并且Wazuh并没有内置日志查看程序，无法以一种非常友好的界面进行日志查看或者过滤，通常有两种解决方案来让日志查看或者过滤更加方便：

（1）利用Python或者PHP自主开发一套日志查看系统，或者进行相应的条件过滤。

（2）将Wazuh的日志与主流的日志平台进行整合，比如与Elastic Stack系统进行整合。

从复杂度上来说，两者均有一定门槛，但是自主开发相对来说可以做到定制，设计需要的功能，不需要特别复杂，而与Elastic进行整合，则需要对Elastic整套系统（ElasticSearch、Kibana、FileBeats等组件）有熟练掌握，其学习曲线也是比较陡峭的。 而我们选择，两个都学，两个都要会。

由于我们并没有学习如何使用Python开发Web应用，所以本节内容的核心在于如何用Python实现类似于tail -f的基于命令行的实时日志查看和过滤输出。在PHP的部分，我们再继续添加Web实时查看和过滤的内容。

##### 1、Python打开文件

首先，需要让Python程序可以以只读方式直接打开相应的日志文件（注意不能是写操作，因为Wazuh会对日志文件进行写操作，避免同时写操作导致冲突），并且记录下文件的长度

##### 2、Python文件定位

我们知道，使用 open() 函数打开文件并读取文件中的内容时，总是会从文件的第一个字符（字节）开始读起。那么，有没有办法可以自定指定读取的起始位置呢？答案是肯定，这就需要移动文件指针的位置。

文件指针用于标明文件读写的起始位置。假如把文件看成一个水流，文件中每个数据（以 b 模式打开，每个数据就是一个字节；以普通模式打开，每个数据就是一个字符）就相当于一个水滴，而文件指针就标明了文件将要从文件的哪个位置开始读起。图 1 简单示意了文件指针的概念。

![image-20211213160314236](https://gitee.com/ymq_typroa/typroa/raw/main/20211213160314.png)

可以看到，通过移动文件指针的位置，再借助 read() 和 write() 函数，就可以轻松实现，读取文件中指定位置的数据（或者向文件中的指定位置写入数据）。

（1）file.tell()：用于判断文件指针当前所处的位置

（2）file.seek(offset, [whence])：用于将文件指针移动至指定位置

- whence：作为可选参数，用于指定文件指针要放置的位置，该参数的参数值有 3 个选择：0 代表文件头（默认值）、1 代表当前位置、2 代表文件尾。
- offset：表示相对于 whence 位置文件指针的偏移量，正数表示向后偏移，负数表示向前偏移。例如，当`whence == 0 &&offset == 3`（即 seek(3,0) ），表示文件指针移动至距离文件开头处 3 个字符的位置；当`whence == 1 &&offset == 5`（即 seek(5,1) ），表示文件指针向后移动，移动至距离当前位置 5 个字符处。

（3）file.read(n)：读取n个字节的内容。

##### 3、对JSON数据进行解析

利用Python对新增日志及时进行解析，只抽取重要字段进行实时显示即可，并不需要显示过多内容。有两种方案实现对JSON数据的解析：

（1）eval(jsonstr)：利用eval函数，将JSON字符串解析为Python对象（列表/字典组合）。

（2）使用json.loads()：反序列化JSON字符串为Python对象，与之对应的序列化操作为：json.dumps()。

#### 二、实现代码

##### 1、实时读取文件内容

此处以Apache的访问日志为例进行实时读取。

```python
import time

file = open(r'D:\XamppNew\apache\logs\access.log')
file.seek(0, 2) # 直接定位到文件末尾

print("================ 开始实时读取日志信息 ================")
while True:    
    try:        
        list = file.readlines()        
        # 每一次均读取最新内容，此处并不需要使用f.tell()，因为readlines会读取到最后位置        
        if len(list) > 0:            
            print(list)        
        time.sleep(5)    
	except:        
		file.close()
```

##### 2、实时读取Wazuh日志

读取Wazuh的日志信息，比读取Apache的访问日志，要多一个解析JSON并格式化输出的操作。同时，为了方便的在VSCode中远程调试Python代码，还需要在VSCode中安装Python插件（Jupyter和Pylance会自动安装），同时在Wazuh服务器上安装Python3运行环境。

![image-20211213210247311](https://gitee.com/ymq_typroa/typroa/raw/main/20211213210247.png)

Wazuh的JSON日志格式：

```json
{"timestamp":"2021-12-13T19:52:38.852+0800","rule":{"level":5,"description":"sshd: authentication failed.","id":"5716","mitre":{"id":["T1110"],"tactic":["Credential Access"],"technique":["Brute Force"]},"firedtimes":3,"mail":false,"groups":["syslog","sshd","authentication_failed"],"pci_dss":["10.2.4","10.2.5"],"gpg13":["7.1"],"gdpr":["IV_35.7.d","IV_32.2"],"hipaa":["164.312.b"],"nist_800_53":["AU.14","AC.7"],"tsc":["CC6.1","CC6.8","CC7.2","CC7.3"]},"agent":{"id":"000","name":"centqiang"},"manager":{"name":"centqiang"},"id":"1639396358.5588","full_log":"Dec 13 19:52:38 centqiang sshd[23271]: Failed password for root from 192.168.112.188 port 56902 ssh2","predecoder":{"program_name":"sshd","timestamp":"Dec 13 19:52:38","hostname":"centqiang"},"decoder":{"parent":"sshd","name":"sshd"},"data":{"srcip":"192.168.112.188","srcport":"56902","dstuser":"root"},"location":"/var/log/secure"}
```

基于上述日志格式，提取有价值的信息，利用Python进行格式化输出，此处需要注意JSON日志的格式和层次。为了更加方便地理清JSON数据的格式和层次，可以使用在线格式化校验工具：https://www.bejson.com/json/format/

![image-20211213213933140](https://gitee.com/ymq_typroa/typroa/raw/main/20211213213933.png)

基于上述JSON格式，完成后的Python代码如下（可以先提取一个JSON预警消息在Windows环境调试好代码）

```python
import time, json
from datetime import datetime

file = open('/var/ossec/logs/alerts/alerts.json')
file.seek(0, 2)
while True:    
    try:        
        list = file.readlines()        
        if len(list) == 0:            
            time.sleep(5)            
            continue        
		for line in list:            
            data = json.loads(line)            
            alert_time = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f+0800')            
		print(f"预警时间：{alert_time}，预警级别：{data['rule']['level']}，规则编号：{data['rule']['id']}，触发次数：{data['rule']['firedtimes']}")            
              print(f"攻击源信息：{data['data']}")            
              print(f"应用信息：{data['predecoder']}")            
              print(f"监控位置：{data['location']}，规则描述：{data['rule']['description']}")            
              print(f"原始日志：{data['full_log']}")            
              print()        
		time.sleep(5)    
	except:        
		file.close()
```

上述代码运行时的输出结果如下：

![image-20250214135651629](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250214135651629.png)

##### 3、将日志以邮件形式发送

如果需要对Wazuh的日志预警信息进行长期保存和便于后续分析，也可以将日志解析后，以邮件的形式发送给相关责任人。

```python
import time, json
from datetime import datetime
def wazuh():    
	file = open('/var/ossec/logs/alerts/alerts.json')    
	file.seek(0, 2)    
	while True:        
		try:            
			list = file.readlines()            
			if len(list) == 0:                
                time.sleep(5)                
                continue            
			for line in list:                
                data = json.loads(line)                
                alert_time = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f+0800')                
                line_list = []                
                
                line_list.append(f"预警时间：{alert_time}，预警级别：{data['rule']['level']}，规则编号：{data['rule']['id']}，触发次数：{data['rule']['firedtimes']}")                
                line_list.append(f"攻击源信息：{data['data']}")                
                line_list.append(f"应用信息：{data['predecoder']}")                
                line_list.append(f"监控位置：{data['location']}，规则描述：{data['rule']['description']}")                
                line_list.append(f"原始日志：{data['full_log']}")                
                line_list.append("")                
                output = "\n".join(line_list)                
                print(output)                
                
                body = "<br/>".join(line_list)                
                body += "<br/><br/>========== 原始预警信息 ==========<br/><br/>"                
                body += line                
                mail(body)    # 发送邮件                
                send_sms('18812345678', body)    # 发送短信，代码略            
			   time.sleep(5)        
            except:            
                file.close()
                
                
def mail(body):    
    # 直接导入内置模块    
    import smtplib   # smtplib模块主要用于处理SMTP协议    
    # email模块主要处理邮件的头和正文等数据    
    from email.mime.multipart import MIMEMultipart    
    from email.mime.text import MIMEText    
    
    # 定义发件人和收件人    
    sender = 'student@woniuxy.com'  # 发送邮箱    
    receiver = '15903523@qq.com'  # 接收邮箱    
    
    # 构建邮件的主体对象    
    msg = MIMEMultipart()    
    msg['Subject'] = 'Wazuh预警信息'    
    msg['From'] = sender    
    msg['To'] = receiver    
    
    content = MIMEText(body, 'html', 'utf-8')    
    msg.attach(content)    
    
    # 建立与邮件服务器的连接并发送邮件    
    smtpObj = smtplib.SMTP()   # 如果基于SSL，则 smtplib.SMTP_SSL    
    smtpObj.connect('mail.woniuxy.com', '25')    
    smtpObj.login(user='student@woniuxy.com', password='Student123')    
    smtpObj.sendmail(sender, receiver, str(msg))    
    smtpObj.quit()
    
if __name__ == '__main__':    
    wazuh()
```

#### 三、利用Python写出一个HTML文件

##### 1、定义HTML模块文件

```html
<!DOCTYPE html>
<html lang="en">
    <head>    
        <meta charset="UTF-8">    
        <meta http-equiv="X-UA-Compatible" content="IE=edge">    
        <meta name="viewport" content="width=device-width, initial-scale=1.0">    
        <title>在线查看预警信息</title>    
        <style>        
            table, td {            
                border: solid 1px red;        
            }    
        </style>
    </head>
    <body>    
        <table border="1" width="800" align="center">        
            <tr>            
                <td>用户ID</td>            
                <td>用户名</td>            
                <td>密码</td>            
                <td>姓名</td>            
                <td>电话</td>        
            </tr>        
            ${content}    <!-- 此处的变量用于在Python中替换真实内容 -->    
        </table>
    </body>
</html>
```

##### 2、将数据库内容写出到HTML文件

```python
import pymysql
from pymysql.cursors import DictCursor
conn = pymysql.connect(user="root",password="123456",host="localhost",                       database="woniusales",charset="utf8")
cursor = conn.cursor(DictCursor)

sql = "select * from user"
cursor.execute(sql)
result = cursor.fetchall()

with open("D:/template.html", mode='r', encoding='utf-8') as f:    
    template = f.read()
    
content = ""
for user in result:    
    content += "<tr>\n"    
    content += f"<td>{user['userid']}</td>\n"    
    content += f"<td>{user['username']}</td>\n"    
    content += f"<td>{user['password']}</td>\n"    
    content += f"<td>{user['realname']}</td>\n"    
    content += f"<td>{user['phone']}</td>\n"    
    content += "</tr>\n"
    
new_content = template.replace("${content}", content)
with open("D:/user.html", mode='w', encoding='utf-8') as f:    
    f.write(new_content)
```

上述代码输出的user.html的运行效果：

![image-20220722191522315](https://gitee.com/ymq_typroa/typroa/raw/main/20220722191522.png)

> 上述功能可以用于利用Python代码生成安全审计报告，预警报告等可视化操作，甚至引入e-charts来绘制图表，均可以的。