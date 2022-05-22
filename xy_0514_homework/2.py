# @Description: 打印一个整数的所有质因数
# 90
# 2,3,3,5
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/15 13:38
# @File : 2.py

num = int(input())
temp = num
i = 2
result = []
while True:
    if temp == 1:
        break
    if temp % i == 0:
        result.append(i)
        temp = temp / i
    else:
        i += 1
print(num, '=', '*'.join(map(str, result)))

num = int(input())

i = 2

while True:

    if num % i == 0:
        num = num / i
        if num == 1:
            print(i)
            break
        print(i, end=',')

    else:
        i += 1


num = int(input())
i = 2
res = set()

while True:

    if num % i == 0:
        num = num / i
        if num == 1:
            res.add(i)
            break
        res.add(i)

    else:
        i += 1
res = list(res)
for i in res[:-1]:
    print(i, end=',')
print(res[-1])