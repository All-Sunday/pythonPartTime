# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/7 12:37
# @File : test_user.py
import time
import unittest

import numpy
import pandas as pd
from ddt import ddt, data, unpack
from selenium import webdriver
from selenium.webdriver.common.by import By

file_path = r'E:\code_workplace\python\2022\january\data\springboot16r3y\用户测试用例.xlsx'
excel_reader = pd.ExcelFile(file_path)
sheet_names = excel_reader.sheet_names

df = excel_reader.parse(sheet_name=sheet_names[0], dtype=object)  # login sheet
df = df[df['expected'] != '账号或密码不正确'][['用例描述', 'userId', 'password']]
login_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[1], dtype=object)  # buy sheet
df = df[df['expected'] == '提交成功'][['数量', '总价格', '购买日期', '配送方式', '用户名', '手机', '地址']]
buy_infos = [tuple(row) for row in df.values]
# print(buy_infos[0][2].strftime('%Y-%m'),type(buy_infos[0][2].strftime('%Y-%m')))  # pandas._libs.tslibs.timestamps.Timestamp 转字符串
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[2], dtype=object)  # search sheet
df = df[['商品名称', '品牌']]
search_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[3], dtype=object)  # comment sheet
df = df[df['expected'] == '留言成功']
comments = list(df['content'].values)
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[5], dtype=object)  # info sheet
df = df[df['expected'] == '修改密码成功，下次登录系统生效'][['原密码', '新密码', '确认密码']]
password_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[6], dtype=object)  # password sheet
df = df[df['expected'] == '修改信息成功'][['姓名', '性别', '手机', '地址']]
df = df.fillna('')
personal_infos = [tuple(row) for row in df.values]
time.sleep(1)


