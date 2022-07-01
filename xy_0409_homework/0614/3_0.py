# @Description: 调用 bar()函数绘制教材部分例 8.6 中的图像直方图效果，图像文件可以自己任意指定
# 提示：利用 plot 函数绘制直线，然后在合适位置显示标记字符。
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/15 18:47
# @File : 1.py
from itertools import groupby

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from pandas import Series

image_data = np.array(Image.open('jojo.jpg'))
hd = []
for i in range(image_data.shape[0]):
    for j in range(image_data.shape[1]):
        hd.append(image_data[i, j, 0] * 0.299 + image_data[i, j, 1] * 0.587 + image_data[i, j, 2] * 0.114)
# print(pd.value_counts(hd), type(pd.value_counts(hd)))
# print(Series(hd).value_counts(), type(Series(hd).value_counts()))
print(len(hd), max(hd), min(hd))
x = []
nums = []
# list区间分组统计 1
for k, g in groupby(sorted(hd), key=lambda x: x // 1):
    # print('{}-{}: {}'.format(k*1, (k+1)*1-1, len(list(g))))
    x.append(int(k))
    nums.append(len(list(g)))
print(x)
print(nums)

# list区间分组统计 2
begin, end = 0, 1
x = [i for i in range(256)]
nums = [0] * 256
for v in sorted(hd):
    if begin <= v < end:
        nums[begin] += 1
    else:
        begin = int(v)
        end = begin + 1
        nums[begin] += 1

print(x)
print(nums)
plt.bar(x, nums, 1, color='k')
# plt.hist(hd, 256, color='k')
plt.show()
