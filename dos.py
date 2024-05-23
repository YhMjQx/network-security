import time,os
from collections import Counter

def get_cpu_load_01():
    uptime = os.popen('uptime').read()
    #print(type(uptime))
    #print(uptime)
    cpu_load = float(uptime.split(',')[3].split(' ')[4])
    #print(cpu_load)
    return cpu_load

def get_cpu_load_02():
    uptime = os.popen('uptime').read()
    #print(type(uptime))
    #print(uptime)
    cpu_load = float(uptime.replace(': ',',').split(',')[4])
    #print(cpu_load)
    return cpu_load


def get_cpu_load_03():
    uptime = os.popen('uptime').read()
    #print(type(uptime))
    #print(uptime)
    cpu_load = float(os.popen("uptime | awk -F ': ' '{print$2}' | awk -F ',' '{print$1}'").read())
    #print(cpu_load)
    return cpu_load


def get_TCP_conn():
    netstat = int(os.popen('netstat -ant | wc -l').read())
    return netstat


def get_queue_size():
    queue = os.popen('ss -lnt | grep :80').read()
    # os.popen('ss -lnt | grep :80 | awk "{print $2}"')
    recv_q = int(queue.split()[1])
    send_q = int(queue.split()[2])
    return recv_q,send_q


def get_most_ip():
    netstat = os.popen('netstat -ant | grep :80').read()
    netstat_list = netstat.split('\n')
    ip_list=[]
    for line in netstat_list:
        try:
            ip = line.split()[4].split(':')[0]
            ip_list.append(ip)
            #print(ip)
        except:
            pass
    # 直接使用Python内置的计数器来实现排序
    ip_dict = Counter(ip_list)
    most_ip = ip_dict.most_common(1)
    # print(most_ip)
    # print(type(most_ip))  # <class 'list'>
    return most_ip


def firewall_mostip(most_ip):
    result = os.popen(f"firewall-cmd --add-rich-rule='rule family=ipv4 source address={most_ip} port port=80 protocol=tcp reject'").read()
    if 'success' in result:
        print(f'已成功将可疑IP{most_ip}封禁')
    else:
        print('可疑IP封禁失败，请转接人工处理')   


if __name__ == '__main__':
    while True:
        #cpu_load = get_cpu_load_01()
        #cpu_load = get_cpu_load_02()
        cpu_load = get_cpu_load_03()

        TCP_conn = get_TCP_conn()

        recv_q,send_q = get_queue_size()

        print(f"cpu_load:{cpu_load} TCP_conn:{TCP_conn} TCP_Queue:{recv_q,send_q}")
        time.sleep(2)
        #print(type())
        if cpu_load > 33.3 or TCP_conn > 2000 or recv_q > send_q -10:
            print("CPU 负载过高或TCP连接数太多，可能遭遇DOS攻击，请注意！！！")
            most_ip = get_most_ip()
            print(f"出现可疑IP:{most_ip[0][0]} 具有连接数:{most_ip[0][1]} ")
            firewall_mostip(most_ip[0][0])
