import jieba

f = open('hlm.txt', 'r', encoding='utf-8')
txt = f.read()
wordsList = jieba.lcut(txt)
targets = ['贾宝玉', '林黛玉']

for target in targets:
    count = wordsList.count(target)
    print("{}\t{}".format(target, count))
