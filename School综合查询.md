# ==School综合查询==



- **查询所有考试平均成绩在80分以上的学生的姓名**

下面是成绩表

![image-20231203145056135](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231203145056135.png)

1. 找到平均成绩在80分以上的studentid `SELECT studentid AVG(score) FROM grade GROUP BY studentid HAVING SCORE >= 80;`
2. 通过找到的studentid在student表中进行多表查询

```sql
SELECT s.sname s.studentid,AVG(g.score) AS AvgScore FROM grade g,student s WHERE s.studentid=g.studentid GROUP BY studentid HAVING AvgScore >= 80;
```



- **查询所有外语考试成绩在80分以上的学生的姓名**

下面是class表

![image-20231203152704778](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231203152704778.png)

1. 先判断是几张表连接（这里是三张表。英语课程存在于course表中，成绩存在于grade表中，学生姓名存在sttudent表中）
2. 先在course和grade两表中进行双表查询得到对应的 cname和 AVG(score) 
3. 然后再去student表中进行连接 得到对应的sname

```sql
#在这里我们简单说一下这种复杂查询语句的思路
#一：先写单表，并且 SELECT 的内容为 * ，需要 SELECT 的内容最后在从临时表中去写
SELECT * FROM grade WHERE courseid='C01' AND score >= 80;  #这里先用courseid='C01'来代替一下cname='外语'，等把class表连接上了之后，再改过来就好了
#二：一张表一张表的加，从单表加到双表，查询结果是否成功，再由双表加到三表
SELECT * FROM student s,grade g,course c WHERE s.studentid = g.studentid AND g.courseid = c.courseid AND c.cname='外语' AND g.score >= 80;
#三：最后查询我们想要的内容
SELECT s.sname c.cname g,score FROM grade g,student s,course c WHERE g.studentid = s.studentid AND g.courseid = c.courseid AND c.cname='外语' AND g.score >= 80;
```



- **查询所有C01课程的成绩在80以上的学生的学号，姓名和成绩**

```sql
#在这里我们分析，courseid studentid sname grade只需要两张表student和grade就够了
SELECT s.studentid s.sname g.grade FROM student s,grade g WHERE s.studentid = g.studentid AND g.courseid='C01' AND g.score >= 80;
```



- **查询所有男生中数学成绩最高的学生**

```sql
#首先 男生 为sex，需要考虑student表
#其次 数学 为course，需要考虑class表
#然后 成绩 为grade，需要考虑grade表
SELECT * FROM student s,grade g,course c WHERE s.studentid = g.studentid AND g.courseid = c.courseid AND s.sex='男' AND c.cname='数学' ORDER BY g.score DESC LIMIT 1; 
```



- **查询所有女生的语文平均成绩**

```sql
#女生 为sex，需要student表
#语文 为course，需要course表
#成绩 为grade，需要grade表
SELECT ROUND(AVG(score),1) FROM student s,course c,grade g WHERE s.studentid = g.studentid AND g.courseid = c.courseid AND s.sex='女' AND c.cnaem='语文';
```

> 其中 ROUND(m,n) 表示对m采取小数的四舍五入，小数的个数就是n的大小

- **查询测试二班所有学生的平均成绩**

```sql
#测试二班 为class，需要class表
#成绩 为grade，需要grade表
#但是由于class表和grade表没有主外键关联，class表只与student表有关，所以这里还需要student表
SELECT AVG(score) FROM student s,grade g,class c
WHERE s.studentid=g.studentid AND s.classid=c.classid AND c.classname='测试二班' 
```



- **查询成绩最好的前十名学生的所在班级**

```sql
#使用平均成绩来判断
#第一步：先找平均分前十的分数
SELECT AVG(score) AS AvgScore FROM grade GROUP BY grade.studentid ORDER BY AvgScore LIMIT 10;
#然后向下扩展，上面找到平均分了之后，只需要将对应的班级名称查询出来对应上就好了，但是要查询出对应的classname我们需要将student表也引进来，因为grade表中没有与班级有关的，所以我们只能从grade表中去找studentid或classid与class表关联。
#又因为只有studen表中的classid才和class表中的classid有主外键关系，而student表和grade表的关联的向又是

#上面我们已经找到了排名前是的平均分，通过对studentid进行分组，可以得到每一个studentid对应的AvgScore，然后下面要引进classname，但是因为grade与class表并没有主外键关联，因此这个时候就会形成笛卡尔积，只有student表与class通过classid进行主外键关联，所以，我们也需要将student表引进，从而通过这个来防止class表与grade表形成笛卡尔积

SELECT c.classname AVG(g.score) AS AvgScore FROM grade g,student s,class c WHERE s.studentid = g.studentid AND s.classid = c.classid GROUP BY g.studentid ORDER BY AvgScore DESC LIMIT 10; 
#当然，我们也可以对查询的结果班级进行一下去重，因为排名前10的学生有可能会有部分人在一个班里
SELECT DISTINCT(classname) FROM (SELECT c.classname AVG(g.score) AS AvgScore FROM grade g,student s,class c WHERE s.studentid = g.studentid AND s.classid = c.classid GROUP BY g.studentid ORDER BY AvgScore DESC LIMIT 10) AS temp;
```



- **查询班级学生数量最少的班级名称**

```sql
#只需要对班级进行分组，然后对每一个组里面的学生行数进行统计，就是没个班级的人数，最后，把统计到的人数结果进行升序（默认排序方式）最上面的1个就是人数最小的班级人数
SELECT classid COUNT(studentid) AS stunum FROM student WHERE GROUP BY classid  ORDER BY stunum LIMIT 1; 
```

# ==SQL基本函数的使用==

## SUBSTR（下标从一开始）

**字符串截取**

```sql
#语法
#SELECT SUBSTR('XXXX',M,N);
#截取字符串从第m个位置开始往后截取n个
SELECT SUBSTR('我是你爸爸',1,4); 
#结果：我是你爸
```

## ASCII（返回第一个字符的ASCII值）

```sql
#语法
#SELECT ASCII('XXXX');  
SELECT ASCII('我是你爸爸');
```

## CHAR_LENGTH（返回字符串长度）

```sql
SELECT CHAR_LENGTH('我是你爸爸');   #结果返回5
```

## CONCAT（字符串拼接）

```sql
SELECT CONCAT('HELLO','WORLD');
#结果返回 HELLO WORLD
```

## HEX（取十六进制）

```sql
SELECT HEX('H');  #结果返回48，相对应的
```





## 应用

```sql
#列出所有学生的姓
SELECT DISTINCT(SUBSTR(sname,1)) FROM student;

#通过十六进制查询
#记住，SQL查询中字符串不需要添加单引号
SELECT * FROM student WHERE sname=0xE6B288E99B85E7BBBF

#获取当前用户
SELECT USER();
#查看当前版本号
SELECT VERSION();
#查看当前数据库名称
SELECT DATABASE();
```



