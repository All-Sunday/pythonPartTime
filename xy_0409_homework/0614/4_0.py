# @Description: 绘制一个心形图案，参考数学函数为 ρ=a(1-sinθ)（θ 的取值范围[0,2]），x=pcosθ，
# y=psinθ，在直角坐标系上的绘制图案效果如图 2.9.3（a）所示，在极坐标中的绘制效果如
# 图 2.9.3（b）所示。
# 提示：极坐标绘制函数参考格式：plt.polar(theta,p)
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/17 20:12
# @File : 4_0.py
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

theta = np.linspace(0, 2 * np.pi, 1024)  # 角度范围 0-2*pi，划为1024等份
a = 1
p = a * (1 - np.sin(theta))
x = p * np.cos(theta)
y = p * np.sin(theta)
plt.plot(x, y, 'r')
plt.title('心形曲线-直角坐标系')
plt.show()


plt.rcParams['font.sans-serif'] = ['SimHei']

theta = np.linspace(0, 2 * np.pi, 1024)  # 角度范围 0-2*pi，划为1024等份
# 1
# plt.axes(polar=True)    # 开启极坐标模式
# plt.plot(theta, 1. - np.sin(theta), color="r")

# 2
p = 1 - np.sin(theta)
# plt.subplot(211)
plt.polar(theta, p)
plt.title('心形曲线-极坐标系')
plt.show()

