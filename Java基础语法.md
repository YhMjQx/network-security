[TOC]



# ==Java基础语法==

教材内容

#### 一、在Idea中创建项目

![image-20230823014816090](https://gitee.com/ymq_typroa/typroa/raw/main/202308230148153.png)

![image-20230823014940928](https://gitee.com/ymq_typroa/typroa/raw/main/202308230149967.png)

此时，在src目录下编写Java代码，编写之前，最好再创建一个包（package)，包名建议为：com.woniuxy.basic，然后在包下面新建Java Class源代码文件，命名为HelloWorld.java，源代码如下：

```java
package com.devaudit.basic;

public class Dev_Basic {

//    入口函数：是一个static静态方法，拥有一个字符串数组的参数类型，用于接收命令行参数
    public static void main(String[] args) {
        System.out.println("Hello Java");
        for (int i=0;i<args.length;++i) {
            System.out.println(args[i]);

        }
    }
}

```

源码上右键运行，如果能够成功输出Hello World，说明项目创建完成。

> 常用快捷键：main+回车，生成接口函数，sout+回车生成输出方法，ctrl+d，复制本行到下一行。

最后，为了保证不出现乱码，建议将所有编码设置为utf-8：

![image-20230823144517969](https://gitee.com/ymq_typroa/typroa/raw/main/202308231445072.png)

> 我们来讲一下如果带参数的话要怎么传参和实现输出
>
> 方法一：进入运行参数配置，手动添加参数
>
> ![image-20241120105631876](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241120105631876.png)
>
> ![image-20241120105823095](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241120105823095.png)
>
> 这里以 xupt ymq 30 为例
>
> ![image-20241120105801890](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241120105801890.png)
>
> 此时再运行就有结果了
>
> ![image-20241120105919095](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241120105919095.png)
>
> 方法二：命令行运行代码并携带参数
>
> cd 到编译后的 ./out/production/ 目录下，执行 java 完整的包名+类名 参数 指令即可
>
> ![image-20241120123234416](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241120123234416.png)
>
> 同样的，我们可以在 cmd 中转到指定目录然后执行 java 完整的包名+类名 参数
>
> ![image-20241120123831280](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241120123831280.png)

#### 二、基础语法与术语

1、数据类型

![img](https://gitee.com/ymq_typroa/typroa/raw/main/202308230155397.png)

基础类型转换

```java
int i = 100;
long l = 999999999;
short s = 1;
float f = 123.456f;
double d = 1234.5678;
char c = 'A';  // java中，字符串只能用双引号，字符只能用单引号
System.out.println(c);

// 类型转换：隐式转换和显示转换
float ff = i + s; // 隐式转换
System.out.println(ff);  // 101.0  隐式转换为单精度浮点数 101.0
System.out.println(i + f); //223.456  也是隐式转换为浮点数

int result = i + (int)f;  // 显示转换 基础类型直接转换
System.out.println(result);  // 223

String temp = String.valueOf(i+f);  //将小数转换为字符串
int result2 = (int)Float.parseFloat(temp);  //将字符串转换为整数
System.out.println(result2);  // 223
```

2、输入输出

命令行参数：

```java
D:\JAVA\Java-Development_and_code_audit\JavaCore\out\production\JavaCore>java com/devaudit/basic/Dev_Basic xupt ymq 30
Hello Java
xupt
ymq
30  

// 带参数在命令行运行，java后面跟的是包名+类名，不是.class文件名
```

交互式输入：

```java
// 通过命令行进行交互式输入
System.out.println("请输入你的姓名：");
Scanner sc = new Scanner(System.in);
String name = sc.next();
System.out.println("您的姓名为：" + name);
```

输出的处理：

```java
// 通过命令行进行交互式输入
System.out.println("请输入你的姓名：");
Scanner sc = new Scanner(System.in);
String name = sc.next();
System.out.println("您的姓名为：" + name);

// 输出部分的各种用法
System.err.println("这是一段错误消息");
// 按固定格式输出
System.out.printf("你的用户名为：%s\n",name);
System.out.print("好消息");
```

3、字符串处理

关于 == 与 equals 的注意事项：==比较的是数据的地址和值，equals只比较值，不比较地址

```java
// 字符串处理
// 两个用户名是相等的，因为没有重新开辟内存空间
String name = "Woniu";
String name2 = "Woniu";

//两个密码是不相等的，因为String是一个类，两个密码分别开辟了不同的内存空间
String password = new String("123456");
String password2 = new String("123456");
System.out.println(System.identityHashCode(password));  //1163157884
System.out.println(System.identityHashCode(password2));  //1956725890
System.out.println(System.identityHashCode(name));  //1163157884
System.out.println(System.identityHashCode(name2));  //1163157884

//        if(password == password2){  // == 即会比较数值也会比较地址
if(password.equals(password2)){  // equals 值比较数值大小
	System.out.println("密码相等");
}
else{
	System.out.println("密码不等");
}

if(name == name2){
	System.out.println("用户名相等");
}
else{
	System.out.println("用户名不等");
}
```

基础操作：

```java
System.out.println("请输入你的电话号码：");
Scanner sc = new Scanner(System.in);
String phone = sc.next();
System.out.println("你的电话号码为" + phone.length() + "位");

for (short i=0;i<phone.length();++i){
	System.out.println(phone.charAt(i));
}

boolean b = phone.matches("^1[3-9]\\d{9}$");
if(b){
	System.out.println("手机号码正确");
}
else{
	System.out.println("手机号码错误");
}
```

4、数组

```java
// 数组操作
String source = "zhangsan-lisi-wangwu-zhaoliu";
String[] names = source.split("-");
for(String name:names){
    System.out.println(name);
}

// 数组的定义
String[] names2 = {"zhangsan","lisi","wangwu","zhaoliu"};
System.out.println(names2.length);
names2[1] = "ymq";
for (String name:names2){
    System.out.println(name);
}
//数组只能通过下标改值，查值
```

5、List与ArrayList

一种扩展数组，增强了很多功能的Java内置类。

```java
List<Object> list = new ArrayList<>();
list.add("zhangsan");list.add(123);
list.add("lisi");
People p = new People();
list.add(p);
for (Object item: list) {    
    System.out.println(item);
}
List<Integer> list2 = new ArrayList<Integer>();
list2.add(11111);
list2.add(22222);
list2.add(33333);
list2.add(44444);
System.out.println(list2.get(1));
list2.remove("444444");
list2.remove(1);
```

6、Map与HashMap

用于创建Key-Value键值对的对象，类似于PHP的关联数组或Python的字典

```java
Map<String,String> m1 = new HashMap<>();
m1.put("username","woniu");
m1.put("password","Woniu123");
m1.put("address","sichuanchengdutianfu");
m1.put("phone","15896347963");
System.out.println(m1.get("phone"));
```

利用List添加Map的方式，完成一个二维表结构数据的构造：

```java
Map<String,String> m1 = new HashMap<>();
m1.put("username","woniu");
m1.put("password","Woniu123");
m1.put("address","sichuanchengdutianfu");
m1.put("phone","15896347963");

Map<String,String> m2 = new HashMap<>();
m2.put("username","ymq");
m2.put("password","Y1mq23");
m2.put("address","sichuanchengdutianfu");
m2.put("phone","15896347963");

Map<String,String> m3 = new HashMap<>();
m3.put("username","yyds");
m3.put("password","Yyds123");
m3.put("address","sichuanchengdutianfu");
m3.put("phone","15896347963");
//        System.out.println(m3.get("phone"));

List<Map> mlist = new ArrayList<>();
mlist.add(m1);
mlist.add(m2);
mlist.add(m3);

for(Map user: mlist){
    System.out.printf("%s\t%s\t%s\n",user.get("username"),user.get("password"),user.get("address"));
}
```

输出结果为：

```
woniu	Woniu123	sichuanchengdutianfu
ymq	Y1mq23	sichuanchengdutianfu
yyds	Yyds123	sichuanchengdutianfu
```

7、利用FastJSON处理JSON数据

> 在这里说一下如何将 fastjson-1.2.24.jar 和 mysql-connector-java-5.1.34.jar 导入Java项目
>
> - 首先创建一个目录
>
> ![image-20241201224314097](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20241201224314097.png)
>
> - 再将俩jar文件导入进去，并右键只有选择 Add as library
>
> ![image-20241201224317991](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241201224317991.png)
>
> ![image-20241201224716057](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241201224716057.png)
>
> - 在  项目结构 中查看 是否存在 lib
>
> ![image-20241201225007484](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241201225007484.png)
>
> ![image-20241201224932987](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241201224932987.png)

（1）将List或Map直接输出为JSON字符串

```java
String json = JSON.toJSONString(users);System.out.println(json);    // 直接将上述List对象输出为字符串[{"password":"1234569","address":"chengdu","phone":"18812345678","username":"woniu"},{"password":"1234568","address":"chengdu","phone":"13812345678","username":"admin"},{"password":"1234567","address":"chengdu","phone":"15812345678","username":"qiang"}]
```

（2）原始的生成JSON的方式

JSON数据无论使用何种框架，最终都是对JSONObject和JSONArray的处理，JSONObject即Map，JSONArray即List。

```java
public String list2json(){
    Map<String,String> m1 = new HashMap<>();
    m1.put("username","woniu");
    m1.put("password","Woniu123");
    m1.put("address","sichuanchengdutianfu");
    //        m1.put("phone","15896347963");

    Map<String,String> m2 = new HashMap<>();
    m2.put("username","ymq");
    m2.put("password","Y1mq23");
    m2.put("address","sichuanchengdutianfu");
    //        m2.put("phone","15896347963");

    Map<String,String> m3 = new HashMap<>();
    m3.put("username","yyds");
    m3.put("password","Yyds123");
    m3.put("address","sichuanchengdutianfu");
    //        m3.put("phone","15896347963");
    //        System.out.println(m3.get("phone"));

    List<Map> mlist = new ArrayList<>();
    mlist.add(m1);
    mlist.add(m2);
    mlist.add(m3);

    String json = JSON.toJSONString(mlist);
    //        System.out.println(json);  // 这里通过 JSON.toJOSNString 的函数已经成功将mlist对象转换为 json 字符串了
    return json;
}
```

```java
// 任何JSON数据，核心只有两个，JSONObject（用于表达Map），JSONArray（用于表达Array）
public String jsonobjectoriginal(){
    JSONObject object = new JSONObject();
    object.put("username","lisi");
    object.put("phone","13312345678");
    object.put("address","hangzhou");

    //        return object.toJSONString();  //{"address":"hangzhou","phone":"13312345678","username":"lisi"}
    return object.toString();  //{"address":"hangzhou","phone":"13312345678","username":"lisi"}
}

public String jsonarrayoriginal(){
    JSONArray array = new JSONArray();
    array.add("wangwu");
    array.add("17312345678");
    array.add("shanxixiian");

    //        return array.toJSONString(); //["wangwu","17312345678","shanxixiian"]
    return array.toString();  //["wangwu","17312345678","shanxixiian"]
}
```

（3）将JSON字符串反序列化为Java对象

```java
//将Map的JSON字符串反序列化为Map对象
public void MapJson2MapObtect(){
    System.out.println("请输入一段Map的JSON字符串：");
    Scanner sc = new Scanner(System.in);
    String MapJson = sc.next();

    JSONObject array = JSON.parseObject(MapJson);
    for(String key: array.keySet()){
        System.out.println("Key为 " + key + " 的值为 " + array.get(key));
    }
}

// 将Array的JSON字符串转换为Array
public void ArrayJson2Array(){
    System.out.println("请输入一段Array的JSON字符串：");
    Scanner sc = new Scanner(System.in);
    String ArrayJson = sc.next();

    JSONArray array = JSON.parseArray(ArrayJson);
    for (int i = 0 ; i < array.size() ; ++i){
        System.out.println(array.get(i));
    }
}

//将List包裹Map的JSON字符串转换为对象的形式，此时需要两层分开单独处理
public void ArrayMapJson2Object(){
    System.out.println("请输入Array包裹Map的JSON字符串：");
    Scanner sc = new Scanner(System.in);
    String ArrayMapJson = sc.next();

    JSONArray array = JSON.parseArray(ArrayMapJson);
    for (int i = 0 ; i < array.size() ; ++i){
        // 此时，每一个array.get(i)都是一个Map，需要先将其转换为字符串，再进行循环遍历。使用 String.valueOf() 函数来进行字符串的强转
        //            System.out.println(array.get(i));
        String MapJson = String.valueOf(array.get(i));  // MapJson 是Map的JSON数据格式，现在需要将其反序列化
        JSONObject Map = JSON.parseObject(MapJson);
        for (String Key: Map.keySet()){
            System.out.println("Key为 " + Key + " 的值为 " + Map.get(Key));
        }
        System.out.println("\n");
    }
}
```

#### 三、面向对象编程

1、面向对象三大特性：封装、继承、多态

**封装**：访问修饰符，public, protected, private，属性私有、方法公有，所有方法均封装于类之中，重载（同名不同参）

**继承**：子类拥有父类的特性，子类可以重写父类的方法，子类可以扩展自已的新方法，父类可以定义子类对象，祖宗类Object可以定义所有其他类型数据，Object obj = new String(“”) , Object obj = new People(); 父子类之间也可以进行强类型转换。Java中还存在一个祖宗类：Exception，可以用于定义其他任意异常类。

**多态**：同一个接口有不同的实现，扮演不同的角色，拥有不同的形态。在多态中必须存在有继承或实现关系的子类和父类，子类对父类中的某些方法进行重新定义，基类引用指向派生类对象，动态加载的特性。

**构造方法**：使用public 类名() 定义的特殊方法，用于实例化时进行传参，如果没有定义构造方法， 则使用默认构造方法，一旦显式定义了构造方法，那么实例化时必须按照构造方法的参数来。

2、类与实例

创建类和实例，并配置构造方法。

```java
package com.devaudit.basic;

// public修饰的类，该类的类名一定要和文件名一样
public class OOPDemo {
    public static void main(String[] args) {
        People p1 = new People();
        p1.setName("zhangsan");
        System.out.println(p1.getName());

        //或者直接通过构造方法传name值，但如果只有显式声明的构造方法，那么原本默认的构造方法便无法使用了，所以重载构造方法时，建议保留原本的构造方法
        People p = new People();
        People p2 = new People("lisi");
        People p3 = new People("wangwu");
        System.out.println(p.getName());
        System.out.println(p2.getName());
        System.out.println(p3.getName());


    }
}

class People{
    private String name = "人名";
    public String sex = "性别";

    //定义构造方法：将类名作为方法名
    public People(){
        //默认没有任何参数，没有做任何处理的构造方法
    }
    public People(String name){
        this.name = name;
    }


    public void eat(){
        System.out.println("eating");
    }

    public void sleep(){
        System.out.println("sleepping");
    }

    private void output(){
        System.out.println("outputting");
    }

    public void setName(String name){
        this.name = name;
    }

    public String getName(){
        return this.name;
    }
}
```

3、继承

```java
Father f1 = new Father();
f1.setName("father");
System.out.println(f1.getName());
f1.drive();

class Father extends People{
    public void drive(){
        System.out.println("driving");
    }
}
```

单一继承，Father同样可以继续作为父类

```java
class Father extends People{
    public void drive(){
        System.out.println("driving");
    }
}

class Son extends Father{
    //重写父类方法 override
    public void drive(){
        System.out.println("driving AMG");
    }
    //重载本类方法 overload
    public void drive(String type){
        System.out.println("driving "+type);
    }

    public void run(){
        System.out.println("Running");
    }
}

class Daughter extends Father{
    
}
```

可以使用父类声明，子类实例化的方式

```java
Father fs = new Son();
fs.drive();
System.out.println(fs.getName());
Father fd = new Daughter();
fd.drive();
```

关于String的equals方法，研究一下父类和子类对应的方法

```java
//Object类的equals方法，比较地址
public boolean equals(Object obj) {
	return (this == obj);
}
```

String类继承自Object类，而在String类中重写了equals方法，只进行值的比较

```java
    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }
        if (anObject instanceof String) {
            String anotherString = (String)anObject;
            int n = value.length;
            if (n == anotherString.value.length) {
                char v1[] = value;
                char v2[] = anotherString.value;
                int i = 0;
                while (n-- != 0) {
                    if (v1[i] != v2[i])
                        return false;
                    i++;
                }
                return true;
            }
        }
        return false;
    }
```

顺便发现定义String类的代码如下：

```java
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence
```

final关键字的意思是：本类不能被继承，是最底层的类，不能充当父类

4、抽象类

介于类与接口之间的一种类型，使用abstract class来定义：类是可以实例化，抽象类不可以实例化，只能继承，抽象类中的方法可以实现，抽象类中也可以定义成抽象方法abstract void function()，则不能被实现。

```java
//抽象类不能被实例化
abstract class Animal{
    //正常类属性和房啊
    public String type = "animal";
    public  void  eat(String type){
        System.out.println(type+"is eating");
    }
    //抽象方法在抽象类中不能被实现，只能声明，而在子类中必须重载
    public  abstract void run();
}

class Dog extends Animal{
    public  void run(){
        System.out.println(type + "is running");
    }
}
```

5、接口

接口是一种极端情况下的抽象类，不能实例化，且接口中的方法不能被实现，全部为抽象方法。

```java
interface  Phone{
    //接口当中的方法都是抽象方法，本接口当中不能实现，implements了该接口的子类中必须要实现
    public void  call();
    public  void play();
}

class HuaWei implements Phone{
    @Override
    public void call() {

    }

    @Override
    public void play() {
        
    }
}
```

6、多态

动态加载特性：

```
Class clazz = Class.forName("java.lang.Runtime")
```

#### 四、异常处理

1、try…catch…finally

```java
public void BefferRead(){
    // 将下面四个变量在 try 外定义，以防止在 catch 和 finally 中无法访问
    File file = null;
    InputStreamReader reader = null;
    InputStream is = null;
    BufferedReader br = null;
    try{
        file = new File("D:/keys.txt");
        is = new FileInputStream(file);
        reader = new InputStreamReader(is,"UTF-8");  // 使用 InputStreamReader 并配合编码格式，才能正确以字符的形式来读取文件
        br = new BufferedReader(reader);
        String line = ""; //用于接收文本的每一行
        while ((line = br.readLine()) != null) {
            System.out.println(line);
        }

    }
    catch (Exception e){
        e.printStackTrace();
    }
    //        catch (FileNotFoundException e) {
    //            e.printStackTrace();
    //        }
    //        catch (UnsupportedEncodingException e){
    //            e.printStackTrace();
    //        }
    //        catch (IOException e){
    //            e.printStackTrace();
    //        }
    finally {
        // 无论是否出现异常，均需要做一些收尾的工作，比如关闭文件指针
        try {
            is.close();

        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

2、throws

在方法体后面直接定义本方法不处理异常，有异常抛出给调用该方法的地方（甩锅）。

```java
// 写文件，使用 throws 将异常甩锅给该函数被调用的地方
public void BufferedWriter() throws Exception{
    File file = new File("D:/test.txt");
    OutputStream os = new FileOutputStream(file,true);
    OutputStreamWriter writer = new OutputStreamWriter(os,"UTF-8");
    BufferedWriter bw = new BufferedWriter(writer);
    String content = "这是缓冲区输出的内容";
    bw.write(content,0,content.length());
    bw.flush(); //强制将缓冲区的内容发送出去，不必等到缓冲区满
    bw.close(); //关闭流
    writer.close(); //关闭流
    os.close(); //关闭流
}

public static void main(String[] args) throws Exception {
    FileReadWrite filerw = new FileReadWrite();
//        filerw.BefferRead();
    filerw.BufferedWriter();  // 由于这里调用了BufferedWriter()函数，因此该函数内部的异常在该调用的地方产生了
    // 但由于我们还可以将 main 函数内部的异常再进行甩锅，所以在main函数后继续使用 throws
    // 此时所有的异常都被甩锅给了JVM
}
```

最终，JVM承担了所有。 

4、自定义异常

```
package com.woniuxy.demo;public class MyException extends RuntimeException{    public MyException(){    }    public MyException(String msg){        super(msg);    }}使用时，直接在满足某个条件下：throw new MyException(String msg)
```

#### 五、Java操作文件

缓冲区读写方式（按行读取），可以提升IO性能，减少对硬盘的频繁的读写操作。

```java
public void BefferRead(){
    // 将下面四个变量在 try 外定义，以防止在 catch 和 finally 中无法访问
    File file = null;
    InputStreamReader reader = null;
    InputStream is = null;
    BufferedReader br = null;
    try{
        file = new File("D:/keys.txt");
        is = new FileInputStream(file);
        reader = new InputStreamReader(is,"UTF-8");  // 使用 InputStreamReader 并配合编码格式，才能正确以字符的形式来读取文件
        br = new BufferedReader(reader);
        String line = ""; //用于接收文本的每一行
        while ((line = br.readLine()) != null) {
            System.out.println(line);
        }

    }
    catch (Exception e){
        e.printStackTrace();
    }
    //        catch (FileNotFoundException e) {
    //            e.printStackTrace();
    //        }
    //        catch (UnsupportedEncodingException e){
    //            e.printStackTrace();
    //        }
    //        catch (IOException e){
    //            e.printStackTrace();
    //        }
    finally {
        // 无论是否出现异常，均需要做一些收尾的工作，比如关闭文件指针
        try {
            is.close();

        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

最终JVM承担了所有

#### 六、Java操作数据库

1、使用Statement

```
Connection conn = null;try {    Class.forName("com.mysql.jdbc.Driver").newInstance();    conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/learn?user=root&password=123456&useUnicode=true&characterEncoding=UTF8");        Statement stmt = this.getConnection().createStatement();    String sql = "select * from user where userid < 10";    rs = stmt.executeQuery(sql);    while (rs.next()) {        System.out.println(rs.getString("username"));    }}catch(Exception e) {    e.printStackTrace();}return conn;
```

2、使用PreparedStatement

使用PreparedStatement对SQL语句进行预处理，可以有效防止SQL注入

```
// 常规操作，会存在SQL注入漏洞Scanner scanner = new Scanner(System.in);String username = scanner.next();String password = scanner.next();Class.forName("com.mysql.jdbc.Driver").newInstance();Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/learn?user=root&password=123456&useUnicode=true&characterEncoding=UTF8");Statement statement = conn.createStatement();  String sql = "select * from user where username='"+username+"' and password='"+password+"'";ResultSet rs = statement.executeQuery(sql);    // 以下操作进行预处理，可以有效防止SQL注入String sql = "select * from user where username=? and password=?";PreparedStatement ps = conn.prepareStatement(sql);ps.setString(1, username);ps.setString(2, password);ResultSet rs = ps.executeQuery();
```

3、更新数据表

```
public void update() throws Exception {    String sql = "update user set password='test123' where userid=4";    Statement stmt = this.getConnection().createStatement();    stmt.executeUpdate(sql);}
```

#### 七、Java网络访问

1、发送GET请求

```
public String sendGet(String getUrl) {    String body = "", line = "";    // 定义核心类HttpURLConnection    HttpURLConnection urlConnection = null;    try {        // 利用URL类和getUrl地址来实例化核心类HttpURLConnection        URL url = new URL(getUrl);        urlConnection = (HttpURLConnection) url.openConnection();        // 设置HTTP请求的各项参数，包括请求头信息等，默认可不设置以下参数        urlConnection.setUseCaches(false);        urlConnection.setConnectTimeout(10000);        urlConnection.setReadTimeout(10000);        urlConnection.setRequestProperty("Cookie", "SessionID=1212312y7u2u3478huidh8923");        urlConnection.setRequestProperty("User-Agent", "Java-Client");        // 打开连接，进行请求的处理        urlConnection.connect();        // 利用InputStream将响应读取取字节流中        InputStream is = urlConnection.getInputStream();        // 利用InputStreamReader将响应转换为字符流，并使用UTF-8进行编码        InputStreamReader isr = new InputStreamReader(is, "UTF-8");        // 利用缓冲区读取响应文本，提升性能，按行读取响应文本，更加方便        BufferedReader br = new BufferedReader(isr);        // 将每一行的内容附加到字符串body后面，加上换行符,让响应可读性更强        // 保证响应给客户端的文本可以被完整还原，与查看源文件看到的内容一致        while ((line = br.readLine()) != null) {            body += "\n" + line;        }        // 关闭缓冲区对象        br.close();    } catch (Exception e) {        e.printStackTrace();    }    // 断开本次连接    urlConnection.disconnect();    // 将获取到的响应正文内容返回    return body;}
```

2、发送POST请求

```
public String sendPost(String postUrl, String postData) {    String body = "", line = "";    HttpURLConnection urlConnection = null;    try {        URL url = new URL(postUrl);        urlConnection = (HttpURLConnection) url.openConnection();        // 设置HTTP请求的各项参数，包括请求头信息等，默认情况请设置如下参数        urlConnection.setDoOutput(true);        urlConnection.setDoInput(true);        urlConnection.setRequestMethod("POST");        urlConnection.setUseCaches(false);        urlConnection.setInstanceFollowRedirects(false);        urlConnection.setRequestProperty("Cookie", "");        // 定义PrintWriter对象，用于将POST请求正文发送给服务器端        PrintWriter out = new PrintWriter(urlConnection.getOutputStream());        out.print(postData);        out.flush();        // 接收服务器端响应，并用字符串变量body来接收，方法与GET完全一致        BufferedReader in = new BufferedReader(new InputStreamReader(                urlConnection.getInputStream(), "UTF-8"));        while ((line = in.readLine()) != null) {            body += "\n" + line;        }        // 关闭输入输出流对象        in.close();        out.close();    } catch (Exception e) {        e.printStackTrace();    }    urlConnection.disconnect();    return body;}
```

#### 九、Java实现网络爬虫

https://blog.csdn.net/qq_40794973/article/details/88918441

> 如果遇到代码本身没问题，还能正常运行，但是编译器的编译界面一直报错，此时如果java版本没变，其他啥都没变，尝试清除缓存并重启IDEA
>
> ![image-20241206091004641](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241206091004641.png)
>
> ![image-20241206091023121](https://gitee.com/ymq_typroa/typroa/raw/main/image-20241206091023121.png)

snipaste