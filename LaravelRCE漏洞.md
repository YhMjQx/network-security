[TOC]



# ==LaravelRCE漏洞==

![image-20250204130906106](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204130906106.png)![image-20250204131026586](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204131026586.png)![image-20250204131546190](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204131546190.png)![image-20250204131337732](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204131337732.png)![image-20250204131731216](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204131731216.png)![image-20250204132129654](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204132129654.png)![image-20250204132301496](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204132301496.png)![image-20250204132346855](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204132346855.png)![image-20250204132530949](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204132530949.png)![image-20250204133053914](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204133053914.png)![image-20250204134105044](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204134105044.png)![image-20250204134126107](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204134126107.png)![image-20250204135032772](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204135032772.png)![image-20250204142232550](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204142232550.png)

> ![image-20250204143048076](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204143048076.png)
>
> ![image-20250204143202661](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204143202661.png)
>
> 我们利用这样的方式去将 日志文件 清空 
>
> 然后写入一个符合规范的 phar 文件

![image-20250204143317261](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204143317261.png)

> ![image-20250204144112178](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204144112178.png)
>
> 清空日志文件之后，往中输入内容的时候，直接输入 utf-64le 格式的内容，然后将整个日志文件格式更换为 utf-8 的格式，此时该文件中的其他内容都会因格式错误而变成乱码，此时这些不可编码的字符（非 base64 字符）在进行base64编码和解码的时候就会消失，至此，整个日志文件内容就只剩下了 payload 内容

![image-20250204144522237](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204144522237.png)![image-20250204145013946](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204145013946.png)![image-20250204145539708](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204145539708.png)

> ![image-20250204144715869](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204144715869.png)

![image-20250204145913929](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204145913929.png)![image-20250204150111848](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204150111848.png)

环境部署成功之后长这样

![image-20250204150032512](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204150032512.png)

![image-20250204150339377](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204150339377.png)![image-20250204150414681](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204150414681.png)![image-20250204150919855](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204150919855.png)

![image-20250204152031551](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204152031551.png)

![image-20250204152100175](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204152100175.png)

![日志文件进行补齐，使得日志文件始终为两个字节的倍数](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204152221616.png)![image-20250204152338238](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204152338238.png)![image-20250204152155769](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204152155769.png)

![image-20250204152425920](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204152425920.png)

记得在这个 payload 最后要跟一个 a，随便一个字节的字符都可以，目的是为了打乱日志文件中的另一个 shell 编码顺序，确保 日志文件中只存在一个 shell 代码

![image-20250204152729072](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204152729072.png)

此时 日志文件就会含有工具生成的 payload

![image-20250204152959773](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204152959773.png)

接下来，进行日志清空（利用转码的方式），保留 payload

![image-20250204153124892](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204153124892.png)

此时，日志文件中的内容就变成了如下图所示的一段序列化数据，并且包含 phar 格式的文件头

该 payload 会在日志文件里面存放一个 test.txt 文件

![image-20250204153232571](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204153232571.png)

最终再去调用 phar 伪协议进行文件读取，来使得，日志文件中的序列化数据进行反序列化

![image-20250204153518414](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204153518414.png)

![image-20250204153532111](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204153532111.png)

为神马是访问日志文件目录下的 test.txt 文件呢？别忘了 phar 伪协议的作用就是 读取压缩包里面的文件

但在这个应用场景中，将 test.txt 文件内容读取出来了之后

![image-20250204153614157](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204153614157.png)

 此时此刻

![image-20250204154018085](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250204154018085.png)

