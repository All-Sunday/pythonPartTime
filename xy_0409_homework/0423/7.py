# 手机号码数字转英文单词
letter_dict = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
               '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
phone = input('请输入电话号码：').strip()
for num in phone:
    print(letter_dict[num], end=' ')
