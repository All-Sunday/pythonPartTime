scores = input('请输入评委为歌手打分的列表')[1:-1].split(',')  # 歌手分数
scores = [float(i) if '.' in i else int(i) for i in scores]  # 转换数据类型
scores.remove(max(scores))  # 去掉最高分
scores.remove(min(scores))
scores.sort()  # 排序
print('歌手有效得分列表为：' + str(scores))
score = round(sum(scores) / len(scores), 2)
print('该选手的最终得分为' + '%.2f' % score)
