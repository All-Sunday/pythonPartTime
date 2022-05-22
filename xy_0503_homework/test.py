# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/6 22:19
# @File : test.py
import math

myList = ['a', 'b', 'c', 'd', 'e']
myList[0] = "hello"
math.sqrt(4)
print(myList)

myList[-2] = False
print(myList)

myList[2:4] = [1, 2]
print(myList)

myList[1:] = "world"
print(myList)

myList[1:] = ["world"]
print(myList)

# myList = [1, 2, 3, 4, 5]
# # myList[1:] = 32
# myList[1:] = '32'
# print(myList)

# myList = [1, 2, 3, 4, 5]
# myList[1] = [6, 7, 8]
# print(myList)
#
# myList = [1, 2, 3, 4, 5]
# myList[:3] = [6, 7, 8]
# print(myList)
#
# myList = [1, 2, 3, 4, 5]
# myList[:3] = [[6, 7, 8]]
# print(myList)


print("1：world是字符串，会被当作list处理，相当于['w','o','r','l','d']" + '["world"]' + "本身就是list,且只含一个元素")
print("2：报错 myList[1:] = '32'  [1, '3', '2']")
print("3：myList[1] = [6, 7, 8] myList[:3] = [6, 7, 8]  myList[:3] = [[6, 7, 8]]")

# print('6--------------')
myList = [['香蕉', '黄色'], ['草莓', '红色'], ['葡萄', '紫色']]
newList = myList
print(newList)

copyList = myList.copy()
print(copyList)
sliceList = myList[:]
print(sliceList)
myList[0] = ['西瓜', '红色']
print(newList)
print(copyList)
print(sliceList)
myList[2][1] = '绿色'
print(newList)
print(copyList)
print(sliceList)
print('1：newList是直接赋值，和原myList是等价的，修改其中任何值都会受影响；copyList是其第一层实现深拷贝，内部嵌套的List仍是浅拷贝；[:]切片浅拷贝整个列表，同样的，只对第一层实现深拷贝')
myList = [('香蕉', '黄色'), ('草莓', '红色'), ('葡萄', '紫色')]
myList[2][1] = '红色'
print(myList)

print("2：TypeError: 'tuple' object does not support item assignment   tuple元素只能读，不可以写")

res = 0
for i in range(1, 100):
    if i % 2 != 0:
        # print(i)
        res += i
print('res =', res)
