[TOC]



# ==PHP面向对象编程实战==

### 1.创建数据库类

```php
<?php
    // function create_dbcon() {
    //     $conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote') or die("数据库连接失败");
    //     mysqli_set_charset($conn,'utf-8');
    //     return $conn;
    // }

    /**利用面向对象的特性改造数据库操作 */
    class DB {
        // 为DB类定义数据库连接的必要属性,并给定默认值
        var $host = 'localhost';
        var $username = 'root';
        var $password = 'p-0p-0p-0';
        var $database = 'woniunote';

        // 定义一个方法，用于建立数据库连接
        function connect_db() {
            $conn = mysqli_connect($this->host,$this->username,$this->password,$this->database) or die("数据库连接失败");
            mysqli_set_charset($conn,'utf8');
            return $conn;
        }

        // 定义一个方法，用于执行sql查询语句
        function query($sql) {
            $conn = $this->connect_db();
            $result = mysqli_query($conn,$sql);
            $rows = mysqli_fetch_all($result,MYSQLI_ASSOC);
            return $rows;
        }

        // 定义一个方法，用于执行数据库修改sql语句
        function update($sql) {
            $conn = $this->connect_db();
            $result = mysqli_query($conn,$sql);
            if(!$result) {
                die("数据库更新失败");
            }
        }
        /**但是我们发现 query  update 两个方法，调用一次就要创建一次数据库连接
         * 一点连接创建好做一件事就不用了，浪费了很多资源，这确实是个问题，我们应该一个链接可以做很多事情才对
        */

        // // 定义一个方法，用于关闭数据库连接，不过这方法时错误的
        // function closecondb() {
            // 在函数体内创建一个局部变量的连接，然后关闭，这不是很蠢吗
        //     $conn = $this->connect_db();
        //     mysqli_close($conn);
        //     echo "数据库连接已关闭 <br>";
        // }
        /**该方法可以使用类的析构方法
         * 类的析构方法，当类的实例使用完并从内存中释放时，将会出发调用该方法
         * PHP中内置了16个魔术方法 均已 __开头，例如 __destruct() 析构函数
         */
        function __destruct(){
            
        }
    }
?>
```

### 2.在代码中进行引用

```php
<?php

    include_once("commoncondb.php");
    $db1 = new DB();
    $db1->host = '127.0.0.1';
    $db1->username = 'root';
    $db1->password = 'p-0p-0p-0';
    $db1->database = 'woniunote';

    $rows = $db1->query("select articleid,headline from article where articleid<11;");
    // print_r($rows);

    // $result = $db1->update("update article set headline='会员福利姬到底是个什么鬼？' where articleid=9;");

    ////// mysqli_close($db1->conn);  // 此方法是错误的，传参不能直接通过类实例引用类方法中局部变量，除非他是一个public属性
    $db1->closecondb();
?>

```

### 3.存在的问题

- 每次执行 query 和 update 方法时，都会调用 connect_db 方法，建立一次数据库连接
- 如何关闭数据库连接
  - 这是**错误**的举例：mysqli_close($db->conn) 不能直接通过类实例引用类方法中的局部变量，除非变量是 类的public属性
  - 下面的说法是**正确**的：使用类析构方法可以完成自动的关闭，并且代码在调用中不需要考虑关闭连接的问题

```php
<?php
    // function create_dbcon() {
    //     $conn = mysqli_connect('localhost','root','p-0p-0p-0','woniunote') or die("数据库连接失败");
    //     mysqli_set_charset($conn,'utf-8');
    //     return $conn;
    // }

    /**利用面向对象的特性改造数据库操作 */
    class DB {
        // 为DB类定义数据库连接的必要属性,并给定默认值
        // 由于在类实例化时通过传参，使用类方法可以对这些属性进行赋值，于是边设置为私有属性，更安全
        private $host = '';//localhost
        private $username = '';//root
        private $password = '';//p-0p-0p-0
        private $database = '';//woniunote
        // 将数据库连接对象定义为类属性
        private $conn = null;
        
        // 定义一个方法，用于建立数据库连接
        function connect_db() {
            $this->conn = mysqli_connect($this->host,$this->username,$this->password,$this->database) or die("数据库连接失败");
            mysqli_set_charset($this->conn,'utf8');
            return $this->conn;
        }

        // 使用类的构造方法，当类在进行实例化时，触发执行该方法
        function __construct($host='localhost',$username='root',$password='p-0p-0p-0',$database='woniunote') {
            // 函数内传的形参具有默认值，我们在构造类实例时，可以按照自己的需求传参
            $this->host=$host;
            $this->username=$username;
            $this->password=$password;
            $this->database=$database;
            // 因此，实例化一个对象，就只会创建一个 $conn 对象
            echo "调用构造函数，创建数据库连接 <br>";
            $this->connect_db();
        }

        // 定义一个方法，用于执行sql查询语句
        function query($sql) {
            // $conn = $this->connect_db();
            $result = mysqli_query($this->conn,$sql);
            $rows = mysqli_fetch_all($result,MYSQLI_ASSOC);
            return $rows;
        }

        // 定义一个方法，用于执行数据库修改sql语句
        function update($sql) {
            // $conn = $this->connect_db();
            $result = mysqli_query($this->conn,$sql);
            if(!$result) {
                die("数据库更新失败");
            }
        }
        /**但是我们发现 query  update 两个方法，调用一次就要创建一次数据库连接
         * 一点连接创建好做一件事就不用了，浪费了很多资源，这确实是个问题，我们应该一个链接可以做很多事情才对
         * 使用类的构造函数 __construct() 
        */

        // // 定义一个方法，用于关闭数据库连接，不过这方法时错误的
        // function closecondb() {
            // 在函数体内创建一个局部变量的连接，然后关闭，这不是很蠢吗
        //     $conn = $this->connect_db();
        //     mysqli_close($conn);
        //     echo "数据库连接已关闭 <br>";
        // }
        /**该方法可以使用类的析构方法
         * 类的析构方法，当类的实例使用完并从内存中释放时，将会出发调用该方法
         * PHP中内置了16个魔术方法 均已 __开头，例如 __destruct() 析构函数
         */
        function __destruct() {
            // 解决办法，将 $conn 变量升级为类的 public 属性
            echo "调用析构函数，关闭数据库连接 <br>";
            mysqli_close($this->conn);
        }
    }
?>
```

- 类的属性是私有的，那么又怎么使用不同的属性值连接不同的数据库呢？
  - 使用构造方法然后带有默认参数和值的方式，进行传参，然后使用构造方法修改类的私有属性

```php
// 使用类的构造方法，当类在进行实例化时，触发执行该方法
function __construct($host='localhost',$username='root',$password='p-0p-0p-0',$database='woniunote')
{
    // 函数定义时传的形参具有默认值，我们在构造类实例时，可以按照自己的需求传参
    $this->host=$host;
    $this->username=$username;
    $this->password=$password;
    $this->database=$database;
    // 因此，实例化一个对象，就只会创建一个 $conn 对象
    echo "调用构造函数，创建数据库连接 <br>";
    $this->connect_db();
}
```

