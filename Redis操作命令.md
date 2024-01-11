# ==Redis操作命令==

## 一、Kev的操作命令

| 命令      | 描述                                                         | 用法                                                         |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| DEL       | （1）删除给定的一个或多个Key （2）不存在的Key将被忽略        | DEL key [key ...]                                            |
| EXISTS    | (1) 检查给定Key是否存在                                      | EXISTS key                                                   |
| EXPIRE    | （1）为给定Key设置生存时间 （2）对一个已经指定生存时间的Key设置执行 EXPIRE ，新的值会替代旧的值 | EXPIRE key seconds                                           |
| KEYS      | 查找所有符合给定模式 pattern 的key，例如：（1）KEYS 匹配所有key （2）KEYS h?llo 匹配 hello，hallo，hxllo等 （3）KEYS hllo 匹配hllo，heeeeello等 （4）KEYS h[ae]llo 匹配 hello和hallo | KEYS pattern                                                 |
| MIGRATE   | （1）原子性的讲Key从当前实例传送到目标实例指定的数据库上 （2）源数据库Key删除，新数据库Key增加 （3）阻塞进行迁移的两个实例，直到迁移成功，迁移失败，等待超时三个之一发生 | MIGRATE host port key destination-db timeout [COPY] [REPLACE]<br />移动单个数据<br/>migrate 目标Redis的ip 目标Redis的端口 Key 目标数据库号 时延 |
| MOVE      | (1) 将当前数据库的Key移动到给定数据库中 （2）执行成功的条件为当前数据库有Key，而给定数据库没有Key | MOVE key db                                                  |
| PERSIST   | （1）移除给定Key的生存时间，将Key变为持久数据                | PERSIST key                                                  |
| PANDOMKEY | （1）从当前数据库随机返回且不删除一个Key                     | PANDOMEY                                                     |
| RENAME    | （1）将Key的键名修改为新键名（2）新键名已存在，RENAME将覆盖旧值 | RENAME key newkey                                            |
| TYPE      | （1）返回Key所存储的值的类型                                 | TYPE key                                                     |

**del操作**

![image-20240110203603357](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240110203603357.png)

**exists操作**

![image-20240110203737311](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240110203737311.png)

**ttl和expire搭配使用**

> ttl 用于查看变量的生命周期（单位为秒）
> 当结果为 -1 时，表示生命周期为永久存在
> 当结果表示-2时，表示生命周期结束，该变量已销毁
>
> expire用于设置变量的周期（单位为秒）

![image-20240110204601027](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240110204601027.png)

*name 变量永久存在 设置其生命周期为10秒，可以用 ttl name 来查看其生命时长 当生命周期过了之后该变量就不再存在，所以就 get 不到了*

**persist** 

*相当于是和expire互补的一条指令，它用于将变量的生命周期设为永久*

![image-20240110205438531](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240110205438531.png)

**move **

*移动该数据库中的变量到别的数据库中，别的数据库中不能已经存在该变量*

![image-20240110210252389](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240110210252389.png)

**randomkey**

*任意获取一个Key*

![image-20240110212244995](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240110212244995.png)

## 二、字符串的操作命令

