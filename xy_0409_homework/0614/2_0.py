# @Description: 调用 scatter 函数绘制正弦函数的曲线，请在曲线中添加一个表示 XY 的轴线，并在
# X 轴方向输出刻度标记文本，效果如图 2.9.2 所示。
# 提示：利用 plot 函数绘制直线，然后在合适位置显示标记字符。
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/15 18:47
# @File : 1.py
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

x = np.linspace(-np.pi, np.pi, 80)
sin = np.sin(x)
plt.title('Sin函数曲线')
plt.rcParams['axes.unicode_minus'] = False
plt.plot((-4, 4), (0, 0), )
plt.plot((0, 0), (-1.2, 1.2))
plt.text(-np.pi, 0, '-pi')
plt.text(np.pi, 0, 'pi')
plt.text(0, 0, '0')
plt.text(3.8, 0, 'X')
plt.text(0, 1.1, 'Y')
plt.scatter(x, sin, marker='*', c=sin, cmap='prism')
plt.xlim(-4, 4)
plt.ylim(-1.2, 1.2)
plt.show()
