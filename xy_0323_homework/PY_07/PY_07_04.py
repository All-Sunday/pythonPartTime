stu = {'李白': '男', '李清照': '女', '杜牧': '男', '蔡文姬': '女', '李冶': '未填',
       '杜甫': '男', '刘禹锡': '男', '刘采春': '女', '谢道韫': '女', '苏轼': '男'}

name = input('新同学姓名：').strip()
sex = input('新同学性别：').strip()
stu[name] = sex
if stu['李冶'] == '未填':
    stu['李冶'] = '女'
print('当前学生信息为：', stu)
last_name_num = {}
for key in stu.keys():
    last_name_num[key[0]] = last_name_num.get(key[0], 0) + 1
print('各姓氏的人数为：', last_name_num)

women = []
for k, v in stu.items():
    if v == '女':
        women.append(k)
print('所有女生的名单：', end='')
for i in range(len(women)):
    if i != len(women) - 1:
        print(women[i], end='、')
    else:
        print(women[i])
