def fun(m):
    if m < 2:
        print("不是素数")
    else:
        for i in range(2, m):
            if m % i == 0:
                return False
        else:
            return True


res = []
for i in range(101, 201):
    if fun(i):
        res.append(i)

print('101~200之间有' + str(len(res)) + '个素数：')
for i in res:
    print(i, end=' ')
