[TOC]



# ==XSS-labs闯关挑战==

**步骤**

- 第一步使用 `<>"` 测试一下是否对一些特殊字符进行了转义或实体转换等。
- 第二步，打开页面源代码，看真实的输入对应转换成了什么样子
- 再根据页面源代码的变化，进行payload的构造

```
<script>alert(1)<script>

" onclick="alert(1)

' onclick='alert(1)

" onclick="alert(1)

" /><a href=javascript:alert(1)>click here</a>

发现对小写的on变为o_n,najiuchagshi换大写的
" ONclick="alert(1)

发现直接删掉了on，那就双写绕过
" oONnclick="alert(1) 

发现value中特殊字符都做了实体转换，但其他的并没有，那我也实体转换，你该如何应对
&#x006a;&#x0061;&#x0076;&#x0061;&#x0073;&#x0063;&#x0072;&#x0069;&#x0070;&#x0074;&#x003a;&#x0061;&#x006c;&#x0065;&#x0072;&#x0074;&#x0028;&#x0031;&#x0029;


```

- 第九题单独讲一下

这一把单纯哟个实体转换就不行了，会告诉我们输入的链接不合法，如果我们输入正常的链接就不会爆出这样的问题，哪这两者差别在哪里呢，差别就在于是否存在 `http://` 这样的字眼，我们给的链接也就是payload一般不会写 `http://` 这样的内容对吧，就根据这个我们就没法成功，那现在我们知道了，我们就去再尝试一下

首先尝试更换 `http://`  的位置，尝试放在最后，这样方便注释掉，然后前面对我们的payload进行实体编码

```
&#x006a;&#x0061;&#x0076;&#x0061;&#x0073;&#x0063;&#x0072;&#x0069;&#x0070;&#x0074;&#x003a;&#x0061;&#x006c;&#x0065;&#x0072;&#x0074;&#x0028;&#x0031;&#x0029;;//http://
这里是对javascript:alert(1)进行实体编码然后加上 ;//http:// 加分号的目的是为了可以实现注释

" </a><script>alert(1)<script><img src=" 本来我也想用这种标签闭合的方式来注入，但是发现这样http:// 就不知道该往哪放了
```

- 第十题

页面没有让我们输入的地方

![image-20240725221534332](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240725221534332.png)

查看页面源代码

![image-20240725221605576](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240725221605576.png)

竟然有隐藏的表单

要想能够正常提交数据，我们需要有输入的地方还要有可以提交的功能，由于是form表单形式提交，于是我们需要将隐藏的表单显现出来并自主添加提交按钮

![image-20240725222209064](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240725222209064.png)

全部将hidden修改为text并添加按钮，尝试提交一些值

![image-20240725222255486](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240725222255486.png)

此时此刻，整个页面止呕这两个地方发生了改变

![image-20240725222349125](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240725222349125.png)

所以我们可以确定注入点在t_sort这个位置

于是尝试特殊字符

![image-20240725222613819](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240725222613819.png)

竟然只剩下了一个双引号，那么标签的东西肯定是用不了了，那就试试单击事件，但是既然是单击事件，那我们还需要点击，那这个hidden的属性依旧需要删掉。

**payload如下**

`clickhere"%20onclick="alert(1)"%20type="button`

![image-20240725222953696](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240725222953696.png)

注意双引号的闭合

- 第十一题与第十题类似

打开题目直接看源码

![image-20240726144514276](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726144514276.png)

发现依旧是表单的形式，而且我们在url地址中的输入，页面和源代码中根本没有输出，就很奇怪，所以我们还是先用第十题的方式

![image-20240726145216549](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726145216549.png)

输入和内容点击提交，配合F12发现，有变换的只有后两个输入框。而我们发现第四个输入框的内容不正是refer的意思吗

![image-20240726145123151](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726145123151.png)

我们先尝试在第三个输入框进行注入

<>" 全部被实体转换，并且有引号，因此无法闭合绕过

所以再考虑第四个输入框的注入

依旧是修改页面源码可以让我们输入并提交

![image-20240726155400304](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726155400304.png)

- 第十二题

依旧是和上面的题目类似的，这次是user-agent注入

![image-20240726160339360](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726160339360.png)

这内容一看就是user-agent，因此我们在http请求头中修改user-agent字段的值为payload然后发送即可

![image-20240726163937793](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726163937793.png)

- 第十三题

![image-20240726175527735](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726175527735.png)

依旧是form表单和hidden

hidden改为text，然后自己添加button点击提交，查看页面源代码

![image-20240726184244743](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726184244743.png)

依旧是第三输入框和第四输入框，估计第三输入框输入的内容依旧会被转码，无法闭合或绕过。

![image-20240726185158434](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726185158434.png)

我们可以试试看

![image-20240726185222162](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726185222162.png)

果然

所以还是把注意放在第四输入框

![](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726194046914.png)

ok，抓包发现请求中的Cookie真的是call me maybe，ok这次是Cookie注入

**" onclick="alert(1)" type="button**

![image-20240726194628552](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726194628552.png)

可惜我没有Live HTTP headers，没法在浏览器里面直接点，所以就用F12填一下payload发现成功。

![image-20240726194757626](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726194757626.png)

- 第十四题，页面图片访问不了，这题没法做
- 第十五题涉及到一些没学过的框架知识，做不了，参数主要是包含一个页面，利用别人的页面的注入点作为自己的注入点

- 第十六题

不管注入什么我们都会发现很多东西都被替换成了 `&nbsp;` 这是空格的实体字符，这个题的考点就在于空格的替换 又因为在html中 %0A 和 %0D  也可作为空格，所以我们也可以通过这些来绕过

所以payload为 `<a%0Aonmouseover="alert">`

![image-20240726210925668](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726210925668.png)

- 第十七题

url为 `http://192.168.1.9/xss-labs/level17.php?arg01=a&arg02=b`

但是页面源代码为

![image-20240726211250173](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726211250173.png)

我们可以看到，两个参数都写在了这里，并且参数的值并没有添加双引号，我们也就不用考虑双引号的闭合绕过的问题，直接上payload `arg02= onmouseover=alert(1)`  鼠标划过即可

![image-20240726212551508](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726212551508.png)

- 第十八题，先看源代码

![image-20240726212750294](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726212750294.png)

和十七题差不多，payload也是一样 `arg02= onmouseover=alert(1)`

![image-20240726212930095](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726212930095.png)

- 第十九题，直接看源码，好像还是一样的

![image-20240726213014002](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726213014002.png)

用前两题的payload发现被添加了双引号，我们尝试双引号注入看是否会被转码等

![image-20240726213140676](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726213140676.png)

果然双引号被绕过了，进行了实体编码，这种情况下我们是无法使用双引号的闭合来绕过的

![image-20240726213350276](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726213350276.png)

这里就涉及到flash插件的知识，没学过可恶

答案是 `arg01=version&arg02=<a href="javascript:alert(1)">111</a>`

![image-20240726213912036](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240726213912036.png)

- 第二十关

依旧是插件不支持
