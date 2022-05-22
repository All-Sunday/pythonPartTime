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
    sender_username = 'cs010101012' + '@163.com'
    pwd = 'JPKVLXFGCBJZAPMJ'
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


def query_youyou(name, header):
    api_url = 'https://api.youpin898.com/api/homepage/es/template/GetCsGoPagedList'
    HTTPJSONKEY = {"listType": "30", "gameId": "730", "keyWords": name, "pageIndex": 1, "pageSize": 50, "sortType": "0",
                   "listSortType": "2"}
    if ' | ' not in name:
        HTTPJSONKEY['exterior'] = 'WearCategoryNA'
    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou', e)
        return False, 'youyou请求错误' + str(e)

    if res_json['Msg'] != '请求成功':
        return False, res_json['Msg']

    if res_json['Data'] is None:
        msg = '*****' + name + '未搜索到'
        return False, msg

    commodity_dict = None
    if ' | ' in name:
        for data in res_json['Data']:

            if data['CommodityName'].find(name) == 0:
                id = data['Id']

                sign, commodity_dict = query_youyou_detail1(id, name, header)
                if sign:
                    for key in commodity_dict:

                        if len(commodity_dict[key]) < 2:
                            sign, commodity_dict = query_youyou_detail2(commodity_dict[key][0], name, commodity_dict,
                                                                        header)
                            if not sign:
                                return False, commodity_dict
                else:
                    return False, commodity_dict
                break
    else:
        for data in res_json['Data']:
            if name == data['CommodityName']:
                id = data['Id']

                sign, commodity_dict = query_youyou_detail1(id, name, header)
                if sign:
                    for key in commodity_dict:
                        if len(commodity_dict[key]) < 2:
                            sign, commodity_dict = query_youyou_detail2(commodity_dict[key][0], name, commodity_dict,
                                                                        header)
                            if not sign:
                                return False, commodity_dict
                else:
                    return False, commodity_dict
                break

    if commodity_dict is None:
        msg = '*****' + name + '未遍历到'
        return False, msg
    else:

        return True, commodity_dict


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

    if res_json['Data']['CommodityList'] is not None:
        deposit = res_json['Data']['TemplateInfo']['LeaseDeposit']
        price = res_json['Data']['TemplateInfo']['MinPrice']
        commodity_dict[res_json['Data']['TemplateInfo']['CommodityName']] = [id, eval(deposit), eval(price)]

    return True, commodity_dict


def query_youyou_detail2(id, name, commodity_dict, header):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'
    HTTPJSONKEY = {"templateId": id, "pageSize": 30, "pageIndex": 1, "sortType": 1, "listSortType": 4, "listType": 30}

    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_detail2', e)
        return False, 'youyou_detail2请求错误' + str(e)

    if res_json['Msg'] != 'success':
        return False, res_json['Msg']

    if res_json['Data']['CommodityList'] is not None:
        deposit = res_json['Data']['TemplateInfo']['LeaseDeposit']
        price = res_json['Data']['TemplateInfo']['MinPrice']
        if res_json['Data']['TemplateInfo']['CommodityName'] in commodity_dict:
            commodity_dict[res_json['Data']['TemplateInfo']['CommodityName']] = [id, eval(deposit), eval(price)]

    return True, commodity_dict


def query_buff(name, header):
    api_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search=' + name + '&use_suggestion=0&trigger=search_btn&_=&page_size=50'

    if ' | ' not in name:
        api_url += '&exterior=wearcategoryna'
    try:
        res_json = json.loads(requests.get(api_url, headers=header).text)
    except (Exception, BaseException) as e:
        print('buff', e)
        return False, 'buff请求错误' + str(e) + 'Login Required'

    if res_json['code'] != 'OK':
        return False, res_json['code']
    if len(res_json['data']['items']) == 0:
        msg = '*****buff ' + name + '未搜索到'
        return False, msg

    buff_dict = None

    for data in res_json['data']['items']:
        if name == data['short_name']:

            id = data['id']

            sign, buff_dict = query_buff_detail(id, name, header)
            if not sign:

                return False, buff_dict
            break

    if buff_dict is None:
        msg = '*****buff ' + name + '未遍历到'
        return False, msg
    else:

        return True, buff_dict


def query_buff_detail(id, name, header):
    api_url = 'https://buff.163.com/goods/' + str(id) + '?from=market'
    header[
        'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    header.pop('Cookie')

    try:
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

    return True, buff_dict


def get_res(name, rate, headers_youpin, headers_buff):
    sign, commodity_res = query_youyou(name, headers_youpin)

    if sign:
        sign, buff_res = query_buff(name, headers_buff)
        if sign:
            for key in commodity_res:
                if len(commodity_res[key]) >= 2:
                    if commodity_res[key][-1] < buff_res[key] * rate:
                        msg = key + ' 售价为' + str(commodity_res[key][-1]) + '，buff为' + str(buff_res[key])
                        print(msg)
                        sign, eamil_res = send_mail(msg, key)
                        print(sign, eamil_res)
                    if commodity_res[key][-2] < buff_res[key] * rate:
                        msg = key + ' 押金为' + str(commodity_res[key][-2]) + '，buff为' + str(buff_res[key])
                        print(msg)
                        sign, eamil_res = send_mail(msg, key)
                        print(sign, eamil_res)
            return True, 'done'
        elif 'Login Required' in buff_res:
            print('***********************************')
            print('***********************************')
            return False, buff_res

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
    f = open("cookie.txt", "r")
    cookie = f.read().strip()
    f.close()
    ua = UserAgent(path=r"fake_useragent.json")

    headers_youpin = {'Host': 'api.youpin898.com',
                      # 'Connection': 'keep-alive',
                      'AppType': '1',
                      'Content-Type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain, */*',
                      'User-Agent': ua.random, 'Origin': 'https://youpin898.com', 'Sec-Fetch-Site': 'same-site',
                      'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://youpin898.com/',
                      'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7'}
    headers_buff = {'Host': 'buff.163.com',
                    # 'Connection': 'keep-alive',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'User-Agent': ua.random,
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://buff.163.com/market/csgo',
                    'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7'}


    while True:
        start_time = datetime.datetime.now()
        print(start_time, 'Begin-----------------------')

        df = pd.read_excel(source_path, header=None)

        for row in df.itertuples():
            headers_youpin['User-Agent'] = ua.random
            headers_buff['User-Agent'] = ua.random
            headers_buff['Cookie'] = cookie
            sign, res = get_res(row[1], row[2], headers_youpin, headers_buff)
            if sign:
                print(row[1], res)
            else:
                print(res)
                if ('未搜索到' not in res) and ('soup错误' not in res):
                    msg = '程序error'
                    print(msg)
                    sign, eamil_res = send_mail(msg, res)
                    print(sign, eamil_res)
                    if 'Login Required' in res:
                        sys.exit()

        end_time = datetime.datetime.now()
        total_time = str(end_time - start_time)
        print(end_time, 'Finish-----------------------共耗时', total_time)


main()
