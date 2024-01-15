

# ==Oracle安装与配置==

## 一、基础知识

首先，需要再虚拟机中导入Oracle的镜像文件，然后惊醒安装

所有的安装过程以及安装好之后的创建用户或者建表等操作都在 [数据库管理系统-18-Oracle安装与配置_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1SY411p7F9/?p=167&spm_id_from=pageDriver&vd_source=a77f2b447879bb3f0a4841dab71a491e)]这里面，可以去看看

Oracle ： 数据库服务 -》表空间 -》 多张表
这是与mysql的不同之处、
Mysql： MySQL服务 -》 创建多个数据库 -》 每个库中多张表
SQLServer： SQL服务 -》 创建多个数据库 -》 每个库中多张表

Oracle默认端口：1521，必须确保 TNSListener 服务启动

Oracle没有 Auto_Increment，不能呢个直接设置主键列为自增长，要自增长，必须使用序列对象

## 二、日期与反引号



- 使用 insert 语句插入日期和时间时，不能直接使用字符串，必须使用函数 to_date 进行类型转换`to_date('2024-01-14 14:28:20','YYYY-MM-DD HH24:MI:SS')`

```
SELECT SUM(money) FROM orders WHERE ordertime BETWEEN to_date('2021-01-01','yyyy-mm-dd') AND to_date('2020-12-31','yyyy-mm-dd');
```



- 在Mysql中用于区别表名和列名的 反引号 无法在Oacle中使用，Oracle中不存在需要用到反引号的时候



- 查询 Date 类型的列，需要转换成 年月日 时:分:秒，也需要使用函数

```
SELECT customerid,name,to_char(regtime,'YYYY-MM-DD HH24:MI:SS') FROM customer WHERE customerid=1500
```





## 三、基础SQL查询

- Oracle中使用了 GROUP BY 之后，即**分组查询过程中，无意义的列是不允许直接被select的**，比如 GROUP BY categoryid的情况下，是不允许 name goodsid * 这些列出现在select的查询结果中的，这样会直接报错，**所以一般情况下，分组查询时，只有用于分组的列和聚合函数可以用于select，当然，聚合数据是可以多选的**

  - 所以相对来说，Oracle是更加严谨的

  - 下面两种情况分别解释

    1.正确

![image-20240114213116664](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240114213116664.png)

​		

```
SELECT COUNT(goodsid),categoreid FROM goods GROUP BY categoryid;
```



![image-20240114210750031](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240114210750031.png)

​			

```
SELECT categoryid,COUNT(goodsid),SUM(salenums) FROM goods GROUP BY categoryid;
```



​			2.错误

![image-20240114210515135](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240114210515135.png)



- WHERE子句中不能使用列的别名（这一点和MySQL是一样的），但是 ORDER BY 可以使用 列的别名
  - ![image-20240114211234368](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240114211234368.png)
  - ![image-20240114211859887](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240114211859887.png)

```
select publisher p from goods where goodsid in (100,110,120,115,90) order by p desc;
```



- GROUP BY ... HAVING... 后面也不能使用列的别名，会报错（标识符无效）
  - ![image-20240114212202786](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240114212202786.png)
  - 解决办法：使用原本的列的名字
    - ![image-20240114212355790](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240114212355790.png)

​	

```
select categoryid,COUNT(goodsid) sumbook from goods GROUP BY categoryid having COUNT(goodsid) < 180;
```


## 四、book数据库综合练习

- 查询那种学历的人购买金额最高（连接，分组，汇总，排序）

```sql
select c.degree,SUM(o.money) sm from customer c,orders o where c.customerid=o.customerid GROUP BY c.degree ORDER BY sm desc; 
```

- 查询哪个省的客户最喜欢看书（三表联合查询，聚合，分组，排序）

```sql
select c.province,SUM(i.quantity) sq from customer c,orders o,orderitem i where c.customerid=o.customerid and o.orderid=i.orderid GROUP BY c.provience ORDER BY sq desc;
```

- 查询哪个出版社出版的图书最多

```sql
select publisher,COUNT(*) sum from goods GROUP BY publisher ORDER BY sum;
```

- 查询哪一类别的书利润最高

