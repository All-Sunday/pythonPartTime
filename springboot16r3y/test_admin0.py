# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/8 23:36

import time
import unittest
import pandas as pd
from ddt import ddt, data
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

file_path = r'E:\code_workplace\python\2022\january\data\springboot16r3y\管理员测试用例.xlsx'
excel_reader = pd.ExcelFile(file_path)
sheet_names = excel_reader.sheet_names

df = excel_reader.parse(sheet_name=sheet_names[0], dtype=object)  # password sheet
df = df[df['expected'] == '修改密码成功，下次登录系统生效'][['原密码', '新密码', '确认密码']]
password_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[1], dtype=object)  # info sheet
df = df[df['expected'] == '修改信息成功'][['用例描述', '用户名']]
df = df.fillna('')
personal_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[2], dtype=object)  # users sheet
df = df[df['expected'].isin(('添加成功', '删除成功', '显示用户名为test的用户', '显示用户个人信息', '修改成功'))][
    ['用例描述', '用户名', '密码', '姓名', '头像', '性别', '手机', '地址']]
df = df.fillna('')
users_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[3], dtype=object)  # sellers sheet
df = df[df['expected'].isin(('添加成功', '删除成功', '显示卖家账号为aaa的卖家账号', '显示卖家姓名为李明的卖家账号', '显示卖家账号个人信息', '修改成功'))][
    ['用例描述', '卖家账号', '密码', '卖家姓名', '头像', '性别', '手机']]
df = df.fillna('')
sellers_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[4], dtype=object)  # e-bike sheet
df = df[~df['expected'].isin(('无法进行查询', '无法查看详情', '无法进行删除'))][
    ['用例描述', '商品名称', '图片', '品牌', '型号', '颜色', '成色', '原价', '二手价', '数量', '购买日期', '卖家账号', '联系电话',
     '商品详情']]
df = df.fillna('')
e_bike_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[5], dtype=object)  # buy sheet
df = df[~df['expected'].isin(('无法进行查看', '无法进行删除', '无法查询'))][['用例描述', '商品名称', '卖家账号']]
df = df.fillna('')
buy_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[6], dtype=object)  # evaluate sheet
df = df[~df['expected'].isin(('无法修改订单编号', '无法进行删除', '无法查看详情', '无法查询'))][
    ['用例描述', '订单编号', '商品名称', '购买日期', '评分', '评价日期', '卖家账号', '用户名', '手机', '评价内容']]
df = df.fillna('')
evaluate_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[7], dtype=object)  # comment sheet
df = df[~df['expected'].isin(('无法查看详情', '无法删除', '无法进行查询'))][
    ['用例描述', '回复内容', '用户名']]
df = df.fillna('')
comments = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[8], dtype=object)  # notice sheet
df = df[~df['expected'].isin(('标题不能为空', '图片不能为空', '内容不能为空', '无法进行查看', '无法进行删除'))][
    ['用例描述', '标题', '图片', '简介', '内容']]
df = df.fillna('')
notice_infos = [tuple(row) for row in df.values]
time.sleep(1)

df = excel_reader.parse(sheet_name=sheet_names[9], dtype=object)  # slideshow sheet
df = df[~df['expected'].isin(('名称不能为空', '无法查看详情', '无法删除', '无法进行查询'))][
    ['用例描述', '名称', '图片']]
df = df.fillna('')
slideshow_infos = [tuple(row) for row in df.values]
time.sleep(1)


