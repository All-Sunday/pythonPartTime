# zip 两个list生成dict
letter_list = []
for i in range(65, 91):
    letter_list.append(chr(i))

num_list = []
for i in range(26):
    num_list.append(i + 1)

res = dict(zip(letter_list, num_list))
print(res)
