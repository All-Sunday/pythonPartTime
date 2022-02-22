# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/1/17 20:19
# @File : selenium_pandas.py

import datetime
import random
import time

import requests
import schedule
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from pyDes import *
import base64


def init(start_url, domain, chromedriver_path, chrome_port):
    # 启动谷歌浏览器
    options = Options()
    options.add_argument('--no-sandbox')                # 解决DevToolsActivePort文件不存在的报错
    options.add_argument('window-size=1920x3000')       # 设置浏览器分辨率
    options.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')           # 隐藏滚动条，应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')      # 不加载图片，提升运行速度
    # options.add_argument('--headless')                  # 开启无头模式（无界面启动）

    options.add_experimental_option("debuggerAddress", "127.0.0.1:" + chrome_port)
    driver = webdriver.Chrome(chromedriver_path, options=options)
    # driver.execute_script('window.open("' + start_url + '")')
    # driver.switch_to.window(driver.window_handles[-1])
    # time.sleep(0.5)
    # driver.switch_to.window(driver.window_handles[0])
    driver.get(start_url)
    driver.implicitly_wait(1)
    return driver



def get_res(pic_wait, start_url, s_date, e_date, df, key_words, res_path, a_list_num, domain, driver, handles):
    # min_sign2 = df['sign2'].min()
    # min_modified = df['modified'].min()
    # print('min_sign2:', min_sign2, 'min_modified:', min_modified)
    l = len(df[(df.sign2 == df.modified) & (df.sign2 == 0)])    # df 同一行两列值相等 且为特定值
    # print(l, l > 0)
    print(l)
    # time.sleep(100)
    # for n in range(max_times):
    # while (min_sign2 == 0) and (min_modified == 0):  # 有未被修改的
    while l > 0:  # 有未被修改的   同一行！！！
        i = 0
        res = []

        # for key_word in key_words[:2]:
        # for i in range(len(key_words)):
        # while i < 5:
        for i in df.itertuples():    # df遍历 df修改数据
            try:
                # i += 1
                index, name, price, sign, floating, price1, price2, sign2, modified = getattr(i, 'Index'), getattr(i, 'name'), getattr(i, 'price'), getattr(i, 'sign'), getattr(i, 'floating'), getattr(i, 'price1'), getattr(i, 'price2'), getattr(i, 'sign2'), getattr(i, 'modified')
                # print(index, name, amount, index)
                # print(index > index)
                # if index == 3:
                #     df.loc[index, 'added'] = 1
                #     print(df.loc[index])
                # continue

                if (modified == 1) or (sign2 != 0):
                    continue
                if sign not in ('-', '+', '+-', '-+'):
                    print('sign标记错误！！')
                    df.loc[index, 'sign2'] = 3
                    df.to_excel(res_path, index=False)
                    continue
                driver.get('https://gameflip.com/zh/listings/onsale')
                time.sleep(4)
                # print(key_words[i])
                print(name)
                driver.find_element_by_xpath('//form[@class="form-inline"]/div/input').clear()   # 搜索框
                driver.find_element_by_xpath('//form[@class="form-inline"]/div/input').send_keys(name + '\n')
                time.sleep(1.5)
                wait_times = 0
                # while driver.find_element_by_xpath('//div[@class="spinner"]').get_attribute('style') != 'display: none;':
                while driver.find_element_by_xpath('//footer/div[last()]').get_attribute('style') != 'display: none;':   # 搜索后页面出现蒙版 需等待
                    # while r'display: none;' not in driver.page_source:
                    wait_times += 1
                    if wait_times > 6:
                        driver.refresh()
                    time.sleep(0.6)

                div_list = driver.find_elements_by_xpath('//div[@class="item-list"]/div')[1:-2]
                # print(len(div_list))
                # if len(div_list) == 1:  # 只有一个商品 或 无商品 都是一个div
                if r'item-detail' not in driver.page_source:  # 无商品
                    print('没有该商品:', name)
                    df.loc[index, 'sign2'] = 2
                    time.sleep(0.8)
                    df.to_excel(res_path, index=False)
                    continue

                exist = False   # 是否有该商品
                # while (r'页' not in driver.page_source) or (r'</a>' in driver.find_element_by_xpath('//ul[@class="pager"]/li[2]').get_attribute('innerHTML')):  # 只有当前一页 或有下一页  获取元素源码
                while True:  # 只有当前一页 或有下一页 或是最后一页  获取元素源码
                    selected_num = 0
                    div_list = driver.find_elements_by_xpath('//div[@class="item-list"]/div')[1:-2]
                    for div in div_list:
                        # print(selected_num)
                        search_name = div.find_element_by_xpath('./div[3]/div/div/h4[@class="name"]/a').text.strip()
                        if name == search_name:
                            # print(div.find_element_by_xpath('./div[1]').get_attribute('innerHTML'))
                            # div.find_element_by_xpath('./div[1]/input').click()   # 选中
                            div.find_element_by_xpath('./div[1]/input').send_keys(Keys.SPACE)   # selenium 选中checkbox
                            time.sleep(0.3)
                            selected_num += 1
                            exist = True
                    time.sleep(2)
                    if selected_num > 0:  # 选中数量大于0
                        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//div[@class="d-none d-md-inline-block col-md-4 buttons"]/button[1]'))   # 更改价格
                        time.sleep(2)
                        # print(driver.find_element_by_xpath('//input[@value="new_price"]').get_attribute('outerHTML'))
                        # driver.find_element_by_xpath('//input[@value="new_price"]').click()
                        driver.find_element_by_xpath('//input[@value="new_price"]').send_keys(Keys.SPACE)   # selenium 选中radio
                        time.sleep(0.5)
                        if sign == '-':
                            top_price = price
                            low_price = price2
                        elif sign == '+':
                            top_price = price1
                            low_price = price
                        else:
                            top_price = price1
                            low_price = price2
                        new_price = format(round(random.uniform(low_price, top_price), 2), '0.2f')  # random 小数随机数 format 保留两位小数->str
                        driver.find_element_by_xpath('//input[@placeholder="New Price"]').send_keys(new_price)
                        time.sleep(0.6)
                        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//div[@class="row text-left buttons"]/button[1]'))   # apply all
                        time.sleep(1)

                        wait_times = 0
                        while driver.find_element_by_xpath('//div[@id="listings-bulk-change-price-dialog"]').get_attribute('style') != 'display: none;':     # 等待修改进度条完成
                            wait_times += 1
                            time.sleep(1)
                    time.sleep(2.5)

                    wait_times = 0
                    # while driver.find_element_by_xpath('//div[@class="spinner"]').get_attribute('style') != 'display: none;':
                    while driver.find_element_by_xpath('//footer/div[last()]').get_attribute('style') != 'display: none;':   # 页面出现蒙版 需等待
                        # while r'display: none;' not in driver.page_source:
                        wait_times += 1
                        if wait_times > 6:
                            driver.refresh()
                        time.sleep(0.6)

                    if r'页' in driver.page_source:
                        if r'</a>' in driver.find_element_by_xpath('//ul[@class="pager"]/li[2]').get_attribute('innerHTML'):   # 下一页可点
                            # driver.find_element_by_xpath('//ul[@class="pager"]/li[2]/a').click()  # 下一页
                            driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//ul[@class="pager"]/li[2]/a'))  # 下一页
                            time.sleep(2)
                            print('下一页')
                        else:
                            break
                    else:
                        break

                if not exist:
                    print('所有页都没有该商品:', name)
                    df.loc[index, 'sign2'] = 1
                    time.sleep(0.8)
                    df.to_excel(res_path, index=False)
                    continue

                time.sleep(2)

                # time.sleep(100)
                # i += 1
                df.loc[index, 'modified'] = 1
                df.to_excel(res_path, index=False)
            except:
                continue

        # min_sign2 = df['sign2'].min()
        # min_modified = df['modified'].min()
        # print('min_sign2:', min_sign2, 'min_modified:', min_modified)
        l = len(df[(df.sign2 == df.modified) & (df.sign2 == 0)])
        print(l)

    df.to_excel(res_path, index=False)

    return

