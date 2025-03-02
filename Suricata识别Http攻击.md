[TOC]



# ==Suricata识别Http攻击==

教材内容

#### 一、定义HTTP攻击类型

编辑 classification.config 文件，为HTTP协议增加以下类别，并设定相应的 priority

```
config classification: web-status-error, Web服务器状态异常, 4
config classification: web-scan-attack, Web页面扫描攻击, 2
config classification: web-sql-injection, SQL注入攻击, 1
config classification: web-xss-attack, XSS跨站攻击, 2
config classification: web-ssrf-attack, SSRF请求伪造, 2
config classification: web-shell-attack, 站点木马植入, 1
config classification: web-file-upload, 文件上传异常, 2
```

HTTP协议是明文传输的，流量特征存在于URL地址、POST请求正文、请求头或响应头、文件上传的情况（POST请求正文）

#### 二、URL地址栏异常

##### 1、状态码异常

主要检测403，404， 500等状态码异常行为，并设定针对连续404的扫描攻击特征。

```yaml
# 针对状态码异常的检测
alert http any any <> any $HTTP_PORTS (msg:"Web服务器404异常"; content:"404"; http_stat_code; classtype: web-status-error; sid: 5610001; rev: 1;)

alert http any any <> any $HTTP_PORTS (msg:"Web服务器403异常"; content:"403"; http_stat_code; classtype: web-status-error; sid: 5610002; rev: 1;)

alert http any any <> any $HTTP_PORTS (msg:"Web服务器500异常"; content:"500"; http_stat_code; classtype: web-status-error; sid: 5610003; rev: 1;)

# 如果持续404，则视为扫描攻击
alert http any any <> any $HTTP_PORTS (msg:"频繁404状态码，疑似扫描"; content:"404"; http_stat_code;threshold: type threshold, track by_src, count 5, seconds 20; classtype: web-scan-attack; sid: 5610004; rev: 1;)
```

##### 2、SQL注入攻击

```yaml
# 针对地址栏的SQL注入检测
alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg: "SQL注入攻击-select"; content:"select"; http_uri; nocase; classtype: web-sql-injection; sid: 5611001; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg: "SQL注入攻击-union"; content:"union"; http_uri; nocase; classtype: web-sql-injection; sid: 5611002; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg: "SQL注入攻击-order by"; content:"order by"; http_uri; nocase; classtype: web-sql-injection; sid: 5611003; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-database"; content:"database()"; http_uri; nocase; classtype: web-sql-injection; sid:5611004; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-version"; content:"version()"; http_uri; nocase; classtype: web-sql-injection; sid:5611005; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-user"; content:"user()"; http_uri; nocase; classtype: web-sql-injection; sid:5611006; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-updatexml"; content:"updatexml("; http_uri; nocase; classtype: web-sql-injection; sid:5611007; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-extract"; content:"extract("; http_uri; nocase; classtype: web-sql-injection; sid:5611008; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-if"; content:"if("; http_uri; nocase; classtype: web-sql-injection; sid:5611009; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-and"; content:"|20|and|20|"; http_uri; nocase; classtype: web-sql-injection; sid:5611010; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-or"; content:"|20|or|20|"; http_uri; nocase; classtype: web-sql-injection; sid:5611011; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-||"; content:"|7C 7C|"; http_uri; nocase; classtype: web-sql-injection; sid:5611012; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-&&"; content:"&&"; http_uri; nocase; classtype: web-sql-injection; sid:5611013; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-#"; content:"|23|"; http_uri; nocase; classtype: web-sql-injection; sid:5611014; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击---"; content:"--"; http_uri; pcre: "/\++|\s+/i"; nocase; classtype: web-sql-injection; sid:5611015; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-concat"; content:"concat("; http_uri; nocase; classtype: web-sql-injection; sid:5611016; rev: 1;)

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"SQL注入攻击-groupconcat"; content:"groupconcat("; http_uri; nocase; classtype: web-sql-injection; sid:5611017; rev: 1;)   

# 第二种写法：将多个关键特征整合到一条规则中  但十分不建议这么写，报错率极高
alert http any any -> $HOME_NET any (msg:"SQL注入攻击"; content:"/"; http_uri; pcre: "/union|select|from|updatexml|extract|database\(|user\(|version\(|information_schema|where|columns|--\s+|--\++|%20and%20|\s+or\s+|\|\||&&/i"; classtype: web-sql-injection; sid: 5611020; rev: 1;)
或
alert http $EXTERNAL_NET any <> $HOME_NET any (msg: "SQL注入攻击"; classtype: web-sql-injection; content: "/"; http_uri; pcre: "/union|select|from|order by|updatexml|extract|database\(|user\(|version\(|infromation_schema|where|column|--\s+|--\++|%20and%20|%20or%20|\|\||&&|concat\(|group_concat\(||23||if\(/i"; sid: 5611018; rev: 1;)
```

可以使用sqlmap或其他扫描工具进行规则测试（正向匹配攻击特征），除些以外，还需要进行反向测试（像普通用户一样进行功能使用，用以检测规则是否存在误报）。

![image-20250216221115563](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250216221115563.png)

