[TOC]



# ==ThinkPHP框架项目实战==

## 在ThinkPHP框架下，渲染 login-ajax.html

![image-20240303211930627](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240303211930627.png)

## 一、修改route目录下的 app.php

```php
#添加如下路由规则
// 用户登录
Route::get('user','User/index');
```

表示当我们在浏览器中输入 localhost/login ，便会自动跳转到User这个控制器下的login方法，因此我们还需要自己创建一个User控制器并再起内部添加login方法

## 二、在 app/contrillor 目录下创建 User.php

并添加如下内容

```php
<?php
namespace app\controller;  // PHP命名空间，用于对不同的类进行归类管理，同时允许不同命名空间下类重名

use app\BaseController;  //引用命名空间

class User extends BaseController{
    public function index() {
        return 'Login';
        // return view('../../view/login.html');
    }
}
?>
```

现在访问 localhost/user

![image-20240304203151838](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240304203151838.png)

## 三、渲染login.html页面

那么我们现在要渲染 login.html 页面，就可以在该方法下渲染，使用 view 视图，就是上面代码中的 `return view('../../view/login.html');` 前提是需要将login.html页面代码复制到指定的view目录下

试着访问一下 localhost/user发现是报错的

![image-20240304203420462](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240304203420462.png)

> 在这里我们提一嘴，config/app.php 文件中 最后一行的代码 `'show_error_msg'  => true,`   作用是 显示错误信息  true表示正确输出错误在哪 false是默认选项，但只是报错，但不知道错在哪 ，调试环境就修改为 true ，生产环境就默认flase就好

### 1.安装 think-view 库

上述的报错就是因为没有安装这个模版引擎

在框架目录下执行以下命令

```
D:\PHP\ThinkPHP\TPDemo>composer require topthink/think-view
```

![image-20240304203942983](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240304203942983.png)

然后我们访问一下 localhost/user

![image-20240304204318719](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240304204318719.png)

> 这个图片中URL地址的login是正确的，之所以我上面说user，是因为我将login修改了一下改成了user，总体换下来效果还是一样的

这是为什么呢

> 注意：我们是将 public 目录设置为DocumentRoot，我们访问视图 view 目录下的文件时，是以public为默认主目录的，因此我们需要将 `return view('../../view/login.html');` 修改为 `return view('../view/login.html');`

现在访问 localhost/user

![image-20240304204606375](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240304204606375.png)

可以访问了，但是由于该模板文件使用的是 ajax 方式，因此还需要引入jquery库，以及背景图片

public目录下创建image目录存放背景图

jquery库存放在 public/static 目录下

### 2.User.php目录下创建登录方法

```php
public function login() {
    // 助手函数 request 获取request对象
    $username = request()->post('username');
    $password = request()->post('password');
    $vericode = request()->post('vericode');

    // 验证前后端连通性
    // if($username == 'ymq') {
    //     return 'login-pass';
    // }
    // else{
    //     return 'login-fail';
    // }

    // 从数据库中测试登录

}
```

### 3.实现数据库访问

#### ORM模型

对象关系映射 Object-Relation Mapping ：将关系型数据库中的一张表映射为PHP中的一个类或对象。表的每一列就是类的一个属性，每一行就相当于是类的一个实例

### （1）修改数据库连接信息

修改文件 config/database.php 

```
// 数据库类型
'type'            => env('database.type', 'mysql'),
// 服务器地址
'hostname'        => env('database.hostname', '127.0.0.1'),
// 数据库名
'database'        => env('database.database', 'woniunote'),
// 用户名
'username'        => env('database.username', 'root'),
// 密码
'password'        => env('database.password', 'p-0p-0p-0'),
// 端口
'hostport'        => env('database.hostport', '3306'),
```

### （2）定义模型

在 app目录下 新建文件夹 model ，然后在model目录下新建文件 User.php

```php
<?php
    namespace app\model;
    use think\Model;
    class User extends Model {
        // 如果主键名不为id，则必须手工指定主键名称
        protected $pk = 'userid';
        // 当前模型指定表名称，如果类名与表名一致，则可以不用指定
        protected $name = 'users';
    }
?>
```

这是一个继承自Model类的类，我们将会在User控制器下的login方法中使用到他

### （3）编写User控制器下的login方法

```php
public function login() {
    // 助手函数 request 获取request对象
    $username = request()->post('username');
    $password = request()->post('password');
    $vericode = request()->post('vericode');

    // 验证前后端连通性
    // if($username == 'ymq') {
    //     return 'login-pass';
    // }
    // else{
    //     return 'login-fail';
    // }

    // 从数据库中测试登录
    $user = new \app\model\User();  // 这就是刚刚的那个类
    $result = $user->where(
        [
            'username' => $username,
            'password' => $password
        ]
    )->select(); // 这些方法都是继承自Model类的
    if(count($result) == 1) {
        return 'login-pass';
    }
    else {
        return 'login-fail';
    }
    // return json($result);
    // print_r($result);
}
```



