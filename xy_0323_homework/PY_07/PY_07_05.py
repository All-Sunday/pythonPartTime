import random

print('[1]输入要抽选的人数')
print('[2]输出学生名单')
print('[3]删除不能参会的学生')
print('[4]排序')
print('[0]退出')
print('----------')
students = set([])
while True:
    key = input('请输入您的选项：').strip()
    if not key.isdigit():
        print('输入的数据不符要求，请重新输入！')
    else:
        if key == '1':
            num = int(input('请输入要抽选的人数：').strip())
            while len(students) < num:
                students.add(random.randint(100000, 999999))
        elif key == '2':
            print('参会的学生名单：', students)
        elif key == '3':
            stu_no = int(input('请输入不能参会的学生学号：').strip())
            if stu_no in students:
                students.remove(stu_no)
                print(str(stu_no) + '已退出！')
            else:
                print('该学号不存在！')
        elif key == '4':
            sorted_students = list(students)
            sorted_students.sort()
            print('排序后的学生名单：', sorted_students)
        elif key == '0':
            print('\n---座谈会抽选活动完成。---')
            break
        else:
            print('输入的数据不符要求，请重新输入！')
