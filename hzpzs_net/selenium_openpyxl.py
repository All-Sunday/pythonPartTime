# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/3/1 16:19
# @File : selenium_openpyxl.py

import datetime
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
import openpyxl


def init(start_url, domain, res_path, chromedriver_path, chrome_port):
    # 启动谷歌浏览器
    options = Options()
    options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    options.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
    # options.add_argument('--headless')                  # 开启无头模式（无界面启动）

    options.add_experimental_option("debuggerAddress", "127.0.0.1:" + chrome_port)
    driver = webdriver.Chrome(chromedriver_path, options=options)
    # driver.execute_script('window.open("' + start_url + '")')
    # driver.switch_to.window(driver.window_handles[-1])
    # time.sleep(0.5)
    # driver.switch_to.window(driver.window_handles[0])
    # driver.get(start_url)

    if not os.path.exists(res_path):
        res_wk = openpyxl.Workbook()
        res_sheet = res_wk.active
        res_sheet.append(
            ['id', '经销代理的化妆品名化妆品', '代理/经销区域', '销售渠道', '发布日期', '单位名称', '身份', '联系人', '联系地址', '联系手机', '联系QQ', '电子邮件'])
        res_wk.save(res_path)

    res_wk = openpyxl.load_workbook(res_path)
    res_sheet = res_wk.active
    return driver, res_wk, res_sheet


def get_res(start_url, s_date, e_date, res_path, res_wk, res_sheet, domain, driver, handles):
    i = 0
    print('sssssss')

    for i in range(300):
        time.sleep(0.5)
        land_trs_list = driver.find_elements_by_xpath(
            '//div[@class="el-dialog__body"]//table[@class="el-table__body"][1]/tbody/tr')
        driver.execute_script("arguments[0].click();", land_trs_list[i + 1].find_element_by_xpath('./td[1]/div/p/span'))
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)

        sidebar_items = driver.find_elements_by_xpath('//div[@class="sidebar_content"]/ul/li')
        sign = False
        for sidebar_item in sidebar_items:
            if sidebar_item.text.strip() == '交易':
                driver.execute_script("arguments[0].click();", sidebar_item)
                sign = True
                time.sleep(0.5)
        if not sign:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)
            continue
        trs_list = driver.find_elements_by_xpath('//table[@class="el-table__body"][1]/tbody/tr')
        res = []
        for tr in trs_list:
            # mon = tr.find_element_by_xpath('./td[1]//span[@class="can_clicks"]').text.strip()
            # mon = tr.find_element_by_xpath('./td[1]/div/span/div/span').text.strip()
            area = tr.find_element_by_xpath('./td[4]/div/div').text.strip()
            price = tr.find_element_by_xpath('./td[6]/div/div').text.strip()
            # print(mon, area, price)
            # print(mon)
            res.append([area, price])
            time.sleep(0.2)
        print(res)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
    # pinpai = list(df['品牌'])
    #
    # for key_word in key_words[:amount]:
    #     i += 1
    #     # driver.find_element_by_xpath('//input[@id="key"]').clear()
    #     # driver.find_element_by_xpath('//input[@id="key"]').send_keys(key_word + '\n')
    #     target_url = 'https://www.ic.net.cn/search/' + key_word + '.html?isExact=1'
    #     driver.get(target_url)
    #     time.sleep(0.5)
    #     if target_url != driver.current_url:
    #         driver.get(target_url)
    #         time.sleep(0.5)
    #     # li_list = driver.find_elements_by_xpath('//ul[@id="resultList"]/li')[5:]
    #     li_list = driver.find_elements_by_xpath('//ul[@id="resultList"]/li[@class="stair_tr"]')
    #
    #     li_list += driver.find_elements_by_xpath('//ul[@id="resultList"]/li[@class="stair_tr gray_bg"]')
    #     num = len(li_list)
    #     # search_num = int(driver.find_element_by_xpath('//span[@id="icCount"]').text)
    #     # if search_num > 49:  # 一页最多49
    #     #     search_num = 49
    #     search_title = driver.find_element_by_xpath('//*[@id="search_Name"]').text.strip()
    #     # if (num != (search_num + 1)) or (key_word != search_title):
    #     if key_word != search_title:
    #         # print(num, search_num, key_word, search_title)
    #         print(num, key_word, search_title)
    #         data = [pinpai[i - 1], i, key_word, '', '', '']
    #         print(pinpai[i - 1], i, key_word,)
    #         res_sheet.append(data)
    #         res_wk.save(res_path)
    #         continue
    #
    #     amount_xianhuo = 0
    #     amount_youxian = 0
    #     amount_remai = 0
    #     for li in li_list:
    #         a_list = li.find_elements_by_xpath('./div[@class="result_id"]/a')
    #         # print('sss')
    #         if len(a_list) == 0:
    #             span_list = li.find_elements_by_xpath('./div[@class="result_id"]/span')
    #             if len(span_list) == 3:
    #                 # print(span_list[1].get_attribute('title'))
    #                 if span_list[1].get_attribute('title') == '优先库存':
    #                     amount_youxian += int(li.find_element_by_xpath('./div[@class="result_totalNumber"]').text.strip())
    #                 elif span_list[1].get_attribute('title') == '热门现货':
    #                     amount_remai += int(li.find_element_by_xpath('./div[@class="result_totalNumber"]').text.strip())
    #         elif len(a_list) == 1:
    #             if li.find_element_by_xpath('./div[@class="result_id"]/a/span').get_attribute('title') == '现货排名':
    #                 amount_xianhuo += int(li.find_element_by_xpath('./div[@class="result_totalNumber"]').text.strip())
    #     data = [pinpai[i - 1], i, key_word, amount_xianhuo, amount_youxian, amount_remai]
    #     # print(data)
    #     if (i % 100) == 0:
    #         print(i)
    #     if (i % 10) == 0:
    #         driver.find_element_by_xpath('//a[@id="LOGO"]').click()
    #         time.sleep(0.6)
    #     res_sheet.append(data)
    #     res_wk.save(res_path)
    #
    #     time.sleep(0.2)

    # time.sleep(100)
    return


def start(s_date, e_date, res_path, domain, chromedriver_path, chrome_port):
    start_time = datetime.datetime.now()
    print(start_time, 'Begin-----------------------')

    start_url = domain
    driver, res_wk, res_sheet = init(start_url, domain, res_path, chromedriver_path, chrome_port)
    driver.implicitly_wait(0.3)
    handles = driver.window_handles

    get_res(start_url, s_date, e_date, res_path, res_wk, res_sheet, domain, driver, handles)

    end_time = datetime.datetime.now()
    print(end_time, 'Finish-----------------------共耗时', end_time - start_time)


if __name__ == '__main__':
    file_path = r'E:\code_workplace\python\2022\january\data\hzpzs_net\res.xlsx'
    # df = pd.read_excel(file_path).iloc[19609:19800]
    # df = df[['品牌', '型号']]
    # print(type(df['型号'].values))   # <class 'numpy.ndarray'>
    # time.sleep(100)

    # key_words = ['TPS63001DRCR']
    # key_words = df['型号'].values
    # print(key_words)
    # time.sleep(100)

    # amount = len(key_words)

    domain = ['https://www.hzpzs.net/hzpdl_2/']

    s_date = '20190101'
    e_date = '20210909'

    chromedriver_path = r'E:\code_workplace\python\chromedriver.exe'
    chrome_port = '9221'

    i = 0
    start(s_date, e_date, file_path, domain[i], chromedriver_path, chrome_port)
