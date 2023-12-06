# ==Book数据库查询==

首先我们需要先熟悉 book 数据库中各个表的内容

- **customer**



![image-20231206213058148](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231206213058148.png)

- **orders**

![image-20231206213306670](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231206213306670.png)

- **orderitem**

![image-20231206214632146](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231206214632146.png)

- **goods**

![image-20231206214932582](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231206214932582.png)

![image-20231206215023258](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231206215023258.png)

注意：这里的salesprice只是商品最新的价格，而商品当时卖出去时的售价在orderitem表中的price

- **category**

![image-20231206215001867](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231206215001867.png)

## 请查询哪种学历的人群购买金额最高

- 一看到学历，去想需要customer表，一看到金额，去想到需要使用orders表。

  所以可以知道，这是两张表的连接查询

  表连接，列分组，汇总，排序

```sql
SELECT c.degree SUM(o.price) AS sm FROM customer c,orders o WHERE c.customerid = o.customerid GROUP BY c.degree ORDER BY sm DESC LIMIT 1;
```



## 查询哪个省的客户最喜欢看书

- 省这个字段在customer这张表中，
  书的数量是 quantity 在orderitem这张表中，

  我们事实上用到的只有上面两张表，但是因为customer表和orderitem表没有主外键关联，而orders表与customer表（customerid）和orderitem表（orderid）有主外键关联

```sql
SELECT c.provience,SUM(i.quantity) AS sq FROM customer c,orders o,orderitem i WHERE c.customer = o.customer AND o.orderid = i.orderid GROUP BY c.province ORDER BY sq DESC LIMIT 1;
```



## 查询哪个出版社出版的图书最多

- 出版社 publisher 在 goods 表中
  这是一个简单的单表查询

```sql
SELECT publisher,COUNT(*) NUM FROM goods GROUP BY publisher ORDER BY NUM DESC; 
SELECT publisher,COUNT(publisher) NUM FROM goods GROUP BY publisher ORDER BY NUM DESC; 
```

> 如果 `goods` 表中的每行都有非空的 `publisher` 值，那么这两个查询语句将得到相同的结果。但是如果有某些行的 `publisher` 列为 NULL，那么第一个查询语句将统计包括这些 NULL 值在内的行数，而第二个查询语句将不会统计 NULL 值，只会计算非空 `publisher` 值的行数。因此，第一个查询语句的结果可能会比第二个查询语句的结果大。
