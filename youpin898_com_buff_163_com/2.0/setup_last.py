# 取消df_youyou全部变量 无法每轮结束后重读excel
import random
import sys
import datetime
import json
import threading
import time
import pandas as pd
import requests
from thresd import *
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header
import smtplib


def send_mail(mail_title='', mail_content=''):
    sender_username = 'cs010101012' + '@163.com'
    pwd = 'JPKVLXFGCBJZAPMJ'
    receiver = ['CSGO20251351@163.com']
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


def query_youyou(name, youyou_id, types, header):
    sign, commodity_dict = query_youyou_detail1(youyou_id, name, types, header)
    if sign:
        return True, commodity_dict
    else:
        return False, str(youyou_id) + commodity_dict


def query_youyou_detail1(id, name, types, header):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'
    HTTPJSONKEY = {"templateId": str(id), "pageSize": 10, "pageIndex": 1, "sortType": 1, "listSortType": 1,
                   "listType": 10}

    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_detail1', e)
        return False, 'youyou_detail1请求错误' + str(e)

    if res_json['Msg'] != 'success':
        return False, res_json['Msg']
    templateInfo = res_json['Data']['TemplateInfo']
    if not (((templateInfo['Exterior'] == '无涂装') and (templateInfo['CommodityName'] == name)) or (
            name + ' (' + templateInfo['Exterior'] + ')' == templateInfo['CommodityName'])):
        return False, 'UUid,' + str(id) + '(' + templateInfo['CommodityName'] + ')与excel名称(' + name + ')不匹配'

    commodity_dict = {}
    exteriors = res_json['Data']['Filters'][-1]['Items']
    for exterior in exteriors:
        if exterior['Name'] in types:
            if exterior['Name'] == '无涂装':
                commodity_dict[name] = [exterior['FixedVal']]
                continue
            commodity_dict[name + ' (' + exterior['Name'] + ')'] = [exterior['FixedVal']]

    if res_json['Data']['CommodityList'] is not None:
        if templateInfo['CommodityName'] in commodity_dict:
            commodity = res_json['Data']['CommodityList'][0]
            price = commodity['Price']

            sign, res = query_youyou_detail3(id, templateInfo['CommodityName'], header)
            if sign:
                commodity_dict[templateInfo['CommodityName']] = [id, res[1], eval(price), res[0], commodity['Id']]
            else:
                commodity_dict[templateInfo['CommodityName']] = [id, 0, eval(price), '0', commodity['Id']]

    return True, commodity_dict


def query_youyou_detail2(id, name, header):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'

    HTTPJSONKEY = {"templateId": str(id), "pageSize": 10, "pageIndex": 1, "sortType": 1, "listSortType": 1,
                   "listType": 10}

    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_detail2', e)
        return False, 'youyou_detail2请求错误' + str(e)

    if res_json['Msg'] != 'success':
        return False, res_json['Msg']

    templateInfo = res_json['Data']['TemplateInfo']
    if res_json['Data']['CommodityList'] is not None:
        if templateInfo['CommodityName'] in name:
            commodity = res_json['Data']['CommodityList'][0]
            price = commodity['Price']

            sign, res = query_youyou_detail3(id, templateInfo['CommodityName'], header)
            if sign:
                return True, [id, res[1], eval(price), res[0], commodity['Id']]
            else:
                return True, [id, 0, eval(price), '0', commodity['Id']]
    return False, '没有人出售'


def query_youyou_detail3(id, name, header):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'

    HTTPJSONKEY = {"templateId": str(id), "pageSize": 10, "pageIndex": 1, "sortType": 1, "listSortType": 4,
                   "listType": 30}

    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_detail2', e)
        return False, 'youyou_detail2请求错误' + str(e)

    if res_json['Msg'] != 'success':
        return False, res_json['Msg']

    templateInfo = res_json['Data']['TemplateInfo']
    if res_json['Data']['CommodityList'] is not None:
        if templateInfo['CommodityName'] == name:
            commodity = res_json['Data']['CommodityList'][0]
            deposit = commodity['LeaseDeposit']

            return True, [commodity['Id'], eval(deposit)]
    return False, '没有人出售'


def query_buff(df, res_dict, header, sleep_time, ua):
    for row in df.itertuples():
        header['User-Agent'] = ua.random
        sleep_time1 = sleep_time + random.randint(1, 5) / 10
        sign, sign_content = query_buff_detail(row[3], row[1], res_dict, header, sleep_time1)
        if not sign:
            print('***********************************')
            print('***********************************')
            print(sign_content)
            if ('soup错误' not in sign_content) and ('timed out' not in sign_content):
                msg = '程序error'
                print(msg)
                sign, eamil_res = send_mail(msg, sign_content)
                print(sign, eamil_res)
                if 'Forbidden' in sign_content:
                    sys.exit()
        print('buff ' + row[1] + ' done')


