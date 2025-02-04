[TOC]



# ==ThinkPHP非强制路由漏洞==

通过unserialize触发

通过phar触发

与文件操作相关的函数执行 phar://xxx 时，会自动进行反序列化操作，而再构造phar文件时，我们可以自行添加想要进行序列化的内容

## 一、理解ThinkPHP路由原理

### 1、路由规则

在默认的 /tpdemo/route/route.php 文件中，定义了默认路由：

```php
// 定义了匿名控制器，访问 /public/route.php 时，直接返回结果
Route::get('think', function () {
    return 'hello,ThinkPHP5!';
});


// 访问地址 /public/hello/woniu 对应控制器为：Index，对应方法：hello，对应参数名：name，对应参数值：woniu
Route::get('hello/:name', 'index/hello');

// 自定义以下路由，那么控制器代码应该如何写?
Route::get("test$","Test/index");  // 以 $ 结尾表示 URL以test 结尾
Route::get("test/demo/:a/:b","Test/demo");  //:a :b  分别表示参数a和b
```

### 2、控制器

以下代码位于： /tpdemo/application/index/controller/Test.php

```php
<?php

namespace app\index\controller;

class Test {
    public function index() {
        echo "Test -- Index";
    }

    public function demo($a,$b) {
        echo $a + $b;
    }
}

?>
```

### 3、访问路径

上述控制器Test由于定义了路由规则，所以按照正常的路由规则访问即可：

```
http://192.168.230.188/tpdemo/public/test
```

![image-20240905224429632](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905224429632.png)

```
http://192.168.230.188/tpdemo/public/test/demo/100/200
```

![image-20240905224506010](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905224506010.png)

事实上，ThinkPHP为了考虑与早期八本的兼容性，默认保留了兼容模式，只要定义了类文件，即使不定义路由规则，也可以直接访问，这类参数再 /tpdemo/config/app.php 的全局配置文件中可以看到

![image-20240905230407453](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905230407453.png)

所以，基于兼容模式和非强制路由的情况下，我们可以直接不在定义路由规则的情况下，直接使用兼容模式访问控制并传参

```
http://192.168.230.188/tpdemo/public/index.php?s=index/test/index

http://192.168.230.188/tpdemo/public/index.php?s=index/test

http://192.168.230.188/tpdemo/public?s=index/test
```

以上三种情况的访问结果均是 Test -- Index

![image-20240905230823676](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905230823676.png)

传参的URL不同模式

```
http://192.168.230.188/tpdemo/public/index.php?s=index/test/demo/a/100/b/100

http://192.168.230.188/tpdemo/public?s=index/test/demo/a/100/b/100
```

![image-20240905231016522](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905231016522.png)

```
http://192.168.230.188/tpdemo/public/index.php?s=index/test/demo&a=100&b=100
```

![image-20240905231100965](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905231100965.png)

### 4、自动加载机制

![image-20240905231749313](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905231749313.png)

## 二、搜索潜在漏洞

![image-20240905231819907](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905231819907.png)

## 三、漏洞调用分析

URL地址访问时，注意路径使用斜杠（/），类的路径使用反斜杠（\），此时，基本上就可以通过这样的方法调用任意类中的任意方法，然后传参

![image-20240905231836737](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905231836737.png)

比如这里的第一个URL地址

![image-20240905233032370](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905233032370.png)

**调用的是 下图这个方法think控制器下的Request类的input方法**

![image-20240905233401749](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905233401749.png)

然后

![image-20240905233458360](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905233458360.png)

![image-20240905233637845](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240905233637845.png)
