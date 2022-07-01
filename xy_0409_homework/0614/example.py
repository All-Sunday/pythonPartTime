# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/12 19:02
# @File : 1.py
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()  # 该语句可以省略
plt.subplot(221, title="No 1", xticks=np.arange(6))  # 设置图表标题和 X 轴刻度范围
plt.plot((2, 4), (3, 6), c='g')
plt.subplot(223, xlabel="Number", ylabel="Value")  # 设置坐标轴标签
plt.plot((1, 2), (4, 3), c='b')

plt.subplot(224, facecolor='#00FFFF')  # 设置子绘图区填充颜色为青色
plt.plot((1, 2), (3, 4), c='y')
plt.subplots_adjust(wspace=0.4, hspace=0.6)  # 调整各子绘图区之间的间隔
plt.show()

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(6, 4))  # 创建一个指定大小的全局绘图区
fig.add_subplot(221)  # 添加第 1 个子绘图区
plt.plot((1, 6, 2), c='r', marker='o')  # 在第 1 个子绘图区绘制红色折线与圆点标记
fig.add_subplot(224)  # 添加第 4 个子绘图区
x = np.random.randint(0, 100, 10)  # 随机生成 10 个坐标点的 x 坐标序列
y = np.random.normal(0, 100, 10)  # 随机生成 y 坐标序列
plt.scatter(x, y, c='g')  # 在第 4 个子绘图区绘制随机生成的坐标点
plt.show()

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4))  # ax 用于访问指定坐标系
plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 指定中文字体为黑体
subjects = ['语文', '数学', '英语', '体育']  # 设置分类轴显示的文本内容
score = [80, 98, 92, 70]  # 某同学的分数
ax.set_title("考试成绩")  # 设置子绘图区的标题
ax.set_xlabel("科目")  # 设置子绘图区 X 分类轴的标签
ax.set_ylabel("分数")  # 设置子绘图区 Y 数值轴的标签
ax.set_xticks([0, 1, 2, 3])  # 设置 X 分类轴的标记数据
ax.set_xticklabels(subjects)  # 设置 X 分类轴标记显示文本内容
ax.set_yticks([0, 30, 60, 90, 120])  # 设置 Y 数值轴的标记数据
ax.bar([0, 1, 2, 3], score, label="Name")  # 绘制柱状图
ax.legend(loc='upper right')  # 显示图例
plt.show()

import math  # 导入数学函数库
import matplotlib.pyplot as plt  # 导入绘图库

plt.title("三角函数曲线")  # 显示图表标题
plt.ylim(-1, 2)  # 设置 y 轴的取值范围
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号
x = -math.pi
xx = []
sinx = []
cosx = []
while x <= math.pi:
    sinx.append(math.sin(x))  # sinx 列表添加当前坐标点的 sin 函数值
    cosx.append(math.cos(x))  # cosx 列表添加当前坐标点的 cos 函数值
    xx.append(x)  # xx 列表添加当前坐标点的 x 坐标值
    x += 0.1
plt.plot(xx, sinx, marker='*')  # 绘制 sin 函数的曲线
plt.plot(xx, cosx, marker='D')  # 绘制 cos 函数的曲线
plt.show()

import numpy as np  # 导入 numpy 库
import matplotlib.pyplot as plt  # 导入绘图库

x = np.linspace(-np.pi, np.pi, 100)  # 快速生成 x 轴上（-π,π）之间的 100 个数
sin, cos = np.sin(x), np.cos(x)  # 计算相应的 sin 函数值和 cos 函数值
plt.title("三角函数曲线")  # 显示图表标题
plt.ylim(-1, 2)  # 设置 y 轴的取值范围
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号
plt.plot(x, sin, color='b', linewidth=2, ls='-', label='sin 函数')  # 绘制 sin 函数曲线
plt.plot(x, cos, color='r', linewidth=5, ls='--', label='cos 函数')  # 绘制 cos 函数曲线
plt.legend(loc='upper right')  # 右上显示图例文字
plt.show()

import matplotlib.pyplot as plt

score = [0.16, 0.28, 0.32, 0.14, 0.1]  # 各等级的成绩数据
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.title("成绩分布图")  # 图表标题
labels = ['优秀', '良好', '中', '及格', '不及格']  # 数据标记
explode = (0.2, 0, 0, 0, 0)  # 第 1 块分裂出来
plt.axis("equal")
plt.pie(score, explode=explode, autopct='%0.1f%%', labels=labels)
# autopct='%4.1f%%'控制数据标记的格式化显示，显示 1 位小数
plt.legend(bbox_to_anchor=(1, 0.6))  # 显示图例
plt.show()

from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
iris = load_iris()  # 载入鸢尾花数据集
dt = iris.data  # 获得数据集中 150 条数据记录
tg = iris.target  # tg 用于存放每个样本的类别数据
x = dt[:, 0]  # x 存放所有样本的花萼长度
y = dt[:, 2]  # y 存放所有样本的花瓣长度
label = "山鸢尾花\n 变色鸢尾花\n 维吉尼亚鸢尾花"  # 图例文本
plt.scatter(x, y, c=tg, marker="^", cmap="viridis", label=label)  # 绘制散点图
plt.legend()
plt.show()

import matplotlib.pyplot as plt
from numpy import random

data = random.randint(100, size=50)
plt.hist(x=data, bins=10, range=[30, 100], rwidth=0.75)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image  # 导入 Image 库

