# @Description: 设计一个楼房类（Building），包含楼的长、宽、层数及每平米单价属性，并具有求
# 楼房的面积及总价等功能。最后编写利用该类的主程序。
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/14 10:50
# @File : 1.py
class Building:
    def __init__(self, l, w, f, p):
        self.length = l
        self.width = w
        self.floor = f
        self.price = p

    def get_total_area(self):
        area = self.length * self.width * self.floor
        return area

    def get_total_price(self):
        return self.get_total_area() * self.price


b = Building(30, 10, 10, 28000)
print('面积为：', b.get_total_area(), '平方米')
print('总价为：', b.get_total_price(), '元')
