package com.ymqyyds.vul;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Member;
import java.lang.reflect.Method;

class Test{
    public String name="蜗牛学院";
    public int age = 21;
    private String addr ="huawei";
    private int price = 10000;

    // 重载两个构造方法，一个不需要传参，一个需要，此时实例化对象的时候，可以传参也可以不传参
    public Test(){

    }

    public Test(int price){
        this.price = price;
    }

    public int setPrice(int price){
        System.out.println("新价格为：" + price);
        return price;
    }

    public int getPrice(){
        return this.price;
    }

    private void getAddr(){
        System.out.println("私有方法：" + this.addr);
    }
}


public class Reflact {
    public static <Filed> void main(String[] args) throws Exception {
        System.out.println("类正常实例化调用方法：");
        Test t1 = new Test();
        System.out.println("t1.price = " + t1.getPrice());

        Test t2 = new Test(20000);
        System.out.println("t2.price = " + t2.getPrice());

        //利用java的类反射机制实现属性和方法的调用（包括构造方法）
        // 使用Class.forName可以获取到类本身,实际上是在JVM中动态加载类
        // Class 是类型 class 是关键字
        System.out.println("开始学习类反射机制：");
        System.out.println("使用字符串实例化一个反射类：");
        Class clazz = Class.forName("com.ymqyyds.vul.Test");
//        Class clazz = Test.class;  // 这句代码和上一句代码是一样的 类型后加一个 .class 表示该类型的值

        //直接使用 clazz 实例化一个类
        //newInstance() 的返回值是泛型，所以我们可以强转，也可以使用 Object 类的实例来接收  但是这种普通的 newInstance() 是无法传参数的，newInstance() 就相当于类本身的构造方法  如果类本身的构造方法有参数怎么办？此时会直接报错
        System.out.println("实例化动态加载类t3：");
        Test t3 = (Test) clazz.newInstance();
        System.out.println("t3.price = " + t3.getPrice());

        //使用 clazz 调用类方法
        System.out.println("使用反射类clazz实例化对象 o 并调用方法 getPrice：");
        Object o = clazz.newInstance();  // 实例化动态加载的类，类型必须使用 Object，
        Method m1 = clazz.getDeclaredMethod("getPrice");
        int price1 = (int)m1.invoke(o,null);  // invoke() 的参数第一个是Object对象，第二个是m1方法所需要的参数
        System.out.println("price1 = " + price1);

        System.out.println("使用反射类clazz实例化对象 o 并调用方法 setPrice：");
        Method m2 = clazz.getDeclaredMethod("setPrice", int.class);  // 这里带了一个 int.class 参数的意思是表示调用的 setPrice 这个方法需要有一个 int 型的参数
        int price2 = (int)m2.invoke(o,15000);
        System.out.println("price2 = " + price2);


        // 尝试使用 类反射调用 私有属性和私有方法
        //类反射调用私有属性
        System.out.println("使用反射类调用私有属性：");
        Field f1 = clazz.getDeclaredField("price");  // getField() 只能访问共有属性 getDeclaredField() 才能访问私有属性
        f1.setAccessible(true);  // 设置私有属性有权被访问
        System.out.println(f1.get(o));  //使用 f1.get() 获取所访问的私有属性的值，需要传入一个动态加载的类

        System.out.println("使用反射类调用私有方法：");
        Method m3 = clazz.getDeclaredMethod("getAddr");
        m3.setAccessible(true);
        m3.invoke(o,null);


        //类本身的构造方法如果有参数，怎么使用类反射机制来调用
        System.out.println("使用反射类创建一个构造器并调用需要传参的构造方法：");
        Class clazz1 = Class.forName("com.ymqyyds.vul.Test");
        Constructor c = clazz1.getConstructor(int.class);  // 创建一个构造器，该构造器可以传入参数，来代替构造方法，因此getConstructor() 函数所穿的参数就是构造方法所传参数的类型值
        Object obj = c.newInstance(300000);
        System.out.println("然后使用反射类实例化对象 obj 并调用方法 getPrice");
        Method m4 = clazz1.getDeclaredMethod("getPrice");
        int price3 = (int)m4.invoke(obj,null);
        System.out.println(price3);



        // 遍历所有方法和属性
        // 遍历方法
        System.out.println("遍历方法");
        Method[] methods = clazz1.getDeclaredMethods();
        for (Method method : methods) {
            System.out.println("metthod = " + method + "  methodname = " + method.getName() + "  methodmodifiers = " + method.getModifiers());
        }

        //遍历属性
        System.out.println("遍历属性");
        Field[] fields = clazz1.getDeclaredFields();
        for (Field field : fields){
            System.out.println("field = " + field + "  fieldname = " + field.getName() + "fieldmodifiers = " + field.getModifiers());
        }

    }
}
