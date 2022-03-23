month = int(input())

if (month < 1) or (month > 12):
    print('输入的月份错误！')
else:
    if 3 <= month <= 5:
        print('春季')
    elif 6 <= month <= 8:
        print('夏季')
    elif 9 <= month <= 11:
        print('秋季')
    else:
        print('冬季')
