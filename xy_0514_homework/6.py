# @Description: 石头剪刀布大赛
# 输入第 1 行给出正整数 N（≤105），即双方交锋的次数。随后 N 行，每行给出一次交锋的信息，即甲、乙双方同时给出的的手势。C 代表“锤子”、J 代表“剪刀”、B 代表“布”，第 1 个字母代表甲方，第 2 个代表乙方，中间有 1 个空格
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/15 15:32
# @File : 6.py


N = int(input())
num1 = 0  # 定义三个变量，记录甲胜，平，输次数
num2 = 0
num3 = 0
C1, J1, B1 = 0, 0, 0  # 记录甲获胜字母的次数
C2, J2, B2 = 0, 0, 0  # 记录乙获胜字母的次数
for i in range(0, N):
    one, two = map(str, input().split(' '))
    # 这里将胜、平、输三种情况直接列出来，比较好理解
    if one == 'C' and two == 'J' or one == 'J' and \
            two == 'B' or one == 'B' and two == 'C':
        num1 += 1
    elif one == two:
        num2 += 1
    else:
        num3 += 1
    # 下面是具体获胜的是锤头，布还是剪刀
    if one == 'C' and two == 'J':
        C1 += 1
    elif one == 'J' and two == 'B':
        J1 += 1
    elif one == 'B' and two == 'C':
        B1 += 1
    elif two == 'C' and one == 'J':
        C2 += 1
    elif two == 'J' and one == 'B':
        J2 += 1
    elif two == 'B' and one == 'C':
        B2 += 1
print('{0} {1} {2}'.format(num1, num2, num3))
print('{2} {1} {0}'.format(num1, num2, num3))
if B1 >= C1 and B1 >= J1:
    print('B', end=' ')
elif C1 >= J1 and C1 >= B1:
    print('C', end=' ')
else:
    print('J', end=' ')
if B2 >= C2 and B2 >= J2:
    print('B')
elif C2 >= J2 and C2 >= B2:
    print('C')
else:
    print('J')

N = int(input().strip())

type1, type2, type3 = 0, 0, 0
C1, J1, B1 = 0, 0, 0
C2, J2, B2 = 0, 0, 0
for i in range(0, N):
    a, b = input().strip().split(' ')

    if a == 'C' and b == 'J' or a == 'J' and b == 'B' or a == 'B' and b == 'C':
        type1 += 1
    elif a == b:
        type2 += 1
    else:
        type3 += 1

    if a == 'C' and b == 'J':
        C1 += 1
    elif a == 'J' and b == 'B':
        J1 += 1
    elif a == 'B' and b == 'C':
        B1 += 1
    elif b == 'C' and a == 'J':
        C2 += 1
    elif b == 'J' and a == 'B':
        J2 += 1
    elif b == 'B' and a == 'C':
        B2 += 1

print('%d %d %d' % (type1, type2, type3))
print('%d %d %d' % (type3, type2, type1))

if B1 >= C1 and B1 >= J1:
    print('B', end=' ')
elif C1 >= J1 and C1 >= B1:
    print('C', end=' ')
else:
    print('J', end=' ')
if B2 >= C2 and B2 >= J2:
    print('B')
elif C2 >= J2 and C2 >= B2:
    print('C')
else:
    print('J')
