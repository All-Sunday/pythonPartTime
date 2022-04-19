year = int(input("请输入一个年份："))
if (year % 4 == 0) and (year % 100 != 0) or (year % 400) == 0:
    print(str(year) + "年是闰年")
else:
    print(str(year) + "年不是闰年")

score = float(input('请输入一个百分制成绩[0~100]:'))
if score >= 80:
    print(str(score) + '分对应的等级第为A')
elif score >= 70:
    print(str(score) + '分对应的等级第为B')
elif score >= 60:
    print(str(score) + '分对应的等级第为C')
else:
    print(str(score) + '分对应的等级第为D')


def max_num(num1, num2):
    if num1 > num2:
        return num1
    else:
        return num2
max = max_num(5, 9)
print('最大的是：' + str(max))

def avg_score(score1, score2, score3):
    return round((score1 + score2 + score3) / 3, 2)
avg = avg_score(50, 90.5, 80)
print('三门课的平均成绩是：' + str(avg))
