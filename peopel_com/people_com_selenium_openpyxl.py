# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/1/9 17:22
# @File : people_com.py
# -*- coding:utf-8 -*-

import datetime
import re
import time
import os
import openpyxl
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys


def init(start_url, domain, chromedriver_path, res_path):
    # 启动谷歌浏览器
    options = Options()
    options.add_argument('--no-sandbox')                # 解决DevToolsActivePort文件不存在的报错
    options.add_argument('window-size=1920x3000')       # 设置浏览器分辨率
    options.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')           # 隐藏滚动条，应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')      # 不加载图片，提升运行速度
    # options.add_argument('--headless')                  # 开启无头模式（无界面启动）

    driver = webdriver.Chrome(chromedriver_path, options=options)
    driver.execute_script('window.open("' + start_url + '")')
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[0])
    driver.get(start_url)

    if not os.path.exists(res_path + '_' + domain[:3] + '.xlsx'):
        res_wk = openpyxl.Workbook()
        res_sheet = res_wk.active
        res_sheet.append(['文章标题', '文章内容', '发布日期', '信息来源', '网站', '关键词', '网址'])
        res_wk.save(res_path + '_' + domain[:3] + '.xlsx')

    res_wk = openpyxl.load_workbook(res_path + '_' + domain[:3] + '.xlsx')
    res_sheet = res_wk.active
    return driver, res_wk, res_sheet


def get_res(site, start_url, s_date, e_date, key_words, a_list_num, domain, res_wk, res_sheet, res_path, driver, handles):
    res = []
    all_a_list = []
    driver.switch_to.window(handles[0])
    driver.get(start_url)
    for key_word in key_words:      # 循环搜索关键词

        driver.switch_to.window(handles[0])
        driver.find_element_by_xpath('//*[@id="q"]').clear()
        driver.find_element_by_xpath('//*[@id="q"]').send_keys(key_word)  # 输入搜索内容

        time.sleep(0.5)
        start_date_js = "$('input[id=date_start]').val('" + s_date + "')"   # 修改日期
        driver.execute_script(start_date_js)
        end_date_js = "$('input[id=date_end]').val('" + e_date + "')"
        driver.execute_script(end_date_js)
        # display_js = 'document.getElementsByClassName("jsearch-criteria-btn ok")[0].style.display = "block";'   # 让 确定 按钮显示
        # driver.execute_script(display_js)
        time.sleep(1)
        # driver.find_element_by_xpath('//*[@class="jsearch-criteria-btn ok"]').click()  # 点击 确定 按钮
        driver.find_element_by_xpath('//*[@id="q"]').send_keys(Keys.ENTER)  # 回车 使条件生效
        time.sleep(1)

        # print(driver.find_element_by_xpath('//*[@id="jsearch-no-result-box"]').get_attribute('style'))
        if driver.find_element_by_xpath('//*[@id="jsearch-no-result-box"]').get_attribute('style').split('lay: ')[1].split(';')[0] == 'block':  # 无数据
            continue

        a_list = []
        while True:
            div_list = driver.find_elements_by_xpath('//div[@id="jsearch-result-items"]/div')  # 数据divs
            time.sleep(0.5)

            for div in div_list:
                a_href = div.find_element_by_xpath('./div[3]//div[@class="jsearch-result-url"]/a').text   # 获取 a标签 文本
                if a_href == '':
                    # print(div.find_element_by_xpath('./div[3]//div[@class="jsearch-result-url"]/a').get_attribute('href').split('url=')[1].split('&q=')[0])
                    a_href = div.find_element_by_xpath('./div[3]//div[@class="jsearch-result-url"]/a').get_attribute('href').split('url=')[1].split('&q=')[0].replace('%253A', ':').replace('%252F', '/').replace('%3A', ':').replace('%2F', '/')
                if domain in a_href:
                    if a_href not in all_a_list:
                        a_list.append(a_href)
                        all_a_list.append(a_href)

            if re.findall(r'下一页', driver.page_source, re.S):

                if driver.find_element_by_xpath('//div[@id="pagination"]/a[last()]').text == '下一页':  # 若最后一个a标签是下一页 说明还有下一页
                    driver.find_element_by_xpath('//div[@id="pagination"]/a[last()]').click()   # 点击 下一页
                    time.sleep(1)
                else:
                    break
            else:               # 数据不够一页时 不显示下一页
                break

        print(a_list)
        print(len(a_list))  # 去重

        get_data(site, a_list[a_list_num:], key_word, domain, res, res_wk, res_sheet, res_path, driver, handles)  # 通过 a 链接获取详细信息
    print(res)
    # res_df = pd.DataFrame(res)
    # res_df.columns = ['文章标题', '文章内容', '发布日期', '信息来源', '网站', '关键词', '网址']
    # res_df.to_excel(res_path + '_' + domain[:3] + '.xlsx', index=None)


