score = float(input('请输入一个百分制成绩[0~100]:'))

if (score < 0) or (score > 100):
    print('输入成绩有误！')
else:
    if score >= 60:
        gpa = round((score - 60) / 10, 2) + 1
    else:
        gpa = 0
    if score >= 90:
        print(str(score) + '分对应的绩点为' + str(gpa) + '，五级制等第为A')
    elif score >= 80:
        print(str(score) + '分对应的绩点为' + str(gpa) + '，五级制等第为B')
    elif score >= 70:
        print(str(score) + '分对应的绩点为' + str(gpa) + '，五级制等第为C')
    elif score >= 60:
        print(str(score) + '分对应的绩点为' + str(gpa) + '，五级制等第为D')
    else:
        print(str(score) + '分对应的绩点为' + str(gpa) + '，五级制等第为E')
print('=====END=====')
