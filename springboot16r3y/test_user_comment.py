# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/5 22:50
# @File : test_user_comment.py
import time
import unittest

import pandas as pd
from ddt import ddt, data, unpack
from selenium import webdriver

start_url = 'http://localhost:8080/springboot16r3y/front/index.html'
file_path = r'E:\code_workplace\python\2022\january\data\springboot16r3y\用户测试用例.xlsx'
excel_reader = pd.ExcelFile(file_path)
sheet_names = excel_reader.sheet_names
df = excel_reader.parse(sheet_name=sheet_names[3])
df = df[df['expected'] == '留言成功']
comments = list(df['content'].values)


@ddt
class TestUserComment(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome(executable_path=r'E:\code_workplace\python\chromedriver.exe')
        cls.driver.get('http://localhost:8080/springboot16r3y/front/index.html')
        # time.sleep(20)
        time.sleep(1)
        cls.driver.find_element_by_xpath('//div[@class="navs"]/div/ul/li[4]/a').click()
        time.sleep(1)
        cls.driver.find_element_by_xpath('//input[@name="username"]').send_keys('test')
        cls.driver.find_element_by_xpath('//input[@name="password"]').send_keys('123456')
        cls.driver.find_element_by_xpath('//i[@class="layui-anim layui-icon"][1]').click()
        cls.driver.find_element_by_xpath('//button').click()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    @data(*comments)
    def test_user_comment(self, comment):
        time.sleep(0.5)
        self.driver.refresh()
        time.sleep(0.5)
        self.driver.switch_to.frame('iframe')
        self.driver.find_element_by_xpath('//textarea[@class="layui-textarea"]').clear()
        self.driver.find_element_by_xpath('//textarea[@class="layui-textarea"]').send_keys(comment)

        time.sleep(0.1)
        self.driver.find_element_by_xpath('//button[@class="layui-btn btn-submit"]').click()
        while True:
            time.sleep(0.05)
            if r'layui-layer-dialog' in self.driver.page_source:
                self.assertTrue(r'layui-layer-dialog' in self.driver.page_source)
                break
        time.sleep(0.1)
