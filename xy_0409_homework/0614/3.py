import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

image_data = np.array(Image.open('jojo.jpg'))
hd = []
for i in range(image_data.shape[0]):
    for j in range(image_data.shape[1]):
        hd.append(image_data[i, j, 0] * 0.299 + image_data[i, j, 1] * 0.587 + image_data[i, j, 2] * 0.114)

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

plt.bar(x, nums, 1, color='k')
plt.show()
