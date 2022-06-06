num = int(input())
gifts = []
for i in range(1, num + 1):
    if (i % 11 == 0) or ('9' in str(i)):
        gifts.append(i)

print('礼物分数：', len(gifts))
print('应发放礼物的序号：', end='')
for i in gifts:
    print(i, end=' ')
