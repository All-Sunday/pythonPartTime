# @Description: 设计一个矩形类（Rect），具有长、宽属性，类还具有求解并显示矩形的周长和面积
# 的功能以及求两个矩形面积和的功能。
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/14 16:36
# @File : 3.py
class Rect:
    def __init__(self, l, w):
        self.length = l
        self.width = w

    def get_perimeter(self):
        perimeter = (self.length + self.width) * 2
        return perimeter

    def get_area(self):
        area = self.length * self.width
        return area

    def sum(self, rect):
        sum_res = self.get_area() + rect.get_area()
        return sum_res


r1 = Rect(3, 4)
r2 = Rect(4, 5)

print('矩形r1（3，4）的周长为：', r1.get_perimeter())
print('矩形r1（3，4）的面积为：', r1.get_area())
print('两个矩形 r1（3，4） 和 r2（4，5）的面积和为：', r1.sum(r2))
