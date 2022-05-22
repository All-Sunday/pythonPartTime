# @Description: 分发饼干
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/15 14:09
# @File : 3.py

g = eval(input().strip())
s = eval(input().strip())
g.sort()
s.sort()
i = j = res = 0
while i < len(g) and j < len(s):
    if g[i] <= s[j]:
        res += 1
        i += 1
    j += 1
print(res)

g = eval(input().strip())
g.sort()
s = eval(input().strip())
s.sort()

g_index = s_index = res = 0
while (g_index < len(g)) and (s_index < len(s)):
    if g[g_index] <= s[s_index]:
        res += 1
        g_index += 1
        s_index += 1
    else:
        s_index += 1
print(res)
