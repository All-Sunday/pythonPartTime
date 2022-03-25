import time

t1 = time.time()
while True:
    n = input('请输入行数（1——9）：')
    if n.isdigit():
        n = int(n)
        if 0 < n < 10:
            break

for i in range(1, n + 1):
    print(' ' * (n - i), end='')

    j = 1
    while j != i + 1:
        print(j, end='')
        j = j + 1

    j = i - 1
    while j != 0:
        print(j, end='')
        j = j - 1
    print()

t2 = time.time()
print('运行时间为：' + str(t2 - t1) + 's')
