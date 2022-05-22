# 矩阵转置 矩阵乘积
import random

a = [[random.randint(-1, 1) for j in range(5)] for i in range(10)]
print('转置前：', a)
a_t = [[row[i] for row in a] for i in range(len(a[0]))]
print('转置后：', a_t)
res = []
row = len(a_t)
col = len(a[0])
for i in range(row):
    oneRow = col * [0]
    for j in range(col):
        s = 0
    for k in range(len(a)):
        s += a_t[i][k] * a[k][j]
    oneRow[j] = s
    res.append(oneRow)
print('矩阵的转置与矩阵本身的乘积', res)