def query_buff_detail(id, name, res_dict, header, sleep_time):
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
        target_a1 = soup.find('a', attrs={'class': 'i_Btn i_Btn_trans_bule active'})
        print(target_a1)
        target_as.append(target_a1)
    except (Exception, BaseException) as e:
        print('soup', e)
        if "attribute 'find_all'" in str(e):
            return False, 'soup错误' + str(e)

    names = []
    for a in target_as:

        type_ = a.text.strip()
        if type_ in ('崭新出厂', '略有磨损', '久经沙场', '破损不堪', '战痕累累', '★'):
            if type_ == '★':
                res_dict[name] = eval(a.span.attrs['data-price'])
                names.append(name)
                continue
            res_dict[name + ' (' + type_ + ')'] = eval(a.span.attrs['data-price'])
            names.append(name + ' (' + type_ + ')')
    page_name = soup.find('div', attrs={'class': 'detail-cont'}).find('div').find('h1').text.strip()
    if page_name not in res_dict:
        for n in names:
            res_dict.pop(n)
        return False, 'buffid,' + str(id) + '(' + page_name + ')与excel名称(' + name + ')不匹配'
    return True, 'buff ' + name + ' done'


# def get_buff(source_path, res_dict, header, setup, ua, time_gap=0):
def get_buff(df, res_dict, header, setup, ua, time_gap=0):
    while True:
        if setup[3] < datetime.datetime.now().hour < setup[4]:
            sleep_time = setup[5]
        else:
            sleep_time = setup[6]

        gap = time_gap
        if time_gap != 0:
            gap = random.randint(time_gap - 180, time_gap)
        print('buff_gap', gap)
        time.sleep(gap)

        # df_buff = pd.read_excel(source_path, header=None).dropna(subset=[1])
        #
        # df_buff[[1, 2]] = df_buff[[1, 2]].astype('int')
        # print('df_buff read')

        s_time = datetime.datetime.now()
        print(s_time, 'Begin-----------------------')
        query_buff(df, res_dict, header, sleep_time, ua)
        e_time = datetime.datetime.now()
        total_time = str(e_time - s_time)
        print(e_time, 'buff重新获取Finish-----------------------共耗时', total_time)
        if time_gap == 0:
            break


mutex = threading.Lock()
y_num = 0
# df_youyou = pd.DataFrame()
start_time = datetime.datetime.now()


