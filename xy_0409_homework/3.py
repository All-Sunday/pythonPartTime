def fun(x):  # 逆序数 回文数
    result = 0
    while x > 0:
        result = result * 10 + x % 10
        x = x // 10
    return result


res = []
for i in range(1000, 10000):
    if i == fun(i):
        res.append(i)

print('1000~9999之间的所有的回文数：', res)
