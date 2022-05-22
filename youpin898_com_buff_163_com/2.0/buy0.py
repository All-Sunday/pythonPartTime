# @Description: 下单 不停地查询数据库 符合条件的下单 根据验证码登录获取auth （客户auth会失效 舍弃）
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/14 20:47
# @File : buy.py

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
    # sender_username = 'MrSunday1' + '@163.com'
    # pwd = 'XWNRJMELACZEFSTR'
    # receiver = ['1544781624@qq.com']
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
    # time.sleep(100)
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
                # 最低押金 最低售价 是同一件商品 -> 租赁
                sign, commodity_dict, mode = True, commodity_dict2, '1'
            else:
                print('租赁', commodity_dict2)
                print('出售', commodity_dict1)
                # 不是同一件商品  租赁 + 买入
                sign2, key_res2 = order_processor(commodity_dict2, '1')
                sign1, key_res1 = order_processor(commodity_dict1, '2')
                if sign1 and sign2:
                    return True, '7'
                elif sign2:
                    return True, '5'  # 租赁+买入 同时下单 但只租赁成功
                elif sign1:
                    return True, '6'
                else:
                    return sign1, key_res1 + key_res2
        elif (not sign1) and sign2:
            sign, commodity_dict, mode = sign2, commodity_dict2, '3'  # 租赁、买入都可 需对比是否是同一商品 但有买入商品获取失败  但只有租赁
        elif (not sign2) and sign1:
            sign, commodity_dict, mode = sign1, commodity_dict1, '4'
        else:
            sign, commodity_dict = sign1, commodity_dict1 + commodity_dict2
    else:
        sign, commodity_dict = query_youyou_detail1(target_data, header, mode)
    if sign:
        print('商品匹配，开始下单', commodity_dict)
        sign, key_res = order_processor(commodity_dict, mode)
        return sign, key_res
    else:
        return False, str(target_data.name) + commodity_dict


def query_youyou0(target_data, header, ua):
    # print(target_data.price1, type(target_data.price1))
    # time.sleep(100)
    header['User-Agent'] = ua.random
    sign, commodity_dict = query_youyou_detail1(target_data, header)
    if sign:
        print(commodity_dict)
        sign, key_res = query_youyou_key(commodity_dict)
        print(sign, key_res)
        # time.sleep(100)
        if sign:
            sign, order_res = query_youyou_order(commodity_dict, key_res, target_data.mode)
            return sign, order_res
        else:
            return sign, key_res
        # return True, commodity_dict
    else:
        return False, str(target_data.yid) + commodity_dict


# def query_youyou_detail1(data, header):
def query_youyou_detail1(data, header, mode):
    api_url = 'https://api.youpin898.com/api/homepage/es/commodity/GetCsGoPagedList'
    # 出售 售价递增
    HTTPJSONKEY = {"templateId": str(data.yid), "pageSize": 5, "pageIndex": 1, "sortType": 1, "listSortType": 1,
                   "listType": 10}

    # if (data.mode == '21') and (data.price1 < data.price2):
    # if data.mode == '21':
    if mode == '1':
        # 租赁 押金递增
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

    # if data.mode == '21':
    commodity = res_json['Data']['CommodityList'][0]
    if mode == '1':
        # if eval(templateInfo['LeaseDeposit']) != eval(data.price1): # templateInfo不一定及时 不够准确
        if eval(commodity['LeaseDeposit']) != eval(data.price1):
            return False, '目前最低押金 ' + commodity['LeaseDeposit'] + ' 与源押金 ' + data.price1 + ' 不符'
    else:
        # if eval(templateInfo['MinPrice']) != eval(data.price2):
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
        if commodity_dict['LeaseGiveConfigs']:
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


def query_youyou_todo(auth):
    api_url = 'https://api.youpin898.com/api/user/Account/ToDoList'
    headers_app = {'Host': 'api.youpin898.com',
                   # 'Connection': 'close',
                   'AppType': '7',
                   'Authorization': auth,
                   'User-Agent': 'okhttp/3.14.9',
                   'Accept-Encoding': 'gzip'}
    try:
        res_json = json.loads(requests.get(api_url, headers=headers_app).text)
    except (Exception, BaseException) as e:
        print('youyou_todo', e)
        return False, 'youyou_todo请求错误' + str(e)
    if 'Msg' in res_json:
        if res_json['Msg'] != '请求成功':
            return False, res_json['Msg']
        return True, True if len(res_json['Data']) == 0 else False
    else:
        if res_json['msg'] != '请求成功':
            return False, res_json['msg']