def start(pic_wait, s_date, e_date, df, key_words, res_path, a_list_num, domain, chromedriver_path, chrome_port):
    start_time = datetime.datetime.now()
    print(start_time, 'Begin-----------------------')

    start_url = domain
    driver = init(start_url, domain, chromedriver_path, chrome_port)
    driver.implicitly_wait(0.3)
    handles = driver.window_handles

    if_allowed = license(driver)
    if if_allowed:
        get_res(pic_wait, start_url, s_date, e_date, df, key_words, res_path, a_list_num, domain, driver, handles)

    end_time = datetime.datetime.now()
    print(end_time, 'Finish-----------------------共耗时', end_time - start_time)
    time.sleep(10)

def license_code(user_code):
    des_Key = "MRSUNDAY" # Key
    des_IV = "\x15\1\x2a\3\1\x23\2\0" # 自定IV向量

    user_code_added = ''
    for i in range(len(user_code)):
        user_code_added += user_code[i]
        user_code_added += str(i)

    selectindex=[0, 1, 3, 5, 4, 7]
    lincese_str = ''
    if user_code_added[0] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:     # 第一个代码是数字  ###  中间增加 自定义字符 增加安全性
        index1, index2, m, n = 0, 4, 'B', 'N'
    else:
        index1, index2, m, n = 1, 5, '7', 'C'
    for i in selectindex:    #  选取 字符串部分字符
        if i == index1:                            ###  中间增加 自定义字符
            lincese_str += m
        lincese_str = lincese_str + user_code_added[i]
        if i == index2:                            ###  中间增加 自定义字符
            lincese_str += n

    k = des(des_Key, CBC, des_IV, pad=None, padmode=PAD_PKCS5)
    EncryptStr = k.encrypt(lincese_str)
    return base64.b64encode(EncryptStr) #转base64编码返回