im = np.array(Image.open("jojo.jpg"))
n = int(im.size / 3)
hd = n * [0]  # hd 列表用于存放每个像素点的灰度值
row = im.shape[0]
col = im.shape[1]
for i in range(row):
    for j in range(col):
        # v = im[i, j, 0] * 0.299 + im[i, j, 1] * 0.587 + im[i, j, 2] * 0.114  # 计算当前像素点的灰度
        v = im[i][j][0] * 0.299 + im[i][j][1] * 0.587 + im[i][j][2] * 0.114  # 计算当前像素点的灰度
        hd[i * col + j] = v  # 保存每一个灰度值
print(len(hd), max(hd), min(hd))
plt.hist(hd, 256, color='k')  # 绘制直方图
# hd：各像素点的灰度值列表，256 是横轴灰度等级数，color 设置填充黑色
plt.show()

# r=sin(a*θ)
# x=r*cos(θ)
# y=r*sin(θ)
import math
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))  # 设置子绘图区
plt.subplots_adjust(wspace=0.3, hspace=0.4)  # 调整子绘图区的间隔
a = [0.5, 1.5, 3]  # 设置 a 的取值序列，控制第 1 行的三个图案
for i in range(3):  # 控制第 1 行的三个子绘图区
    th = 0
    xx = []
    yy = []
    while th <= 2 * math.pi:  # 用循环控制生成所有坐标点的取值序列
        r = math.sin(a[i] * th)
        xx.append(r * math.cos(th))
        yy.append(r * math.sin(th))
        th += 0.03
    ax[0][i].plot(xx, yy, 'b*', label="a=" + str(a[i]))  # 用 plot 函数绘制标记
    ax[0][i].legend(bbox_to_anchor=(0.7, -0.1))  # 指定图例位置
a = [2, 5, 4]
for i in range(3):  # 控制第 2 行的三个子绘图区
    th = 0
    xx = []
    yy = []
    while th <= 2 * math.pi:
        r = math.sin(a[i] * th)
        xx.append(r * math.cos(th))
        yy.append(r * math.sin(th))
        th += 0.03
    ax[1][i].scatter(xx, yy, c="g", lw=0.5, marker="^", label="a=" + str(a[i]))
    # 用 scatter 函数绘制散点图
    ax[1][i].legend(bbox_to_anchor=(0.7, -0.1))
plt.show()

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))
plt.subplots_adjust(wspace=0.3, hspace=0.4)
a = [-0.5, 1.5, 3]
th = np.arange(0, 2 * np.pi, 0.02)  # 快速生成弧度值序列
for i in range(3):
    r = np.sin(a[i] * th)
    x, y = r * np.cos(th), r * np.sin(th)  # 计算坐标点序列
    ax[0][i].plot(x, y, 'b*', label="a=" + str(a[i]))  # 绘制坐标点标记
    ax[0][i].legend(bbox_to_anchor=(0.7, -0.1))  # 通过图例显示当前 a 的取值
a = [2, 5, 4]
for i in range(3):
    r = np.sin(a[i] * th)
    x, y = r * np.cos(th), r * np.sin(th)
    ax[1][i].scatter(x, y, c="g", lw=0.5, marker="^", label="a=" + str(a[i]))
    ax[1][i].legend(bbox_to_anchor=(0.7, -0.1))
plt.show()

import itchat
import numpy as np
import pandas as pd
import jieba
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PIL.Image as Image

# itchat.login()  # 弹出微信二维码图片，在手机上扫码并确认登录
# friends = itchat.get_friends(update=True)  # 获取好友信息
# NickName = friends[0].NickName  # 获取自己的昵称
# cdr = os.getcwd()  # 获取当前目录
# if not (os.path.exists(NickName)):  # 判别昵称文件夹是否已存在
#     os.mkdir(NickName)  # 则创建一个名字为昵称的新文件夹
# os.chdir(cdr + '\\' + NickName)  # 切换到昵称文件夹
friends =
df = pd.DataFrame(friends)  # 把好友数据处理成 DataFrame
Sex = df.Sex  # 获取好友性别信息
Sex_count = Sex.value_counts()  # 统计人数，男：1、女：2、未知：0
plt.figure(figsize=(10, 5))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.subplot(121)
x = [0, 1, 2]
plt.xticks(x, ("男", '女', '未知'))
barW = 0.5
plt.bar(x, Sex_count, barW, color='b', label='性别')  # 绘制柱状图
plt.legend(loc='best')
Signatures = df.Signature  # 获取好友签名信息
text = ' '.join(Signatures)  # 将好友签名数据保存到 text 变量中
file_name = NickName + 'sig.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(text)
f.close()
wordlist = jieba.cut(text, cut_all=True)  # 对好友签名信息进行分词处理
wordSS = ' '.join(wordlist)  # 将分词结果转换成字符串
mask = np.array(Image.open('wx.png'))  # 定义词云图显示的遮罩形状
wcd = WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf',
    background_color='white',
    mask=mask,  # 设置遮罩图片
    max_words=1000,  # 最多显示词数
    max_font_size=100)  # 字体最大值
myWD = wcd.generate(wordSS)  # 根据签名数据生成词云图
myWD.to_file(NickName + '.jpg')  # 将词云图保存为图片文件
plt.subplot(122)
plt.imshow(myWD)  # 显示词云图
plt.axis('off')  # 不显示坐标轴
plt.show()  # 显示图像
