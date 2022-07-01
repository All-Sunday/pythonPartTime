# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/18 7:36
# @File : exam.py
# 2052591-4-2
import math

dict1 = {'a': 1}
print(dict1.get('b', 0))
# dict2=dict([['a', '1],['b','2']])
lst=['北京','上海']
print(list(enumerate(lst)))

fs=open('score.txt','w')
y=1
x=y
y=2
print(x)

a=7
x=math.pow(a,1/3)
print(x)
x0=4
x1=2/3*x0 + a/(3*x0*x0)
print(x1-x0)
i = 0
while abs(x1 - x0) >=0.00001:
    x0=x1
    x1 = 2 / 3 * x0 + a / (3 * x0 * x0)
    i+=1
    print(i)

l = [1,4,2]
l.sort()
# l.reverse()
print(l)

sales=[15.5, 9.7, 18.5, 16.1, 18.7, 23.0, 22.2, 24.9, 33.4, 31.7, 37.9, 47.5]
pl