```sql
select g.category,AVG(i.price-o.costprice) avgharvestmoney from goods g,orderitem i where d.goodsid=i.goodsid GROUP BY g.category ORDER BY avgharvestmoney desc;
```

- 查询哪种类型的书数量最多

```sql
--哪种类型的书一共有多少
select g.category,COUNT(*) num from goods g GROUP BY g.category ORDER BY num desc;
--哪种类型的书库存最多
select g.category SUM(stock) ss from goods g GROUP BY g.category ORDER BY ss desc;
```

- 查询2020年的全年销售额

```sql
select SUM(money) from goods where ordertime between to_date('2020-01-01','yyyy-mm-dd hh24:mi:ss') and to_date('2020-12-31','yyyy-mm-dd hh24:mi:ss');
```

- 找到中国联通的会员，以通知联通的合作活动

```sql
select * from customer where SUBSTR(phone,1,3) IN ('130','131','132','145','155','156','166','171','175','176','185','186','196');
```

- 提取前10名购买金额最多的会员，以赠送礼品

```sql
select * from (
select c.customerid,SUM(o.money) sm from customer c, orders o where c.customerid=o.customerid GROUP BY c.customerid ORDER BY sm desc ) temp where rownum <= 10;
```

> 在 Oracle 中 是不允许使用 LIMIT 来进行限定行数的查询的，这属于 MySQL 中的用法。那么Oracle是用的什么呢，Oracle中有一个虚拟列叫做 rownum ，他的位置其实就是查询出来的结果的最前面的那一列编号，就是 rownum
>
> ![image-20240115200958895](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240115200958895.png)
>
> 这就是 rownum ，Oracle 就是使用这个来限制查询行数的
>
> 但是由于 rownum 只能使用在 WHERE 之后 ，不能用在其他ORDER BY 或者 GROUP BY 之后，所以此时就出现了一个问题，先限制rownum 在分组排序，就会出问题（如果前十行有相同的id就会出问题），所以这种情况下，**要使用 rownum 就只能将 限制行数之前的查询结果 作为一张临时表 然后再进行 rownum 的限制**
>
> **注意：Oracle中对列的名字取别名可以使用AS 也可以不用，但是对表的别名就不能使用AS，只能直接写**

- 查询2019年第三季度毛利润

```sql
select SUM((i.price-g.costprice)*i.quantity) sm from goods g,order o,orderitem i where g.goodsid=i.goodsid AND o.orderid=i.orderid AND ordertime between to_date('2019-07-01','yyyy-mm-dd hh24:mi:ss') AND to_date('2019-09-31','yyyy-mm-dd HH24:MI:SS');
```

- 有那些书卖的最好，挑出卖的最好的前20本

```sql
select * from (select i.goodsid,SUM(i.quantity) sq from goods g,orderitem i where g.goodsid=i.goodsid GROUP BY i.goodsid ORDER BY sq desc ) where rownum <= 20;
```

- 请按性别查询IT技术类图书的够买数量

```sql
select c.sex,SUM(i.quantity) sq from customer c,orders o,orderitem i where c.customerid=o.customerid AND o.orderid=i.orderid AND g.categoryid=1 AND GROUP BY c.sex ;
```



## 五、其他用法

```
自增长列
MySQL: AUTO_INCREMENT
Oracle: 
```



![image-20240115133516871](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240115133516871.png)

高速缓存：（一般是默认不使用的）例如这里的大小是20，意思就是一次性会生成从开始位置往后的20个序列并存放在内存中去

对应的SQL语句 

```
CREATE SEQUENCE MYSEQ INCREMENT BY 1 START 100 MAXVALUE 9999 MINVALUE 100 CACHE 20;
```

至此就有了序列对象了（表中的是序列对象的属性）

![image-20240115135653108](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240115135653108.png)

### 那该如何使用序列呢？

直接使用select语句即可获取

```sql
select myseq.nextval from dual;
```

> dual是Oracle中的一张虚拟表，当无表可用时，就可以使用这张表从而查询select的结果

运行第一次结果是100

![image-20240115140236872](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240115140236872.png)

运行第二次结果是101

![image-20240115140309079](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240115140309079.png)

再往下就是102 103 ...

![image-20240115140332055](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240115140332055.png)

### 那么如何在插入的时候使用序列从而达到自增长的目的呢

