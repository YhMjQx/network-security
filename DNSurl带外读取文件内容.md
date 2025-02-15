[TOC]



# ==DNSurl带外读取文件内容==

如何使用 DNSurl带外读取文件内容，说简单点：将文件内容作为子域名解析进入 DNSlog 

先将linux系统中的 /etc/passwd 文件内容提取出来并保存在文件中

## 一、base64编码

```java
// base64 编码
String b64 = Base64.getEncoder().encodeToString("Hello Woniu".getBytes());  // encodeToString() 函数要求传入一个 byte[] 类型的参数,返回一个String类型的数组
System.out.println(b64);  // SGVsbG8gV29uaXU=

byte[] bb64 = Base64.getEncoder().encode("Hello Woniu".getBytes());  //encode() 函数要求传入一个 byte[] 类型的数组，烦恼回一个 byte[] 对象
System.out.println(bb64);  // [B@45ee12a7  这是一个 byte[] 数组的对象
System.out.println(bb64[0]);  //83 - ASCII 码83对应字符S  正是 Hello Woniu 转化为base64 字符串之后SGVsbG8gV29uaXU=的第一个字符

//
byte[] b64array = new byte[10];  // 定义一个 byte[] 数组类型，长度为10
FileInputStream fileInputStream = new FileInputStream("./data/linux.passwd");
int i = fileInputStream.read();
System.out.println(i);  // 114  正是 ./data/linux.passwd 文件内容中 第一个字符 r 的ASCII码值
int x = fileInputStream.read(b64array);  // 这句代码意思是从 ./data/linux.passwd 文件中读取10个字符存到 b64array 这个 byte[] 数组中  并且，返回结果是bute[] 数组的长度
//        System.out.println(x);  // 10 这个也是该数组的长度
System.out.println(b64array[0]);  //b64array[0] 的值为神马是 111（o） 不应该是114（r）嘛，但是从 b64array[1] 之后又正确了


int y = fileInputStream.read(b64array,0,5);
System.out.println(y);  // 5  这个输出内容是 b64array 数组的长度
System.out.println(b64array[0]);  // 114
for (byte c : b64array) {
    System.out.println(c);
}
```

## 二、Java 如何获取文件长度

```java
FileInputStream fis = new FileInputStream("./data/linux.passwd");
int length = fis.available();
System.out.println("文件长度：" + length);
byte[] bytes = new byte[length];   // 用文件长度来初始化 byte[] 数组
fis.read(bytes);
```

## 三、将文件内容按照每次 60 个字符进行序列化

首先查看文件 base64 长度为 1592 个长度

那么要将它以 60 为间隔分开

那么1592 / 60 取整 为 26，同时 1592 mod 60 = 32

[【技巧】DNSlog外带文件-CSDN博客](https://blog.csdn.net/qinjilll/article/details/141442703)
