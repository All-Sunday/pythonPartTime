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