##### 3、XSS攻击

```yaml
alert http any any -> any $HTTP_PORTS (msg:"XSS攻击"; content:"<script"; http_uri; nocase; classtype: web-xss-attack; sid:5612001; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"XSS攻击"; content:"</script>"; http_uri; nocase; classtype: web-xss-attack; sid:5612002; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"XSS攻击"; content:"javascript"; http_uri; nocase; classtype: web-xss-attack; sid:5612003; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"XSS攻击"; content:"alert("; http_uri; nocase; classtype: web-xss-attack; sid:5612004; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"XSS攻击"; content:"onload="; http_uri; nocase; classtype: web-xss-attack; sid:5612005; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"XSS攻击"; content:"=http|3A|//"; http_uri; nocase; classtype: web-xss-attack; sid:5612006; rev: 1;)

location.href=，document.cookie，onclick=，<iframe 。。。。。
```

![image-20250216231908201](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250216231908201.png)

##### 4、SSRF攻击

```yaml
alert http any any -> any $HTTP_PORTS (msg:"SSRF攻击"; content:"=file|3A|"; http_uri; nocase; classtype: web-ssrf-attack; sid:5613001; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"SSRF攻击"; content:"=http|3A|"; http_uri; nocase; classtype: web-ssrf-attack; sid:5613002; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"SSRF攻击"; content:"=https|3A|"; http_uri; nocase; classtype: web-ssrf-attack; sid:5613003; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"SSRF攻击"; content:"=dict|3A|"; http_uri; nocase; classtype: web-ssrf-attack; sid:5613004; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"SSRF攻击"; content:"=gopher|3A|"; http_uri; nocase; classtype: web-ssrf-attack; sid:5613005; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"SSRF攻击"; content:"=phar|3A|"; http_uri; nocase; classtype: web-ssrf-attack; sid:5613006; rev: 1;)

...............  部分文件包含也以类似的方式去检测 ................
```

![image-20250216231829257](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250216231829257.png)

![image-20250216232524003](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250216232524003.png)

![image-20250216232621505](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250216232621505.png)

##### 5、木马脚本

```yaml
alert http any any -> any $HTTP_PORTS (msg:"URL地址木马"; content:"<?"; http_uri; pcre: "/eval|assert|system\(|exec|$_POST|$_GET/i"; classtype: web-shell-attack; sid:5613007; rev: 1;)
```

#### 二、POST请求异常

##### 1、GET与POST

（1）http.method或http.request_line可以进行请求类型的区分， http.request_line; content:”GET”; startswith;

（2）标准POST请求的Content-Type: application/x-www-form-urlencoded，可以使用http.content_type进行区分

（3）POST请求的正文，默认情况下，至少存在一组key=value，可以使用正则表达式 .+=.+，当然，也可以是 php://input 这种，比如简单匹配： \S+ 或 \w+ 或 \S{5,}，在Suricata中，使用 http.request_body，或 http_client_body 关键字进行匹配

（4）针对文件上传，则可以匹配的特征会更多。

##### 2、请求正文处理

整体上的操作与GET请求一致，只是需要将http_uri换成http.request_body或http_client_body即可。

```yaml
# 处理POST请求，检查请求正文中的敏感字符
alert http any any -> any $HTTP_PORTS (msg:"SQL或XSS攻击-POST"; content: "="; http.request_body; pcre: "/union|select|from|updatexml|extract|database\(|user\(|version\(|information_schema|where|columns|--|#|\s+and\s+|\s+or\s+|\|\||&&|<script>|javascript|alert\(|location.href/i"; http.content_type; content: "x-www-form-urlencoded"; classtype: web-sql-injection; sid: 5614001; rev: 1;)

# 检测POST请求正文中是否存在木马关键字
alert http any any -> any $HTTP_PORTS (msg:"POST正文木马"; content: "="; http.request_body; pcre: "/eval|assert|system\(|exec|$_POST|$_GET/i"; http.content_type; content: "x-www-form-urlencoded"; classtype: web-shell-attack; sid: 5614002; rev: 1;)
```

##### 3、请求头处理

```yaml
# 检查content-type字段
alert http any any -> any $HTTP_PORTS (msg:"正在提交POST请求"; http.content_type; content: "x-www-form-urlencoded"; sid:5615001; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"SQL注入攻击-POST"; http.header; content: "="; pcre: "/union|select|from|updatexml|extract|database\(|user\(|version\(|information_schema|where|columns|--\s+|--\++|\s+and\s+|\s+or\s+|\|\||&&/i"; classtype: web-sql-injection; sid: 5615002; rev: 1;)
```

#### 三、业务逻辑检测

业务逻辑检测主要基于不同的应用系统，进行有针对性的规则设定，具有相当的独有性，无法通用于各种场景。

```yaml
alert http any any -> any $HTTP_PORTS (msg:"多次登录爆破"; content:"login.php"; http_uri; threshold: type threshold, track by_src, count 5, seconds 10; sid:561005;)

alert http any any <> any $HTTP_PORTS (msg:"多次登录爆破"; content:"login.html"; threshold: type threshold, track by_src, count 5, seconds 10; sid:561006;)
```