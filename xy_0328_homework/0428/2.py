x = int(input('请输入第一个整数：'))
y = int(input('请输入第二个整数：'))
z = int(input('请输入第三个整数：'))
if x > y:
    if y > z:
        print('排序后：', z, y, x)
    elif x > z:
        print('排序后：', y, z, x)
    else:
        print('排序后：', y, x, z)
elif x > z:
    print('排序后：', z, x, y)
elif y > z:
    print('排序后：', x, z, y)
else:
    print("排序后：", x, y, z)
