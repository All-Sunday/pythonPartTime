num = input('请输入一个三位数的整数：').strip()
sum = 0
for i in num:
    sum += int(i)
print('和为' + str(sum))
