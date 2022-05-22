# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/16 12:04
# @File : 3.py
x = 10


def f():
    x = 0
    print(x)


print(x)
f()
print(x)
print('(1): 10 0 10')
print('(2): 不是，行A中的变量x是全局变量，行B中的变量x是局部变量。')
print("(3): 10 10 10")
print('(4): 在行A之前增加一行 global x')
