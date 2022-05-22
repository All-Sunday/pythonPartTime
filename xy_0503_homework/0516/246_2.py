import math

r = 2.11
v = round(4 / 3 * math.pi * r * r * r, 2)
print('①半径为2.11的圆球的体积：', v)
outer_r = 16.2
inner_r = 9.4
area = round(math.pi * ((outer_r * outer_r) - (inner_r * inner_r)), 2)
print('②外圆半径为16.2，内圆半径为9.4的圆环的面积：', area)
