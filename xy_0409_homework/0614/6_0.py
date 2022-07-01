# @Description: 读取“三国人名汇总.txt”中的人物名字，读取“三国演义.txt”的全部内容，先统计所
# 有人物的名字在书本中出现的次数，并对出现次数超过 100 次的人物绘制一个柱状图，然后
# 根据人物的词频大小绘制一个三国人名的词云图，
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/17 22:09
# @File : 6_0.py
import jieba
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image
from wordcloud import WordCloud

with open('三国人名汇总.txt', 'r') as f:
    names = f.read().split()
print(names)
name_dict = dict(zip(names, [0] * len(names)))
print(name_dict)

with open('三国演义.txt', 'r', encoding='ANSI', ) as f:
    content = f.read()
print(content)

word_list = list(jieba.cut(content))
for name in names:
    count = word_list.count(name)
    name_dict[name] = count
print(name_dict)

x = []
count = []
for k, v in name_dict.items():
    if v > 100:
        x.append(k)
        count.append(v)

# name_dict = sorted(name_dict.items(), key=lambda x: x[1], reverse=True)
# name_dict = [i for i in name_dict if i[1] > 100]
# x = [i[0] for i in name_dict]
# count = [i[1] for i in name_dict]
print(x, len(x))
print(count, len(count))

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6),dpi=300)
plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.figure(figsize=(5, 6))
plt.subplot(121)
barW = 0.5
plt.bar(x, count, barW, color='b')
plt.xticks(rotation=90)  # 设置x轴标签旋转角度
# plt.show()

mask = np.array(Image.open('sg.png'))  # 定义词云图显示的遮罩形状
wcd = WordCloud(font_path='simhei.ttf',background_color='white', mask=mask, max_words=200, max_font_size=50)
# myWD = wcd.generate(name_dict)
myWD = wcd.fit_words(name_dict)

plt.subplot(122)
plt.imshow(myWD)  # 显示词云图
plt.axis('off')  # 不显示坐标轴
plt.show()  # 显示图像