# def get_res(t_name, source_path, buff_res, header, ua, email_dict, eamil_time_gap):
def get_res(t_name, df, buff_res, header, ua, email_dict, eamil_time_gap):
    global y_num
    # global df_youyou
    global start_time
    # mutex.acquire()
    # if len(df_youyou) == 0:
    #     df_youyou = pd.read_excel(source_path, header=None).dropna(subset=[1])
    #
    #     df_youyou[[1, 2]] = df_youyou[[1, 2]].astype('int')
    #     print('df_youyou first read')
    #
    #     start_time = datetime.datetime.now()
    #     print(start_time, 'Begin-----------------------')
    # mutex.release()
    while True:

        mutex.acquire()
        # if y_num >= len(df_youyou):
        if y_num >= len(df):
            end_time = datetime.datetime.now()
            total_time = str(end_time - start_time)
            print(end_time, 'Finish-----------------------共耗时', total_time)
            # df_youyou = pd.read_excel(source_path, header=None).dropna(subset=[1])
            #
            # df_youyou[[1, 2]] = df_youyou[[1, 2]].astype('int')
            # print('df_youyou read')

            start_time = datetime.datetime.now()
            print(start_time, 'Begin-----------------------')
            y_num = 0
        # data = df_youyou.iloc[y_num]
        data = df.iloc[y_num]
        y_num += 1
        mutex.release()

        if isinstance(data[4], int):
            types = set()
            types.add(type_processor(data[4]))
        else:
            types = set(map(lambda x: type_processor(x), str(data[4]).strip().split()))
        if None in types:
            types.remove(None)
        if len(types) == 0:
            print('***********************************')
            print('***********************************')
            msg = '程序error'
            print(msg)
            content = data[0] + '磨损度不正确'
            sign, eamil_res = send_mail(msg, content)
            print(sign, eamil_res)
            continue
        header['User-Agent'] = ua.random

        sign, commodity_dict = query_youyou(data[0], data[1], types, header)

        if sign:

            for key in commodity_dict:

                if len(commodity_dict[key]) < 2:
                    sign, commodity_res = query_youyou_detail2(commodity_dict[key][0], key, header)
                    if sign:
                        commodity_dict[key] = commodity_res
                    else:
                        if commodity_res == '没有人出售':
                            continue
                        print('***********************************')
                        print('***********************************')
                        print(key + commodity_res)

                        if 'timed out' not in commodity_res:
                            msg = '程序error'
                            print(msg)
                            sign, eamil_res = send_mail(msg, key + commodity_res)
                            print(sign, eamil_res)
                            if 'Forbidden' in commodity_res:
                                sys.exit()
                        continue

                if key in buff_res:
                    msg = ''
                    mode = ''
                    if (buff_res[key] * 0.6) <= commodity_dict[key][2] <= (buff_res[key] * data[3]):
                        msg += key + ' 售价为' + str(commodity_dict[key][2]) + '，buff为' + str(buff_res[key]) + '\n'

                        mode += '2'

                    if (buff_res[key] * 0.6) <= commodity_dict[key][1] <= (buff_res[key] * data[3]):
                        msg += key + ' 押金为' + str(commodity_dict[key][1]) + '，buff为' + str(buff_res[key])
                        mode += '1'

                    if mode != '':
                        if mode == '2':
                            key2 = key + '售'

                        elif mode == '21':
                            if commodity_dict[key][3] == commodity_dict[key][4]:
                                key2 = key + '押'
                                mode = '1'

                        now_timestamp = int(time.time())
                        if (key2 not in email_dict) or (now_timestamp - email_dict[key2] >= eamil_time_gap):
                            print(t_name, msg)

                            row = insert(
                                [key, commodity_dict[key][0], commodity_dict[key][1], commodity_dict[key][2],
                                 commodity_dict[key][3], commodity_dict[key][4], msg,
                                 mode, now_timestamp])
                            time.sleep(0.6)
                            sign_res = orderp(now_timestamp)
                            if (row == 1) and sign_res:
                                email_dict[key2] = now_timestamp
                                email_dict[key + '售'] = now_timestamp
                                print(t_name, True)

        else:
            print('***********************************')
            print('***********************************')
            print(commodity_dict)
            if 'timed out' not in commodity_dict:
                msg = '程序error'
                print(msg)
                sign, eamil_res = send_mail(msg, commodity_dict)
                print(sign, eamil_res)
                if 'Forbidden' in commodity_dict:
                    sys.exit()


def type_processor(t):
    t = str(t)
    type_dict = {'1': '崭新出厂', '2': '略有磨损', '3': '久经沙场', '4': '破损不堪', '5': '战痕累累', '0': '无涂装'}
    if t not in type_dict:
        return None
    return type_dict[t]


def main():
    source_path = r'商品列表.xlsx'
    ua = UserAgent(path=r"fake_useragent.json")
    setup = []
    with open("setup.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            setup.append(eval(line.split('：')[1]))

    thread_num = setup[0]
    threads = []

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

    buff_dict = {}
    buff_time_gap = setup[1]
    email_dict = {}
    eamil_time_gap = setup[2]

    df = pd.read_excel(source_path, header=None).dropna(subset=[1])

    df[[1, 2]] = df[[1, 2]].astype('int')

    # get_buff(source_path, buff_dict, headers_buff, setup, ua)
    get_buff(df, buff_dict, headers_buff, setup, ua)

    if len(buff_dict) == 0:
        msg = '程序error'
        print(msg)
        sign, eamil_res = send_mail(msg, 'buff搜索结果为0')
        print(sign, eamil_res)
        sys.exit()
    print('第一轮buff执行完毕')
    send_mail('第一轮buff执行完毕', '程序正常运行')
    # todo
    # t_buff = threading.Thread(target=get_buff, args=(source_path, buff_dict, headers_buff, setup, ua, buff_time_gap),
    #                           name='buff')
    t_buff = threading.Thread(target=get_buff, args=(df, buff_dict, headers_buff, setup, ua, buff_time_gap),
                              name='buff')
    t_buff.start()

    try:
        for i in range(thread_num):
            # t_youyou = threading.Thread(target=get_res,
            #                             args=('UU%d' % i, source_path, buff_dict, headers_youpin, ua, email_dict,
            #                                   eamil_time_gap), name='UU%d' % i)
            t_youyou = threading.Thread(target=get_res,
                                        args=('UU%d' % i, df, buff_dict, headers_youpin, ua, email_dict,
                                              eamil_time_gap), name='UU%d' % i)
            threads.append(t_youyou)
        for t in threads:
            t.start()
            time.sleep(0.5)
    except (Exception, BaseException) as e:
        print('main', e)
    finally:
        time.sleep(60)


main()
