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
