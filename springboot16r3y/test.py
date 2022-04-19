# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/5 11:33
# @File : test.py


import datetime
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import os
import openpyxl


def init(start_url, domain, res_path, chromedriver_path, chrome_port):
    # 启动谷歌浏览器
    options = Options()
    options.add_argument('--no-sandbox')                # 解决DevToolsActivePort文件不存在的报错
    options.add_argument('window-size=1920x3000')       # 设置浏览器分辨率
    options.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')           # 隐藏滚动条，应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')      # 不加载图片，提升运行速度
    # options.add_argument('--headless')                  # 开启无头模式（无界面启动）

    # options.add_experimental_option("debuggerAddress", "127.0.0.1:" + chrome_port)
    driver = webdriver.Chrome(chromedriver_path, options=options)
    # driver.execute_script('window.open("' + start_url + '")')
    # driver.switch_to.window(driver.window_handles[-1])
    # time.sleep(0.5)
    # driver.switch_to.window(driver.window_handles[0])
    driver.get(start_url)

    # if not os.path.exists(res_path):
    #     res_wk = openpyxl.Workbook()
    #     res_sheet = res_wk.active
    #     res_sheet.append(['品牌', 'i', '型号', '现货排名', '优先', '热卖'])
    #     res_wk.save(res_path)
    #
    # res_wk = openpyxl.load_workbook(res_path)
    # res_sheet = res_wk.active
    # return driver, res_wk, res_sheet
    return driver, None, None


def get_res(start_url, s_date, e_date, df, key_words, res_path, res_wk, res_sheet, amount, domain, driver, handles):
    i = 0
    time.sleep(20)
    driver.refresh()
    time.sleep(0.5)
    driver.find_element_by_xpath('//div[@class="navs"]/div/ul/li[4]/a').click()
    driver.switch_to.frame('iframe')
    for key_word in key_words:
        i += 1
        driver.find_element_by_xpath('//textarea[@class="layui-textarea"]').clear()
        driver.find_element_by_xpath('//textarea[@class="layui-textarea"]').send_keys(key_word)

        time.sleep(0.2)
        driver.find_element_by_xpath('//button[@class="layui-btn btn-submit"]').click()
        # li_list = driver.find_elements_by_xpath('//ul[@id="resultList"]/li')[5:]
        # print(len(li_list))

        # amount_xianhuo = 0
        # amount_youxian = 0
        # amount_remai = 0
        # for li in li_list:
        #     a_list = li.find_elements_by_xpath('./div[@class="result_id"]/a')
        #     # print('sss')
        #     if len(a_list) == 0:
        #         span_list = li.find_elements_by_xpath('./div[@class="result_id"]/span')
        #         if len(span_list) == 3:
        #             # print(span_list[1].get_attribute('title'))
        #             if span_list[1].get_attribute('title') == '优先库存':
        #                 amount_youxian += int(li.find_element_by_xpath('./div[@class="result_totalNumber"]').text)
        #             elif span_list[1].get_attribute('title') == '热门现货':
        #                 amount_remai += int(li.find_element_by_xpath('./div[@class="result_totalNumber"]').text)
        #     elif len(a_list) == 1:
        #         if li.find_element_by_xpath('./div[@class="result_id"]/a/span').get_attribute('title') == '现货排名':
        #             amount_xianhuo += int(li.find_element_by_xpath('./div[@class="result_totalNumber"]').text)
        # data = [df['品牌'][i - 1], i, key_word, amount_xianhuo, amount_youxian, amount_remai]
        # print(data)
        # res_sheet.append(data)
        # res_wk.save(res_path)

        time.sleep(0.3)
    time.sleep(100)
    return

def start(s_date, e_date, df, key_words, res_path, amount, domain, chromedriver_path, chrome_port):
    start_time = datetime.datetime.now()
    print(start_time, 'Begin-----------------------')

    start_url = domain
    driver, res_wk, res_sheet = init(start_url, domain, res_path, chromedriver_path, chrome_port)
    driver.implicitly_wait(0.3)
    handles = driver.window_handles

    get_res(start_url, s_date, e_date, df, key_words, res_path, res_wk, res_sheet, amount, domain, driver, handles)

    end_time = datetime.datetime.now()
    print(end_time, 'Finish-----------------------共耗时', end_time - start_time)

if __name__ == '__main__':
    file_path = r'E:\code_workplace\python\2022\january\data\springboot16r3y\用户测试用例.xlsx'
    excel_reader = pd.ExcelFile(file_path)
    sheet_names = excel_reader.sheet_names
    df = excel_reader.parse(sheet_name=sheet_names[3])
    # print(df)
    # print(df[df['expected'] == '留言成功'])
    # time.sleep(16)
    df = df[df['expected'] == '留言成功']
    # print(type(df['型号'].values))   # <class 'numpy.ndarray'>
    # time.sleep(100)

    # key_words = ['TPS63001DRCR']
    key_words = df['content'].values
    # print(key_words)
    # time.sleep(100)

    amount = 1000

    domain = ['http://localhost:8080/springboot16r3y/front/index.html']

    s_date = '20190101'
    e_date = '20210909'

    chromedriver_path = r'E:\code_workplace\python\chromedriver.exe'
    chrome_port = '9221'

    i = 0
    start(s_date, e_date, df, key_words, file_path[:-5] + 'res' + str(amount) + '.xlsx', amount, domain[i], chromedriver_path, chrome_port)

