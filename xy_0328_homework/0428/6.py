class Cal(object):

    def __init__(self, a, b, x, y):
        self.a = a
        self.b = b
        self.x = x
        self.y = y

    def get_res(self):
        return (self.a + self.b) / (self.x - self.y)


a = 1
b = 2
x = 4
y = 3
cal = Cal(a, b, x, y)
print('表达式值为：', cal.get_res())
