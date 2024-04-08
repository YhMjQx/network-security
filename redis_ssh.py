import time

import paramiko

# 创建SSH连接
import requests

transport = paramiko.Transport(('192.168.230.147',22))
transport.connect(username='root',password='YhMjQx521134')

# 创建SSH客户端连接对象
ssh = paramiko.SSHClient()
# ssh.get_transport = transport
ssh._transport = transport

# stdin 标准输入
# stdout 标准输出
# stderr 标准错误
# stdin, stdout, stderr = ssh.exec_command('ls /opt')

# command_top = 'top -n 1 > /opt/top.log'
# secaped_command_top = f'"{command_top}"'
# stdin, stdout, stderr = ssh.exec_command(secaped_command_top)
# # 等待命令执行完成
# stdout.channel.recv_exit_status()

# 使用cat命令读取文件内容并将其打印到标准输出
# command_cat = 'cat /opt/top.log'
# escaped_command_cat = f'"{command_cat}"'
# stdin, stdout, stderr = ssh.exec_command(escaped_command_cat)
# print(stdout.read().decode())


# 创建sftp链接对象，用于远程传输文件
sftp = paramiko.SFTPClient.from_transport(transport)
# sftp.put('./woniunote.jpg','/opt/woniunote.jpg')
# sftp.get('/opt/text1.cpp','./text.cpp')


import socket

s = socket.socket()
s.connect(('192.168.230.147',6379))
s.send('*2\r\n$4\r\nauth\r\n$9\r\np-0p-0p-0\r\n'.encode())
print(s.recv(1024).decode())
time.sleep(1)
s.send('*3\r\n$3\r\nset\r\n$4\r\nname\r\n$5\r\nwoniuxy\r\n'.encode())
print(s.recv(1024).decode())
time.sleep(1)
s.send('*2\r\n$3\r\nget\r\n$4\r\nname\r\n'.encode())
print(s.recv(1024).decode())

# 当然，上面的代码可以直接使用redis库 进行操作
import redis
red = redis.Redis(host='192.168.230.147',port=6379,password='p-0p-0p-0',db=0)
red.set('addr','shaanxixian')
print(red.get('addr').decode())
red.rpush('students','zhangsan')
red.rpush('students','lisi')
red.rpush('students','wangwu')

print(red.lindex('students',0))
print(red.lindex('students',1))
print(red.lindex('students',2))