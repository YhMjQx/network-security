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



## 查询哪个类别的图书，利润最高

- **类别在category表中，有id和name**
- **每个类别平均利润=售价-进价 即 orderitem 表中的 price 减掉 goods 表中的 costprice** 

- **按照categoryid（类别）进行分组**

```sql
SELECT g.categoryid,AVG(i.price-g.costprice) FROM orderitem i,goods g WHERE i.goodsid=g.goodsid GROUP BY categoryid;
```



## 查询哪种类型书的数量最多

- **数量就是goods表中的stock**

- **对goods表中的categoryid进行分类，统计每一个category的stock数量并查询出来**

```sql
SELECT categoryid,COUNT(salenums) salenum FROM goods
#这个是销售数量
SELECT categoryid,COUNT(stock) stocknum FROM goods GROUP BY category DESC; 
#这个是库存数量
```



## 查询2020年的全年销售额

- **销售额在orders（订单）表中的money**

```sql
SELECT SUM(money) FROM orders WHERE ordertime BETWEEN '2020-01-01' AND '2020-12-31';
```



## 找到中国联通的会员，以通知联通的合作活动

- **通过判断电话号码前三位来区分运营商** 

- **联通号段：130,131,132,145,155,156,166,171,175,176,185,186,196**

```sql
SELECT * FROM customer WHERE SUBSTR(phone,1,3) IN ('130','131','132','145','155','156','166','171','175','176','185','186','196'); 

SELECT * FROM customer WHERE phone like '130%' OR '131%' OR '132%' OR '145%' OR '155%' OR '156%' OR '166%' OR '171%' OR '175%' OR '176%' OR '185%' OR '186%' OR '196%';
```



## 提取前十名

- **在orders表中，有customerid和money**
- **用customer表和orders表结合，从而在对customerid分组和sum(money)的同时可以得到用户姓名和电话**

```sql
SELECT SUM(o.money) summoney FROM customer c,orders o WHERE c.customerid=o.customerid GROUP BY o.customerid ORDER BY summoney DESC; 
```



## 查询2018年第一季度的所有图书类别的销售额

- 在这里要注意，在计算总金额的时候不能再用money而是要用orderitem表中的subtotal
- 因为orders表是订单表，一共有7999条，orderitem表是订单详情表，一共有19941条，所以orders表中的一条可能对应orderitem表中的好几条，此时如果还使用orders表中的money，那不是明显重复计算金额了嘛

![image-20231218211712444](https://gitee.com/ymq_typroa/typroa/raw/main/image-20231218211712444.png)

- 所以此时应该用SUM(i.subtotal)

```sql
SELECT g.categoryid,SUM(i.subtotal) FROM orders o,goods g,orderitem i WHERE i.goodsid=g.goodsid AND o.orderid=i.orderid AND o.ordertime BETWEEN '2018-01-01' AND '2018-03-31' GROUP BY g.categoryid;
```



## 查询2019年第三季度的毛利润

- **毛利润=售价-进价 即 orderitem 表中的 price 乘以 quantity 减掉 goods 表中的 costprice**





## 有哪些书卖的最好，挑卖的最好的前20件商品

- **卖的最好 即 数量最多，在orderitem 表中有 quantity**
- **商品肯定要有goods表**

```sql
SELECT i.goodsid,SUM(i.quantity) sq FROM goods g,orderitem i WHERE g.goodsid=i.goodsid GROUP BY i.goodsid ORDER BY sq DESC;
```



## 查询哪些客户从来没有买过一本书

```sql
SELECT * FROM customer WHERE customer NOT IN (SELECT customer FROM orders);
```



## 请按性别查询IT类图书的购买数量

- **性别sex在customer表中，数量 quantity在orderitem表中**
- **所以实际上我们只需要orderitem和customer两张表就够了，但是由于这两张表并没有直接的主外键关联，所以还必须引入其他的表，此时就有orders表**
- **orders表中的orderid与orderitem表中的orderid主外键关联；orders表中的customerid与customer表中的customerid主外键关联**
- **最后由于因为有IT类图书限制，所以还需要另一个表可以和上面三张表有主外键关联的关系，此时就有了goods表，goods表中的goodsid和orderitem表中的goodsid关联**
- **如果需要显示图书类别名称，就需要将第五张表category也关联进来**在这里先不展示了

```sql
SELECT c.sex,SUM(i.quantity) FROM customer c,goods g,orders o,orderitem i WHERE c.customerid=o.customerid AND g.goodsid=i.goodsid AND o.orderid=i.orderid AND i.quantity=1 GROUP BY c.sex;

SELECT ca.name,c.sex,SUM(i.quantity) FROM customer c,goods g,orders o,orderitem i,categoty ca WHERE c.customerid=o.customerid AND g.goodsid=i.goodsid AND o.orderid=i.orderid AND g.categoryid=ca.id i.quantity=1 GROUP BY c.sex;
```



## 请查询客户最喜欢哪种支付方式

```sql
SELECT paytype,COUNT(paytype) cp FROM orders GROUP BY paytype ORDER BY cp DESC;
```