def query_youyou_auth0(id):
    api_url = 'https://api.youpin898.com/api/youpin/detect/detection/2/624740/' + id + '/app'
    headers_app = {'Host': 'api.youpin898.com',
                   'Connection': 'close',
                   'AppType': '7',
                   'User-Agent': 'okhttp/3.14.9',
                   'Accept-Encoding': 'gzip'}
    try:
        print(requests.get(api_url, headers=headers_app).headers)
        print(requests.get(api_url, headers=headers_app).cookies.keys())
        time.sleep(1000)
        res_json = json.loads(requests.get(api_url, headers=headers_app).text)
    except (Exception, BaseException) as e:
        print('youyou_key', e)
        return False, 'youyou_key请求错误' + str(e)
    if res_json['msg'] != '成功':
        return False, res_json['msg']
    return True, res_json['data']['key']


def query_youyou_auth():
    api_url = 'https://api.youpin898.com/api/user/Auth/SendSignInSmsCode'
    headers_app = {'Host': 'api.youpin898.com',
                   'Connection': 'Keep-Alive',
                   'AppType': '7',

                   'Accept-Encoding': 'gzip',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Authorization': 'Bearer',
                   'Content-Type': 'application/json;charset=utf-8'}
    HTTPJSONKEY = {"RegTime": 0, "Code": "", "Mobile": "15653329103", "Sessionid": "Yl4y9voswYADAJw3ALopAgtf"}
    try:
        res_json = json.loads(requests.post(api_url, headers=headers_app, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_SmsCode', e)
        return False, 'youyou_SmsCode请求错误' + str(e)
    if res_json['Msg'] != '发送成功':
        return False, res_json['Msg']

    return True, res_json['Msg']


def query_youyou_sign(code):
    api_url = 'https://api.youpin898.com/api/user/Auth/SmsSignIn'
    headers_app = {'Host': 'api.youpin898.com',
                   'Connection': 'close',
                   'AppType': '7',

                   'Accept-Encoding': 'gzip',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Authorization': 'Bearer',
                   'Content-Type': 'application/json;charset=utf-8'}
    HTTPJSONKEY = {
        # "DeviceName": "samsung SM-G9550",
        "Code": code, "Mobile": "15653329103",
        'Sessionid': 'Yl4y9voswYADAJw3ALopAgtf'}
    try:
        res_json = json.loads(requests.post(api_url, headers=headers_app, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print('youyou_sign', e)
        return False, 'youyou_sign请求错误' + str(e)
    if res_json['Msg'] != '登录成功':
        return False, res_json['Msg']

    return True, res_json['Data']['Token']


def get_auth():
    while True:
        with open("code.txt", "r") as f:
            i = f.readline().strip()
            print(i)
            if i == '1':
                break
            time.sleep(5)
    print('i')
    sign, auth = query_youyou_auth()
    print(sign, auth)

    if sign:

        with open("code.txt", "w") as f:
            f.write('覆盖输入验证码')
        print('iii')
        while True:
            with open("code.txt", "r") as f:
                i = f.readline().strip()
                if not i.isdigit():
                    time.sleep(5)
                    continue
                else:
                    print(i, type(i))
                    break
                # if not isinstance(i, int):
                #
                # else:
                #     break
        print('iiiio')
        sign, auth = query_youyou_sign(i)
        print(sign, auth)
        return sign, 'Bearer ' + auth
    else:
        if '频繁' in auth:
            time.sleep(3600)
        return sign, auth


ua = UserAgent(path=r"fake_useragent.json")
headers_youpin = {'Host': 'api.youpin898.com',
                  'Connection': 'close',
                  'AppType': '1',
                  'Content-Type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain, */*',
                  'User-Agent': ua.random, 'Origin': 'https://youpin898.com', 'Sec-Fetch-Site': 'same-site',
                  'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://youpin898.com/',
                  'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7'}

# print(2 if 5>2 else 5)
# time.sleep(100)
# insert(['摩托手套（★） | 薄荷 (崭新出厂)', '55916', 88888.0, 85555.0, '摩托手套（★） | 薄荷 (崭新出厂) 售价为85555.0，buff为86666\n', '2', int(time.time())])

# 我的账号目前可以持久用
autho = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlOTQ4NDMwMTVmNDA0YzdjOTA5ZmI0ZTcyNmE1YjdlNiIsIm5hbWVpZCI6Ijk4NjY2NiIsIklkIjoiOTg2NjY2IiwidW5pcXVlX25hbWUiOiJZUDAwMDA5ODY2NjYiLCJOYW1lIjoiWVAwMDAwOTg2NjY2IiwibmJmIjoxNjUyMzQ5MDU5LCJleHAiOjE2NTMyMTMwNTksImlzcyI6InlvdXBpbjg5OC5jb20iLCJhdWQiOiJ1c2VyIn0.tLg0WHT6eb2wmQGLCTuUaFLZt30Oh4lEJraFjC3CMyI'
# autho = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmNWFiZDQyMDQ2NGM0YjUxYTQxNWJjZGJiNGZiMmRmOCIsIm5hbWVpZCI6Ijk4NjY2NiIsIklkIjoiOTg2NjY2IiwidW5pcXVlX25hbWUiOiJZUDAwMDA5ODY2NjYiLCJOYW1lIjoiWVAwMDAwOTg2NjY2IiwibmJmIjoxNjUyNzA3NzE1LCJleHAiOjE2NTI3MDk1MTUsImlzcyI6InlvdXBpbjg5OC5jb20iLCJhdWQiOiJ1c2VyIn0.9e-9hDBcVbRd5Gp6kBhOd7RFW7H9cQnzLfKrPOM0aC4'

# 客户的auth会失效 初步怀疑是绑定了steam的账号和不绑定的不一样机制
# autho = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjMWQzYTQ5MDVmZjc0Yjg5OTA2YTg4YjhmMTY0YmUwMCIsIm5hbWVpZCI6IjYyNDc0MCIsIklkIjoiNjI0NzQwIiwidW5pcXVlX25hbWUiOiLlhajoh6rnlKjnp5Llj5Hlj6rnp5_kuI3lh7rllK4iLCJOYW1lIjoi5YWo6Ieq55So56eS5Y-R5Y-q56ef5LiN5Ye65ZSuIiwibmJmIjoxNjUyNzA5MTI5LCJleHAiOjE2NTI3MTA5MjksImlzcyI6InlvdXBpbjg5OC5jb20iLCJhdWQiOiJ1c2VyIn0.iKoMrBdaOlmbmqQ8k7DT59i_HCm9mYO5xyVqx8mOMUE'
# autho = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjNGJjOTJiMGZmOWE0NDIzYTJmZDE1NmI2NDE0MzYxNyIsIm5hbWVpZCI6IjYyNDc0MCIsIklkIjoiNjI0NzQwIiwidW5pcXVlX25hbWUiOiLlhajoh6rnlKjnp5Llj5Hlj6rnp5_kuI3lh7rllK4iLCJOYW1lIjoi5YWo6Ieq55So56eS5Y-R5Y-q56ef5LiN5Ye65ZSuIiwibmJmIjoxNjUyNzAzNjczLCJleHAiOjE2NTI3MDU0NzMsImlzcyI6InlvdXBpbjg5OC5jb20iLCJhdWQiOiJ1c2VyIn0.tTGmVnmv65EoGqFOElc0LDUsLX3IHmswqAZvGiCbxtA'
sign, todo_res = query_youyou_todo(autho)
print(sign, todo_res)
if (not sign) and (todo_res == '非法的accessToken'):
    print('s')
    # send_mail('需要登陆才能下单', '请尽快输入验证码')
    # autho = query_youyou_auth(random.choice(['6016004', '5248222', '5917624', '', '', '', '', ]))
    while True:
        sign, autho = get_auth()
        if sign:
            print(autho)
            break
while True:
    res = query(6, 0)
    if res is not None:
        update(res, -2)  # 开始处理
        sign, todo_res = query_youyou_todo(autho)
        print(sign, todo_res)
        if (not sign) and (todo_res == '非法的accessToken'):
            print('s')
            send_mail('需要登陆才能下单', '请尽快输入验证码')
            # autho = query_youyou_auth(random.choice(['6016004', '5248222', '5917624', '', '', '', '', ]))
            while True:
                sign, autho = get_auth()
                if sign:
                    print(autho)
                    break
            sign, todo_res = query_youyou_todo(autho)
        print('u')
        # time.sleep(100)
        if sign and todo_res:

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
                send_mail(res.name + o, res.msg)
                update(res, int(yy_res))

        # else:
        # update(res, 1)
        # send_mail()

        else:
            print(todo_res)
            send_mail('下单error', todo_res)
            break
    else:
        time.sleep(0.1)
    # else:
    #     print('无需下单')
