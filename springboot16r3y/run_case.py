# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/6 12:57
# @File : run_case.py
import unittest
from lib.HTMLTestRunner import HTMLTestRunner
import time, sys

from test_seller import TestSeller
from test_user import TestUser
from test_admin import TestAdmin

suite1 = unittest.TestLoader().loadTestsFromTestCase(TestUser)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestSeller)
suite3 = unittest.TestLoader().loadTestsFromTestCase(TestAdmin)
suite = unittest.TestSuite([suite1, suite2, suite3])

if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    filename = r"{0}result.html".format(now)
    print(filename)
    fp = open(filename, 'wb')

    runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'测试执行情况', tester='s')

    runner.run(suite)
    fp.close()
