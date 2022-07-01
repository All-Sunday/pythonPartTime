# @Description: 设计一个 Person 类，具有如下的成员：
# （1）属性：Name 和 Age，表示一个人姓名和年龄；
# （2）方法：Disp，输出各数据成员
# 最后编写一个使用该类的测试程序。
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/14 16:46
# @File : 4.py
class Person:
    def __init__(self, n, a):
        self.Name = n
        self.Age = a

    def Disp(self):
        print(self.Name)
        print(self.Age)


p = Person('李云龙', 28)
print("成员数据为：")
p.Disp()
