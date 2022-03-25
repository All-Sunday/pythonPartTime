while True:
    n = input('请输入一个正整数n：')
    if n.isdigit():
        n = int(n)
        if n > 0:
            break
    print('输入错误，请再次输入！')

while True:
    system = input('请输入需要转换成的进制(8 或 16)：')
    if system == '8':
        result = oct(n)
        break
    elif system != 16:
        result = hex(n)
        break

print('转换结果为：' + result[2:].upper())
