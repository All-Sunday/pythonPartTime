num1 = int(input('请输入第一个整数：'))
num2 = int(input('请输入第二个整数：'))
num3 = int(input('请输入第三个整数：'))
if num1 > num2:
    max_num = num1
    if num1 > num3:
        max_num = num1
    else:
        max_num = num3
else:
    max_num = num2
    if num2 > num3:
        max_num = num2
    else:
        max_num = num3
print('三个数中最大数为：', max_num)

