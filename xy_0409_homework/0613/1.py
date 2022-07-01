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
