[TOC]



# ==故障上报与处理==

> 在一些简单的IIoT设备中，可能只包含一个或多个嵌入式系统，这些系统专门设计用于执行特定的任务，并且不包含传统意义上的操作系统。这些设备通常使用微控制器（MCU）或微处理器（MPU），并通过嵌入式编程实现其功能。这些程序是预先编译和烧录到设备的存储器中的，并在设备上电后直接执行。
>
> 你
>
> 在一些更复杂的IIoT设备中，可能会使用完整的操作系统来提供更高的灵活性、可扩展性和可管理性。这些操作系统可以是专门为嵌入式系统设计的实时操作系统（RTOS），如VxWorks、FreeRTOS、QNX等，也可以是通用操作系统（如Linux）的简化版本或变种。这些操作系统提供了进程管理、内存管理、设备驱动、网络协议栈等功能，使得设备能够运行多个应用程序、与其他设备通信以及进行复杂的数据处理和分析。



在工业物联网（IIoT）设备的故障上报与处理模块中，主要涉及的数据信息通常包括多个方面，旨在全面监测设备的运行状态和性能。以下是对这些信息的详细分析：

### 1、设备状态信息

- **传感器数据**：如温度、湿度、压力、振动等，用于实时监测设备的物理状态。
- **运行状态**：如设备的开关状态、工作模式、生产进度等，反映设备的运行状况。

> 由于设备种类较多，且每一种设备各个型号硬件地址，信息使用的通信协议等都有可能不同，因此我们只是提供一个作为模拟测试的代码

```C++
#include <iostream>  
#include <chrono> // 用于模拟工作时长（非必要，但用于示例）  

// 模拟从设备读取温度的函数  
float readTemperature() {
    // 假设从设备读取到的温度值  
    return 25.0f;
}

// 模拟从设备读取湿度的函数  
float readHumidity() {
    // 假设从设备读取到的湿度值  
    return 50.0f;
}

// 模拟从设备读取压力的函数  
float readPressure() {
    // 假设从设备读取到的压力值  
    return 1013.25f; // 单位可能是hPa或其他，具体取决于设备  
}

// 模拟设备的工作时长（这里只是模拟，实际中需要设备支持）  
std::chrono::duration<double> getUptime() {
    // 假设设备已经运行了24小时30分钟  
    return std::chrono::hours(24) + std::chrono::minutes(30);
}

// 模拟从设备获取状态的函数  
std::string getDeviceStatus() {
     //假设设备的状态是"Online"  
    return "Online";
}

int main() {
    // 读取模拟的设备数据  
    float temperature = readTemperature();
    float humidity = readHumidity();
    float pressure = readPressure();
    std::chrono::duration<double> uptime = getUptime();
    std::string status = getDeviceStatus();

    // 输出模拟的IIoT设备数据  
    std::cout << "Temperature: " << temperature << "°C" << std::endl;
    std::cout << "Humidity: " << humidity << "%" << std::endl;
    std::cout << "Pressure: " << pressure << " hPa" << std::endl;
    std::cout << "Uptime: " << std::chrono::duration_cast<std::chrono::hours>(uptime).count() << "h "
        << std::chrono::duration_cast<std::chrono::minutes>(uptime % std::chrono::hours(1)).count() << "m" << std::endl;
    std::cout << "Device Status: " << status << std::endl;

    return 0;
}
```

该模拟将输出设备此时的温度，湿度，压力运行时间，和当前状态

此时通过主调函数在进行参数值范围的判断，如果查出范围则进行故障上报

### 2、性能参数

- **CPU负载情况**：是衡量设备处理能力的关键指标，包括CPU使用率、任务队列长度等。这些信息有助于发现设备在处理任务时是否出现过载或性能瓶颈。
- 内存使用情况：反映设备内存的占用情况，包括已用内存、剩余内存等。内存不足可能导致设备性能下降或崩溃。
- **磁盘空间**：对于具有存储功能的设备，磁盘空间的使用情况也是重要的性能指标。

```python
import time,os
from collections import Counter

# 获取CPU负载情况
def get_cpu_load():
    uptime = os.popen('uptime').read()
    
    cpu_load = float(os.popen("uptime | awk -F ': ' '{print$2}' | awk -F ',' '{print$1}'").read())
    
    return cpu_load

# 获取设备内存情况  
def get_memory_info():  
    # 使用free命令获取内存信息  
    memory_info = os.popen('free -b').read()  
      
    # 查找以'Mem:'开头的行  
    mem_lines = [line for line in memory_info.split('\n') if line.startswith('Mem:')]  
    if mem_lines:  
        mem_line = mem_lines[0]  
        fields = mem_line.split()[1:]  # 假设'Mem:'后紧跟着的就是数值  
        if len(fields) >= 3:  
            total_memory = int(fields[0])  # 总内存  
            used_memory = int(fields[1])   # 已用内存  
            free_memory = int(fields[2])   # 空闲内存  
            return total_memory, used_memory, free_memory  
    return None, None, None  # 如果找不到或格式不正确，返回None  
  
# 获取设备磁盘空间情况  
def get_disk_space(directory='/'):  
    # 使用df命令获取磁盘空间信息  
    disk_info = os.popen(f'df -B 1 {directory}').read()  
      
    # 查找磁盘信息行（不包括表头）  
    disk_lines = [line for line in disk_info.split('\n') if line and not line.startswith('Filesystem')]  
    if disk_lines:  
        disk_line = disk_lines[-1]  # 通常我们关心的是最后一行，即指定的目录  
        fields = disk_line.split()  
        if len(fields) >= 4:  
            total_space = int(fields[1])  # 总空间  
            used_space = int(fields[2])   # 已用空间  
            avail_space = int(fields[3])  # 可用空间  
            return total_space, used_space, avail_space  
    return None, None, None  # 如果找不到或格式不正确，返回None
```

