f = open('学生成绩文件.txt', 'r', encoding='utf-8')
lines = f.readlines()

scores = []
for student in lines:
    res = student.split()
    scores.append(int(res[2]))

max_score = max(scores)
min_score = min(scores)
total_score = sum(scores)
avg_score = total_score / len(scores)
print('平均分：', avg_score)
print('最低分：', min_score)
print('平均分：', avg_score)
print('最高分：', max_score)
