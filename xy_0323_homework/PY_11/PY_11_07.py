def fib(n):
    if n < 3:
        return 1

    return fib(n - 1) + fib(n - 2)


n = int(input('请输入项数序号（从1开始）：n='))
print('第{}项斐波那契数列值为{}'.format(n, fib(n)))