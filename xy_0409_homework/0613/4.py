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
