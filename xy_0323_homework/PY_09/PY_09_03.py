# 回文数 步数
def find(n, times):
    n = int(n)
    num = n
    n_reversed = 0
    while num > 0:
        n_reversed = n_reversed * 10 + num % 10
        num = num // 10
    if n == n_reversed:
        return times
    n += n_reversed
    times += 1
    if times > 20:
        return '>20'
    return find(n, times)


n = input()
print(find(n, 0))
