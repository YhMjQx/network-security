package com.ymqyyds.vul;

import java.io.*;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;

// 一个类必须要 implements Serializable 这个接口才允许被序列化
class Student implements Serializable {
//    private static final long serialVersionUID = 1122334455;
    public String name = "yourdady";
    public int id = 0;
    public  String phone = "";
    transient int money1 = 9999;
    transient String money2 = "9999";  // transient 修饰的变量不能被序列化，应该说，含有该关键字修饰变量的类都无法被序列化

    public Student() {
        System.out.println("构造方法运行ing...");
    }

    public void study() {
        System.out.println("学生正在学习ing...");
    }

    public void sleep() {
        System.out.println("学生正在休息ing...");
    }

    private void readObject(ObjectInputStream ois) throws Exception {
        ois.defaultReadObject();
        System.out.println("正在被反序列化ing...");

//        //Runtiime方式执行指令
//        Runtime.getRuntime().exec("calc.exe");
//
//        // ProcessBuilder方式执行指令
//        ProcessBuilder pb = new ProcessBuilder("calc.exe");
//        pb.start();


        //// 如果我们在 该重写函数中 进行类反射机制来执行指令呢？
       // // Runtime 方式执行指令
//        Class clazz = Class.forName("java.lang.Runtime");
//        Method m1 = clazz.getDeclaredMethod("getRuntime");  // 通过getRuntime() 这个方法来获取 Runtime 的实例
//        Object obj = m1.invoke(clazz,null);
//        Method m2 = clazz.getDeclaredMethod("exec",String.class);
//        m2.invoke(obj,"calc.exe");

        ////ProcessBuilder 方式执行指令
        Class clazz = Class.forName("java.lang.ProcessBuilder");
        Constructor c = clazz.getConstructor(String[].class);  // 由于该构造方法需要传入参数，所以必须要使用构造器来传参，普通的 newInstance 无法给构造函数传参
        // 由于在创建 Controller 的时候，给的参数类型为 String[] 所以，我们需要把 calc.exe 放在一个数组中传入 newInstance
//        String[] cmd = {"calc.exe"};
        // 然后，又因为newInstance所需要传入的参数，又是一个可变长的Object对象，所以我们在这里要把这一个固定的数组编程二维数组，才能确保他是可变长的
        String[][] cmd = {{"calc.exe"}};
        Object obj = c.newInstance(cmd);  // 给 ProcessBuilder 的构造方法传入要调用的指令，然后接收返回的对象
        Method m1 = clazz.getDeclaredMethod("start");  //使用ProcessBuilder对象来获取方法
        m1.invoke(obj,null);  // invoke获取到的方法  start 函数不需要传参
    }

}

public class unserial {
    // 序列化
    public void Serial() throws Exception{
        Student s = new Student();
        s.name = "ymq";
        s.id = 26221117;
        s.phone = "66674594188";
        s.money1 = 99999;
        s.money2 = "99999";

        FileOutputStream fos = new FileOutputStream("./data/StudentSerial.ser");  // 定义一个文件输出流对象，说白了就是定义一个序列化后的字符串输出的文件位置
        ObjectOutputStream oos = new ObjectOutputStream(fos);  // 定义一个对象输出流对象，说变了就是用文件输出流对象创建一个输出流对象，使得该对象可以序列化
        oos.writeObject(s);  // 使用输出流对象，将定义好的实例进行序列化输出到文件

    }

    // 反序列化
    public void Unserial() throws Exception{
        FileInputStream fis = new FileInputStream("./data/StudentSerial.ser");  // 定义文件输入流对象，说白了就是从某个文件中把序列化后的字符串取出来
        ObjectInputStream ois  = new ObjectInputStream(fis);  // 定义一个对象输入流对象，该对象可以从序列化后的文件中取出序列化后的字符串
        Student obj = (Student) ois.readObject();  // 使用输入流对象，将序列化后的字符串反序列化为对象输入进内存。又因为readObject返回一个 Object 类型的对象，所以使用 Object 类型的对象来接收,但是如果使用了 Object 对象来接收，那么接收之后我是无法来调用 Student 类中的属性和方法的
        // 序列化成功之后我们就可以使用接收的对象来调用Student类中的属性和方法了
//        System.out.println(obj.phone);
//        obj.study();
//        obj.sleep();
//        System.out.println(obj.money1);
//        System.out.println(obj.money2);


    }

    public static void main(String[] args) throws Exception{
        unserial us = new unserial();
        us.Serial();
        us.Unserial();
    }
}
