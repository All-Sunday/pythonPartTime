# @Description: .创建一个 2 行 1 列的绘图区并在第 1 行第 1 列绘制函数 f(x)=x2 的曲线图（x 的取值
# 范围[-1,1])，在第 2 行第 1 列绘制函数 f(x)=1/x 的曲线图（x 的取值范围[0,1]），
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/15 18:47
# @File : 1.py
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
fig, axes = plt.subplots(nrows=2, ncols=1)
plt.subplots_adjust(hspace=0.5)
plt.subplot(211)
x = np.linspace(-1, 1, 100)
y = np.square(x)
plt.title('平方曲线')
plt.rcParams['axes.unicode_minus'] = False
plt.plot(x, y, color='b', linewidth=2, ls='-')

plt.subplot(212)
x = [i / 10 for i in range(1, 10)]
y = [1 / i for i in x]
plt.title('倒数曲线')
plt.plot(x, y, color='g', linewidth=2, ls='-')
plt.show()
