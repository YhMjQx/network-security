[TOC]



# ==Suricata处理文件上传流量==

教材内容

#### 一、文件上传特征

![image-20250217134357168](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250217134357168.png)



（1）请求类型是POST请求，使用 http.method 或 http.request_line 可以进行匹配

（2）Content-Type: multipart/form-data; boundary=XXXXX，这是文件上传独特的特征

（3）请求正文部分存在boundary的值：比如：boundary=————————————XXXXX

（4）正文部分存在：Content-Disposition: form-data; name=”.+”; filename=”.+”

（5）请求正文部分如果是存在文本，文本数据是可以用于检测依据

以下Suricata的规则用于检测是否存在文件上传。

```yaml
alert http any any -> any $HTTP_PORTS (msg:"正在上传文件"; http.method; content:"POST"; http.content_type; content: "multipart/form-data"; http.request_body; content: "Content-Disposition"; classtype: web-file-upload; sid:5616001; rev: 1;)
```

#### 二、文件上传异常

##### 1、木马检测

```yaml
# 检测上传内容中是否存在木马相关的关键字

alert http any any -> any $HTTP_PORTS (msg:"疑似上传木马"; http.method; content:"POST"; http.content_type; content: "multipart/form-data"; http.request_body; content: "Content-Disposition"; http.request_body; pcre: "/eval|assert|system\(|exec|$_POST|$_GET/i"; classtype: web-file-upload; sid:5616002; rev: 1;)
```

![image-20250217141628230](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250217141628230.png)

##### 2、文件保存

如果攻击者试图通过上传页面上传图片马或木马程序，那么我们还可以通过配置将上传成功的文件保存起来。先修改一下配置：

```
- file-store:    
	version: 2    
	enabled: yes
```

![image-20250217141828401](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250217141828401.png)

先执行一个最简单的文件保存的规则：

```yaml
alert http any any -> any $HTTP_PORTS (msg:"上传文件且已保存"; filestore; classtype: web-file-upload; sid:5616003; rev: 1;)
```

然后我们上传一个文件试试：

![image-20250217142316236](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250217142316236.png)

![image-20250217142343216](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250217142343216.png)

可以通过以下命令过滤并找到保存后的文件信息：

```shell
cat eve.json | grep 'event_type":"fileinfo' | grep 'stored":true' | grep rulesid

记得替换对应的 rulesid
```

![image-20250217142633864](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250217142633864.png)

然后 保存文件时，创建的256个目录命名就是从 00-ff ，而文件应该保存至哪个文件夹，是根据文件名称 使用 sha256 处理之后，文件名称前两个字符进行匹配，比如这里，我上传的文件处理之后前两个字符是 94，那么我的这个文件就会保存在 94 这个目录下。

运行 `du -sh *` 进行查看

![image-20250217142950101](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250217142950101.png)

![image-20250217143007770](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250217143007770.png)



并且在预警信息中添加一条：filestore; 如果需要过滤后缀名，也可以使用 fileext: “gif”等，如上述检测发现存在木马上传的情况，则直接将该上传文件保存起来（尤其是图片马）

```yaml
alert http any any -> any $HTTP_PORTS (msg:"疑似上传木马"; content: "<?"; http.request_body; pcre: "/eval|assert|system\(|exec|$_POST|$_GET/i"; http.content_type; content: "multipart/form-data"; filestore; classtype: web-file-upload; sid:5616002; rev: 1;)
```

同时，将在eve.json中写入一条日志信息，并且在 /var/log/suricata 目录下创建 filestore 的新目录，日志信息如下：

```json
{"timestamp":"2021-12-24T11:40:33.291177+0800","flow_id":1799641571118018,"in_iface":"ens33","event_type":"fileinfo","src_ip":"192.168.112.1","src_port":32588,"dest_ip":"192.168.112.195","dest_port":80,"proto":"TCP","http":{"hostname":"192.168.112.195","url":"/security/reg.php","http_user_agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0","http_content_type":"text/html","http_refer":"http://192.168.112.195/security/reg.html","http_method":"POST","protocol":"HTTP/1.1","status":200,"length":187},"app_proto":"http","fileinfo":{"filename":"web-other.jpg","sid":[5616002],"gaps":false,"state":"CLOSED","md5":"603d8e3287ef6d4c04602c819acf6a9a","sha256":"046a744864d044b7c453f0c4f2d911038ce7623a6b5e44d0a0702f10eade4edc","stored":true,"file_id":1,"size":106732,"tx_id":0}}
```

从上述结果可以看出以下5条关键信息：

（1）攻击者试图上传木马入驻，并触发了5616002警告

（2）上传文件所在页面地址为：/security/reg.php

（3）文件已经成功保存：”stored”:true

（4）文件名为：046a744864d044b7c453f0c4f2d911038ce7623a6b5e44d0a0702f10eade4edc

（5）文件所在文件夹为 SHA256 的前两位字符：即：/var/log/suricata/filestore/04 目录下

获取到上述信息后，我们便可以进入该目录去查看文件信息，确认是否存在木马程序。

##### 3、可疑预警

另外，也可以使用以下规则针对用户试图上传一些可能存在木马的文件进行检测和拦截，例如：

```yaml
alert http any any -> any $HTTP_PORTS (msg:"试图上传可疑文件-php"; fileext:"php"; filestore; sid:5616005; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"试图上传可疑文件-phtml"; fileext:"phtml"; filestore; sid:5616006; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"试图上传可疑文件-php5"; fileext:"php5"; filestore; sid:5616007; rev: 1;)

alert http any any -> any $HTTP_PORTS (msg:"试图上传可疑文件-jsp"; fileext:"jsp"; filestore; sid:5616008; rev: 1;)
```

fileext 默认不区分大小写，且不支持正则匹配