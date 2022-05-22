import jieba
# jieba分词 统计词频
f = open('hlm.txt', 'r', encoding='utf-8')

txt = f.read()  # 读文件
wordsList = jieba.lcut(txt)  # 分词结果
actors = [('贾宝玉', "宝玉"), ("林黛玉", "黛玉"), ("薛宝钗", "宝钗"),
          ("王熙凤", "凤姐"), ("贾母", "老太太"), ("袭人",), ("探春",),
          ('贾琏',), ("王夫人", "夫人")]  # actors 是人物列表，每个人物使用了元组
dictActors = {}  # 拟建立的字典

for actor in actors:  # 从人物表中查分词
    if len(actor) == 2:
        count1 = wordsList.count(actor[0])
        count2 = wordsList.count(actor[1])
        dictActors[actor[0]] = count1 + count2
    else:
        count1 = wordsList.count(actor[0])
        dictActors[actor[0]] = count1 + count2

items = list(dictActors.items())  # 将字典表项转化成列表
print(items)
items.sort(key=lambda x: x[1], reverse=True)  # 按频次从大到小排序
for i in range(len(items)):  # 输出统计结果
    word, count = items[i]
    print("{}\t{}".format(word, count))
