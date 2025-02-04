[TOC]



# ==ThinkPHP反序列化漏洞一遍过==

## Windows类的__destruct()

![image-20240902222517624](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902222517624.png)

## Windows类的removeFiles()

![image-20240902222412120](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902222412120.png)

![image-20240902222429243](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902222429243.png)

构造Windows类中的 `$this->files`  也就是 `private $files = []` 属性为 一个具有 ``__toString()` 函数的类实例，序列化值后就可以调用 `__toString()` 函数 

## Conversion类中的__toString()

![image-20240902223249125](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902223249125.png)

## Windows类中的toArray()

![image-20240902223413285](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902223413285.png)

## RelationShip类中的getRelation()

![image-20240902223734335](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902223734335.png)

构造使得 `$relation` 返回得到的结果是类的实例，并且该构造的类实例中没有 visible 这个函数，但是需要有 __call() 函数 

## Request类中的__call()函数

![image-20240902224134303](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240902224134303.png)

构造 `$this->hook[$method]` 类属性为一个关联数组，且 该关联数组中的 键为 visible ，但是值就可以随意构造代码，此时就可以执行代码。所传入的参数基本就没有影响。