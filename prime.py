import time,math

# 检测一个数是不是质数
def is_prime(n):
    max = int(math.sqrt(n)+1)   # 不把这个放在range里是为了防止每次循环都要运算一遍
    for i in range(2,max):
        if n % i == 0:
            return False
    return True

# 计算 n=p*q 中的p,q
def calc_prime_pq(n):
    # // 意思是除完取整
    start = time.time()
    for p in range(2,n//2+1):
        for q in range(2,n//2+1):
            if p * q == n and is_prime(p) and is_prime(q):
                print(f'p={p} q={q}',end=' ')
                end = time.time()
                print(f'time={end-start}')
                exit(0)

# 对计算p q 的算法进行优化
def calc_prime_pq_sup(n):
    max = int(math.sqrt(n)+1)
    start = time.time()
    for p in range(2,max):
        if is_prime(p) and n % p == 0 and is_prime(n//p):
            print(f'p={p} q={n//p}', end=' ')
            end = time.time()
            print(f'time={end - start}')
            exit(0)


if __name__ == '__main__':
    # calc_prime_pq(9943081)  # 139秒
    # calc_prime_pq_sup(9943081)  # 0.001秒  ？？？
    # calc_prime_pq_sup(99460729)  # 0.001秒  ？？？
    calc_prime_pq_sup(9250534949)  # 0.07秒  ？