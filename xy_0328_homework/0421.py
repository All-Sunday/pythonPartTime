class FatherClass(object):

    def __init__(self):
        self.num1 = 1
        self.num2 = 2

    def fcn(self):
        res_sum = self.num1 + self.num2
        res_diff = self.num1 - self.num2
        return res_sum, res_diff


class SonClass(FatherClass):

    def cal(self, num3):
        self.num3 = num3
        res_sum, res_diff = super().fcn()
        return res_sum + self.num3, res_diff - self.num3


test = SonClass()
res_sum, res_diff = test.cal(3)
print('和：', res_sum, '差：', res_diff)
