# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/3/28 11:28
# @File : 1.py
# number = 4
# even = number % 2 == 0
# print(even)
# even = True if number % 2 == 0 else False
# print(even)
# for i in range(30, 51):
#     print(i)
# num < 0
# num > 100
# 字符串.isupper() # 判断是否是大写字母
# 字符串.islower() # 判断是否是大写字母
# a1 = int(input('请输入边长1：'))
# a2 = int(input('请输入边长2：'))
# a3 = int(input('请输入边长3：'))
# if (a1 + a2) > a3 and (a2 + a3) > a1 and (a1 + a3) > a1:
#     print('可以构成三角形')
# else:
#     print('无法构成三角形')
#
# year = int(input("请输入一个年份："))
# if (year % 4 == 0) and (year % 100 != 0) or (year % 400) == 0:
#     print(str(year) + "年是闰年")
# else:
#     print(str(year) + "年不是闰年")
import random

# for i in range(100):
#     print(chr(random.randint(97, 122)))

# random_num = random.randint(0, 9)
# user_num = int(input('请输入选项：0-9'))
# print('计算机的选择是：' + str(random_num) + ' VS 用户的选择：' + str(user_num))
# if random_num > user_num:
#     print('计算机 获胜！')
# elif random_num == user_num:
#     print('平局')
# else:
#     print('用户 获胜！')

list1 = ['sss', 'sss', 'sss\n', 'asfij\n', 'asf\n']
print(list1)
for i in list1:
    print(i)
list1 = ['sss']
list1.append('sss')
print(list1)