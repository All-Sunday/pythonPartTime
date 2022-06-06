import json
import random
import time
from thresd import *
import requests
from fake_useragent import UserAgent
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


def order_processor(commodity_dict, mode):
    sign, key_res = query_youyou_key(commodity_dict)
    print(sign, key_res)
    if sign:
        sign, order_res = query_youyou_order(commodity_dict, key_res, mode)
        return sign, order_res
    else:
        return sign, key_res


def query_youyou(target_data, header, ua):
    header['User-Agent'] = ua.random
    sign = False
    mode = target_data.mode
    if target_data.mode == '21':
        sign2, commodity_dict2 = query_youyou_detail1(target_data, header, '1')
        time.sleep(0.5 + random.randint(1, 5) / 10)
        sign1, commodity_dict1 = query_youyou_detail1(target_data, header, '2')

        if sign1 and sign2:
            if str(commodity_dict1['Id']) == str(commodity_dict2['Id']):

                sign, commodity_dict, mode = True, commodity_dict2, '1'
            else:
                # print('租赁', commodity_dict2)
                # print('出售', commodity_dict1)

                sign2, key_res2 = order_processor(commodity_dict2, '1')
                sign1, key_res1 = order_processor(commodity_dict1, '2')
                if sign1 and sign2:
                    return True, '7'
                elif sign2:
                    return True, '5'
                elif sign1:
                    return True, '6'
                else:
                    return sign1, key_res1 + key_res2
        elif (not sign1) and sign2:
            sign, commodity_dict, mode = sign2, commodity_dict2, '3'
        elif (not sign2) and sign1:
            sign, commodity_dict, mode = sign1, commodity_dict1, '4'
        else:
            sign, commodity_dict = sign1, commodity_dict1 + commodity_dict2
    else:
        sign, commodity_dict = query_youyou_detail1(target_data, header, mode)
    if sign:
        # print('商品匹配，开始下单', commodity_dict)
        sign, key_res = order_processor(commodity_dict, mode)
        return sign, key_res
    else:
        return False, str(target_data.name) + commodity_dict


