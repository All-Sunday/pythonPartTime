# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/1/17 20:19
# @File : selenium_pandas.py

import datetime
import time

import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.select import Select
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
    max_times = (df[df['sign'] == 0]['amount'] - df[df['sign'] == 0]['added']).max()
    print('max_times:', max_times)
    # time.sleep(100)
    # for n in range(max_times):
    while max_times > 0:
        i = 0
        res = []

        # for key_word in key_words[:2]:
        # for i in range(len(key_words)):
        # while i < 5:
        for i in df.itertuples():    # df遍历 df修改数据
            try:
                # i += 1
                index, name, amount, added, sign = getattr(i, 'Index'), getattr(i, 'name'), getattr(i, 'amount'), getattr(i, 'added'), getattr(i, 'sign')
                # print(index, name, amount, index)
                # print(index > index)
                # if index == 3:
                #     df.loc[index, 'added'] = 1
                #     print(df.loc[index])
                # continue
                if sign != 0:
                    continue
                if amount <= added:
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
                while driver.find_element_by_xpath('//footer/div[last()]').get_attribute('style') != 'display: none;':
                # while r'display: none;' not in driver.page_source:
                    wait_times += 1
                    if wait_times > 6:
                        driver.refresh()
                    time.sleep(0.6)

                div_list = driver.find_elements_by_xpath('//div[@class="item-list"]/div')[1:-2]
                print(len(div_list))
                # if len(div_list) == 1:  # 只有一个商品 或 无商品 都是一个div
                if r'item-detail' not in driver.page_source:  # 无商品
                    print('没有该商品:', name)
                    if added == 0:
                        df.loc[index, 'sign'] = 2
                        df.to_excel(res_path, index=False)
                    time.sleep(0.8)
                    continue

                for div in div_list:
                    search_name = div.find_element_by_xpath('./div[3]/div/div/h4[@class="name"]/a').text.strip()
                    if name == search_name:
                        if 'onsale' not in driver.current_url:
                            break
                        div.find_element_by_xpath('./div[4]/div/div[2]/button[2]').click()
                        time.sleep(1)
                        if 'onsale' in driver.current_url:
                            continue
                        break
                if 'onsale' in driver.current_url:
                    print('第一页没有该商品:', name)
                    if added == 0:
                        df.loc[index, 'sign'] = 1
                        df.to_excel(res_path, index=False)
                    time.sleep(0.8)
                    continue
                time.sleep(5)
                print('----', search_name)
                # Select(driver.find_element_by_xpath('//div[@class="edit-item-visibility section"]/div/div/select')).select_by_visible_text('不公开')
                # time.sleep(0.5)
                Select(driver.find_element_by_xpath('//div[@class="edit-item-visibility section"]/div/div/select')).select_by_visible_text('上市')
                time.sleep(0.5)

                wait_times = 0
                while r'icon-delete pointer' not in driver.page_source:
                    wait_times += 1
                    if wait_times > 9:
                        break
                    time.sleep(1)
                time.sleep(pic_wait)
                if r'icon-delete pointer' not in driver.page_source:
                    continue
                scroll_js1 = 'var q=document.documentElement.scrollTop=10000'
                driver.execute_script(scroll_js1)
                time.sleep(0.3)
                scroll_js2 = 'var q=document.documentElement.scrollTop=0'
                driver.execute_script(scroll_js2)
                time.sleep(0.3)
                # time.sleep(2)
                # driver.execute_script(scroll_js1)
                # time.sleep(0.2)

                if driver.find_element_by_xpath('//div[@class="media-body"]/div[2]/div/input').is_selected():
                    pass
                else:
                    driver.find_element_by_xpath('//div[@class="media-body"]/div[2]/div/input').click()
                Select(driver.find_element_by_xpath('//div[@class="edit-item-visibility section"]/div/div/select')).select_by_visible_text('不公开')
                time.sleep(0.5)
                Select(driver.find_element_by_xpath('//div[@class="edit-item-visibility section"]/div/div/select')).select_by_visible_text('上市')
                time.sleep(1)
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//div[@class="col-6 text-left"]/button'))
                # driver.find_element_by_xpath('//div[@class="col-6 text-left"]/button').click()
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//div[@class="buttons text-left"]/button[@class="btn btn-primary"]'))
                time.sleep(4)
                if 'sell_item' in driver.current_url:
                    time.sleep(1)
                if 'sell_item' in driver.current_url:
                    continue
                # time.sleep(100)
                # i += 1
                df.loc[index, 'added'] += 1
                df.to_excel(res_path, index=False)
            except:
                continue
        max_times = (df[df['sign'] == 0]['amount'] - df[df['sign'] == 0]['added']).max()
        print('max_times:', max_times)


    driver.get('https://gameflip.com/zh/listings/draft')  # 删除草稿
    time.sleep(5)
    # div_list = driver.find_elements_by_xpath('//div[@class="item-list"]/div')[1:-2]
    # for div in div_list:
    # print('222222')
    while r'item-detail' in driver.page_source:  # 有商品
        # print('2111')
        div_list = driver.find_elements_by_xpath('//div[@class="item-list"]/div')[1:-2]
        # div_list[0].find_element_by_xpath('./div[4]/div/div[2]/button[3]').click()
        try:
            driver.execute_script("arguments[0].click();", div_list[0].find_element_by_xpath('./div[4]/div/div[2]/button[3]'))
            time.sleep(1)
            driver.find_element_by_xpath('//div[@id="common-dialog"]/div/div/div[2]/div/div[2]/button[1]').click()
            time.sleep(2)
        except:
            driver.refresh()
            time.sleep(3.6)


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
    time.sleep(100)

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


# if __name__ == '__main__':
def main():
    # file_path = r'E:\code_workplace\python\2022\january\data\gameflip_com\commodity.xlsx'
    file_path = input('commodity.xlsx路径：').strip()
    pic_wait = int(input('等待图片延迟时间'))
    df = pd.read_excel(file_path)   # pandas 读取excel
    # df = df[['name', 'amount']]     # df取部分列
    df['added'] = 0  # 已复制个数
    df['sign'] = 0  # 1: 搜索后的页面没有该商品  2：搜索后没有一个商品  0：正常
    # print(df)

    key_words = df['name'].values
    # print(key_words)
    # time.sleep(100)

    domain = ['https://gameflip.com/zh/listings/onsale']  # 特价销售页面

    s_date = '20190101'
    e_date = '20210909'

    # chromedriver_path = r'E:\code_workplace\python\chromedriver.exe'
    chromedriver_path = r'chromedriver.exe'
    chrome_port = '9221'

    i = 0
    a_list_num = 0
    start_time = datetime.datetime.now()
    start(pic_wait, s_date, e_date, df.copy(), key_words, file_path[:-5] + start_time.strftime('%Y%m%d %H-%M-%S') + 'res.xlsx', a_list_num, domain[i], chromedriver_path, chrome_port)
