# @Description: 字符串P型编码
# 100200300 可描述为" 1 个 1、 2个  0、1 个 2 、2 个 0 、1 个 3 、2 个0 "，因此它的 p型编码串为112012201320
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/15 14:15
# @File : 4.py


s = input().strip()
s += ' '
lena = len(s)

sum = 1
i = 0
while i < lena - 1:
    if s[i] == s[i + 1]:
        sum += 1
    else:
        print(sum, end='')
        print(s[i], end='')
        sum = 1
    i += 1


s = input().strip()

sum = 1
i = 0
while i < len(s):
    if i == len(s) - 1:
        if s[i] == s[i - 1]:
            # sum += 1
            pass
        #     print(sum, end='')
        #     print(s[i], end='')
        else:
            sum = 1
        #     print(s[i], sep='1')
        # break
    else:
        if s[i] == s[i + 1]:
            sum += 1
            i += 1
            continue

    print(sum, end='')
    print(s[i], end='')
    sum = 1
    i += 1


s = input().strip()
sum = 1
i = 0
while i < len(s):
    if i == len(s) - 1:
        if s[i] != s[i - 1]:
            sum = 1
    else:
        if s[i] == s[i + 1]:
            sum += 1
            i += 1
            continue

    print(sum, end='')
    print(s[i], end='')
    sum = 1
    i += 1
