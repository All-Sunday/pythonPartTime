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
