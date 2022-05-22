# if分支
x = int(input('请输入x:').strip())
if x < 0:
    y = 0
elif 5 > x >= 0:
    y = x
elif 10 > x >= 5:
    y = 3 * x - 5
elif 20 > x >= 10:
    y = 0.5 * x - 2
elif x >= 20:
    y = 0
print('y:', y)