def query_youyou_detail1(data, header, mode):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'

    HTTPJSONKEY = {"templateId": str(data.yid), "pageSize": 5, "pageIndex": 1, "sortType": 1, "listSortType": 1,
                   "listType": 10}

    if mode == '1':
        HTTPJSONKEY = {"templateId": str(data.yid), "pageSize": 5, "pageIndex": 1, "sortType": 1, "listSortType": 4,
                       "listType": 30}

    try:
        res_json = json.loads(requests.post(api_url, headers=header, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_detail1', e)
        return False, 'youyou_detail1请求错误' + str(e)

    if res_json['Msg'] != 'success':
        return False, res_json['Msg']

    templateInfo = res_json['Data']['TemplateInfo']
    # if templateInfo['CommodityName'] not in commodity_dict:
    if templateInfo['CommodityName'] != data.name:
        return False, 'UUid,' + str(data.yid) + '(' + templateInfo['CommodityName'] + ')与excel名称(' + data.name + ')不匹配'

    if res_json['Data']['CommodityList'] is None:
        return False, '无商品'

    commodity = res_json['Data']['CommodityList'][0]
    if mode == '1':
        if eval(commodity['LeaseDeposit']) != eval(data.price1):
            return False, '目前最低押金 ' + commodity['LeaseDeposit'] + ' 与源押金 ' + data.price1 + ' 不符'
    else:
        if eval(commodity['Price']) != eval(data.price2):
            return False, '目前最低售价 ' + commodity['Price'] + ' 与源售价 ' + data.price2 + ' 不符'

    return True, res_json['Data']['CommodityList'][0]


def query_youyou_key(commodity_dict):
    api_url = 'https://api.youpin898.com/api/youpin/detect/detection/2/624740/' + str(commodity_dict['Id']) + '/app'
    headers_app = {'Host': 'api.youpin898.com',
                   'Connection': 'close',
                   'AppType': '7',
                   'User-Agent': 'okhttp/3.14.9',
                   'Accept-Encoding': 'gzip'}
    try:
        res_json = json.loads(requests.get(api_url, headers=headers_app).text)
    except (Exception, BaseException) as e:
        print('youyou_key', e)
        return False, 'youyou_key请求错误' + str(e)
    if res_json['msg'] != '成功':
        return False, res_json['msg']
    return True, res_json['data']['key']


def query_youyou_order(commodity_dict, key, mode):
    headers_app = {'Host': 'api.youpin898.com',
                   'Connection': 'close',
                   'AppType': '7',
                   'Content-Type': 'application/json; charset=utf-8',
                   'User-Agent': 'okhttp/3.14.9',
                   'Accept-Encoding': 'gzip'}
    if (mode == '2') or (mode == '4'):
        api_url = 'https://api.youpin898.com/api/trade/Cashier/PlaceOrder'

        HTTPJSONKEY = {"Id": commodity_dict['Id'], "OriginalPrice": commodity_dict['Price'], "key": key,
                       "UserId": 624740}

    else:
        api_url = 'https://api.youpin898.com/api/trade/Cashier/LeaseOutPlaceOrder'

        HTTPJSONKEY = {"IsSubsidy": 0, "IsUseFixedQuota": 0, "IsUseQuota": 0,
                       "OriginalLeaseDeposit": commodity_dict['LeaseDeposit'],
                       "OriginalLeaseMaxDays": commodity_dict['LeaseMaxDays'],
                       "OriginalLeaseUnitPrice": commodity_dict['LeaseUnitPrice'],
                       "OriginalLongLeaseDays": 21,
                       "OriginalLongLeaseUnitPrice": commodity_dict['LongLeaseUnitPrice'],
                       "OriginalPrice": commodity_dict['Price'], "OriginalSubsidyMaxDays": 0,
                       "TemporaryQuotaPrice": 0, "Id": commodity_dict['Id'], "JumpUiType": commodity_dict['Type'],
                       "Key": key,
                       "LeaseDays": commodity_dict['LeaseMaxDays'] if 30 > commodity_dict['LeaseMaxDays'] else 30,
                       "UserId": 624740}
        # if commodity_dict['LeaseGiveConfigs']:
        if commodity_dict['LeaseGiveConfigs'] is not None:
            if len(commodity_dict['LeaseGiveConfigs']) == 1:
                i = 0
            else:
                i = 0 if HTTPJSONKEY["LeaseDays"] < commodity_dict['LeaseGiveConfigs'][1]['leaseDays'] else 1
            HTTPJSONKEY["leaseGiveConfigId"] = commodity_dict['LeaseGiveConfigs'][i]['id']
    try:
        res_json = json.loads(requests.post(api_url, headers=headers_app, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_order', e)
        return False, 'youyou_order请求错误' + str(e)
    if res_json['Msg'] != '下单成功':
        return False, res_json['Msg']

    # return True, res_json['Data']['OrderNo']
    return True, mode


ua = UserAgent(path=r"fake_useragent.json")
headers_youpin = {'Host': 'api.youpin898.com',
                  'Connection': 'close',
                  'AppType': '1',
                  'Content-Type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain, */*',
                  'User-Agent': ua.random, 'Origin': 'https://youpin898.com', 'Sec-Fetch-Site': 'same-site',
                  'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://youpin898.com/',
                  'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7'}

while True:
    res = query(6, 0)
    if res is not None:
        update(res, -2)  # 开始处理
        # print('u')

        sign, yy_res = query_youyou(res, headers_youpin, ua)
        if not sign:
            print(res.name, '下单失败', res.msg)
            if '频繁' in yy_res:
                time.sleep(15)
            elif '待支付' in yy_res:
                time.sleep(45)
            elif yy_res != '无商品':
                print(sign, yy_res)
                send_mail('下单error', yy_res + res.msg)
                update(res, -1)
        else:
            if yy_res == '1':
                o = '租赁成功'
            elif yy_res == '2':
                o = '买入成功'
            elif yy_res == '3':
                o = '租赁成功（买入信息获取失败）'
            elif yy_res == '4':
                o = '买入成功（租赁信息获取失败）'
            elif yy_res == '5':
                o = '租赁成功（买入失败）'
            elif yy_res == '6':
                o = '买入成功（租赁失败）'
            elif yy_res == '7':
                o = '租赁+买入成功'
            print(res.name, o, res.msg)
            sign, eamil_res = send_mail(res.name + o, res.msg)
            print(sign, eamil_res)
            update(res, int(yy_res))
    else:
        time.sleep(0.1)