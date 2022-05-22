# 统计英文句子 字母出现次数

statement = input('请输入一个英文句子:').strip()

res = {}
for i in statement:
    if (65 <= ord(i) <= 90) or (97 <= ord(i) <= 122):
        res[i.upper()] = res.get(i.upper(), 0) + 1
print(res)
