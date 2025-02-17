[TOC]



# ==Java开发框架SpringBoot与Maven==

## Maven

简单来说 Maven 解决了 java 原本开发中使用的 lib 依赖问题，使用Maven对应的xml语句和标签，可以让Maven在他自己的对应仓库中去下载对应的依赖，如果本地磁盘已经有了该依赖包，那么直接引用就好了，大大减小了项目源代码的大小，在传播过程中可以避免传播 jar 包

![image-20250111230002973](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250111230002973.png)

如上所示的xml标签，在Maven构建的时候他会自己去Maven的仓库中下载alibab的fastjson的依赖库并匹配好对应的版本

### 如何使用Maven来管理本地源代码，即在编译器中关联源代码

#### （1）使用Maven关联

- 对项目添加Maven框架支持

  ![image-20250115164525466](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115164525466.png)

  ![image-20250115164421937](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115164421937.png)

此时项目中会生成一个 pom.xml，该文件就是进行管理依赖的文件

然后，去maven官网查找依赖的xml，然后把xml按照对应的格式添加进pom.xml，然后右上角的Maven视图进行刷新

![image-20250115170437597](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115170437597.png)

接下来比如要添加mysql-connector5.1.49的依赖包，那么我们编写如下所示xml文件

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.49</version>
</dependency>
```

然后将其放在pom.xml文件的`<dependencies></dependencies>`标签中,，然后点击右上角进行刷新，Maven就会自动帮我们下载

此时我们在右侧的文件栏中将下载好的依赖打开，我们会看到文件上方有这么一句描述

![image-20250115170935387](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115170935387.png)

这是 IDEA 给我们做的反编译，将jar包的源代码反编译之后给我们展示出来，这样虽然方便，反编译后的代码虽然逻辑是一样的，但是会出现变量命名的问题。比如：

![image-20250115171139562](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115171139562.png)

变量命名成了 val...

当然，如果我们将依赖包直接下载到本地，就不会出现这样的问题了

![image-20250115171321092](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115171321092.png)

#### （2）进行源码加载

将自己的源码 src.zip 直接加载到IDEA中去

![image-20250115171704712](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115171704712.png)

![image-20250115171747710](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115171747710.png)

学会使用 Find Usages和jump

![image-20250115175843895](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250115175843895.png)

这是除了代码调试的另一种审计方法

教材内容

#### 一、创建SpringBoot项目

1、新建一个项目并输入基本信息

![image-20250112140446683](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112140446683.png)

2、选择内置依赖

Spring Boot 3.X版本不支持JDK 8且主要支持JDK 17版本，所以如果不想处理JDK版本的问题，可以创建Spring Boot 2.X项目。但是后续配置和使用可能略有不同，建议与笔者保持相同版本。

![image-20250112140628401](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112140628401.png)

点击完成，此时会自动下载依赖的Jar包和其他需要的组件。此处可以帮助我们快速查找后续需要添加的依赖：https://blog.csdn.net/zly03/article/details/127631115，如果在创建项目时，有些依赖没有选中，也不用担心，后续再添加即可。

![image-20250112141306266](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112141306266.png)

3、为服务启动配置端口

![image-20230822000653288](https://gitee.com/ymq_typroa/typroa/raw/main/202308220006334.png)

![image-20250112141806133](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112141806133.png)

等依赖都安装完成了之后，我们点击IDEA右上角的绿色三角进行run

![image-20250112143447518](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112143447518.png)

我们可以看到，此时 tomcat started on ports 9000 ，这就是我们之前在 application 文件中设置的端口号

4、编写UserController接口

![image-20230822003800930](https://gitee.com/ymq_typroa/typroa/raw/main/202308220038978.png)

第一步：先创建一个Java Class类

![image-20250112143159544](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112143159544.png)

第二步：为了让这个接口能够跑起来，需要将这个类注解为RestController

![image-20250112143257259](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112143257259.png)

第三步：构建一个方法叫做 HelloWorld：

创建方法的同时，给这个方法也来一个注解，注解了之后该方法的return内容直接就可以变成一个响应

![image-20250112144052280](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112144052280.png)

我们去浏览器中访问一下 

![image-20250112144146731](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112144146731.png)

该问题的原因是，我们配置了一个接口必须要重启，当然我们为了避免重启的不方便，我们也可以选择配置一下自动构建，也就是下面说的热部署

5、实现热部署

![image-20250112144445345](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112144445345.png)

每次更新了代码后，在Build菜单中单击“Recompile XXXX.java”,便可以触发SpringBoot自动重启，方便及时看到更新后的效果。是因为我们装了 Dev Tools

![image-20250112144607471](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112144607471.png)

然后再去浏览器中访问一下，发现构建的方法的return的内容果真变成了相应

![image-20250112144638838](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112144638838.png)

> 当然，如果我们已经决定该方法是GET请求的话，我们可以直接使用 GETMapping
>
> ![image-20250112144924884](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112144924884.png)
>
> 如果我们给整个控制器来一个注解，那么我们的请求方式也会发生变化
>
> ![image-20250112145057081](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112145057081.png)
>
> ![image-20250112145124148](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250112145124148.png)
>
> ![image-20250112145140880](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112145140880.png)
>
> 

#### 二、URL地址与参数传递

> 上面已经介绍过以GET方式请求和传参，下面介绍如何配置POST请求和传参
>
> - 以Servlet方式请求和接收
>
> - ![image-20250112150628822](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112150628822.png)
>
> - ```java
>   @PostMapping(value = "/login")
>   public String login(HttpServletRequest request) {
>       String username = request.getParameter("username");
>       String password = request.getParameter("password");
>       
>       if(username.equals("woniu") && password.equals("123456")) {
>           return "登录成功";
>       }
>       else {
>           return "登录失败";
>       }
>       
>   }
>   ```
>
> ![image-20250112150535232](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112150535232.png)
>
> ![image-20250112150602330](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112150602330.png)



1、定义URL地址

```java
@RestControllerpublic 
class IndexController {    
    @RequestMapping(value = "/hello", method = RequestMethod.GET)    
    public String hello() {        
        return "Hello World .";    
    }    
    @GetMapping("/list")    
    public List<String> list() {        
        List<String> list = new ArrayList<String>();        
        list.add("111111");        
        list.add("222222");        
        list.add("333333");        
        return list;    
    }
}
```

2、使用URL地址传递

```java
@GetMapping(value = "/list/{id}")
public String list(@PathVariable int id) {    
    return "用户编号为：" + id;
}
// 此处必须要使用 @PathVariable 声明 id 与地址参数的 id 对应上,否则/list/{id}里的id与int id里的id映射关系会发生错误
```

```java
// 需注意list/{maxid}与@PathVariable int maxid里的maxid要对应上，不仅要样子对应上，还要映射关系正确，所以要写的一样还要使用 @PathVariable
@GetMapping(value = "list/{maxid}")
public String list(@PathVariable int maxid) {
    String content = "";
    try{
        Class.forName("com.mysql.jdbc.Driver").newInstance();  //在旧版本的Java中手动加载并注册MySQL JDBC驱动
        Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/woniunote?user=root&password=p-0p-0p-0&useUnicode=true&characterEncoding=UTF8");
        //还可以使用PreparedStatement来对SQL语句进行预处理
        String sql = "select * from users where userid < ?";
        PreparedStatement ps = conn.prepareStatement(sql);  // 创建一个可以预处理SQL语句的对象叫做ps
        ps.setInt(1,maxid);  // 由于上面定义maxid时就用的是String定义的，所以这里使用的就是 setString()。其意思是，把 maxid 的值，复制到第一个 ? 所在位置
        ResultSet rs = ps.executeQuery(); // 由于在上面已经进行了SQL语句的预处理，所以在这里 executeQuery() 时，就可以不传参数

        while(rs.next()){
            int userid = rs.getInt("userid");
            String username = rs.getString("username");
            String password = rs.getString("password");
            String role = rs.getString("role");
            //            response.getWriter().printf("编号 %d,用户名 %s,密码 %s,角色 %s</br>",userid,username,password,role);  // 这里使用 print格式化输出
            //接下来使用给内容修建一个表格
            content += "<table><tr>";
            content += "<td>"+userid+"</td>";
            content += "<td>"+username+"</td>";
            content += "<td>"+password+"</td>";
            content += "<td>"+role+"</td>";
            content += "</tr></table>";
        }
    }
    catch (Exception e) {
        e.printStackTrace();
    }
    return content;

}
```

![image-20250112153426682](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112153426682.png)

3、使用方法参数传递

```java
@RequestMapping(value = "/login", method = RequestMethod.POST)
public String login(String username, String password) {    
    SystemUtility util = new SystemUtility();    
    String sql = "select * from user where username='"+username+"' and password='"+password+"'";    
    System.out.println(sql);
}

