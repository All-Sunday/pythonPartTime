def fibonacci(n):  # 斐波那契数列的第n项，前两项是0，1
    a, b = 0, 1
    if n == 1:
        return 0
    for i in range(n - 1):
        a, b = b, a + b
    return a


res = fibonacci(5)
print(res)
