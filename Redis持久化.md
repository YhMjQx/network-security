# ==Redis持久化与主从复制==

由于Redis是将数据存储在内存中，为了防止有一些重要数据会丢失，或者说数据丢失之后可以备份，我们便使用Redis的持久化

## Redis持久化

#### 一、Redis持久化是什么

所谓redsi持久化，就是将数据保存到永久性存储介质上，在特定时间将保存的数据进行恢复的机制

#### 二、为什么要进行持久化

防止数据的意外丢失，保证数据是安全的

#### 三、证明Redis持久化的存在

Redis为了追求搞笑的读写速度，默认情况下所有的增删改，都是在内存中进行的，断电以后Redis的数据会丢失，丢失的数据是保存在内存中的数据。但是我们会发现，在关闭了Redis服务器之后，再次启动Redis服务，之前的 key还存在，也就是说，Redis是有持久化功能的

#### 四、Redis中持久化的方式，有两种

1.RDB（存快照）

2.AOF（存日志）

### Redis持久化之RDB

这是Redis默认的持久化策略，策略实施原则如下:

在服务器停掉之后，将服务器中暂存的数据保存在 dump.rdb 文件中，当再次开启服务器之后会从硬盘中加载该文件。但值得注意的是，正常情况是只有在服务正常关闭之后才会将内存中数据加载到该文件中，但是如果服务器没来得及正常关闭就崩溃了，那会是个什么情况呢？

所以接下来就轮到我们来自己**配置一下.rdb 文件**的策略

#### 一、redis.conf文件寻找 save配置

RDB启动方式：save命令

每当执行 save 命令的时候，都会立刻进行一次快照保存，就是把运行时Redis服务内存中的所有 key-value存储起来

#### 二、修改save配置

![image-20240112143418596](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112143418596.png)

我们可以让60秒内当有5个key发生变化就执行一个save命令

#### 三、直接使用 bgsave

在使用过程中我们其实可以直接使用**save**在前台保存，如果数据量大则使用**bgsave 直接后台保存**，不影响命令行的使用

![image-20240112144532837](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112144532837.png)

![image-20240112144559102](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112144559102.png)

我们可以看到，直接save之后也是很方便的，还有bgsave

![image-20240112144905028](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112144905028.png)

![image-20240112144923571](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112144923571.png)

**rdb数据的恢复时机：redis启动时**

#### save持久化数据的缺点：

我们都知道redis是单线程模型，那么在数据量过大的情况下执行save指令，save指令执行的时间就会很长，这样排在save之后的其他指令只能长时间被阻塞，这样会拉低服务器性能

![image-20240112145940121](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112145940121.png)

所以线上环境中，**不建议使用save命令，并禁止使用save命令**

**正确的RDB启动方式应该是 bgsave** 

针对于save命令的缺点，需要使用 **bgsave** 命令来在后台进行redis数据快照备份

![image-20240112150122022](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112150122022.png)

**注意：bgsave命令是针对save阻塞问题做的优化，Redis内容所有涉及到rdb的操作都采用bgsave，save命令以后可以放弃使用了**

**RDB启动方式：自动执行**

执行策略就是之前说的save配置

**注意：**

**1.save自动执行时，执行的bgsave**

**2.在执行flushall命令的时候，无论是否满足条件，都会立即生成一个新的空的dump.rdb来覆盖以前的dump.rdb，另外多说一句：flushall很危险，工作中不要用**

#### RDB优点

RDB是一个紧凑压缩的二进制文件，存储效率较高

RDB内部存储的是Redis在某个时间点的数据快照，非常适合于数据备份，全量复制的场景

RDB恢复数据的速度要比AOF快很多

应用：将RDB文件的单独拷贝到远程机器中，用于灾难恢复

#### RDB缺点

RDB方式无论是执行指令还是利用配置，都无法做到实时持久化，有丢失最新数据的风险

bgsave指令每次运行都要fork一个子进程，要牺牲掉一些性能

redis的众多版本中未进行RDB文件格式的统一，在各个版本的服务之间会有不兼容的现象

RDB是基于快照的思想，每次读写都是全部数据，当数据量巨大时，效率非常低（存储速度慢）

### Redis持久化之AOF

AOF文件的存储机制是将客户端在Redis中所做过的指令进行复制存储，就类似于MySQL数据库中存储表或者什么的时候，其sql文件其实就是建表语句啥的

#### 一、AOF

AOF（append only file）持久化：以独立日志的方式记录每次写命令（也就是记录数据产生的过程），重启时再重新执行AOF文件中的命令，达到数据恢复的目的

#### 二、AOF写数据的三种策略

always 每次写入操作均同步到AOF文件中，数据零误差，性能较低

everysec 每秒同步到AOF文件中，数据准确性较高，性能较高，最多丢失1秒的数据

no 由系统控制如何将命令同步到AOF文件中，整个过程不可控

#### 三、AOF功能开启

appendonly yes | no 是否开启AOF功能（进入redis.conf文件中进行设置）

appendfsync always | everysec | no AOF写数据的策略

appendfilename filename建议配置为appendonly-端口号.aof

设置好之后保存退出重启Redis服务器即可，ll即可看见该文件，而且 AOF 开启之后就不会再使用 RDB 了



![image-20240112162348805](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112162348805.png)

![image-20240112162334362](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112162334362.png)

![image-20240112162400113](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112162400113.png)

#### 四、AOF写数据遇到的问题

如果遇到同一个指令重复很多写入操作，那么对于aof来说，全都保存下来明显是没有必要的，于是AOF提供了一个功能叫做 AOF重写 来解决这个问题

比如，我set了一个key，然后del了一个key，AOF就会优化作为根本没有这个key出现过

#### 五、AOF文件格式

![image-20240112162858264](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112162858264.png)

其中 *2 和 *10 分别表示接下来两条数据为一条指令，接下来10条数据为一条指令

$x 表示接下来的一个指令字符串的长度

#### 六、AOF重写

随着命令不断写入AOF文件，AOF文件会越来越大，为了解决这个问题，redis引入了AOF重写机制来压缩AOF文件体积。AOF文件重写是将Redis进程内的数据转化为写命令同步更新到AOF文件的过程。简单点说**就是将对同一个数据的若干条命令合并为最终结果所对应的那一条命令！**这样即将低了磁盘占用量，提高磁盘利用率，又减少了数据恢复所用的时间

##### AOF重写规则

1.进程内已超时的数据不再写入文件

2.忽略无效指令，重写时使用进程内数据直接生成，这样新的AOF文件只保留最终的写入数据

3.对同一数据的多条命令合并为一条命令

### 七、RDB与AOF的区别

![image-20240112181020602](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240112181020602.png)

### 八、RDB与AOF如何抉择

#### 1.如果要求对整体数据特别敏感，建议使用AOF

AOF持久化策略采用everyseconds的话，每秒备份一次命令。该策略是redis保持很好地性能，当出现问题时，最多丢失1秒内的数据。

#### 2.如果对某时段内的数据特别敏感，建议使用RDB

由开发或者运维人员手工使用RDB维护，可以具有针对性的对于某时段内的数据进行灾难备份，且恢复速度较快。所以阶段数据持久化通常使用RDB

如果同时开启RDB和AOF，redis优先使用AOF来恢复数据