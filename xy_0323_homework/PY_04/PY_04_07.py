import math

N = int(input('请输入一个正整数N：'))
j = int(input('请输入一个数字j(0<j<10)：'))
K = 0
m = 0
for i in range(N):
    m += int(j * math.pow(10, i))
    K += m
print(K)
