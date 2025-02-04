[TOC]



# ==ThinkPHP反序列化漏洞续集==

经过上一篇的阐述，我们已经找到了 `__toString()` 函数的调用类，接下来继续往下深入。

## 类的复用

首先我们来了解一下类的复用这个知识点，看如下代码：

```php
<?php
//trait 类
trait A{
    public function aa(){
        echo "AA";
        $this->bb();
    }
}

trait B{
    public function bb(){
        echo "BB";
    }
}

class C{
    use A,B;
    public function cc(){
        $this->aa();
    }
}  
$a = new C();
$a->cc();
?>
```

访问一下该页面：

![image-20240901215442947](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901215442947.png)

此时C类作为纽带，将A和B两个类联系在一起，其实use的作用类似于include把A和B类中的代码复制到C中使用

## 既 `__toString()` 继续审计

```php
$visible = [];
$array = $this->parseAttr($this->visible, $visible);
```

```php
protected function parseAttr($attrs, &$result, $visible = true)
{
    $array = [];

    foreach ($attrs as $key => $val) {
        if (is_array($val)) {
            if ($visible) {
                $array[] = $key;
            }

            $result[$key] = $val;
        } elseif (strpos($val, '.')) {
            list($key, $name) = explode('.', $val);

            if ($visible) {
                $array[] = $key;
            }

            $result[$key][] = $name;
        } else {
            $array[] = $val;
        }
    }

    return $array;
}
```

说白了就是该函数最终目的就是把 `$attrs` 遍历存放在 `$result` 中，并把获取到的键值对中的键放在`$array`，然后返回 `$array` ，当然，前提是 `$attrs` 本就是关联数组，如果不是，就拆分成关联数组

```php
$data  = array_intersect_key($data, array_flip($array));
```

这是内置函数，不担心，而且没有类属性

Conversion 类中

## 再找下面的类属性 `$this->append` 

```php
if (!empty($this->append)) {
    foreach ($this->append as $key => $name) {
        if (is_array($name)) {
            // 追加关联对象属性
            $relation = $this->getRelation($key);

            if (!$relation) {
                $relation = $this->getAttr($key);
                $relation->visible($name);
            }

            $item[$key] = $relation->append($name)->toArray();
        } elseif (strpos($name, '.')) {
            list($key, $attr) = explode('.', $name);
            // 追加关联对象属性
            $relation = $this->getRelation($key);

            if (!$relation) {
                $relation = $this->getAttr($key);
                $relation->visible([$attr]);
            }

            $item[$key] = $relation->append([$attr])->toArray();
        } else {
            $value = $this->getAttr($name, $item);
            if (false !== $value) {
                $item[$name] = $value;
            }
        }
    }
}
```

进入循环

所以 `$this->append` 需要是一个关联数组，并且该关联数组中的键值对的值还必须是是个数组

但是此时想要跳转到 `$this->getRelation($key)` 函数中，发现跳转失败，说明该类中并没有实现该函数，估计就是上面使用的类的复用

此时滑到该类的最上面去分析一下，

![image-20240901224502463](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901224502463.png)

而 Model 类中 同时use了 RelationShip 类和 Conversion 类，所以在 Conversion 类中可以使用 RelationShip  类中的函数

![image-20240901225606760](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901225606760.png)

##   全局搜索一下 getRelation 函数

![image-20240901224723539](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901224723539.png)

### 第一个

![image-20240901225503568](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240901225503568.png)

```php
trait RelationShip{
    private $relation = [];

    public function getRelation($name = null)
    {
        if (is_null($name)) {
            return $this->relation;
        } elseif (array_key_exists($name, $this->relation)) {
            return $this->relation[$name];
        }
        return;
    }
}
```

接下来分析 getRelation 函数，其中所传参数 `$name` 是 `Conversion 类中 $this->append as $key => $name 的 $key` 

-  如果 `$name` 是空 ，则返回 `$this->relation ` 由于该函数所在的类ReloationShip与Conversion类均被被 Model 类use，所以在Conversion类中调用该函数返回 `$this->relation` 就相当于返回 Conversion 自己类的 `$this->relation`
- 否则 `$name` 不是空，并且如果 `$this->relation` 属性中存在 `$name` ，则同理返回 `$this->relation[$name]`  
- 以上条件都不满足，则返回空

所以在Conversion类中继续往下走

```php
if (!$relation) {
    $relation = $this->getAttr($key);
    $relation->visible($name);
}
```

如果 `$relation` 是空，才会进入if语句

## 继续审计 `getAttr` 函数，

依旧无法跳转，继续全局搜索

![image-20240902214524543](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902214524543.png)

