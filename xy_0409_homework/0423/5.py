# 字典姓名 手机号
res = {}
while True:
    name = input('请输入姓名（输入-1结束）：').strip()
    if name == '-1':
        break
    phone = input('请输入手机号（输入-1结束）：').strip()
    if name == '-1':
        break
    res[name] = phone

print('字典为：', res)

while True:
    name = input('请输入要查找的姓名（输入xxx结束）：').strip()
    if name == 'xxx':
        break
    print('手机号为：', res[name])