def get_data(site, a_list, key_word, domain, res, res_wk, res_sheet, res_path, driver, handles):
    driver.switch_to.window(handles[-1])
    for a in a_list:
        # i = 0
        try:
            driver.get(a)
        except:
            driver.get(a)
        time.sleep(1)

        # if re.findall(r'发布日期：', driver.page_source, re.S):
        if (re.findall(r'来源：', driver.page_source, re.S) + re.findall(r'制发日期：', driver.page_source, re.S)):
            if domain == 'gxt.henan.gov.cn':
                title = driver.find_element_by_xpath('//div[@class="titP"]/h1').text
                release_date = driver.find_element_by_xpath('//div[@class="source fl"]/span[1]').text.strip()[5:]
                info_resource = driver.find_element_by_xpath('//div[@class="source fl"]/span[2]').text.strip()[5:]
                p_list = driver.find_elements_by_xpath('//div[@class="conBox"]/*')
            elif domain == 'kjt.henan.gov.cn':
                if re.findall(r'"articl_u1', driver.page_source, re.S):
                    title = driver.find_element_by_xpath('//div[@class="articl_u1"]/h1').text
                    release_date = driver.find_element_by_xpath('//div[@class="articl_u1"]/h2/span[1]').text.strip()[5:]
                    info_resource = driver.find_element_by_xpath('//div[@class="articl_u1"]/h2/span[2]').text.strip()[3:]
                    p_list = driver.find_elements_by_xpath('//div[@class="articl_u2"]/*')
                elif re.findall(r'"article_main', driver.page_source, re.S):
                    title = driver.find_element_by_xpath('//div[@class="article_main"]/h3').text
                    # print(driver.find_element_by_xpath('//div[@class="source"]/center').text.split('：')[-1].strip())
                    release_date = driver.find_element_by_xpath('//div[@class="source"]/center').text.split('：')[-1].strip()
                    # print(driver.find_element_by_xpath('//div[@class="source"]/center').text.split('：')[1].strip()[:-5])
                    info_resource = driver.find_element_by_xpath('//div[@class="source"]/center').text.split('：')[1].strip()[:-5]
                    print(driver.find_element_by_xpath('//div[@class="content"]').get_attribute('innerHTML').strip())
                    print('个数：', len(driver.find_elements_by_xpath('//div[@class="content"]/*')))
                    p_list = driver.find_elements_by_xpath('//div[@class="content"]/*')
                elif re.findall(r'"nav', driver.page_source, re.S):
                    title = driver.find_element_by_xpath('//div[@id="article"]/h1/b').text
                    release_date = driver.find_element_by_xpath('//div[@class="nav"]').text.strip().split('：')[1][:-2]
                    # print(release_date)
                    info_resource = driver.find_element_by_xpath('//div[@class="nav"]/span[2]').text.strip()[3:]
                    # print(info_resource)
                    p_list = driver.find_elements_by_xpath('//div[@class="article"]/*')
                else:
                    title = driver.find_element_by_xpath('//div[@class="page-right"]/div[@class="content"]/p[1]').text
                    release_date = driver.find_element_by_xpath('//div[@class="page-right"]/div[@class="content"]/p[2]/span[1]').text.strip()[5:]
                    # print(release_date)
                    info_resource = driver.find_element_by_xpath('//div[@class="page-right"]/div[@class="content"]/p[2]/span[2]').text.strip()[3:]
                    # print(info_resource)
                    p_list = driver.find_elements_by_xpath('//div[@class="page-right"]/div[@class="content"]/div/*')
            elif domain == 'czt.henan.gov.cn':
                if re.findall(r'"news_fwl', driver.page_source, re.S):
                    print(a)
                    continue
                title = driver.find_element_by_xpath('//div[@class="newscontent"]/h1').text
                release_date = driver.find_element_by_xpath('//div[@class="t_s"]/span[2]').text.strip()[5:]
                info_resource = driver.find_element_by_xpath('//div[@class="t_s"]/span[1]').text.strip()[3:]
                p_list = driver.find_elements_by_xpath('//div[@class="newstxt"]/*')
            elif domain == 'fgw.henan.gov.cn':
                if re.findall(r'"yTit', driver.page_source, re.S):
                    if re.findall(r'"file-box cl', driver.page_source, re.S):
                        release_date = driver.find_element_by_xpath('//div[@class="file-box cl"]/p[3]/span[2]').text.split('：')[1].strip().replace('年', '-').replace('月', '-')[:-1]
                        info_resource = driver.find_element_by_xpath('//div[@class="file-box cl"]/p[2]/span[2]').text.split('：')[1].strip()
                        title = driver.find_element_by_xpath('//div[@class="file-box cl"]/p[1]/em').text.strip()
                        p_list = driver.find_elements_by_xpath('//div[@class="conBox"]/*')[4:]
                    else:

                        release_date = driver.find_element_by_xpath('//div[@class="sj fl"]/span[1]').text.strip()[3:]
                        info_resource = driver.find_element_by_xpath('//div[@class="sj fl"]/span[2]').text.strip()[3:]
                        title = driver.find_element_by_xpath('//p[@class="yTit"]').text
                        p_list = driver.find_elements_by_xpath('//div[@class="conBox"]/*')


            # print(driver.find_elements_by_xpath('//div[@class="conBox"]/*'))
            # time.sleep(100)
            content = ''
            for p in p_list:
                content_div = p.get_attribute('innerHTML').strip()
                if content_div != '':
                    # print(content_div)
                    # print(etree.HTML(content_div))
                    content_b = etree.HTML(content_div).xpath('string(.)').strip()
                    if content_b[-2:] == '\n':
                        content += content_b
                    else:
                        content += content_b + '\n'
            # content = driver.find_element_by_xpath('//div[@class="conBox"]/p').text.strip()
            url = driver.current_url
            if a != url:
                print(a)
                print(url)
                print('a不一样')

            # res.append([i, title, content.strip(), release_date, info_resource, 'gxt', key_word, url])
            res.append([title, re.sub('\n\t\t\t', '', re.sub('\n ', '    ', re.sub('\n\t\t\t\t+', '', re.sub('\n\t\t\t\t\t\n ', '', content.strip())))), release_date, info_resource, site, key_word, url])
            res_sheet.append([title, re.sub('\n\t\t\t', '', re.sub('\n ', '    ', re.sub('\n\t\t\t\t+', '', re.sub('\n\t\t\t\t\t\n ', '', content.strip())))), release_date, info_resource, site, key_word, url])
            res_wk.save(res_path + '_' + domain[:3] + '.xlsx')

        else:
            url = driver.current_url
            print('网页格式不对！！！', url)
            res.append([driver.title, '', '', '', site, key_word, url])
            res_sheet.append([driver.title, '', '', '', site, key_word, url])
            res_wk.save(res_path + '_' + domain[:3] + '.xlsx')

            continue

    return res

