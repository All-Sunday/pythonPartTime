t1 = open('T1.txt')
print('文件内容：')
print(t1.read())
t1.seek(0)
lines = t1.readlines()
print('文件行数：', len(lines))

t2 = open('T2.txt', 'w')
for line in lines:
    newline = ""
    for ch in line:
        if 'A' <= ch < 'Z':
            ch = chr(ord(ch) + ord('a') - ord('A'))
        elif 'a' <= ch < 'z':
            ch = chr(ord(ch) + ord('A') - ord('a'))
        newline = newline + ch
    t2.write(newline)
t1.close()
t2.close()
