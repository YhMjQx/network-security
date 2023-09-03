# ==深信服上网行为管理AC - 部署，认证，上网权限==

1.部署模式

2.用户认证技术

3.应用控制技术

4.流量管理

5.内容审计

## 一、简单介绍

1.上网行为安全（管理）AC

- 针对于内网用户的上网行为进行管控（用户认证，行为管控，流量管控，上网审计）

## 二、部署模式

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903131516210.png" alt="image-20230903131516210" style="zoom:200%;" />

1.路由模式

- 支持所有功能，但是会改变当前网络架构（使用防火墙网关的路由功能）

![image-20230903132046356](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903132046356.png)

2.网桥模式

- 相当于一台交换机部署在网络中，但部分功能无法使用（NAT，VPN，DHCP）（透明转发方式，不改变原有网络结构）

3.旁路模式

- ，旁观的方式部署在网络环境中，不改变原有网络结构，只需在交换机的镜像口监听数据即可，无法控制UDP应用，不支持流量管理、NAT，VPN，DHCP

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903132710847.png" alt="image-20230903132710847" style="zoom:200%;" />

4.认证模式

-  该模式下提供丰富的认证功能，其他管控功能将全部关闭，适用于单独做认证服务器

## 三、用户认证技术

1.不需要认证

- 设备直接通过用户的IP地址做了认证，对于用户是无感知的

2.密码认证

- 本地用户名密码（需要直接在设备上创建用户密码）
- 外部服务器用户名密码
  - MS Active Directory
  - POP3服务器
  - 短信
  - 微信
  - ......

## 四、应用控制

1.上网权限策略

- 可以针对应用及URL进行控制，QQ白名单...

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903141111472.png" alt="image-20230903141111472" style="zoom:200%;" />

需要先自定义一个对象，但有的时候不许呀，主要是看策略管理中的上网权限中新建时，里面是否包含有所应用的对象，如果有就不需要新建<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903135949356.png" alt="image-20230903135949356" style="zoom:200%;" />

## 五、流量管理

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903145251711.png" alt="image-20230903145251711" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903143145043.png" alt="image-20230903143145043" style="zoom:200%;" />

设置好之后可以在下面的页面中进行流量控制，通过禁用和启用达到控制

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903144835893.png" alt="image-20230903144835893" style="zoom:200%;" />

1.配置限制带宽

- 限速

2.配置保证带宽

## 六、内容审计

给办公组新建一个认证策略

![image-20230903153720521](https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903153720521.png)

然后进入上网策略

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903153500896.png" alt="image-20230903153500896" style="zoom:200%;" />

开启web关键字过滤

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903153539762.png" alt="image-20230903153539762" style="zoom:200%;" />

要想在此基础上禁止带有关键字的邮箱发送，我们可以做以下配置

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903155200688.png" alt="image-20230903155200688" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903155230289.png" alt="image-20230903155230289" style="zoom:200%;" />

<img src="https://gitee.com/ymq_typroa/typroa/raw/main/image-20230903155300879.png" alt="image-20230903155300879" style="zoom:200%;" />