[TOC]



# ==Struts2漏洞S2-001==

复现过程

#### 访问首页输入OGNL表达式进行漏洞探测

![image-20250202140218713](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202140218713.png)

submit之后就变成了

![image-20250202140249479](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202140249479.png)

看到这样说明该处存在漏洞

#### 同样使用 burp 进行抓包重放测试

![image-20250202140831826](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202140831826.png)

> 不过值得注意的是，在burp中进行重访的时候，记得要将username字段进行 URL 转码发送，否则 % 与 + 在 前端页面中代表的含义会使得响应错误，比如这里会响应 500 的响应码

#### 查看当前目录

payload 如下：

![image-20250202144158359](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202144158359.png)

![image-20250202144127967](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202144127967.png)

我们可以看到 web 站点的路径就在页面中渲染出来了

#### 命令执行

payloda 如下：

![image-20250202144253729](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202144253729.png)

![image-20250202144444709](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202144444709.png)

![image-20250202144508790](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202144508790.png)

####  命令执行-反弹shell

![image-20250202144715524](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202144715524.png)

然后 在 burp 中对如图所示的 POC 进行 URL 编码即可

![image-20250202144941379](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202144941379.png)

![image-20250202144952917](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250202144952917.png)

> ### 一、漏洞概述
>
> Struts2是一个基于MVC设计模式的Web应用框架，它允许开发者通过标签库在JSP文件中使用OGNL（Object-Graph Navigation Language，对象图导航语言）表达式来访问和操作值栈中的数据。S2-001漏洞源于Struts2框架中的一个标签处理功能：altSyntax。当altSyntax功能开启时（默认开启），Struts2会对标签中的OGNL表达式进行解析并执行。如果用户在表单中输入了恶意的OGNL表达式，并且在表单验证失败时页面重新加载，那么这些表达式就可能会被服务器执行，从而导致远程代码执行漏洞。
>
> ### 二、漏洞原理
>
> 1. **用户提交表单**：用户在Web应用的登录或注册页面提交表单数据。
> 2. **表单验证失败**：如果提交的表单数据不符合验证规则，表单验证将失败。
> 3. **服务器处理**：在表单验证失败后，服务器会将用户之前提交的参数值使用OGNL表达式进行解析，并重新填充到对应的表单数据中。
> 4. **OGNL表达式执行**：如果用户在表单中输入了恶意的OGNL表达式，这些表达式在服务器解析时将被执行。
> 5. **远程代码执行**：通过构造特定的OGNL表达式，攻击者可以执行任意命令，获取服务器敏感信息，甚至控制服务器。