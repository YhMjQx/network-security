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
        function __construct($host='localhost',$username='root',$password='p-0p-0p-0',$database='woniunote')
        {
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
        function __destruct()
        {
            // 解决办法，将 $conn 变量升级为类的 public 属性
            echo "调用析构函数，关闭数据库连接 <br>";
            mysqli_close($this->conn);
        }

    }

?>