@ddt
class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome(executable_path=r'E:\code_workplace\python\chromedriver.exe')
        cls.driver.get('http://localhost:8080/springboot16r3y/front/index.html')
        time.sleep(0.6)

        cls.driver.find_element_by_xpath('//div[@class="navs"]/div/ul/li[5]/a').click()
        time.sleep(0.6)
        cls.driver.find_element_by_xpath('//input[@name="username"]').send_keys('test')
        cls.driver.find_element_by_xpath('//input[@name="password"]').send_keys('123456')
        cls.driver.find_element_by_xpath('//form[@id="loginForm"]/div[5]/div[1]/i').click()
        cls.driver.find_element_by_xpath('//button').click()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    def tearDown(self) -> None:
        time.sleep(5)

    @data(*login_infos)
    def test_user_9login(self, login_info):
        self.driver.get('http://127.0.0.1:8080/springboot16r3y/admin/dist/index.html#/login')
        time.sleep(1)
        self.driver.find_element_by_xpath('//input[@name="username"]').send_keys(login_info[1])
        self.driver.find_element_by_xpath('//input[@name="password"]').send_keys(login_info[2])

        if '买家' in login_info[0]:
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_elements_by_xpath('//input[@type="radio"]')[1])
        elif '卖家' in login_info[0]:
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_elements_by_xpath('//input[@type="radio"]')[2])
        else:
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_elements_by_xpath('//input[@type="radio"]')[0])
        self.driver.find_element_by_xpath('//button').click()
        time.sleep(0.8)
        self.assertEqual('后台管理系统', self.driver.title)
        self.driver.find_element_by_xpath('//div[@class="right-menu"]/div[3]').click()
        time.sleep(0.5)

    @data(*buy_infos)
    def test_user_1buy(self, buy_info):
        self.driver.get('http://localhost:8080/springboot16r3y/front/index.html')
        time.sleep(0.5)

        self.driver.find_element_by_xpath('//div[@class="navs"]/div/ul/li[2]/a').click()
        time.sleep(0.5)

        self.driver.switch_to.frame('iframe')
        self.driver.find_element(By.CSS_SELECTOR, ".list-item:nth-child(7) img").click()
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element(By.CSS_SELECTOR, ".detail-item > .layui-btn"))

        time.sleep(0.5)
        self.driver.find_element(By.ID, "shuliang").clear()
        self.driver.find_element(By.ID, "shuliang").send_keys(buy_info[0])
        if buy_info[2] is not pd.NaT:
            date_js = "$('input[id=goumairiqi]').val('" + buy_info[2].strftime('%Y-%m-%d') + "')"  # 修改日期
            self.driver.execute_script(date_js)

        if buy_info[3] is not numpy.NAN:
            self.driver.find_element(By.CSS_SELECTOR, ".layui-unselect:nth-child(1)").click()
            time.sleep(0.4)
            if buy_info[3] == '自提':
                self.driver.find_element(By.CSS_SELECTOR, "dd:nth-child(2)").click()
            elif buy_info[3] == '送货上门':
                self.driver.find_element(By.CSS_SELECTOR, "dd:nth-child(3)").click()

        if buy_info[4] is not numpy.NAN:
            self.driver.find_element(By.ID, "yonghuming").clear()
            self.driver.find_element(By.ID, "yonghuming").send_keys(buy_info[4])
        if buy_info[5] is not numpy.NAN:
            self.driver.find_element(By.ID, "shouji").clear()
            self.driver.find_element(By.ID, "shouji").send_keys(buy_info[5])
        if buy_info[6] is not numpy.NAN:
            self.driver.find_element(By.ID, "dizhi").clear()
            self.driver.find_element(By.ID, "dizhi").send_keys(buy_info[6])
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()

        while True:
            time.sleep(0.05)
            if r'提交成功' in self.driver.page_source:
                self.assertTrue(r'提交成功' in self.driver.page_source)
                break
            time.sleep(0.1)
        time.sleep(0.5)

    @data(*search_infos)
    def test_user_2search(self, search_info):
        self.driver.get('http://localhost:8080/springboot16r3y/front/index.html')
        time.sleep(0.6)

        self.driver.find_element_by_xpath('//div[@class="navs"]/div/ul/li[2]/a').click()
        time.sleep(0.5)

        self.driver.switch_to.frame('iframe')
        self.driver.find_element(By.ID, "shangpinmingcheng").clear()
        self.driver.find_element(By.ID, "shangpinmingcheng").send_keys(
            search_info[0] if search_info[0] is not numpy.NAN else '')
        self.driver.find_element(By.ID, "pinpai").clear()
        self.driver.find_element(By.ID, "pinpai").send_keys(search_info[1] if search_info[1] is not numpy.NAN else '')
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element(By.ID, "btn-search"))
        time.sleep(0.5)

    @data(*comments)
    def test_user_3comment(self, comment):
        self.driver.get('http://localhost:8080/springboot16r3y/front/index.html')
        time.sleep(0.6)

        self.driver.find_element_by_xpath('//div[@class="navs"]/div/ul/li[4]/a').click()
        time.sleep(0.5)
        self.driver.switch_to.frame('iframe')
        self.driver.find_element_by_xpath('//textarea[@class="layui-textarea"]').clear()
        self.driver.find_element_by_xpath('//textarea[@class="layui-textarea"]').send_keys(comment)

        time.sleep(0.1)
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element_by_xpath('//button[@class="layui-btn btn-submit"]'))
        while True:
            time.sleep(0.05)
            if r'layui-layer-dialog' in self.driver.page_source:
                self.assertTrue(r'layui-layer-dialog' in self.driver.page_source)
                break
        time.sleep(0.5)

    @data(*personal_infos)
    def test_user_4personal_info(self, personal_info):
        self.driver.get("http://localhost:8080/springboot16r3y/admin/dist/index.html")
        time.sleep(0.6)

        self.driver.find_element(By.CSS_SELECTOR, ".el-menu-item:nth-child(2)").click()
        time.sleep(0.4)
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").send_keys(personal_info[0])
        self.driver.find_element(By.CSS_SELECTOR, ".el-select .el-input__inner").click()
        time.sleep(0.4)
        if personal_info[1] == '男':
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element(By.XPATH,
                                                                '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]'))

        else:
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element(By.XPATH,
                                                                '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[2]'))
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(5) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(5) .el-input__inner").send_keys(personal_info[2])
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").send_keys(personal_info[3])
        self.driver.find_element(By.CSS_SELECTOR, ".el-button > span").click()

        while True:
            time.sleep(0.05)
            if r'修改信息成功' in self.driver.page_source:
                self.assertTrue(r'修改信息成功' in self.driver.page_source)
                break
            time.sleep(0.1)
        time.sleep(0.5)

    @data(*password_infos)
    def test_user_5password(self, password_info):
        self.driver.get("http://localhost:8080/springboot16r3y/admin/dist/index.html")
        time.sleep(0.6)

        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item:nth-child(1)").click()
        time.sleep(0.4)
        self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").send_keys(
            password_info[0])
        self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").send_keys(
            password_info[1])
        self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(3) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(3) .el-input__inner").send_keys(
            password_info[2])
        self.driver.find_element(By.CSS_SELECTOR, ".el-button > span").click()

        while True:
            time.sleep(0.05)
            if r'修改密码成功' in self.driver.page_source:
                self.assertTrue(r'修改密码成功' in self.driver.page_source)
                break
            time.sleep(0.1)
        time.sleep(0.5)
