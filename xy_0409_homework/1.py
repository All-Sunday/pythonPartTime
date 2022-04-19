def fibonacci(n):  # 斐波那契数列前n个数
    result = []
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        result.append(a)
    return result


res = fibonacci(5)
print(res)
