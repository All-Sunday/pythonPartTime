# @Description: 批量处理  自定义 程序入口版  无注释  营销方式点击确认
import os
import sys
import time
import datetime
import json
import openpyxl
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
        msg["To"] = Header("me", 'utf-8')

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

    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou', e)
        return False, 'youyou请求错误' + str(e)
    # print(res_json)

    if res_json['Msg'] != '请求成功':
        return False, res_json['Msg']

    if res_json['Data'] is None:
        msg = '*****' + name + '未搜索到'
        return False, msg

    commodity_dict = None
    # start_time = datetime.datetime.now()
    if ' | ' in name:
        for data in res_json['Data']:
            # if name in data['CommodityName']:
            if data['CommodityName'].find(name) == 0:
                id = data['Id']

                sign, commodity_dict = query_youyou_detail1(id, name, header)
                if sign:
                    for key in commodity_dict:
                        # print(commodity_dict)
                        if len(commodity_dict[key]) < 2:
                            sign, commodity_dict = query_youyou_detail2(commodity_dict[key][0], name, commodity_dict,
                                                                        header)
                            # print(commodity_dict)
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
        # print(commodity_dict)
        # end_time = datetime.datetime.now()
        # total_time = str(end_time - start_time)
        # print(end_time, 'Finish-----------------------共耗时', total_time)
        return True, commodity_dict
    # time.sleep(100)


def query_youyou_detail1(id, name, header):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'
    HTTPJSONKEY = {"templateId": id, "pageSize": 30, "pageIndex": 1, "sortType": 1, "listSortType": 4, "listType": 30}

    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_detail1', e)
        return False, 'youyou_detail1请求错误' + str(e)
    # print(res_json)

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
    # print(commodity_dict)
    # print(res_json['Data']['CommodityList'] is not None)
    if res_json['Data']['CommodityList'] is not None:
        deposit = res_json['Data']['TemplateInfo']['LeaseDeposit']
        price = res_json['Data']['TemplateInfo']['MinPrice']
        commodity_dict[res_json['Data']['TemplateInfo']['CommodityName']] = [id, eval(deposit), eval(price)]
    # print(commodity_dict)
    # time.sleep(100)
    return True, commodity_dict


def query_youyou_detail2(id, name, commodity_dict, header):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'
    HTTPJSONKEY = {"templateId": id, "pageSize": 30, "pageIndex": 1, "sortType": 1, "listSortType": 4, "listType": 30}

    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_detail2', e)
        return False, 'youyou_detail2请求错误' + str(e)
    # print(res_json)

    if res_json['Msg'] != 'success':
        return False, res_json['Msg']
    # print(res_json['Data']['CommodityList'] is not None)
    if res_json['Data']['CommodityList'] is not None:
        deposit = res_json['Data']['TemplateInfo']['LeaseDeposit']
        price = res_json['Data']['TemplateInfo']['MinPrice']
        if res_json['Data']['TemplateInfo']['CommodityName'] in commodity_dict:
            commodity_dict[res_json['Data']['TemplateInfo']['CommodityName']] = [id, eval(deposit), eval(price)]
    # print(commodity_dict)
    # time.sleep(100)
    return True, commodity_dict


def query_buff(name, header):
    # api_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search='+name.replace(' ','%20')+'&use_suggestion=0&trigger=search_btn&_=&page_size=50'
    api_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search=' + name + '&use_suggestion=0&trigger=search_btn&_=&page_size=50'
    # api_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search='+'%E8%BF%90%E5%8A%A8%E6%89%8B%E5%A5%97'+'&use_suggestion=0&trigger=search_btn&_=&page_size=50'

    # print(api_url)
    # print(header)
    try:
        # print('ssss')
        # print(requests.get(api_url, headers=header).text)
        res_json = json.loads(requests.get(api_url, headers=header).text)
    except (Exception, BaseException) as e:
        print('buff', e)
        return False, 'buff请求错误' + str(e)
    # print(res_json)

    if res_json['code'] != 'OK':
        return False, res_json['code']
    if len(res_json['data']['items']) == 0:
        msg = '*****buff ' + name + '未搜索到'
        return False, msg

    buff_dict = None
    # start_time = datetime.datetime.now()

    for data in res_json['data']['items']:
        if name == data['short_name']:

            id = data['id']

            sign, buff_dict = query_buff_detail(id, name, header)
            if not sign:
                msg = '*****' + name + 'buff_detail错误'
                return False, msg
            break

    if buff_dict is None:
        msg = '*****buff ' + name + '未遍历到'
        return False, msg
    else:
        # print(buff_dict)
        # end_time = datetime.datetime.now()
        # total_time = str(end_time - start_time)
        # print(end_time, 'Finish-----------------------共耗时', total_time)

        return True, buff_dict


