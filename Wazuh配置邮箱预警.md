[TOC]



# ==Wazuh配置邮箱预警==



#### 一、配置Postfix客户端

##### 1、安装mailx邮件客户端

```shell
yum install postfix mailx cyrus-sasl cyrus-sasl-plain
```

早期的邮件客户端通常使用sendmail来发送邮件，而新版本上使用的是postfix进行邮件的发送和接收。在Linux中，只要配置好邮件客户端及SMTP账号后，不仅可以向当前系统的任意账号发送内部邮件，即我们看到的 /var/spool/mail/user 的文本型邮件，也可以向外网正常的邮箱地址发送邮件，如向 [12345678@qq.com](mailto:12345678@qq.com) 发送邮件。

##### 2、配置postfix

编辑 /etc/postfix/main.cf，配置QQ邮箱。

```shell
relayhost = [smtp.qq.com]:587     # 此处建议使用587端口（针对QQ邮箱）
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_CAfile = /etc/ssl/certs/ca-bundle.crt
smtp_use_tls = yes
```

执行命令写入账户密码

```shell
# echo [smtp.qq.com]:587 15903523@qq.com:xxxx授权码xxxx > /etc/postfix/sasl_passwd
# postmap /etc/postfix/sasl_passwd
# chmod 400 /etc/postfix/sasl_passwd

# chown root:root /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db
# chmod 0600 /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db

# systemctl reload postfix
```

##### 3、向本地系统用户发邮件

```shell
echo "This is email body" | mail -s "test email" root   # 直接使用管道发送简单邮件正文

mail -s "test email" root < /etc/passwd                 # 直接使用输入重定向的方式读取一个文件内容作为正文

cp /dev/null /var/spool/mail/root   # 先清空邮件
使用 mail 命令可以直接查看邮件，输入 序号 查看邮件正文，输入 q 推出， 输入 h 回到邮件列表
```

##### 4、向外部邮箱地址发邮件

```shell
cat /etc/passwd | mail -s "Test Postfix" -r "15903523@qq.com" student@woniuxy.com

mail -s "Test Email Attachment" -r "15903523@qq.com" -a /root/wazuh-filebeat-0.1.tar.gz student@woniuxy.com < /etc/passwd

上述邮件中均需要添加 -r 参数，指定回信地址或发件人地址，否则会以“root@centqiang.localdomain”账户发送导致外发失败。
```

#### 二、在Wazuh中配置邮箱

编辑核心配置文件：/var/ossec/etc/ossec.conf，在配置文件的开始位置，修改邮箱配置节点如下：

```xml
<global>   
    <email_notification>yes</email_notification>   
    <smtp_server>localhost</smtp_server>   
    <email_from>15903523@qq.com</email_from>   
    <email_to>student@woniuxy.com</email_to>
</global>
```

![image-20211216020648935](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20211216020649.png)

另外，在ossec.conf的global节点中，还需要指定针对哪一个级别之上的预警信息发送邮件，比如设置为7级以上：

```xml
<alerts>    
    <log_alert_level>3</log_alert_level>    
    <email_alert_level>7</email_alert_level>
</alerts>
```

#### 三、短信提醒

##### 1、添加短信签名

![image-20211221173929180](https://gitee.com/ymq_typroa/typroa/raw/main/20211221173929.png)

##### 2、添加短信模板

![image-20211221174106386](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20211221174106.png)

##### 3、配置API代码

![image-20211221174653246](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20211221174653.png)

##### 4、申请 AccessKey ID和AccessKey Secret

![image-20211221174827456](https://woniumd.oss-cn-hangzhou.aliyuncs.com/security/dengqiang/20211221174827.png)