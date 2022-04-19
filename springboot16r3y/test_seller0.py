# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/8 16:34
# @File : test_seller.py
import time
import unittest
import numpy
import pandas as pd
from ddt import ddt, data
from selenium import webdriver
from selenium.webdriver.common.by import By

file_path = r'E:\code_workplace\python\2022\january\data\springboot16r3y\卖家测试用例.xlsx'
excel_reader = pd.ExcelFile(file_path)
sheet_names = excel_reader.sheet_names

df = excel_reader.parse(sheet_name=sheet_names[0], dtype=object)  # password sheet
df = df[df['expected'] == '修改密码成功，下次登录系统生效'][['原密码', '新密码', '确认密码']]
password_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[1], dtype=object)  # info sheet
df = df[df['expected'] == '修改信息成功'][['姓名', '性别', '手机']]
df = df.fillna('')
personal_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[2], dtype=object)  # add sheet
df = df[df['expected'] == '操作成功'][['商品名称', '图片', '品牌', '型号', '颜色', '成色', '原价', '二手价', '数量', '购买日期', '商品详情']]
df = df.fillna('')
add_infos = [tuple(row) for row in df.values]
# print(add_infos)
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[3], dtype=object)  # buy sheet
df = df[df['expected'] != '无法进行查询'][['用例描述', '审核状态', '内容', '商品名称', '卖家账号']]
df = df.fillna('')
buy_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[4], dtype=object)  # evaluate sheet
df = df[df['expected'] != '无法进行查询'][['用例描述', '审核状态', '内容', '订单编号', '商品名称', '用户名']]
df = df.fillna('')
evaluate_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[5], dtype=object)  # comment sheet
df = df[df['expected'] == '留言成功']
comments = list(df['content'].values)
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[6], dtype=object)  # search sheet
df = df[['商品名称', '品牌']]
search_infos = [tuple(row) for row in df.values]
time.sleep(1)


