import random

a = [[-1 + int(3 * random.random()) for j in range(5)] for i in range(10)]
print('转置前：', a)

a_t = [[row[i] for row in a] for i in range(len(a[0]))]
print('转置后：', a_t)
