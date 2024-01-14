

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

