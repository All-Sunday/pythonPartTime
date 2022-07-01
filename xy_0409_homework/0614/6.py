import jieba
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image
from wordcloud import WordCloud

with open('三国人名汇总.txt', 'r') as f:
    names = f.read().split()

name_dict = dict(zip(names, [0] * len(names)))

with open('三国演义.txt', 'r', encoding='ANSI', ) as f:
    content = f.read()

word_list = list(jieba.cut(content))
for name in names:
    count = word_list.count(name)
    name_dict[name] = count

x = []
count = []
for k, v in name_dict.items():
    if v > 100:
        x.append(k)
        count.append(v)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6), dpi=300)
plt.rcParams['font.sans-serif'] = ['SimHei']

plt.subplot(121)
barW = 0.5
plt.bar(x, count, barW, color='b')
plt.xticks(rotation=90)

mask = np.array(Image.open('sg.png'))
wcd = WordCloud(font_path='simhei.ttf', background_color='white', mask=mask, max_words=200, max_font_size=50)

myWD = wcd.fit_words(name_dict)

plt.subplot(122)
plt.imshow(myWD)
plt.axis('off')
plt.show()