| 命令   | 描述                                                         | 用法                                                  |
| ------ | ------------------------------------------------------------ | ----------------------------------------------------- |
| SET    | （1）将字符串值value关联到Key  <br />（2）Key已关联则覆盖，无视类型<br />（3）原本Key带有生存时间TTL，那么TTL被清除 | SET key value [EX seconds] [PX milliseconds] [NX\|XX] |
| GET    | (1) 返回Key关联的字符串值<br />(2)  Key不存在返回null<br />(3) Key存储的不是字符串，返回错误，因为GET只用于处理字符串 | GET key                                               |
| MSET   | (1) 同时设置一个或多个Key-Value键值对<br />(2) 某个给定Key已经存在，那么MSET新值会夏盖旧值<br />(3) 如果上面的覆盖不是希望的，那么使用MSETNX命令，所有Key都不存在才会进行覆盖<br />(4) MSET是一个原子性操作，所有Key都会在同一时间被设置，不会存在有些更新有些没更新的情况 | MSET key value [key value ...]                        |
| MGET   | (1) 返回一个或多个给定Key对应的Value <br />(2) 某个Key不存在那么这个Key返回nil | MGET key [key ...]                                    |
| SETEX  | (1)将Value关联到Key<br /> (2) 设置Key生存时间为seconds，单位为秒 <br />(3) 如果Key对应的Value已经存在，则覆盖旧值 <br />(4)SET也可以设置失效时间，但是不同在于SETNX是一个原子操作，即关联值与设置生存时间同一时间完成 | SETEX key seconds value                               |
| SETNX  | (1)当Key不存在时将Key的值设为Value<br /> (2) 若给定的Key已存在，SEXNX不做任何动作 | SETNX key value                                       |
| INCR   | (1) Key中存储的数字值+1，返回增加之后的值 <br />(2) Key不存在，那么Key的值被初始化为0再执行INCR <br />(3) 如果值包含错误类型或者字符串不能被表示为数字，那么返回错误<br /> (4)值限制在64位有符号数字表示之内 | INCR key                                              |
| DECR   | （1）Key中存储的数字值减一 <br />(2) 其余同INCR              | DECR key                                              |
| INCRBY | (1)将key所存储的值加上增量返回增加之后的值<br />(2) 其余同INCR | INCRBY key increment                                  |
| DECRBY | (1)将key所存储的值减去减量decrement<br /> (2) 其余同INCR     | DECRBY key decrement                                  |

 **mset**

![image-20240110215016239](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240110215016239.png)

**mget**

![image-20240110215058615](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240110215058615.png)

**setex**

*set + expire*

`setex key seconds value`

![image-20240110215306761](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240110215306761.png)

**setnx**

*如果setnx的key已经存在则不会做任何操作，反之构建key-value键值对*







## 三、哈希数据的操作命令

| 命令    | 描述                                                         | 用法                                                        |
| ------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| HSET    | (1)将哈希表Key中的域Field的值设为Value<br /> (2) Key不存在，一个新的Hash表被创建<br />(3) Field已经存在，旧的值被覆盖 | HSET key field value <br />*注意：这里的 key是不允许重复的* |
| HGET    | (1)返回哈希表Key中给定域Field的值                            | HGET key field                                              |
| HDEL    | (1)删除哈希表Key中的一个或多个指定域<br /> (2)不存在的域将被忽略 | HDEL key filed [field...]                                   |
| HEXISTS | (1)查看哈希表Key中，给定域Field是否存在，存在返回1，不存在返回0 | HEXISTS key field                                           |
| HGETALL | (1)返回哈希表Key中，所有的域和值                             | HGETALL key                                                 |
| HINCRBY | (1)为哈希表Key中的域Field加上增量Increment <br />(2) 其余同INCR命令 | HINCRYBY key filedincrement                                 |
| HKEYS   | (1)返回哈希表Key中的所有域                                   | HKEYS key                                                   |
| HLEN    | (1)返回哈希表Key中域的数量                                   | HLEN key                                                    |
| HMGET   | (1)返回哈希表Key中，一个或多个给定域的值<br /> (2)如果给定的域不存在于哈希表，那么返回一个nil值 | HMGET key field [field ...]                                 |
| HMSET   | (1)将多个Field-Value对设置到哈希表Key中<br /> (2) 会覆盖哈希表中已存在的域 (3) Key不存在，那么一个空哈希表会被创建并执行HMSET操作 | HMSET key field value [field value ..]                      |
| HVALS   | (1)返回哈希表Key中所有的域和值                               | HVALS key                                                   |

**HSET**

![image-20240111183108735](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111183108735.png)

