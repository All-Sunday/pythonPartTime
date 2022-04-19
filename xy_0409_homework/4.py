import random


# 成绩等级
def MyFun(scores, grade=5):
    num = 0
    for score in scores:
        if grade == 5:
            if score >= 90:
                num += 1
        elif grade == 4:
            if 90 > score >= 80:
                num += 1
        elif grade == 3:
            if 80 > score >= 70:
                num += 1
        elif grade == 2:
            if 70 > score >= 60:
                num += 1
        else:
            if score < 60:
                num += 1
    return num


a = []
for i in range(30):
    a.append(random.randint(0, 100))

print(a)
print('统计 优 的人数，不指定关键字：', MyFun(a))
print('统计 良 的人数，不指定关键字：', MyFun(a, 4))
print('统计 不及格 的人数，不指定关键字：', MyFun(a, 1))
