# 根据id直接爬 buff无需登录cookie
import random
import sys
import datetime
import json
import time

import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header
import smtplib


def send_mail(mail_title='', mail_content=''):
    sender_username = 'MrSunday1' + '@163.com'
    pwd = 'XWNRJMELACZEFSTR'
    receiver = ['1544781624@qq.com']
    host_server = 'smtp.163.com'
    try:
        msg = MIMEText(mail_content, 'plain', 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_username
        msg["To"] = receiver[0]

        smtp = smtplib.SMTP_SSL(host_server)
        smtp.ehlo(host_server)
        smtp.login(sender_username, pwd)

        smtp.sendmail(sender_username, receiver, msg.as_string())
        smtp.quit()
        return True, '邮件发送成功'
    except (Exception, BaseException) as e:
        print('eamil', e)
        return False, 'email' + str(e)


def query_youyou(name, youyou_id, header, sleep_time):
    sign, commodity_dict = query_youyou_detail1(youyou_id, name, header)
    if sign:
        for key in commodity_dict:
            # print(commodity_dict)
            if len(commodity_dict[key]) < 2:
                sign, commodity_dict = query_youyou_detail2(commodity_dict[key][0], name, commodity_dict,
                                                            header, sleep_time)
                # print(commodity_dict)
                if not sign:
                    return False, commodity_dict
        return True, commodity_dict
    else:
        return False, commodity_dict


def query_youyou_detail1(id, name, header):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'
    HTTPJSONKEY = {"templateId": id, "pageSize": 30, "pageIndex": 1, "sortType": 1, "listSortType": 4, "listType": 30}

    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_detail1', e)
        return False, 'youyou_detail1请求错误' + str(e)

    if res_json['Msg'] != 'success':
        return False, res_json['Msg']
    commodity_dict = {}
    exteriors = res_json['Data']['Filters'][-1]['Items']
    for exterior in exteriors:
        if exterior['Name'] in ('崭新出厂', '略有磨损', '久经沙场', '破损不堪', '战痕累累', '无涂装'):
            if exterior['Name'] == '无涂装':
                commodity_dict[name] = [exterior['FixedVal']]
                continue
            commodity_dict[name + ' (' + exterior['Name'] + ')'] = [exterior['FixedVal']]
    templateInfo = res_json['Data']['TemplateInfo']
    if templateInfo['CommodityName'] not in commodity_dict:
        return False, 'UUid,' + str(id) + '(' + templateInfo['CommodityName'] + ')与excel名称(' + name + ')不匹配'
    if res_json['Data']['CommodityList'] is not None:
        deposit = templateInfo['LeaseDeposit']
        price = templateInfo['MinPrice']
        if templateInfo['CommodityName'] in commodity_dict:
            commodity_dict[templateInfo['CommodityName']] = [id, eval(deposit), eval(price)]

    return True, commodity_dict


def query_youyou_detail2(id, name, commodity_dict, header, sleep_time):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'
    HTTPJSONKEY = {"templateId": id, "pageSize": 30, "pageIndex": 1, "sortType": 1, "listSortType": 4, "listType": 30}

    try:
        time.sleep(sleep_time)
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_detail2', e)
        return False, 'youyou_detail2请求错误' + str(e)

    if res_json['Msg'] != 'success':
        return False, res_json['Msg']

    templateInfo = res_json['Data']['TemplateInfo']
    if res_json['Data']['CommodityList'] is not None:
        deposit = templateInfo['LeaseDeposit']
        price = templateInfo['MinPrice']
        if templateInfo['CommodityName'] in commodity_dict:
            commodity_dict[templateInfo['CommodityName']] = [id, eval(deposit), eval(price)]

    return True, commodity_dict


def query_buff(name, buff_id, header, sleep_time):
    sign, buff_dict = query_buff_detail(buff_id, name, header, sleep_time)
    return sign, buff_dict


def query_buff_detail(id, name, header, sleep_time):
    api_url = 'https://buff.163.com/goods/' + str(id) + '?from=market'

    try:
        time.sleep(sleep_time)
        res_html = requests.get(api_url, headers=header).text
    except (Exception, BaseException) as e:
        print('buff_detail', e)
        return False, 'buff_detail错误' + str(e)

    soup = BeautifulSoup(res_html, 'html.parser')
    try:
        target_as = soup.find('div', attrs={'class': 'relative-goods'}).find_all('a')
    except (Exception, BaseException) as e:
        print('soup', e)
        if "attribute 'find_all'" in str(e):
            return False, 'soup错误' + str(e)

    buff_dict = {}
    for a in target_as:

        type_ = a.text.strip()
        if type_ in ('崭新出厂', '略有磨损', '久经沙场', '破损不堪', '战痕累累', '★'):
            if type_ == '★':
                buff_dict[name] = eval(a.span.attrs['data-price'])
                continue
            buff_dict[name + ' (' + type_ + ')'] = eval(a.span.attrs['data-price'])
    page_name = soup.find('div', attrs={'class': 'detail-cont'}).find('div').find('h1').text.strip()
    if page_name not in buff_dict:
        return False, 'buffid,' + str(id) + '(' + page_name + ')与excel名称(' + name + ')不匹配'
    return True, buff_dict


def get_res(name, youyou_id, buff_id, rate, headers_youpin, headers_buff, sleep_time, email_dict, eamil_time_gap):
    sign, commodity_res = query_youyou(name, youyou_id, headers_youpin, sleep_time)

    if sign:
        sign, buff_res = query_buff(name, buff_id, headers_buff, sleep_time)
        if sign:
            for key in commodity_res:
                if (len(commodity_res[key]) >= 2) and (key in buff_res):
                    if commodity_res[key][-1] < buff_res[key] * rate:
                        msg = key + ' 售价为' + str(commodity_res[key][-1]) + '，buff为' + str(buff_res[key])
                        print(msg)
                        now_timestamp = int(time.time())
                        key2 = key + '售'
                        if (key2 not in email_dict) or (now_timestamp - email_dict[key2] >= eamil_time_gap):
                            email_dict[key2] = now_timestamp
                            sign, eamil_res = send_mail(key, msg)
                            print(sign, eamil_res)
                    if commodity_res[key][-2] < buff_res[key] * rate:
                        msg = key + ' 押金为' + str(commodity_res[key][-2]) + '，buff为' + str(buff_res[key])
                        print(msg)
                        now_timestamp = int(time.time())
                        key2 = key + '押'
                        if (key2 not in email_dict) or (now_timestamp - email_dict[key2] >= eamil_time_gap):
                            email_dict[key2] = now_timestamp
                            sign, eamil_res = send_mail(key, msg)
                            print(sign, eamil_res)
            return True, 'done'
        # elif 'Login Required' in buff_res:
        #     print('***********************************')
        #     print('***********************************')
        #     return False, buff_res

        else:
            print('***********************************')
            print('***********************************')
            return False, buff_res

    else:
        print('***********************************')
        print('***********************************')
        return False, commodity_res


def main():
    source_path = r'商品列表.xlsx'
    ua = UserAgent(path=r"fake_useragent.json")

    headers_youpin = {'Host': 'api.youpin898.com',
                      'Connection': 'close',
                      'AppType': '1',
                      'Content-Type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain, */*',
                      'User-Agent': ua.random, 'Origin': 'https://youpin898.com', 'Sec-Fetch-Site': 'same-site',
                      'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://youpin898.com/',
                      'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7'}
    headers_buff = {'Host': 'buff.163.com',
                    'Connection': 'close',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'User-Agent': ua.random,
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Dest': 'document',
                    'Referer': 'https://buff.163.com/market/csgo',
                    'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7'}
    email_dict = {}
    eamil_time_gap = 5400
    while True:
        start_time = datetime.datetime.now()
        print(start_time, 'Begin-----------------------')

        df = pd.read_excel(source_path, header=None).dropna(subset=[1])
        df[[1, 2]] = df[[1, 2]].astype('int')

        for row in df.itertuples():
            headers_youpin['User-Agent'] = ua.random
            headers_buff['User-Agent'] = ua.random

            if 8 < datetime.datetime.now().hour < 22:
                sleep_time = 1 + random.randint(1, 5) / 10
            else:
                sleep_time = 2 + random.randint(1, 5) / 10

            sign, res = get_res(row[1], row[2], row[3], row[4], headers_youpin, headers_buff, sleep_time, email_dict,
                                eamil_time_gap)

            if sign:
                print(row[1], res)
            else:
                print(res)
                if 'soup错误' not in res:
                    msg = '程序error'
                    print(msg)
                    sign, eamil_res = send_mail(msg, res)
                    print(sign, eamil_res)
                    if 'Forbidden' in res:
                        sys.exit()

        end_time = datetime.datetime.now()
        total_time = str(end_time - start_time)
        print(end_time, 'Finish-----------------------共耗时', total_time)


main()