@ddt
class TestAdmin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome(executable_path=r'E:\code_workplace\python\chromedriver.exe')
        cls.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html#/login')
        time.sleep(1)
        cls.driver.find_element_by_xpath('//input[@name="username"]').send_keys('admin')
        cls.driver.find_element_by_xpath('//input[@name="password"]').send_keys('123456')
        cls.driver.execute_script("arguments[0].click();",
                                  cls.driver.find_elements_by_xpath('//input[@type="radio"]')[0])

        cls.driver.find_element_by_xpath('//button').click()
        time.sleep(0.8)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    def tearDown(self) -> None:
        time.sleep(5)

    @data(*password_infos)
    def test_admin_1password(self, password_info):
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
    def test_admin_2personal_info(self, personal_info):
        self.driver.get("http://localhost:8080/springboot16r3y/admin/dist/index.html")
        time.sleep(0.6)

        self.driver.find_element(By.CSS_SELECTOR, ".el-menu-item:nth-child(2)").click()
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").send_keys(personal_info[1])
        self.driver.find_element(By.CSS_SELECTOR, ".el-button > span").click()

        while True:
            time.sleep(0.05)
            if r'修改信息成功' in self.driver.page_source:
                self.assertTrue(r'修改信息成功' in self.driver.page_source)
                break
            time.sleep(0.1)
        time.sleep(0.5)

    @data(*users_infos)
    def test_admin_3user(self, users_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(3) > .el-submenu__title").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item").click()
        time.sleep(0.2)

        if '新增' in users_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-button--success").click()
            time.sleep(0.2)

            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").send_keys(users_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").send_keys(users_info[2])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").send_keys(users_info[3])
            if users_info[4] == '√':
                self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\yonghu_touxiang1.jpg")
            self.driver.find_element(By.CSS_SELECTOR, ".el-select .el-input__inner").click()
            if users_info[5] == '男':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]'))
            elif users_info[5] == '女':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[2]'))

            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").send_keys(users_info[6])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").send_keys(users_info[7])
            self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

        elif '删除' in users_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-delete").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2)").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)
        elif '查询' in users_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item__content .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item__content .el-input__inner").send_keys(
                users_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(1)

        elif '查看' in users_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-tickets").click()
            time.sleep(1)
            self.assertTrue(r'详情' not in self.driver.page_source)
        else:
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item__content .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item__content .el-input__inner").send_keys(
                users_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-child(1) .el-icon-edit").click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").send_keys(users_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").send_keys(users_info[2])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").send_keys(users_info[3])
            if users_info[4] == '√':
                self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\yonghu_touxiang1.jpg")
            self.driver.find_element(By.CSS_SELECTOR, ".el-select .el-input__inner").click()
            if users_info[5] == '男':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]'))
            elif users_info[5] == '女':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[2]'))

            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").send_keys(users_info[6])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").send_keys(users_info[7])
            self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

    @data(*sellers_infos)
    def test_admin_4seller(self, sellers_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(4) > .el-submenu__title").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item").click()
        time.sleep(0.2)

        if '新增' in sellers_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-button--success").click()
            time.sleep(0.2)

            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").send_keys(
                sellers_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").send_keys(
                sellers_info[2])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").send_keys(
                sellers_info[3])
            if sellers_info[4] == '√':
                self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\yonghu_touxiang1.jpg")
            self.driver.find_element(By.CSS_SELECTOR, ".el-select .el-input__inner").click()
            if sellers_info[5] == '男':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]'))
            elif sellers_info[5] == '女':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[2]'))

            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").send_keys(
                sellers_info[6])

            self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

        elif '删除' in sellers_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-delete").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2)").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)
        elif '查询' in sellers_info[0]:
            if sellers_info[1] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").send_keys(
                    sellers_info[1])
            if sellers_info[3] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").send_keys(
                    sellers_info[3])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(1)

        elif '查看' in sellers_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-tickets").click()
            time.sleep(1)
            self.assertTrue(r'详情' not in self.driver.page_source)
        else:
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item__content .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item__content .el-input__inner").send_keys(
                sellers_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-child(1) .el-icon-edit").click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").send_keys(
                sellers_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").send_keys(
                sellers_info[2])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").send_keys(
                sellers_info[3])
            if sellers_info[4] == '√':
                self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\yonghu_touxiang1.jpg")
            self.driver.find_element(By.CSS_SELECTOR, ".el-select .el-input__inner").click()
            if sellers_info[5] == '男':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]'))
            elif sellers_info[5] == '女':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[2]'))

            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").send_keys(
                sellers_info[6])
            self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

    @data(*e_bike_infos)
    def test_admin_5e_bike(self, e_bike_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(5) > .el-submenu__title").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item").click()
        time.sleep(0.2)

        if '修改' in e_bike_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item__content .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item__content .el-input__inner").send_keys(
                e_bike_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-child(1) .el-icon-edit").click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, ".is-required .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".is-required .el-input__inner").send_keys(e_bike_info[1])
            if e_bike_info[2] == '√':
                self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\1617071916390.jpg")
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").send_keys(e_bike_info[3])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(4) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(4) .el-input__inner").send_keys(e_bike_info[4])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(5) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(5) .el-input__inner").send_keys(e_bike_info[5])
            self.driver.find_element(By.CSS_SELECTOR, ".el-select .el-input__inner").click()
            time.sleep(0.4)
            if e_bike_info[6] != '':
                if e_bike_info[6] == '九成新':
                    self.driver.execute_script("arguments[0].click();",
                                               self.driver.find_element(By.XPATH,
                                                                        '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]'))
                elif e_bike_info[6] == '八成新':
                    self.driver.execute_script("arguments[0].click();",
                                               self.driver.find_element(By.XPATH,
                                                                        '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[2]'))
                elif e_bike_info[6] == '七成新':
                    self.driver.execute_script("arguments[0].click();",
                                               self.driver.find_element(By.XPATH,
                                                                        '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[3]'))
                else:
                    self.driver.execute_script("arguments[0].click();",
                                               self.driver.find_element(By.XPATH,
                                                                        '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[4]'))
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").send_keys(e_bike_info[7])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(8) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(8) .el-input__inner").send_keys(e_bike_info[8])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(9) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(9) .el-input__inner").send_keys(e_bike_info[9])
            if e_bike_info[10] is not pd.NaT:
                self.driver.find_element(By.CSS_SELECTOR, ".el-date-editor > .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-date-editor > .el-input__inner").send_keys(
                    e_bike_info[10].strftime('%Y 年 %m 月 %d 日'))
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(11) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(11) .el-input__inner").send_keys(
                e_bike_info[11])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(12) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(12) .el-input__inner").send_keys(
                e_bike_info[12])
            self.driver.find_element(By.CSS_SELECTOR, ".ql-editor").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".ql-editor").send_keys(e_bike_info[13])
            self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()

            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)
        elif '查询' in e_bike_info[0]:
            if e_bike_info[1] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").send_keys(
                    e_bike_info[1])
            if e_bike_info[3] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").send_keys(
                    e_bike_info[3])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(1)
        else:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-delete").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2)").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

    @data(*buy_infos)
    def test_admin_6buy(self, buy_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(6) > .el-submenu__title").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item").click()
        time.sleep(0.2)
        if '查看' in buy_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-tickets").click()
            time.sleep(1)
            self.assertTrue(r'详情' not in self.driver.page_source)
        elif '删除' in buy_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-delete").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2)").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)
        else:
            if buy_info[1] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").send_keys(
                    buy_info[1])
            if buy_info[2] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").send_keys(
                    buy_info[2])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(1)

    @data(*evaluate_infos)
    def test_admin_7evaluate(self, evaluate_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(7) > .el-submenu__title").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item").click()
        time.sleep(0.2)

        if '修改' in evaluate_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-edit").click()
            time.sleep(0.5)

            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(1) .el-input__inner").send_keys(
                evaluate_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(2) .el-input__inner").send_keys(
                evaluate_info[2])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(3) .el-input__inner").send_keys(
                evaluate_info[3].strftime('%Y-%m-%d'))
            self.driver.find_element(By.CSS_SELECTOR, ".el-select .el-input__inner").click()
            if evaluate_info[4] == '1':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]'))
            elif evaluate_info[4] == '2':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[2]'))
            elif evaluate_info[4] == '3':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[3]'))
            elif evaluate_info[4] == '4':
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[4]'))
            else:
                self.driver.execute_script("arguments[0].click();",
                                           self.driver.find_element(By.XPATH,
                                                                    '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[5]'))
            self.driver.find_element(By.CSS_SELECTOR, ".el-date-editor > .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-date-editor > .el-input__inner").send_keys(
                evaluate_info[5].strftime('%Y 年 %m 月 %d 日'))
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(6) .el-input__inner").send_keys(
                evaluate_info[6])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(8) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(8) .el-input__inner").send_keys(
                evaluate_info[7])
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-col:nth-child(7) .el-input__inner").send_keys(
                evaluate_info[8])
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").send_keys(evaluate_info[9])
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element(By.CSS_SELECTOR, ".btn-success"))

            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

        elif '删除' in evaluate_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-delete").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2)").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)
        elif '查看' in evaluate_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-tickets").click()
            time.sleep(1)
            self.assertTrue(r'详情' not in self.driver.page_source)
        else:
            if evaluate_info[1] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").send_keys(
                    evaluate_info[1])
            if evaluate_info[2] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").send_keys(
                    evaluate_info[2])
            if evaluate_info[7] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(3) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(3) .el-input__inner").send_keys(
                    evaluate_info[7])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(1)

    @data(*comments)
    def test_admin_8evaluate(self, comment):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(8) > .el-submenu__title").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item").click()
        time.sleep(0.2)

        if '查看' in comment[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-tickets").click()
            time.sleep(1)
            self.assertTrue(r'详情' not in self.driver.page_source)
        elif '回复' in comment[0]:
            self.driver.find_element(By.CSS_SELECTOR,
                                     ".el-table__row:nth-last-child(1) .el-button:nth-child(3) > span").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-row:nth-child(3) .el-textarea__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-row:nth-child(3) .el-textarea__inner").send_keys(comment[1])
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element(By.CSS_SELECTOR, ".btn-success"))
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)
        elif '修改' in comment[0]:
            self.driver.find_element(By.CSS_SELECTOR,
                                     ".el-table__row:nth-last-child(1) .el-button:nth-child(2) > span").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-row:nth-child(3) .el-textarea__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-row:nth-child(3) .el-textarea__inner").send_keys(comment[1])
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element(By.CSS_SELECTOR, ".btn-success"))
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

        elif '删除' in comment[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-delete").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2)").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

        else:
            if comment[2] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").send_keys(
                    comment[2])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(1)

    @data(*notice_infos)
    def test_admin_9notice(self, notice_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(9) > .el-submenu__title").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item:nth-child(1)").click()
        time.sleep(0.2)

        if '新增' in notice_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-button--success").click()
            time.sleep(0.2)
            self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").send_keys(notice_info[1])
            if notice_info[2] == '√':
                self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\yonghu_touxiang1.jpg")
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").send_keys(notice_info[3])
            self.driver.find_element(By.CSS_SELECTOR, ".ql-editor").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".ql-editor").send_keys(notice_info[4])

            self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

        elif '修改' in notice_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-edit").click()
            time.sleep(0.2)
            self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").send_keys(notice_info[1])
            if notice_info[2] == '√':
                self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\yonghu_touxiang1.jpg")
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner").send_keys(notice_info[3])
            self.driver.find_element(By.CSS_SELECTOR, ".ql-editor").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".ql-editor").send_keys(notice_info[4])

            self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)
        elif '查看' in notice_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-tickets").click()
            time.sleep(1)
            self.assertTrue(r'详情' not in self.driver.page_source)
        else:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-delete").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2)").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

    @data(*slideshow_infos)
    def test_admin_9slideshow(self, slideshow_info):
        self.driver.get('http://localhost:8080/springboot16r3y/admin/dist/index.html')
        time.sleep(0.5)

        self.driver.find_element(By.CSS_SELECTOR, ".el-submenu:nth-child(9) > .el-submenu__title").click()
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, ".is-opened .el-menu-item:nth-child(2)").click()
        time.sleep(0.2)

        if '新增' in slideshow_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-button--success").click()
            time.sleep(0.2)
            self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").send_keys(slideshow_info[1])
            if slideshow_info[2] == '√':
                self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\yonghu_touxiang1.jpg")

            self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)
        elif '查看' in slideshow_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-tickets").click()
            time.sleep(1)
            self.assertTrue(r'详情' not in self.driver.page_source)
        elif '修改' in slideshow_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-edit").click()
            time.sleep(0.2)
            self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").send_keys(slideshow_info[1])
            time.sleep(0.5)
            if r'el-icon-delete' in self.driver.page_source:
                hover = ActionChains(self.driver).move_to_element(
                    self.driver.find_element(By.CSS_SELECTOR, ".el-upload-list__item-actions"))
                hover.perform()
                self.driver.find_element(By.CSS_SELECTOR, ".el-icon-delete").click()
                time.sleep(1)
            if slideshow_info[2] == '√':
                self.driver.find_element(By.NAME, "file").send_keys(r"C:\Users\15447\Desktop\yonghu_touxiang1.jpg")

            self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)

        elif '删除' in slideshow_info[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".el-table__row:nth-last-child(1) .el-icon-delete").click()
            time.sleep(0.5)
            self.driver.find_element(By.CSS_SELECTOR, ".el-button--default:nth-child(2)").click()
            while True:
                time.sleep(0.05)
                if r'操作成功' in self.driver.page_source:
                    self.assertTrue(r'操作成功' in self.driver.page_source)
                    break
                time.sleep(0.1)
            time.sleep(0.5)
        else:
            if slideshow_info[1] != '':
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").clear()
                self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(1) .el-input__inner").send_keys(
                    slideshow_info[1])
            self.driver.find_element(By.CSS_SELECTOR, ".el-icon-search").click()
            time.sleep(1)
