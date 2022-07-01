class identifier:
    def __init__(self, a):
        self.id = a

    def getyear(self):
        year = self.id[6:10]
        return year

    def Disp(self):
        print(self.id)


i = identifier('411110199905102453')
print('出生年份为：', i.getyear())
print('身份证号码为：', end='')
i.Disp()
