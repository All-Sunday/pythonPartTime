file1 = open('合并前1.txt', 'r', encoding='utf-8')
file2 = open('合并前2.txt', 'r', encoding='utf-8')
file3 = open('合并.txt', 'w', encoding='utf-8')

lines1 = file1.readlines()
lines2 = file2.readlines()

file3.writelines(lines1)
file3.write('\n')
file3.writelines(lines2)

file1.close()
file2.close()
file3.close()