@PostMapping(value = "login2")
public String login2(String username,String password) {
    return "用户名：" + username + " , 密码为：" + password;
}
```

![image-20250112151259681](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112151259681.png)

4、在方法中定义HttpServletRequest，然后直接利用Servlet传递

```java
@PostMapping(value = "/login")
public String login(HttpServletRequest request) {
    String username = request.getParameter("username");
    String password = request.getParameter("password");

    if(username.equals("woniu") && password.equals("123456")) {
        return "登录成功";
    }
    else {
        return "登录失败";
    }
}
```

#### 三、实现用户登录注册

1、处理Session

```java
@GetMapping(value = "/session")public String session(HttpServletRequest req) {    HttpSession session = req.getSession();    session.setAttribute("username", "WoniuSession");    return session.getAttribute("username").toString();}
```

2、登录验证

```

```

3、用户注册

```

```

#### 四、实现查询返回JSON字符串

默认情况下，SpringBoot自带JSON格式转换功能，对Array、List、Map等内置数据格式可以进行自动转换。但是如果是特殊类型，如ResultSet，建议先将其转换为List对象：

```java
import com.alibaba.fastjson.JSON;import com.alibaba.fastjson.JSONArray;import com.alibaba.fastjson.JSONObject;public String rs2Json(ResultSet rs) {    JSONArray jsonArray = new JSONArray();    JSONObject rowObj = null;    try {        ResultSetMetaData rsmd = rs.getMetaData();        while (rs.next()) {            rowObj = new JSONObject();            int columnCount = rsmd.getColumnCount();            for (int i = 1; i <= columnCount; i++) {                String columnName = rsmd.getColumnName(i);                String value = rs.getString(columnName);                rowObj.put(columnName, value);            }            jsonArray.add(rowObj);        }    } catch (SQLException e) {        e.printStackTrace();    }    return jsonArray.toString();}
```



在编写这样的代码时，我们发现 JSON 在代码编译时找不到，会报错，原因时因为我们并没有在Maven的pom.xml中配置依赖，解决方法如下：

![image-20250112153903281](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112153903281.png)

我们编写如图所示的代码将其放在 pom.xml 的 dependencies 标签中

![image-20250112154224387](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112154224387.png)

```xml
</dependencies> 
	<dependency>
    	<groupId>com.alibaba</groupId>
    	<artifactId>fastjson</artifactId>
    	<version>1.2.24</version>
	</dependency>
</dependencies>
```

然后打开IDEA右侧的Maven视图并刷新Maven依赖，之后等待依赖下载完成即可

![image-20250112154352669](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112154352669.png)

下载完之后我们可以看到，此时该依赖中的字体颜色已变成白色，则表示已下载完成

![image-20250112154436594](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112154436594.png)

此时源代码中的JSON也可以访问了，甚至我们还可以直接在Maven视图中下载依赖的源代码

![image-20250112154649651](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250112154649651.png)