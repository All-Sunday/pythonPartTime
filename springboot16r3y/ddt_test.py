# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/5 22:13
# @File : ddt_test.py
'''
ddt结合unittest来进行数据处理的第三方库，很强大
安装pip install ddt
ddt需要和unittest或pytest结合使用
'''
from ddt import ddt, data, unpack
import unittest

test_print = [1, 3]
test_b = [[1, 2, 3], [4, 5, 6]]


@ddt  # 装饰测试类
class TestMath(unittest.TestCase):

    @data(test_print)  # 装饰测试函数，通过这种方式传参，如果通过*test_data传参，则有几个参数，执行几次测试用例
    def test_print(self, item):
        print('item:{0}'.format(item))

    @data(*test_b)
    @unpack  # 当要取内层嵌套，如test_b的值时，用unpack修饰
    def test_b(self, i, j, k):  # 使用unpack后，必须内层嵌套的值都以变量的形式传入，否则报错
        print('我是i:{0}，j:{1}，k:{2}'.format(i, j, k))
