def f1(x, y):
    res = []
    for i in range(x):
        if i == 0:
            res.append(y)
        else:
            res.append(res[i - 1] * 10 + y)
    return sum(res)


def f2(x, y):
    res = 0
    if x == 1:
        return y
    for q in range(x):
        if q == 0:
            res += y
        else:
            res += y * 10 ** q
    res += f2(x - 1, y)
    return res


n, j = [int(i) for i in input().split()]
J = f2(n, j)
print(J)
