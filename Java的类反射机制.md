[TOC]



# ==Java的类反射机制==

教材内容

#### 一、基本概念

##### 1、序列化与反序列化

（1）序列化：将对象写入IO流中，ObjectOutputStream类的 writeObject() 方法可以实现序列化。

（2）反序列化：从IO流中恢复对象，ObjectInputStream 类的 readObject() 方法用于反序列化。

（3）意义：序列化机制允许将实现序列化的Java对象转换位字节序列，这些字节序列可以保存在磁盘上，或通过网络传输，以达到以后恢复成原来的对象。序列化机制使得对象可以脱离程序的运行而独立存在。

![image-20220425162731793](https://gitee.com/ymq_typroa/typroa/raw/main/20220425162731.png)

（4）序列化与反序列化是让 Java 对象脱离 Java 运行环境的一种手段，可以有效的实现多平台之间的通信、对象持久化存储。主要应用在以下场景：

> HTTP：多平台之间的通信，管理等，也可以用于流量带外。
>
> RMI：是 Java 的一组拥护开发分布式应用程序的 API，实现了不同操作系统之间程序的方法调用。值得注意的是，RMI 的传输 100% 基于反序列化，Java RMI 的默认端口是 1099 端口。
>
> JMX：JMX 是一套标准的代理和服务，用户可以在任何 Java 应用程序中使用这些代理和服务实现管理,中间件软件 WebLogic 的管理页面就是基于 JMX 开发的，而 JBoss 则整个系统都基于 JMX 构架。

（5）Java代码审计思路

如果是Java原生类，则需要入口类有readObject方法，同时实现了序列化接口，使其可以进行有效的反序列化，此时如果存在DNS解析，或者实现反序列化（利用Runtime对象进行类反射操作）。

需要有最终的执行函数(可以执行代码或者命令)，比如Runtime.getRuntime().exec，ProcessBuilder().start，getHostAddress，文件读写…..等等，这些函数需要自己平常去收集，这样审计起来会更得心应手。

> https://blog.csdn.net/weixin_45864705/article/details/127057380

##### 2、Java类反射机制

（1）反射机制的作用: 通过java语言中的反射机制可以操作字节码文件(可以读和修改字节码文件)，可以通过另外的方式调用到类的属性和方法，甚至私有属性和方法。可以把一个类的调用一个方法的调用编程字符串来调用。

（2）反射机制的相关类在java.lang.reflect.*包下面。

（3）反射机制的相关类有哪些：Constructor、Field、Method、Class等类

（4）java.lang.Class 代表字节码文件，代表整个类

（5）java.lang.reflect.Method 代表字节码中的方法字节码，代表类中的方法java.lang.reflect.Constructor 代表字节码中的构造方法字节码，代表类中的构造方法java.lang.reflect.Field 代表字节码中的属性字节码，代表类中的属性。

如果有多个文件的同时，不区分.java 文件还能正常访问吗

```java
public class RunCalc {    
    public static void main(String[] args) throws Exception{        
        // 正常运行一个应用程序        
        Runtime calc = Runtime.getRuntime();         
        calc.exec("calc");         
        // 使用类反射机制运行一个应用 程序        
        Class clazz = Class.forName("java.lang.Runtime");   
        // 也可以使用 java.lang.Runtime.class获取        
        Object obj = clazz.getMethod("getRuntime", null).invoke(clazz,null);        
        clazz.getMethod("exec",String.class).invoke(obj, "calc.exe");    
    }
}
```

![image-20250112220912096](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112220912096.png)

如果在另一个文件中和出现了相同的类，那么就会报错，编译的时候根本不会通过

（6）Java中为什么要使用反射机制，直接创建对象不是更方便？
如果有多个类，每个用户所需求的对象不同，直接创建对象，就要不断的去new一个对象，非常不灵活。而java反射机制，在运行时确定类型，绑定对象，动态编译最大限度发挥了java的灵活性。

（7）获取成员变量

```java
Field[] field = c.getDeclaredFields()    // getFields则获取public属性
```

（8）获取并调用方法

```java
Method[] method = c.getDeclaredMethods()   // getMethods则获取public方法
```

（9）获取构造方法

```java
Constructor[] constructor = c.getDeclaredConstructors();   // getConstructors则获取所有构造方法
```

（10）访问私有属性

```java
f.setAccessible(true);
```

#### 二、类反射机制实践

##### 1、普通类调用

```
package com.woniuxy.core;import java.lang.reflect.Constructor;import java.lang.reflect.Field;import java.lang.reflect.Method;import javax.activation.FileDataSource;public class Reflect {    public static void main(String[] args) throws Exception{//        Class clazz = Class.forName("java.lang.Runtime");   // 也可以使用 java.lang.Runtime.class获取//        Object obj = clazz.getMethod("getRuntime", null).invoke(clazz,null);//        String[] app = {"calc.exe"}; //        clazz.getMethod("exec",String.class).invoke(obj, app);        Class clazz = Test.class;//        Object obj = clazz.newInstance();  // 如果是默认构造方法，使用此方法        Constructor constructor = clazz.getDeclaredConstructor(int.class);        Object obj = constructor.newInstance(20000);        Method method = clazz.getMethod("setPrice", int.class);        int price = (int)method.invoke(obj, 5000);        System.out.println(price);        Field[] fields = clazz.getDeclaredFields();        for (Field field: fields) {            // 反射时可以访问私有属性            field.setAccessible(true);            if (field.getName() == "addr") {                field.set(obj, "火车南站");            }            System.out.println(field.get(obj));        }        // 反射时访问私有方法        Method method2 = clazz.getDeclaredMethod("getAddr", null);        method2.setAccessible(true);        method2.invoke(obj, null);    }}class Test {    public String name = "蜗牛学院";    public int age = 8;    private String addr = "大鼎世纪广场";    private int price = 10000;    public Test(int price) {        this.price = price;    }    public int setPrice(int price) {        System.out.println("新价格为：" + price);        return price;    }    private void getAddr() {        System.out.println("私有方法:" + this.addr);    }}
```

##### 2、调用ProcessBuilder

如果要执行命令，也可以反射ProcessBuilder类（注意构造方法）

```
Class clazz = Class.forName("java.lang.ProcessBuilder");Constructor c = clazz.getConstructor(List.class);Object o = c.newInstance(Arrays.asList("calc.exe"));Method m = clazz.getMethod("start");m.invoke(o, null);
```

如果用ProcessBuilder的另外一个构造方法：ProcessBuilder(String… command)，可变长参数是一个数组的形式存在。

```
Class clazz = Class.forName("java.lang.ProcessBuilder");Constructor c = clazz.getConstructor(String[].class);Object o = c.newInstance(new String[][]{{"calc.exe"}});Method m = clazz.getMethod("start");m.invoke(o, null);
```

