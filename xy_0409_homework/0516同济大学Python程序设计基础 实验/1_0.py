# 读文件 交换大小写 str.swapcase()
t1 = open('T1.txt')
print('文件内容：')
print(t1.read())
t1.seek(0)
lines = t1.readlines()
print('文件行数：', len(lines))

t2 = open('T2.txt', 'w')
for line in lines:
    t2.write(line.swapcase())
t1.close()
t2.close()
