# s = "http://sports.sina.com.cn/"
s = input('请输入字符串：').strip()
print('字符串中字母t出现的次数:', s.count('t'))
print('字符串中"com"子字符串出现的位置:', s.find('com'))
print('将字符串中所有的"."替换为"-":', s.replace('.', '-'))
print('提取"sports"和"sina"两个子字符串串(分别使用正向切片和反向切片方式):', s[7:13], s[-12:-8])
print('将字符串中的字母全变为大写:', s.upper())
print('输出字符串的总字符个数:', len(s))
print('在字符串后拼接子字符串"index":', s + 'index')