def license(driver):
    time.sleep(5)
    # driver.find_element_by_xpath('//li[@id="megamenu_7"]/ul/li/div/div/ul/li/a').click()
    user_url = driver.find_element_by_xpath('//li[@id="megamenu_7"]/ul/li/div/div/ul/li/a').get_attribute('href')
    # print(user_url)
    driver.get(user_url)
    time.sleep(5)

    try:
        user_code = driver.find_element_by_xpath('//div[@class="col-12 col-md-3 profile-left"]/div[3]/h3/span').text.strip()
    except:
        driver.get(user_url)
        time.sleep(5)
        user_code = driver.find_element_by_xpath('//div[@class="col-12 col-md-3 profile-left"]/div[3]/h3/span').text.strip()
    # user_code = 'WB9ZNT'
    # print(user_code)
    key = license_code(user_code)
    # print(key)
    allowed_code = requests.get('http://ss.zzuspc.top/1.txt').text.split('\n')
    for i in range(len(allowed_code)):
        allowed_code[i] = bytes(allowed_code[i], encoding='utf-8')
    # print(allowed_code)

    if key not in allowed_code:
        print('当前账号未注册！')
        time.sleep(100)
        return False
    return True



def main1(file_path, chrome_port):
    # file_path = r'E:\code_workplace\python\2022\january\data\gameflip_com\price.xlsx'
    # file_path = input('price.xlsx路径：').strip()
    # pic_wait = int(input('等待图片延迟时间'))
    pic_wait = 2
    df = pd.read_excel(file_path)   # pandas 读取excel
    # df = df[['name', 'amount']]     # df取部分列
    # df['added'] = 0  # 已复制个数
    df['price1'] = df.apply(lambda x: round(x['price'] * (1 + x['floating']), 2), axis=1)   # df 根据两列值 生成一列值
    df['price2'] = df.apply(lambda x: round(x['price'] * (1 - x['floating']), 2), axis=1)
    df['sign2'] = 0  # 1: 搜索后的页面没有该商品  2：搜索后没有一个商品 3：sign标记错误 0：正常
    df['modified'] = 0  # 1: 改价成功 0：未成功
    # print(df)

    key_words = df['name'].values
    # print(key_words)
    # time.sleep(100)

    domain = ['https://gameflip.com/zh/listings/onsale']  # 特价销售页面

    s_date = '20190101'
    e_date = '20210909'

    # chromedriver_path = r'E:\code_workplace\python\chromedriver.exe'
    chromedriver_path = r'chromedriver.exe'
    # chrome_port = '9222'
    # chrome_port = input('谷歌端口号：').strip()

    i = 0
    a_list_num = 0
    start_time = datetime.datetime.now()
    start(pic_wait, s_date, e_date, df.copy(), key_words, file_path[:-5] + start_time.strftime('%Y%m%d %H-%M-%S') + 'res.xlsx', a_list_num, domain[i], chromedriver_path, chrome_port)
# if __name__ == '__main__':
def main():
    file_path = input('price.xlsx路径：').strip()
    schedule_time = int(input('每轮时间间隔（分钟）：').strip())
    chrome_port = input('谷歌端口号：').strip()

    main1(file_path, chrome_port)
    # schedule.every(2).minutes.do(main1, file_path)
    schedule.every(schedule_time).minutes.do(main1, file_path, chrome_port)   # schedule 定时任务 schedule 传参
    while True:
        schedule.run_pending()
        time.sleep(1)