def start(site, start_url, s_date, e_date, key_words, a_list_num, domain, log_path, res_path, chromedriver_path):
    start_time = datetime.datetime.now()
    print(start_time, 'Begin-----------------------')

    # zhsmd_url = 'http://www.zhsmd.cn/web#action=1302&model=x_kdzhgl&view_type=list&cids=1&menu_id=976'
    # telecomhb_url = 'http://hbjf.telecomhb.com:6200/webpay/billpay/PaymentElecNetNew.jsp'
    # login_url = 'http://crm.telecomhb.com:9500/portal-web/main/mainPage'

    driver, res_wk, res_sheet = init(start_url, domain, chromedriver_path, res_path)
    driver.implicitly_wait(30)
    handles = driver.window_handles

    get_res(site, start_url, s_date, e_date, key_words, a_list_num, domain, res_wk, res_sheet, res_path, driver, handles)

    end_time = datetime.datetime.now()
    print(end_time, 'Finish-----------------------共耗时', end_time - start_time)

if __name__ == '__main__':
    log_path = r'../data/yuguang/log.xlsx'
    res_path = r'../data/yuguang/res'

    start_url_dict = {'河南省工业和信息化厅': 'https://search1.henan.gov.cn/jrobot/search.do?webid=10023&pos=title&od=0&q='}

    key_words = ['项目补助']

    domain = ['gxt.henan.gov.cn']

    s_date = '20190101'
    e_date = '20210909'


    chromedriver_path = r'E:\code_workplace\python\chromedriver.exe'

    i = 0
    a_list_num = 0
    for key, value in start_url_dict.items():
        if i == 1:
            print(key, value, s_date, e_date, key_words, domain[i], log_path, res_path, chromedriver_path)
            start(key, value, s_date, e_date, key_words[16:], a_list_num, domain[i], log_path, res_path, chromedriver_path)

        i += 1