def query_buff_detail(id, name, header):
    api_url = 'https://buff.163.com/goods/' + str(id) + '?from=market'
    header[
        'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

    try:
        res_html = requests.get(api_url, headers=header).text
    except (Exception, BaseException) as e:
        print('buff_detail', e)
        return False, 'buff_detail错误' + str(e)
    # print(res_html)

    soup = BeautifulSoup(res_html, 'html.parser')
    target_as = soup.find('div', class_='relative-goods').find_all('a')
    # print(target_as)
    buff_dict = {}
    for a in target_as:
        # print(a)
        type_ = a.text.strip()
        if type_ in ('崭新出厂', '略有磨损', '久经沙场', '破损不堪', '战痕累累', '★'):
            if type_ == '★':
                buff_dict[name] = eval(a.span.attrs['data-price'])
                continue
            buff_dict[name + ' (' + type_ + ')'] = eval(a.span.attrs['data-price'])
        # print(type)
        # print(a.span.attrs['data-price'])
    # print(buff_dict)

    return True, buff_dict


def get_res(name, rate, headers_youpin, headers_buff):
    # time.sleep(1.6)

    sign, commodity_res = query_youyou(name, headers_youpin)
    # sign = True
    if sign:
        # name = 'M4A1 消音型 | 守护者'
        sign, buff_res = query_buff(name, headers_buff)
        if sign:
            # print(commodity_res,buff_res)
            for key in commodity_res:
                if len(commodity_res[key]) >= 2:
                    if commodity_res[key][-1] < buff_res[key] * 0.99:
                        msg = key + ' 售价为' + str(commodity_res[key][-1]) + '，buff为' + str(buff_res[key])
                        # print('出售', key)
                        print(msg)
                        sign, eamil_res = send_mail(msg)
                        print(sign, eamil_res)
                    if commodity_res[key][-2] < buff_res[key] * 0.99:
                        msg = key + ' 押金为' + str(commodity_res[key][-2]) + '，buff为' + str(buff_res[key])
                        # print('租赁', key)
                        print(msg)
                        sign, eamil_res = send_mail(msg)
                        print(sign, eamil_res)
            return True, 'done'
        elif buff_res == 'Login Required':
            print('***********************************')
            print('***********************************')
            # print(buff_res)
            # sys.exit()
            return False, buff_res

        else:
            print('***********************************')
            print('***********************************')
            # print(buff_res)
            return False, buff_res

    else:
        print('***********************************')
        print('***********************************')
        # print(commodity_res)
        return False, commodity_res


def main():
    # source_path = input('请输入excel文件路径:').strip()
    source_path = r'商品列表.xlsx'

    # cookie = input('请输入状态码：').strip()
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
    headers_buff[
        'Cookie'] = 'Device-Id=yKFpzWg0xqrvXmsCGeDz; Locale-Supported=zh-Hans; game=csgo; _ga=GA1.2.746510344.1651845703; _gid=GA1.2.892802311.1651845703; NTES_YD_SESS=B9iUXa.t8k5qFFrpIBwhcWPYA2CfXCF4cOEy8neUuuTstMe.tG1VzrRvyEjKyiNYNC74udVEGO96x0tiOW.D0Nn.WRyP6pjtrn8zWtAEFBVjYIxKW3P7ARw9iWc8Xq1D6CIb5rTPEkDkr48nYnQj74JKm7ZmpCrsqbgf0DRzPzzPBRq2jY7ByGtbCuwtTo4wHfEbbDbFo77zubROkIs0GRyTS8qcP0zdwKHucAJK98vvJ; S_INFO=1651894318|0|0&60##|13253592653; P_INFO=13253592653|1651894318|1|netease_buff|00&99|hen&1651893410&netease_buff#hen&411600#10#0#0|&0|null|13253592653; remember_me=U1102321332|eCGToLxttxR3uY2ZTryrRvQQqhCHBz9Z; session=1-t8pvbM-wxJBmGkLW5VR0dLyhQHnB5f11W53qsPMTPoJM2038073836; csrf_token=IjQ5NmQwMTM0ZTRjZmY5YWI0ODMxOGMzZjA3ZjdhMTJmMGVmMGJhNzAi.FVkXzw.j-Y0YQx38YKiVv1_zfi91xYt5qk'
    # headers_buff['Cookie'] = ''
    # print(headers_youpin)
    # time.sleep(100)

    while True:
        start_time = datetime.datetime.now()
        print(start_time, 'Begin-----------------------')

        # df = pd.read_excel(source_path, header=None)[:5]
        df = pd.read_excel(source_path, header=None)[450:]
        # print(df)
        # time.sleep(100)
        # phones = df[0].apply(str).values

        # n = 0
        for row in df.itertuples():
            # if n % 10 == 0:
            #     print(row)
            # print(row[0], row[1], row[2])
            # time.sleep(100)
            sign, res = get_res(row[1], row[2], headers_youpin, headers_buff)
            if sign:
                print(row[1], res)
            else:
                print(res)
                if '未搜索到' not in res:
                    msg = '程序error'
                    print(msg)
                    sign, eamil_res = send_mail(msg, res)
                    print(sign, eamil_res)
                    if res == 'Login Required':
                        sys.exit()

            # n += 1
        end_time = datetime.datetime.now()
        total_time = str(end_time - start_time)
        print(end_time, 'Finish-----------------------共耗时', total_time)


main()
