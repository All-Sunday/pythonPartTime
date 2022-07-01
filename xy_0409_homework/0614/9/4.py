import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

theta = np.linspace(0, 2 * np.pi, 1024)
a = 1
p = a * (1 - np.sin(theta))
x = p * np.cos(theta)
y = p * np.sin(theta)
plt.plot(x, y, 'r')
plt.title('心形曲线-直角坐标系')
plt.show()

plt.rcParams['font.sans-serif'] = ['SimHei']

theta = np.linspace(0, 2 * np.pi, 1024)
p = 1 - np.sin(theta)
plt.polar(theta, p)
plt.title('心形曲线-极坐标系')
plt.show()
