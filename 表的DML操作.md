# ==表的DML操作==

![image-20231125144302109](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231125144302109.png)

创建好了表之后我们就要开始进行对表的DML操作



## 一、插入数据

```sql
#针对列名或表名，可以通过添加 `` 来进行区分 例如： `school`.`stu_info`
#在SQL语句中 单引号用于分割字符串 对于数值型 可以不加单引号

#INSERT INTO `student`.`stu_info` (id,name,phone,sex,age,degree,college,createtime)
INSERT INTO stu_info (id,name,phone,sex,age,degree,college,createtime)
VALUES ('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30')

#如果在插入数据时，每一列都要插入数据，则可以忽略列名
INSERT INTO stu_info #(id,name,phone,sex,age,degree,college,createtime)
VALUES ('XUPT02','张明宇','12345678910','男','20','本科','西邮','2023-11-25 19:21:30')

#如果只是部分列插入数据，则必须明确指定列名
INSERT stu_info (id,name,phone,createtime)
VALUES ('XUPT03','卢瑞征','12345678910','2023-11-25 19:28:34')

#如果要批量插入数据，一次性插入多条数据
INSERT INTO stu_info (id,name,phone,sex,age,degree,college,createtime)
VALUES ('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30');
INSERT INTO stu_info (id,name,phone,sex,age,degree,college,createtime)
VALUES ('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30');
INSERT INTO stu_info (id,name,phone,sex,age,degree,college,createtime)
VALUES ('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30');
INSERT INTO stu_info (id,name,phone,sex,age,degree,college,createtime)
VALUES ('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30');
INSERT INTO stu_info (id,name,phone,sex,age,degree,college,createtime)
VALUES ('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30');

#但是标准的批量插入语法如下：
INSERT INTO stu_info (id,name,phone,sex,age,degree,college,createtime)
VALUES ('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30'),
('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30'),
('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30'),
('XUPT01','杨明强','13772816626','男','19','本科','西邮','2023-11-25 19:21:30')

```



## 二、删除数据

```sql
#删除数据
TRUNCATE TABLE stu_info;  #截断表的数据
DELETE FROM stu_info;  #清空表的数据 可以带 WHERE 条件决定删除哪些行
DELETE FROM stu_info WHERE id='XUPT01';
DELETE FROM stu_info WHERE id IN ('XUPT01','XUPT06'); 
```



## 三、更新数据

```sql
#更新数据
UPDATE stu_info SET name='牛大逼';
UPDATE stu_info SET name='王老五' WHERE id='XUPT03';
```



#如何防止字段中的内容重复 —— 设置主键和索引中标识unique