从这里就可以看出，只有这个才是定义函数，其他的都是一个在Model类中，一个在Conversion类中调用该函数

接下来的两个函数都在Attribute类中

![image-20240902214805935](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902214805935.png)

## 又在调用 getData 函数

![image-20240902214832810](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902214832810.png)

- 首先 getAttr 函数中的 `$name` 参数是 `$this->append as $key => $name`  中的 `$key`
- 所以 getData 函数中的 `$name` 和 getAttr 是一样的
- 如果 `$this->data`  和 `$this->relation` 中不包含 `$name` ，则分别返回 `$this->data[$name]` 或 `$this->relation[$name]` 

## 接下来继续审计 visible 函数

还是无法跳转，全局搜索

![image-20240902215826155](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902215826155.png)

### 第一个

Query类，写死的，无效

![image-20240902215948303](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902215948303.png)

### 第二个

没有对属性操作，pass掉

![image-20240902220104098](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902220104098.png)

### 第三个

就在Copnversion类中，和调用的代码在一个类中，所以是自己类调用自己类，但是由于该函数又在操作数组，并没有对属性值操作，所以还是pass掉

![image-20240902220157780](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902220157780.png)

那走到这如果都pass掉，路就死了，没有继续往下走的函数可以调用了

## __call 函数

此时，由于visible 函数三个都无法利用，所以另辟蹊径，选择 __call 函数

全局搜索

![image-20240902220656810](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902220656810.png)

我直接说结果吧

Request类中

![image-20240902221921112](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902221921112.png)

此时，只需要构造 `$this->hook[$method]` 为一个关联数组，我只需要构造 `$this->hook` 是一个关联数组，并且其中的键为 visible ，而值 我就可以随意构造，并执行该函数。就比如：

 ```php
 由于执行 __call($name,$args) 时，错误执行的函数名被传过来会被当作 $name 参数传进来，其所执行的参数依旧是作为 $args 传递给 __call() 函数
 
 所以此时 $relation->visible($name);
 
 但是 $relation 会被构造为一个不具有 visible 方法但具有 __call 方法的类实例，此时执行这段代码就会执行 $relation 类实例中的 __call 方法
     
 构造 $this->hook = ["visible":"system"];
     
 所以 $method = "visible";
 $this->hook = [$method]  =>  "system"
     
 此时再构造 $args 为 "ifconfig"
     
 就会执行 system("ifconfig")
 ```

但是

```php
array_unshift($args, $this);
```

这句话就毁掉了上面的大部分逻辑，因为该代码的作用如下：

```php
比如 $args = ["ifconfig"];  $this = new Request();
则执行了该代码之后
$args = [new Request(),"ifconfig"];

所以要执行的代码就变成了：
call_user_func_array("system",[new Request(),"ifconfig"]);
此时就无法再利用call_user_func_array()来执行了，因为恶意可执行函数暂时没有哪一个可以接受类实例作为参数
```

既然如此，无法正确将参数传递给我构造的函数，那么我就放弃你，转而执行其他的函数，这时，我们去这个类中搜索其他的 `call_user_func` 函数，然后再找还有没有其他的可控点，最终确定了

## filterValue ()

![image-20240904170149437](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240904170149437.png)

但是该函数执行的参数，比如 `&$value` 和 `$value` 我们并不知道哪来的，所再搜索 到底谁在调用 filterValue 

最终确定为该类中的 input 函数，然后再去确定 `$this->filterValue($data, $name, $filter);` 这句代码中调用 该函数的参数都从哪来

![image-20240904170849965](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240904170849965.png)

## ` $data = $this->getData($data, $name);`

ok，getData中找不到 `$data` 的可控点

![image-20240904171541343](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240904171541343.png)

那就再找，到底谁在调用 input() ，简直疯了

## `$filter = $this->getFilter($filter, $default);`

![image-20240904171643461](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240904171643461.png)

这也是一样，去找谁到底在用 getFilter() 

## param()

![image-20240904171839850](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240904171839850.png)

`$data` 构造由 `$this->param` 构造即可

**但是，绷不住了，param函数中调用input函数时存在$name这个变量，如果该变量是空的话，input函数根本无法正确执行，直接进去就结束了，所以为了不让param函数中的`$name`变量为空，还需要确定谁在调用 param 函数，并确保 `$name` 变量不能为空** 

## isAjax()

![image-20240904174107294](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240904174107294.png)

最终确定，是 isAjax() 函数在调用

再进行一系列的分析，最终得到如下Payload

![image-20240904175838565](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240904175838565.png)![image-20240904175917234](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240904175917234.png)

最终借助我们自己再页面中添加的unserialize函数执行POC

![image-20240904180003295](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240904180003295.png)

