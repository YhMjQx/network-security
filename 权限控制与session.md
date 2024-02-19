[TOC]



# ==权限控制与session==

![image-20240219203903397](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240219203903397.png)

服务器通过session id 来辨别客户端是否登录过？用户是什么样改的，角色是什么样的等等。通过SESSION ID 可以唯一标识一个用户。

**但是如果一个没有权限的用户，拿到了一个拥有权限的 SESSION ID，那么该用户就可以使用该 SESSION ID 冒充用户**

```php
session_start();  //启用session模块，为客户端生成唯一标识 PHPSESSID
$_SESSION['islogin']='true';
// 登录成功后，取得当前登录用户的用户名和角色，进而判断是否有权限新增文章
$_SESSION['username']=$user['username'];
$_SESSION['role']=$role;
```

只要用到有关SESSION的东西就需要**开启**SESSION模块

我们也可以对SESSION保存中的内容进行编辑，不是编辑SESSIONID号码，而是像上面代码所说的那样 就类似于，以关联数组的形式保存信息

而且 `$_SESSION 是一个全局变量，主要在对应的目录下，都可以使用和获取 。就 $_SESSION['username']` 类似于这样的方式获取信息既可以

这样我们也可以根据信息来对不同人员做不同的判断和权限的限制





当然，我们可以使用 Fidder 进行侦测以及重发甚至是利用不同的SESSIONID进行测试

### SESSION ID 细节

同一台客户机，其SESSIONID的值是一样的，但是该SESSIONID多对应的值，也就是其中的 `$_SESSION['islogin']  $_SESSION['username']  $_SESSION['role']` 这些值，不同用户对应的值是不一样的，但是SESSION ID 确实一样的。

#### 获取不同的SESSION ID

要想在同一台客户机上访问时弄出第二个SESSION ID，很简单的一个方法，我们使用 Fidder 重发登录请求，重发时，在请求中删掉SESSIONID的值，此时服务器就会重新给客户端分配一个SESSIONID，我们就可以获得第二个SESSIONID了。

#### 利用SESSION ID

我们还可以使用普通用户通过获取到管理员用户的SESSIONID来达到进行管理员操作的目的

当然我们也可以使用获取到的SESSIONID来进行对其内部值的利用，可以进行判断，权限控制
