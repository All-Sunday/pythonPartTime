import sys
sys.setrecursionlimit(1000000000)


def find(n):
    n = int(n)
    num = n
    n_reversed = 0
    while num > 0:
        n_reversed = n_reversed * 10 + num % 10
        num = num // 10
    if n == n_reversed:
        return n
    n += n_reversed
    return find(n)

n = input("请输入任意一个自然数：")
print("寻找到的回文数是：", find(n))
