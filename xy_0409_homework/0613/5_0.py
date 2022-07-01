# @Description: 从题 4 派生类 Teacher，并添加下列成员：
# （1）属性：No 和 Ta，分别表示教师的工号和教龄；
# （2）方法：NewDisp，输出所有成员的值。
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


class Teacher(Person):
    def __init__(self, name, age, no, ta):
        Person.__init__(self, name, age)
        self.No = no
        self.Ta = ta

    def NewDisp(self):
        Person.Disp(self)
        print(self.No)
        print(self.Ta)


t = Teacher('李云龙', 28, '10001', 8)
print("成员数据为：")
t.NewDisp()
