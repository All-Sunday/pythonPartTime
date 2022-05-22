def getText(s):
    s = s.lower()
    new_s = s.replace(',', ' ').replace('.', ' ').replace(';', ' ').replace('?', ' ').replace('-', ' ').replace('"', ' ').replace('\'', ' ')
    return new_s


f = open('PY_08_05_Words.txt', 'r', encoding='utf-8')
txt = f.read()
txt = getText(txt)
wordsList = txt.split()

res = {}

for word in wordsList:
    if word == ' ' or word == '\n':
        continue
    if word in res:
        res[word] += 1
    else:
        res[word] = 1

items = list(res.items())
items.sort(key=lambda x: x[1], reverse=True)

print('单词出现频率排名前10如下：')
for i in range(10):
    word, count = items[i]
    print("{:<10}{:>5}".format(word, count))
