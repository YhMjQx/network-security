[TOC]



# ==Suricata规则字段解析==

教材内容

#### 一、Payload关键字

##### 1、content

可以匹配所有字符；从 a 到 z，大写和小写以及所有特殊标志。针对一些特殊符号或中文等，需要使用十六进制进行匹配，写法：|3A| 表示冒号，以此类推。`|0D| -> \r ， |0A| -> \n`

另外，默认情况下，content 中给定的值是包含运算（模糊匹配，但不是正则表达式），同时也可以在content后面具体指定对应的字段，比如http_stat_code， http_uri，等进行更精准的匹配。另外，还可以辅助使用 startswith，endswith来进行更加精准地匹配。`content: “GET"; startswith; http_request_line;`

##### 2、nocase

不区分大小写，通常放在 content 后面

##### 3、dsize

有效载荷的内容的长度，基本用法：`dsize:[<>!]number; || dsize:min<>max;`

（1）dsize: 100，表示有效载荷的内容的长度大小等于100

（2）`dsize: <100` `dsize: >100 ` `dsize: !100`表示 dsize不等于100 `dsize: 100<>200` 表示dsize在100 ~ 200 之间

```yaml
alert tcp any any -> any any (msg:"dsize less than value"; dsize:<10; sid:2; rev:1;)
```

##### 4、bsize

可以提取任意字段中的内容长度，并进行判断，如：

```yaml
alert dns any any -> any any (msg:"bsize less than value"; dns.query; content:"google.com"; bsize:<25; sid:2; rev:1;)
```

##### 5、pcre

标准的正则表达式匹配，基本语法：`pcre:"/<regex>/opts";` ，需要注意两点：

（1）必须使用 / 进行包裹，最后的位置可以设置选项。

（2）通常情况下，pcre最好不要单独存在，否则会影响匹配性能。最好先有content做初次筛选，再用pcre进行更精准的匹配。

##### 6、其他

url_decode，可以对URL地址或POST请求数据等进行过URL编码的数据进行解码处理

#### 二、转码关键字

> 将流量数据转换为对应的字符之后，再与 content 对比

##### 1、to_md5

##### 2、to_sha1

##### 3、url_encode

##### 4、base64_decode

对字段的值进行Base64解码，并在解码后进行匹配（前提：知道解码后具体的内容）

```yaml
Buffer content:
http_uri = "GET /en/somestring&dGVzdAo=¬_base64"

Rule:
alert http any any -> any any (msg:"Example"; content:"somestring"; http_uri; base64_decode:bytes 8, offset 1, relative; base64_data; content:"test"; sid:10001; rev:1;)
#意思是，根据content定位到somestring后面的位置，然后再往后移动一位，然后往后取8位字符并对其进行base64解码，然后与content匹配
```



#### 三、Flow流关键字

##### 1、flowbits：

对数据包进行匹配后设置一个标识位，在下一个数据名检查对应标识是否存在来决定是否预警。

![image-20220726153847989](https://gitee.com/ymq_typroa/typroa/raw/main/20220726153848.png)

##### 2、flow

如：flow: established,to_server; established表示连接已经建立，to_server表示客户端连接到服务器。

##### 3、flowint

（1）基本语法

```yaml
flowint: name, < +,-,=,>,<,>=,<=,==, != >, value;    = 号用于赋初始值  +- 数学运算  其他 数字比较判断
flowint: name, (isset|notset);    用于判断某个变量是否已经初始化
```

（2）用法示例

```yaml
alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg: "出现404错误"; content: "404"; http_stat_code; classtype: HTTP-status-404; flowint: urlcount, notset; flowint: urlcount, =, 1; sid: 561003; noalert;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg: "出现404错误"; content: "404"; http_stat_code; classtype: HTTP-status-404; flowint: urlcount, isset; flowint: urlcount, +, 1; sid: 561004; noalert;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg: "出现404错误"; content: "404"; http_stat_code; classtype: Web-Url-Scan; flowint: urlcount, >=, 5; sid: 561005; rev: 2;)
```

![image-20250215234424991](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215234424991.png)

![image-20250215234439895](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215234439895.png)

![image-20250215235137528](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250215235137528.png)

> 上述规则用来做阈值预警存在的问题：无法设定具体某个时间段，所以针对不限时累加有效，针对限时阈值，则无效，此时可以使用threshold关键字进行阈值设置。

##### 4、stream_size

整个数据包的大小的检测和判断，可以使用比较运算符，与dsize不同，dsize主要是判断payload，stream_size则是整个数据包

#### 四、阈值关键字

> limit 限制警报的数量

##### 1、threshold

```yaml
threshold: type <threshold|limit|both>    默认建议使用threshold或者both, 如果设置为limit，则会限制警告的数量，而both则是两者的结合，是一个不错的选项。

track <by_src|by_dst|by_rule|by_both>     track 优先使用by_src，by_src可以有效过滤源IP，类似于Wazuh的 <same_source_ip ></same_source_ip>。

count <N>, seconds <T>                    T秒内连续出现N次，则触发警告
```

```yaml
threshold: type <threshold|limit|both>, track <by_src|by_dst|by_rule|by_both>, count <N>, seconds <T>
```

##### 2、实例

```yaml
alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg: "出现404错误"; content: "404"; http_stat_code; classtype:  Web-Url-Scan; threshold: type threshold, track by_src, count 5, seconds 30; sid: 561006; rev: 3;)
```

只需 30 秒内 访问出现5 次 404 即可进行预警

![image-20250216000136551](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250216000136551.png)

![image-20250216000150218](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250216000150218.png)

![image-20250216000226867](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250216000226867.png)

> 规则库下载：https://rules.emergingthreats.net/open/ https://www.snort.org/downloads
>
> 各种字段功能介绍：https://www.cnblogs.com/linagcheng/p/12559922.html

#### 五、Sticky Buffer字段

这是在新的Suricata版本中，提供了一套新的关键字，如http协议中的关键字，通常以 http.xxxx 而非 http_xxxx 这种形式存在，使得

在规则中其后面的内容只应该匹配这个关键字，不应该再有其他关键字出现。而非sticky buffer关键字则没有这个限制。

```yaml
alert http $EXTERNAL_NET any <> $HOME_NET 80 (msg:"出现404错误"; http.response_line; content:"Not Found"; nocase; content: "404";  sid: 561005;)
```

比如这条规则，使用http.response_line，这是一个sticky buffer关键字，后面跟的两个content都只对他进行匹配，虽然也是两个条件，但是条件只针对这个sticky buffer的关键字内容进行过滤。而后面除非遇到新的Sticky Buffer字段，再对该新字段进行匹配。