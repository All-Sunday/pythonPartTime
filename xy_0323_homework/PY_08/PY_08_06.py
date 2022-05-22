# csv.writer写数据到csv
import csv

data = [['99100', 90, 100, 91, 80], ['99101', 89, 95, 99, 80], ['99102', 87, 90, 67, 100], ['99103', 100, 99, 95, 90],
        ['99104', 78, 80, 86, 88]]
for i in data:
    i.append(sum(i[1:]))

with open('PY_08_06_Scores.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    print('开始写入文件......')
    writer.writerow(['学号', '语文', '数学', '英语', 'python', '总分'])
    for i in data:
        writer.writerow(i)
    print('文件写入成功！')
