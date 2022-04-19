# @Description: 批量处理膨胀 程序入口版  无注释
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/13 23:01
import os
import time
import datetime
import json
import openpyxl
import pandas as pd
import requests


def init(res_path):
    if not os.path.exists(res_path):
        wk = openpyxl.Workbook()
        ws = wk.active
        ws.append(['手机号', '营销活动', '营销方式', '姓名', '主套餐', '入网时间', '余额', '用户状态', '近三个月均话费', '区县名称', '网格名称', '微网格名称'])
        wk.save(res_path)
    wk = openpyxl.load_workbook(res_path)
    return wk


def query_phone(phone_no, header, cookie):
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/blocks/sBscUsrInfoQry'
    HTTPJSONKEY = {"serviceno": phone_no}

    try:
        res_json = json.loads(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
    except:
        return False, '登录状态过期'

    if res_json['fail']:
        return False, res_json['resultdesc']
    details = res_json['object']

    return True, details


def query_activity(phone_no, mkname, header, cookie):
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/hxx/market/fuzzyMkcaseQry'

    HTTPJSONKEY = {"qunflag": "0", "phone_no": phone_no, "flag": "4", "markobj_type": "00", "mkname": mkname,
                   "mktype": "营销执行"}

    try:
        res_json = json.loads(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
    except:
        return False, '登录状态过期'

    if res_json['fail']:
        return False, res_json['resultdesc']
    activities = res_json['object']

    return True, activities


def query_means(phone_no, activity, header, cookie):
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/hxx/market/queryMkcaseWay'

    HTTPJSONKEY = {"phone": phone_no, "choose_act_id": activity['mkcaseid'],
                   "choose_cust_group_id": activity['cust_group_id'], "choose_channel_type": activity['channel_type'],
                   "choose_id_no": activity['id_no']}

    try:
        res_json = json.loads(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
    except:
        return False, '登录状态过期'

    if res_json['fail']:
        return False, res_json['resultdesc']
    means = res_json['object']
    target_means = ''
    for i in range(len(means)):
        if '当月生效' in means[i]['means_name']:
            target_means = means[i]['means_name']
            break
    if target_means == '':
        return False, '无' + '当月生效'
    return True, target_means

def query_means_detail(phone_no, means, header, cookie):



    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/hxx/market/queryMkcaseWayDetail'

    HTTPJSONKEY = {"means_id": means['means_id'], "choose_act_id": means['mkcaseid'], "yxzxflag": "YXZXFLAG",
                   "channel_type": means['channel_type'], "phone": phone_no}

    try:
        res_json = json.loads(requests.post(api_url, headers=header, cookies=cookie, json=HTTPJSONKEY).text)
    except:
        return False, '登录状态过期'

    if res_json['fail']:
        return False, res_json['resultdesc']
    means_detail = res_json['object']
    return True, means_detail

def query_details(phone_no, header, cookie):
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/personalhomepage/queryPersonal?phoneno=' + phone_no

    try:
        res_json = json.loads(requests.get(api_url, cookies=cookie).text)
    except:
        return False, '登录状态过期'

    if res_json['jsondata']['retVal']['resultcode'] == '0002':
        return False, '未查询到该用户信息'
    details = res_json['jsondata']['retVal']['resultlist'][0]
    return True, details


def get_res(phone, cookies, wk, ws, res_path):
    headers = {
        'Host': 'hxx.anhuiyidong.com.cn:9004',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; CDY-TN00 Build/HUAWEICDY-TN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36',
    }
    time.sleep(1.6)

    sign, phone_res = query_phone(phone, headers, cookies)
    if sign:

        sign, activity_res = query_activity(phone, '膨胀', headers, cookies)
        if sign:
            target_activity = ''
            for i in range(len(activity_res)):
                if ('膨胀' in activity_res[i]['mkname']) and ('无忧版' in activity_res[i]['mkname']):
                    target_activity = activity_res[i]
                    break

            if target_activity == '':
                return
            sign, means_res = query_means(phone, target_activity, headers, cookies)

            phone_details = [phone, target_activity['mkname'], means_res, phone_res['CUST_NAME'],
                             phone_res['PROD_PRC_NAME'], phone_res['OPEN_TIME'][:-6], float(phone_res['CUR_FEE']) / 100]
            if sign:
                sign, details_res = query_details(phone, headers, cookies)
                if sign:
                    phone_details.append(details_res['user_status_name'])
                    phone_details.append(details_res['three_avg_total_fee'])
                    phone_details.append(details_res['city_code'])
                    phone_details.append(details_res['area_code'])
                    phone_details.append(details_res['grid_code'])

                    # print(phone_details)
                    ws.append(phone_details)
                    wk.save(res_path)
    elif phone_res == '登录状态过期':
        print('***********************************')
        print('***********************************')
        print(phone_res)
        cookies['JSESSIONID'] = input('请输入状态码：').strip()
        time.sleep(10)


global cookies


def main():
    source_path = input('请输入excel文件路径:')
    cookies = {'JSESSIONID': ''}
    cookies['JSESSIONID'] = input('请输入状态码：').strip()
    start_time = datetime.datetime.now()
    print(start_time, 'Begin-----------------------')
    res_path = source_path.split('.')[0] + datetime.datetime.now().strftime('%Y%m%d %H-%M-%S') + '.xlsx'

    wk = init(res_path)

    df = pd.read_excel(source_path, header=None)

    phones = df[0].apply(str).values

    n = 0
    for phone in phones:
        # if n % 10 == 0:
        #     print(phone)
        get_res(phone, cookies, wk, wk.active, res_path)
        # n += 1
    end_time = datetime.datetime.now()
    total_time = str(end_time - start_time)
    print(end_time, 'Finish-----------------------共耗时', total_time)