### 3、网络连接信息

- **网络连接数**：指设备当前建立的网络连接数量，包括TCP连接、UDP连接等。过多的网络连接可能导致网络拥堵或性能下降。
- **网络带宽**：反映设备的网络传输能力，包括上行带宽和下行带宽。带宽不足可能导致数据传输延迟或丢失。
- **网络延迟**：指数据在网络中传输所需的时间，包括发送延迟、传输延迟和接收延迟。网络延迟过大可能导致实时性要求高的应用无法正常工作。

```python
# 获取当前设备TCP连接数
def get_TCP_conn():
    netstat = int(os.popen('netstat -ant | wc -l').read())
    return netstat


# 获取当前设备TCP队列情况
def get_queue_size():
    queue = os.popen('ss -lnt | grep :80').read()
    # os.popen('ss -lnt | grep :80 | awk "{print $2}"')
    recv_q = int(queue.split()[1])
    send_q = int(queue.split()[2])
    return recv_q,send_q


# 获取当前设备最多连接数IP
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


```

### 4、智能预警

基于上面所有获得到的IIoT设备信息，我们可通过主调函数对各个参数值的判断进行故障判断，如果超出该值设定范围则进行故障上报

```python
# 对具有攻击行为的IP进行封禁
def firewall_mostip(most_ip):
    result = os.popen(f"firewall-cmd --add-rich-rule='rule family=ipv4 source address={most_ip} port port=80 protocol=tcp reject'").read()
    if 'success' in result:
        print(f'已成功将可疑IP{most_ip}封禁')
    else:
        print('可疑IP封禁失败，请转接人工处理')  
        
        
if __name__ == '__main__':
    import socket  
	import time  
  
	# 服务器地址和端口  
	SERVER_HOST = '192.168.17.129'  # 替换为你的服务器IP地址  
	SERVER_PORT = 12345  
  
def create_socket_connection(host, port):  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client_socket.connect((host, port))  
    return client_socket  
  
def send_message(client_socket, message):  
    client_socket.sendall(message.encode()) 
	while True:  
    cpu_load = get_cpu_load_03()  
    TCP_conn = get_TCP_conn()  
    recv_q, send_q = get_queue_size()  
    total_memory, used_memory, free_memory = get_memory_info()  
    total_space, used_space, avail_space = get_disk_space()  
  
    # 构建要发送的消息  
    message = f"free_memory:{free_memory} avail_space:{avail_space}\n"  
    message += f"cpu_load:{cpu_load} TCP_conn:{TCP_conn} TCP_Queue:{recv_q},{send_q}\n"  
  
    # 连接到服务器并发送消息  
    with create_socket_connection(SERVER_HOST, SERVER_PORT) as client_socket:  
        send_message(client_socket, message)  
  
    # 如果满足某些条件，发送警告消息  
    if free_memory < total_memory / 4 or avail_space < total_space / 2:  
        warning_message = "空闲内存和可用空间较少，请及时处理\n"  
        with create_socket_connection(SERVER_HOST, SERVER_PORT) as client_socket:  
            send_message(client_socket, warning_message)  
  
    if cpu_load > 33.3 or TCP_conn > 2000 or recv_q > send_q - 10:  
        warning_message = "CPU 负载过高或TCP连接数太多，请注意！！！\n"  
        most_ip = get_most_ip()  
        warning_message += f"发现可疑IP:{most_ip[0][0]} 具有连接数:{most_ip[0][1]}\n"  
        with create_socket_connection(SERVER_HOST, SERVER_PORT) as client_socket:  
            send_message(client_socket, warning_message)   
            firewall_mostip(most_ip[0][0])  
  
    time.sleep(2)
```

如果不预警的话，可以如下：

```python
if __name__ == '__main__':
    while True:
        cpu_load = get_cpu_load_03()

        TCP_conn = get_TCP_conn()

        recv_q,send_q = get_queue_size()

        total_memory, used_memory, free_memory = get_memory_info()

        total_space, used_space, avail_space = get_disk_space()

        print(f"free_memory:{free_memory} avail_space:{avail_space}")
        print(f"cpu_load:{cpu_load} TCP_conn:{TCP_conn} TCP_Queue:{recv_q, send_q}")
        time.sleep(2)
        #print(type())
        if free_memory < total_memory/4 or avail_space < total_space/2:
            print("空闲内存和可用空间较少，请及时处理")
        if cpu_load > 33.3 or TCP_conn > 2000 or recv_q > send_q -10:
            print("CPU 负载过高或TCP连接数太多，设备，请注意！！！")
            most_ip = get_most_ip()
            print(f"发现可疑IP:{most_ip[0][0]} 具有连接数:{most_ip[0][1]} ")
            firewall_mostip(most_ip[0][0])

```



基于网络安全的考虑，可能会有黑客会对我们的设备进行攻击，此时可能**会造成设备性能下降，温度升高等影响设备运行**，所以如果出现具有攻击行为的IP地址我们还会对其进行封禁，防止设备持续出现故障

> 对于主调函数来说，我们可以将输出的故障信息通过socket基于设备使用的网络协议将故障信息传输到服务器，然后服务器对故障信息进行分析处理等

![image-20240526174009808](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240526174009808.png)