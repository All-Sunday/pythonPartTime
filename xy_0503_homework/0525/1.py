# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/25 13:20
# @File : 1.py
_x1 = 1
print(_x1)
s = 'hello python'
s = s.capitalize()
print(s)
d = {'chinese': 0.98, 'math': 0.84}
print(d)
d = dict(chinese=0.98)
print(d)
# d=dict([(chinese,0.98)])
# print(d)
a = lambda x, y, z: x + 2 + y ** 2 - 3 * z
b = lambda x, y, z: 3 * x + y * 2 * z
c = lambda x, y: x * 5 - y
print(a(1, 2, 3) - b(3, 2, 1) + c(3, -4))
x = (5, 1, 3)
# print(x[3])


num = 32
while num % 4 == 0:
    num = num / 2
    print(num)
print(32 / 2)


def func(b, *a, **c):
    return a, c


result = func('b', 9, 2, 7, 3, x=5, y=4)
x = 6
print(result)


def func(a, b):
    if b == 1:
        return a
    else:
        return a + func(a, b - 1)


print(func(2, 3))

i = 8


def funp(var=i):
    print(var - 1)


for i in range(3, 6):
    funp()

data = [2, 3, 5, 8, 130]
new_data = []
for i in range(20, 1, -3):
    if i not in data:
        new_data.append(i)

print(new_data)

I = [54, 36, 75, 28, 50]
I.append(42)
print(I)
I.insert(2, 24)
print(I)
res = I.pop(5)
print(res)
I.sort(reverse=True)
print(I)
I.clear()
print(I)


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


print(fun(100, 501))

result = []
for n in range(100, 501):
    # if (n <= 101) or (n >= 500):
    #     print(n)
    i = n // 100
    j = n // 10 % 10
    k = n % 10
    if n == i ** 3 + j ** 3 + k ** 3:
        result.append(n)
# print(result)
for i in range(len(result)):
    if i % 2 == 0:
        print(result[i], end=' ')
    else:
        print(result[i])
