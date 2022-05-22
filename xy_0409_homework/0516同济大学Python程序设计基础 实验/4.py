file = open('JJ.txt', 'w')
i = input('请输入职工的工号、姓名和奖金(格式：工号,姓名,奖金)：').strip()
num = 1
while i != "" and num < 10:
    num += 1
    file.write(i + '\n')
    i = input().strip()
file.close()

file = open('JJ.txt', 'r')
new_file = open('NewJJ.txt', 'w')
lines = file.readlines()
res = []
for line in lines:
    line_list = line.split(',')

    line_list[2] = eval(line_list[2][:-2])
    res.append(line_list)

sorted_res = sorted(res, key=lambda x: x[2])
for data in sorted_res:
    s = data[0] + ',' + data[1] + ',' + str(data[2]) + '元'

    new_file.write(s + '\n')

file.close()
new_file.close()
