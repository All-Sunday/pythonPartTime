def fun(m):  # 判断素数
    if m < 2:
        print("不是素数")
    else:
        for i in range(2, m):
            if m % i == 0:
                return False
        else:
            return True


res = []
for i in range(2, 101):
    if fun(i):
        res.append(i)

print('2~100之间的所有的素数：', res)
