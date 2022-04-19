import math


def s(x):
    res = 0
    i = 1
    while True:
        a = math.pow(x, i * 2 - 1) / math.factorial(i * 2 - 1)
        if i % 2 == 0:
            a = -a
        res += a
        i += 1
        if abs(a) < math.pow(10, -6):
            break
    return res


print('级数和：', s(1))
