<?php

/**
 * 封装：public private protected
 * 1.默认情况下，所有属性和方法，在没有明确设置访问修饰符时，均为public
 * 2.private 表示类私有，被定义的属性只有在类的定义代码中才可以使用，类的实例和子类中均无法使用
 * 3.protected 表示受类的保护，实例中不能直接使用，只有在在本类和子类的定义代码中才可以使用
 */
class People{
    // 在类中，这些东西叫做属性
    // 定义类时，可以给属性设置一个初始值
    // 使用了访问修饰符后，就不再需要 var 
    private $name = '父亲';
    var $age = '';
    var $addr = '';
    var $nation = '';

// 定义People类所具有的方法，默认情况下，方法的定义与函数完全一致
    function talk() {
        echo "$this->name 正在说话 他的年龄才 $this->age 岁<br>";
    }
    protected function work() {
        echo "$this->name 正在工作 他的年龄才 $this->age 岁<br>";
    }
    // 设置公有方法调用私有方法
    function eat($type='长寿面') {
        echo "$this->name 正在吃 $type <br>";
        $this->work();
    }
    // 针对私有属性，如何在示例中对其进行修改？
    // 设置公有方法操作私有属性
    function changename($name) {
        $this->name = $name;
    }
    function getname() {
        return $this->name;
    }
}

// $p1 = new People();
// // $p1->name = 'ymqyyds';  //实力无法使用类的私有属性
// $p1->age = 20;
// $p1->talk();
// $p1->changename("ymqyyds");
// echo $p1->getname()."<br>";
// $p1->eat();


/**继承：子承父业，继承传统，发扬光大
 * 定义子类 Man 会继承父类People的所有非私有属性和方法
 * 子类继承父类时，可以在子类中调用父类的protected修饰的属性和方法，也可以覆盖和重写父类的方法
 * 子类也可以在自己的类中扩展和创新新的方法和属性
 * final 关键字，如果一个类被 final 修饰，则该类不能被继承，表明该类就是最后一个类了
 */

class Man extends People {
    // 什么都不做可直接使用People的所有非私有方法和属性
    var $name;
    var $phone = '';
    // 父类的方法在子类中可以覆盖，也称为，重写 override
    function talk() {
        echo "$this->name 正在说话 <br>";
    }
    function eat($type='长寿面') {
        echo "$this->name 正在吃 $type <br>";
        parent::work();
    }

    function callphone() {
        echo "请打电话给1377281626 <br>";
    }
}
/**子类调用属性和方法，如果没有重写，那么首先调用父类的，如果子类有重写，那么就调用子类重写的 */

$m = new Man();
// 其实子类也可以直接定义一个父类定义过的属性并使用
// $m->name = 'wcnb';
// echo $m->name."<br>";

$m->talk(); // 不重写时，父亲 ...
$m->eat();  // 不重写时，父亲 ...
// 以上调用类的方法时，如果子类没有重写父类的方法，那么调用的结果还是父类方法的结果，如果重写了，那么久调用的是 子类的方法 

// 通过下面修改类姓名的方式才得以修改子类的属性，然后再调用父类的方法，结果就和父类不一样了
// $m->changename('儿子');
// echo $m->getname()."<br>";  // 儿子
$m->name = '儿子'; // 也可以直接给子类属性赋值
$m->talk();  //儿子 正在...
$m->eat();  //儿子正在吃，父亲正在工作 eat的是子类方法，work的是父类方法
// $m->work();

/**多态:多种形态 */
// 抽象类：只要类的方法中有一个方法使用 abstract 关键字定义，则该类就是抽象类，该方法就是抽象方法
// 抽象类的特点：不能被实例化，只能被继承，抽象方法不能有实现代码（不能有函数体）
abstract class animal{
    // function can() {
    //     echo "this function will be rewrited in the children <br>";
    // }
    abstract function can(); // 抽象方法必须被子类实现，且父类不能有实现的代码

}
class cat extends animal{
    function can(){
        echo "i can climb <br>";
    }

}
class dog extends animal{
    function can() {
        echo "i can swim <br>";
    }

}
function test($obj){
    $obj->can();
}
test(new cat());
test(new dog());

?>