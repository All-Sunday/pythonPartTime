# 水仙花数
def fun(a, b):
    result = []
    for n in range(a, b + 1):
        i = n // 100
        j = n // 10 % 10
        k = n % 10
        if n == i ** 3 + j ** 3 + k ** 3:
            result.append(n)
    return result


print(fun(100, 999))