对应的就是

![image-20240111183137030](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111183137030.png)

**HGET**

![image-20240111183343870](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111183343870.png)

**hgetall**

![image-20240111184228363](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111184228363.png)

**hkeys**

![image-20240111184500773](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111184500773.png)

这是普通键值对与哈希键值对的区别

**hlen**

*其结果就是这个key中的filed的个数*

**hmset**

![image-20240111185256411](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111185256411.png)



## 四、列表类型常用命令

| 命令      | 描述                                                         | 用法                                   |
| --------- | ------------------------------------------------------------ | -------------------------------------- |
| LPUSH     | (1)将一个或多个值Value插入到列表Key的表头 <br />(2) 如果有多个Value值，那么各个Value值按从左到右的顺序依次插入表头<br /> (3) Key不存在，一个空列表会被创建并执行LPUSH操作<br />(4)Key存在但不是列表类型，返回错误 | LPUSH key value [value ...             |
| LPUSHX    | (1)将值Value插入到列表Key的表头，当且仅当Key存在且为一个列表 (2)当Key不存在时，LPUSHX命令什么都不做 | LPUSHX key value                       |
| LPOP      | (1) 移除并返回列表Key的头元素                                | LPOP key                               |
| LRANGE    | (1)返回列表Key中指定区间内的元素，区间以偏移量Start和Stop指定<br /> (2)Start和Stop都以0为底开始计数<br /> (3)可使用负数下标，-1表示列表最后一个元素，-2表示列表倒数第二个元素，以此类推 <br />(4)Start大于列表最大下标，返回空列表 <br />(5) Stop大于列表最大下标，Stop=列表最大下标 | LRANGE key start stop                  |
| LREM      | (1)根据Count的值，移除列表中与Value相等的元素<br /> (2) Count>0表示从头到尾搜索，移除与Value相等的元素，数量为Count<br /> (3) Count<0表示从尾到头搜索，移除与Value相等的元素，数量为Count<br />(4) Count=0表示移除表中所有与Value相等的元素 | LREM key count value                   |
| LSET      | (1)将列表Key下标为index的元素值设为Value<br /> (2) Index参数超出范围，或对一个空列表进行LSET时，返回错误 | LSET key index value                   |
| LINDEX    | (1)返回列表Key中，下标为Index的元素                          | LINDEX keyindex                        |
| LINSERT   | (1)将值Value插入列表Key中，位于Pivot前面或者后面<br /> (2) Pivot不存在于列表Key时，不执行任何操作<br /> (3) Key不存在，不执行任何操作 | LINSERT key BEFORE \|AFTER pivot value |
| LLEN      | (1)返回列表Key的长度<br /> (2) Key不存在，返回0              | LLEN key                               |
| LTRIM     | (1)对一个列表进行修剪，让列表只返回指定区间内的元素，不存在指定区间内的都将被移除 | LTRIM key start stop                   |
| RPOP      | (1)移除并返回列表Key的尾元素                                 | RPOP key                               |
| RPOPLPUSH | (在一个原子时间内，执行两个动作: <br />(1)将列表Source中最后一个元素弹出并返回给客户端<br /> (2)将Source弹出的元素插入到列表Desination，作为Destination列表的头元素 | RPOPLPUSH source destination           |
| RPUSH     | (1)将一个或多个值Value插入到列表Key的表尾                    | RPUSH key value [value ...]            |
| RPUSHX    | (1)将Value插入到列表Key的表尾，当且仅当Key存在并且是一个列表<br /> (2) Key不存在RPUSHX什么都不做 | RPUSHX key value                       |

列表插入的值是可以重复的

**lpush（左插入） rpush（右插入）**

![image-20240111190726174](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111190726174.png)

**lpop（左删） rpop（右删）**

**lindex lrange**

*lindex：取下标为多少的值   lrange：取下标区域范围内的值*

![image-20240111191941688](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111191941688.png)

**linsert**

*在什么前面或什么后面插入值*

![image-20240111192245769](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111192245769.png)





## 五、其他常用命令列表

| 命令     | 描述                                                         | 用法                                                      |
| -------- | ------------------------------------------------------------ | --------------------------------------------------------- |
| SADD     | (1)将一个或多个member元素加入到key中，已存在在集合的member将被忽略<br /> (2)假如key不存在，则只创建一个只包含member元素做成员的集合<br /> (3)当key不是集合类型时，将返回一个错误 | SADD key number [member ...]                              |
| SCARD    | (1)返回key对应的集合中的元素数量                             | SCARD key                                                 |
| SREM     | (1)移除集合key中的一个或多个member元素，不存在的member将被忽略 | SREM key member[member ...]                               |
| SMEMBERS | (1)返回集合key中的所有成员<br /> (2)不存在的key被视为空集    | SMEMBERS key                                              |
| ZADD     | (1)将一个或多个member元素及其score值加入有序集key中 <br />(2) 如果member已经是有序集的成员，那么更新member对应的score并重新插入member保证member在正确的位置上<br />(3) score可以是整数值或双精度浮点数 | ZADD key score member [[score member] [score member] ...] |
| ZCARD    | (1)返回有序集key的元素个数                                   | ZCARD key                                                 |
| ZCOUNT   | (1)返回有序集key中，score值>=min且<=max的成员的数量          | ZCOUNT keymin max                                         |
| ZRANGE   | (1)返回有序集key中指定区间内的成员，成员位置按score从小到大排序<br /> (2)具有相同score值的成员按字典序排列<br /> (3) 需要成员按core从大到小排列，使用ZREVRANGE命令<br />(4)下标参数start和stop都以0为底，也可以用负数，-1表示最后一个成员，-2表示倒数第二个成员 <br />(5)可通过WITHSCORES选项让成员和它的score值一并返回 | ZRANGE key start stop [WITHSCORES]                        |
| ZRANK    | (1)返回有序集key中成员member的排名，有序集合成员按score值从小到大排列 <br />(2)排名以0为底，即score最小的成员排名为0 <br />(3) ZREVRANK命令可将成员按score值从大到小排名 | ZRANK key number                                          |
| ZREM     | (1)移除有序集key中的一个或多个成员，不存在的成员将被忽略<br /> (2) 当key存在但不是有序集时，返回错误 | ZREM key<br/>member                                       |
| SELECT   | (1)切换到指定数据库，数据库索引index用数字指定，以0作为起始索引值 (2) 默认使用0号数据库 | SELECT index                                              |
| DBSIZE   | (1) 返回当前数据库的Key的数量                                | DBSIZE                                                    |
| SHUTDOWN | (1)停止所有客户端<br /> (2) 如果至少有一个保存点在等待，执行SAVE命令 <br />(3)如果AOF选项被打开，更新AOF文件<br /> (4)关闭Redis服务器 | SHUTDOWN [SAVE \| NOSAVE]                                 |
| FLUSHDB  | (1) 清空当前数据库中的所有Key                                | FLUSHDB                                                   |
| FLUSHALL | (1)清空整个 Redis 服务器的数据 (删除所有数据库的所有Key)     | FLUSHALL                                                  |

集合插入的值是不能重复的

**sadd（普通集合）**

![image-20240111194004796](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111194004796.png)

**zadd（有序集合）**

![image-20240111195202994](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111195202994.png)

*顺序只与score有关*

**zrange zrevrange**

![image-20240111195732974](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111195732974.png)

*注意：其中 `zrevrange stringzset 1 4` 表示从下标为 4 到 1 输出，而 `zrange stringzset 1 4` 就是从下标为 1 到 4 输出。其中 withscores 的意思就是输出值的同时价格scores一同输出*

**zrem**

![image-20240111200413756](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240111200413756.png)
