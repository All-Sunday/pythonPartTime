# @Description: 定义一个 identifier 类，具有一个属性 id，存放身份证号，以及如下函数：
# （1）getyear 函数用于从身份证号码中提取出生年份；
# （2）Disp 方法用于输出身份证号码。
# 编写利用该类的主程序。
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/14 10:50
# @File : 1.py
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
