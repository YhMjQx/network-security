[TOC]



# ==Servlet与JSP结合==

后台接口我们称之为 Servlet，可以和JSP联动，将数据处理好了之后交由JSP输出到前端，也可以自己输出内容到前端

这一节课的内容就是将用户注册和文件上传使用Servlet来实现

## 一、如何在JSP也买那种使用Ajax方式提交数据

首先来点常识，有关编译的问题。

out > artifacts > JavaWeb_Tomcat_war_exploded 目录下的东西才是我们真正运行的环境

![image-20250110215435113](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250110215435113.png)

web 目录下的内容只是我们的开发环境

![image-20250110215558026](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250110215558026.png)

ajax方式提交的前端代码

```jsp
<%--
  Created by IntelliJ IDEA.
  User: hp
  Date: 2025/1/10
  Time: 15:17
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>用户注册</title>
    <script src="static/jquery-3.4.1.min.js" type="application/javascript"></script>
    <script>
        function doReg(){
            var username = $("#username").val();
            var password = $("#password").val();
            var formData = new FormData();  // 带附件上传,使用该对象，会自己构造一个 multipart 类型的请求
            formData.append("username",username);
            formData.append("password",password);
            formData.append("photo",$("#photo").prop("files")[0]);
            enctype="multipart/form-data";

            // 将数据交给 doreg.jsp 处理和上传
            $.ajax({
                url: 'doreg.jsp',
                type: 'POST',
                data: 'formData',
                cache: false,
                processData: false,
                contentType: false,


                success : function (data) {
                    window.alert(data);
                }
            });

        }
    </script>
</head>
<body>
    选择文件: <input type="file" id="photo" /> <br/>
    <input type="text" value="woniu" id="username" /> <br/>
    <input type="password" value="123456" id="password" /> <br/>
    <input type="button" value="上传" onclick="doReg()" />
</body>
</html>

```

后端代码

```jsp
<%@ page import="org.apache.commons.fileupload.disk.DiskFileItemFactory" %>
<%@ page import="org.apache.commons.fileupload.servlet.ServletFileUpload" %>
<%@ page import="java.util.List" %>
<%@ page import="org.apache.commons.fileupload.FileItem" %>
<%@ page import="org.apache.commons.fileupload.servlet.ServletRequestContext" %>
<%@ page import="java.io.File" %><%--
  Created by IntelliJ IDEA.
  User: hp
  Date: 2025/1/10
  Time: 17:45
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>注册认证</title>
</head>
<body>
    <%
        request.setCharacterEncoding("utf-8");
        response.setCharacterEncoding("utf-8");
        String savePath = request.getServletContext().getRealPath("/upload");  //
        DiskFileItemFactory factory = new DiskFileItemFactory();
        ServletFileUpload upload = new ServletFileUpload(factory);
        try{
            // 使用 commons-filupload 组件，会获取所有表单元素，所以不再需要 request.getxxx() 这样的操作
            List<FileItem> items = upload.parseRequest(new ServletRequestContext(request));
            for(FileItem item:items){
                // 如果不是普通的表单元素，则实现文件上传
                if(!item.isFormField()) {
                    System.out.println("savePath = " + savePath);
                    item.write(new File(savePath + "/" + item.getName()));
                    response.getWriter().println("文件上传成功");
                }
                // 如果该表单的名称叫做 username ，则定义一个变量去获得该表单的值
                else if (item.getFieldName().equals("username")){
                    String username = item.getString();
                    System.out.println("username: "+username);
                }
                // 如果该表单的名称叫做 password ，则定义一个变量去获得该表单的值
                else if(item.getFieldName().equals("password")) {
                    String password = item.getString();
                    System.out.println("password: "+password);
                }
            }
        } catch (Exception e) {
            // 防止上传时文件不存在导致的异常错误
            e.printStackTrace();
        }
    %>
</body>
</html>

```

但是，我是用 ajax 方式上传文件，我明明使用了 formData 对象，并且设置了 ContentType: false 但最终还是给我报错![image-20250110234327307](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250110234327307.png)

~操了，为啥呀，我真醉了，看了这么多帖子，都只有这方法，问题和症状完全一样，就是解决不了~

![image-20250110223328477](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250110223328477.png)

使用 ajax 上传文件和注册时发生了一个非常令人恶心的事情，报错信息如下

```
org.apache.commons.fileupload.FileUploadException: the request was rejected because no multipart boundary was found
	at org.apache.commons.fileupload.FileUploadBase$FileItemIteratorImpl.<init>(FileUploadBase.java:1033)
	at org.apache.commons.fileupload.FileUploadBase.getItemIterator(FileUploadBase.java:334)
	at org.apache.commons.fileupload.FileUploadBase.parseRequest(FileUploadBase.java:358)
	at org.apache.jsp.doreg_jsp._jspService(doreg_jsp.java:142)
	at org.apache.jasper.runtime.HttpJspBase.service(HttpJspBase.java:70)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:765)
	at org.apache.jasper.servlet.JspServletWrapper.service(JspServletWrapper.java:465)
	at org.apache.jasper.servlet.JspServlet.serviceJspFile(JspServlet.java:383)
	at org.apache.jasper.servlet.JspServlet.service(JspServlet.java:331)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:765)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:231)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
	at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
	at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:197)
	at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:97)
	at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:543)
	at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:135)
	at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92)
	at org.apache.catalina.valves.AbstractAccessLogValve.invoke(AbstractAccessLogValve.java:698)
	at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:78)
	at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:367)
	at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:639)
	at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65)
	at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:885)
	at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1693)
	at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)
	at org.apache.tomcat.util.threads.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1191)
	at org.apache.tomcat.util.threads.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:659)
	at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
	at java.lang.Thread.run(Thread.java:748)

```

