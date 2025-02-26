[TOC]



# ==Suricata冰蝎流量分析==

我的 Fiddler 抓不到 冰蝎的流量.......

只能用 wireshark 了......

我们发现 ，冰蝎发送的流量竟然是 tcp 层面的流量

![image-20250218002149867](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250218002149867.png)

而且，就仅仅一个 请求 + 响应，内容占据了 416kb，说明 冰蝎的流量真的很大

![image-20250218002351214](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250218002351214.png)

##### 1、流量特征

（1）从请求头和响应头并不能看到明显的特征。

（2）请求正文的长度很长，有点与真实情况不符。

（3）不存在key=value&key=value的格式。

（4）冰蝎的流量全部是Base64编码（先加密，再Base64），此类情况通常只出现在一种情况下：文件上传时。但是，在响应当中，通常也不太会使用Base64编码。

##### 2、识别规则

（1）正文长度过长的规则

> 由于 dsize 不支持 http 协议，所以这里使用了 tcp 的协议

通过http.content_type为x-www-form-urlencoded时（表明不是文件上传），dsize长度多于4000时，有可能是异常流量。

```yaml
alert tcp any any -> $HOME_NET 80 (msg:"疑似冰蝎流量"; dsize: >1000; classtype: web-other-alert; sid: 5618004; rev: 1;)
```

（2）不存在key=value&key=value的格式，Base64也存在=号，但是Base64的=号在末尾

```yaml
alert http any any -> $HOME_NET 80 (msg:"疑似冰蝎流量"; http.request_body; content: !"="; depth: 100; classtype: web-shell-attack; sid: 5618005; rev: 1;)
```

这个 depth 是为了担心，正常情况下， 如果 depth 再大点的话，就会匹配到正常流量当中的 = ，所以这里只设置了 100

![image-20250218002759364](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250218002759364.png)

（3）POST正文全是Base64

```yaml
alert http any any -> $HOME_NET 80 (msg:"疑似冰蝎流量"; http.request_body; pcre: "/^[A-Za-z0-9\+\/]{1000,}=*$/"; classtype: web-shell-attack; sid: 5618006; rev: 1;)
```

（4）将 = 的判断与全文均是base64的判断整合

```yaml
alert http $EXTERNAL_NET any -> $HOME_NET $HTTP_PORTS (msg:"冰蝎"; http.request_body; content:!"="; depth:100; pcre:"/^[A-Za-z0-9\+\/]{2222,}=*$/"; classtype:web-shell-attack; sid:5618005;rev:1;) 
```

![image-20250218003635961](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250218003635961.png)