@ddt
class TestSeller(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome(executable_path=r'E:\code_workplace\python\chromedriver.exe')
        cls.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html#/login')
        time.sleep(1)
        cls.driver.find_element_by_xpath('//input[@name="username"]').send_keys('abc')
        cls.driver.find_element_by_xpath('//input[@name="password"]').send_keys('123456')
        cls.driver.execute_script("arguments[0].click();",
                                  cls.driver.find_elements_by_xpath('//input[@type="radio"]')[2])

        cls.driver.find_element_by_xpath('//button').click()
        time.sleep(0.8)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    def tearDown(self) -> None:
        time.sleep(5)

    @data(*password_infos)
    def test_seller_1password(self, password_info):
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

    @data(*personal_infos)
    def test_seller_2personal_info(self, personal_info):
        self.driver.get("http://localhost:8080/springboot16r3y/admin/dist/index.html")
        time.sleep(0.6)

        self.driver.find_element(By.CSS_SELECTOR, ".el-menu-item:nth-child(2)").click()
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(8) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(8) .el-input__inner").send_keys(personal_info[0])
        self.driver.find_element(By.CSS_SELECTOR, ".el-select .el-input__inner").click()
        time.sleep(0.5)
        if personal_info[1] == '男':
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element(By.XPATH,
                                                                '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]'))
        else:
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element(By.XPATH,
                                                                '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[2]'))
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(11) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(11) .el-input__inner").send_keys(personal_info[2])
        self.driver.find_element(By.CSS_SELECTOR, ".el-button > span").click()

        while True:
            time.sleep(0.05)
            if r'修改信息成功' in self.driver.page_source:
                self.assertTrue(r'修改信息成功' in self.driver.page_source)
                break
            time.sleep(0.1)
        time.sleep(0.5)

    @data(*add_infos)
    def test_seller_3add(self, add_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(3) > .el-submenu__title").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-button--success").click()
        time.sleep(0.2)

        self.driver.find_element(By.CSS_SELECTOR, ".is-required .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".is-required .el-input__inner").send_keys(add_info[0])
        if add_info[1] == '√':
            self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\1617071916390.jpg")
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").send_keys(add_info[2])
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(4) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(4) .el-input__inner").send_keys(add_info[3])
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(5) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(5) .el-input__inner").send_keys(add_info[4])
        self.driver.find_element(By.CSS_SELECTOR, ".el-select .el-input__inner").click()
        time.sleep(0.4)
        if add_info[5] != '':
            if add_info[5] == '九成新':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]'))
            elif add_info[5] == '八成新':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[2]'))
            elif add_info[5] == '七成新':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[3]'))
            else:
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[4]'))
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").send_keys(add_info[6])
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(8) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(8) .el-input__inner").send_keys(add_info[7])
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(9) .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(9) .el-input__inner").send_keys(add_info[8])
        if add_info[9] is not pd.NaT:
            # date_js = "$('input[id=goumairiqi]').val('" + add_info[9].strftime('%Y-%m-%d') + "')"  # 修改日期
            # self.driver.execute_script(date_js)
            self.driver.find_element(By.CSS_SELECTOR, ".el-date-editor > .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-date-editor > .el-input__inner").send_keys(
                add_info[9].strftime('%Y 年 %m 月 %d 日'))

        self.driver.find_element(By.CSS_SELECTOR, ".ql-editor").send_keys(add_info[10])

        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()

        while True:
            time.sleep(0.05)
            if r'操作成功' in self.driver.page_source:
                self.assertTrue(r'操作成功' in self.driver.page_source)
                break
            time.sleep(0.1)
        time.sleep(0.5)

    @data(*buy_infos)
    def test_seller_4buy(self, buy_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.6)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(4) span").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item").click()
        time.sleep(0.2)

        if '审核' in buy_info[0]:
            self.driver.find_element(By.XPATH,
                                     '//tr[@class="el-table__row"][1]/td[last()]/div/button').click()
            time.sleep(0.2)
            self.driver.find_element(By.CSS_SELECTOR, ".el-select--medium .el-input__inner").click()
            time.sleep(0.5)
            if buy_info[1] == '通过':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    ".//body/div[@class='el-select-dropdown el-popper']//ul/li[1]"))
            else:
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    ".//body/div[@class='el-select-dropdown el-popper']//ul/li[2]"))
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").send_keys(buy_info[2])
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--primary").click()
            time.sleep(0.2)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2) > span").click()

            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(1)
        else:
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").send_keys(
                buy_info[3])
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").send_keys(
                buy_info[4])
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--medium > span:nth-child(2)").click()
            time.sleep(0.5)
        time.sleep(0.5)

    @data(*evaluate_infos)
    def atest_seller_5evaluate(self, evaluate_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.6)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(5) span").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item").click()
        time.sleep(0.2)

        if '审核' in evaluate_info[0]:
            self.driver.find_element(By.XPATH,
                                     '//tr[@class="el-table__row"][1]/td[14]/div/button').click()
            time.sleep(0.2)
            self.driver.find_element(By.CSS_SELECTOR, ".el-select--medium .el-input__inner").click()
            time.sleep(0.5)
            if evaluate_info[1] == '通过':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    ".//body/div[@class='el-select-dropdown el-popper']//ul/li[1]"))
            else:
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    ".//body/div[@class='el-select-dropdown el-popper']//ul/li[2]"))
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").send_keys(evaluate_info[2])
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--primary").click()
            time.sleep(0.2)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2) > span").click()

            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(1)
        elif '查看' in evaluate_info[0]:
            self.driver.find_element(By.XPATH,
                                     '//tr[@class="el-table__row"][1]/td[15]/div/button').click()
            while True:
                time.sleep(0.05)
                if r'查询' not in self.driver.page_source:
                    self.assertTrue(r'查询' not in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(1)
        else:
            self.driver.find_element(By.CSS_SELECTOR,
                                     ".el-form-item:nth-child(1) > .el-form-item__content > .el-input > .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR,
                                     ".el-form-item:nth-child(1) > .el-form-item__content > .el-input > .el-input__inner").send_keys(
                evaluate_info[3])
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").send_keys(
                evaluate_info[4])
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(3) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(3) .el-input__inner").send_keys(
                evaluate_info[5])
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--medium > span:nth-child(2)").click()
            time.sleep(0.5)
        time.sleep(0.5)

    @data(*comments)
    def test_user_6comment(self, comment):
        self.driver.get('http://localhost:8080/springboot16r3y/front/index.html')
        time.sleep(0.6)

        self.driver.find_element_by_xpath('//div[@class="navs"]/div/ul/li[4]/a').click()
        time.sleep(0.5)
        if 'login' in self.driver.current_url:
            self.driver.find_element_by_xpath('//input[@name="username"]').send_keys('abc')
            self.driver.find_element_by_xpath('//input[@name="password"]').send_keys('123456')
            self.driver.find_element_by_xpath('//form[@id="loginForm"]/div[5]/div[2]/i').click()
            self.driver.find_element_by_xpath('//button').click()
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

    @data(*search_infos)
    def test_user_7search(self, search_info):
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
