import random


def fun(x):
    return x * x


data = []
for i in range(10):
    data.append(random.randint(10, 99))
print('原始的数据序列为：', data)

new_data = list(map(lambda x: fun(x), data))
print('平方值计算后的数据序列为：', new_data)
print('所有元素的平方和为：', sum(new_data))
