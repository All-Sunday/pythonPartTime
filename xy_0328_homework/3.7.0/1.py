print('-----柳蓉霞-----')
print('-----1-----')
num1 = int(input('请输入第一个整数：'))
num2 = int(input('请输入第二个整数：'))
result = num1 * num1 + num2 * num2
print('两个数的平方和为：', result)
print('-----2-----')
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
print('-----3-----')
num1 = int(input('请输入第一个整数：'))
num2 = int(input('请输入第二个整数：'))
num3 = int(input('请输入第三个整数：'))
if num1 > num2:
    if num2 > num3:
        print('升序排序：', num3, num2, num1)
    elif num1 > num3:
        print('升序排序：', num2, num3, num1)
    else:
        print('升序排序：', num2, num1, num3)
elif num1 > num3:
    print('升序排序：', num3, num1, num2)
elif num2 > num3:
    print('升序排序：', num1, num3, num2)
else:
    print("升序排序：", num1, num2, num3)

