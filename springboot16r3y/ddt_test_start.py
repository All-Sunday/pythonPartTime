# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/5 22:14
# @File : ddt_test_start.py
import unittest
import test  # 这里需要导入测试文件
from lib.HTMLTestRunner import HTMLTestRunner
import time, sys

# from ddt_test import TestMath
from springboot16r3y import ddt_test

testunit = unittest.TestSuite()
# 将测试用例加入到测试容器(套件)中
testunit.addTest(unittest.makeSuite(ddt_test.TestMath))
# testunit.addTest(unittest.makeSuite(youdao.Youdao))

if __name__ == '__main__':
    # 取前面时间
    now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
    filename = r"{0}result.html".format(now)
    print(filename)
    fp = open(filename, 'wb')

    runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'测试执行情况')

    # 执行测试用例
    runner.run(testunit)
    fp.close()
