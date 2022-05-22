# 头歌刷题  立方分解
# 9
# 9*9*9=729=73+75+77+79+81+83+85+87+89

num = int(input().strip())
s = []
for i in range(num):
    s.append((num * num - num + 1) + 2 * i)
# print(s)
print("%d*%d*%d=%d=" % (num, num, num, num * num * num) + '+'.join(map(str, s)))

num = int(input().strip())
print("%d*%d*%d=%d=" % (num, num, num, num * num * num), end="")

res = (num * num) - num + 1
for i in range(0, num - 1):
    print(res, end="+")
    res += 2

print(res)
