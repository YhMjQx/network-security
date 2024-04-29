import socket,threading,os,time,scapy
import statistics

from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import ARP
from scapy.sendrecv import sr1
# 引入以下，方式报ERROR，WARNNING
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# 端口扫描
# 对目标IP进行端口扫描，尝试连接目标IP和端口，如果连接成功，说明端口开放，否则未开放

def singal_port_scanner(ip):
    for port in range(1,65536):
        try:
            s = socket.socket()
            s.settimeout(0.5)  # 超时时间要在连接之前设置，不然等测试连接完成了之后在设置还有什么意义
            s.connect((ip,port))
            print(f'{ip} 的 {port} 号端口可用')
            s.close()
        except:
            pass
            # 主打的就是错误情况（连接不上）不处理，只输出连接正常的情况
            # print(f'{ip} 的 {port} 号端口不可用')

def thread_port_scanner(ip,start):
    for i in range(start,start+50):
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((ip,i))
            print(f'{ip} 的 {i} 号端口可用')
            s.close()
        except:
            pass


# 直接爆破的情况有风险，很容易被封IP，因此我们可以使用常用端口代替所有端口，然后每次休息一定的时间
# 将常用端口进行优先扫描，量少后，可以让每一次端口扫描完成后，停止3秒（可以防止IDS，IPS的阈值检测）
# 另外，如果是真实环境，建议在扫描之前，先用别的公网ip进行验证，确认是否存在入侵防御
def normal_port_scanner(ip):
    common_ports = [
        21,22,23,25,53,80,110,143,443,445,3306,8080,8443,1521,5432,9000,9080,9092,9200,9300,27017,6379,5672,15672,5900,3389
    ]
    for port in common_ports:
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((ip,port))
            print(f'{ip} 的 {port} 号端口可用')
            s.close()
        except:
            pass
        time.sleep(3)


# 如果想要进行内网渗透，则必须要知道有哪些IP地址是存活的，可以访问的
# IP地址工作在IP层，ICMP，ARP 都含有IP信息
# 首先执行 ping 进行IP探测
# 但是这种情况一旦主机开启了防火墙，阻拦了ICMP，我们就没有办法通过此方法进行探测了，那么该如何解决呢
def ip_scanner_ping1():
    for i in range(1,255):
        respondes = os.popen(f'ping 192.168.1.{i}').read()
        if 'TTL=' in respondes:
            print(f'192.168.1.{i} online')

def ip_scanner_ping2():
    for i in range(1,255):
        respondes = os.popen(f'ping 192.168.110.{i} -n 1 -w 100 | findstr TTL=').read()
        if len(respondes) > 0:
            print(f'192.168.110.{i} online')


# 经发现，电脑是不会方式ARP的流量的，否则就会直接断网，所以我们可以使用ARP数据包作为嗅探
# ARP扫描IP
def scapy_ip_scanner(start):
    for i in range(start,start+10):
        try:
            pkg = ARP(psrc='192.168.110.39', pdst=f'192.168.110.{i}')
            replay = sr1(pkg, timeout=1, verbose=False)  # verbose=False 不报错
            # print(replay[ARP].hwsrc)
            print(f'192.168.110.{i} 在线 MAC为 {replay[ARP].hwsrc}')
        except:
            # print(f'192.168.110.{i}不在线')
            pass



# 扫描端口，端口在TCP协议通信中存在，因此我们可以构造TCP数据包通信，并且不需要完整的三次握手
# 如果可以有 SYN -> FIN ACK 半连接状态，即回复的数据包中flags=FA 就说明，目标端口正常开放
# 如果 SYN -> RST ACK 这种半连接状态 即回复的数据包中flags=RA 就说明，目标端口未正常开放
def scapy_port_scanner(ip):
    # 利用这种数据包构造的方式我还可以伪造源IP地址
    #以及伪造数据包类型，比如直接发送一个ACK的数据包，跳过SYN和FINSYN, 甚至直接发送四次挥手的数据包
    # pkg=IP(src='110.110.110.110',dst='192.168.230.147')/TCP(dport=80,flags="A")
    # replay=sr1(pkg,timeout=3)
    common_ports = [
        21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 8080, 8443, 1521, 5432, 9000, 9080, 9092, 9200, 9300, 27017,
        6379, 5672, 15672, 5900, 3389
    ]
    for port in common_ports:
        try:
            pkg = IP(src="192.168.110.39",dst=ip)/TCP(dport=port,flags="S")
            replay = sr1(pkg,timeout=1,verbose=False)
            # print(f'端口 {port} 开放，回复数据包类型 {replay[TCP].flags}')
            # if replay[TCP].flags == 'SA':
            if replay[TCP].flags == 0x012:
                print(f'端口 {port} 开放')
        except:
            pass


if __name__ == '__main__':
    # singal_port_scanner('192.168.230.135')
    # singal_port_scanner('192.168.230.147')

    # for i in range(1,65536,50):
    #     t = threading.Thread(target=thread_port_scanner, args=('192.168.230.147', i))
    #     t.start()

    # normal_port_scanner('192.168.230.147')

    # 加个多线程也一样提升速度
    # ip_scanner_ping1()
    # ip_scanner_ping2()


    # for i in range(1,255,10):
    #     t=threading.Thread(target=scapy_ip_scanner,args=(i,))
    #     t.start()

    scapy_port_scanner('192.168.230.147')
