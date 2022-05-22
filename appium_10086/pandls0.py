# @Description:  限制主机 限制不同主机也只允许一个运行
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/13 23:01

import os
import threading
import time
import datetime
import json
import seleninm
import openpyxl
import license
import pandas as pd
import requests


def init(res_path):
    if not os.path.exists(res_path):
        wk = openpyxl.Workbook()
        ws = wk.active
        ws.append(['手机号', '营销活动', '营销方式', '姓名', '身份证号', '主套餐', '入网时间', '余额', '用户状态', '近三个月均话费', '区县名称', '网格名称', '微网格名称'])
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
    print(res_json)
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
    print(res_json)
    if res_json['fail']:
        return False, res_json['resultdesc']
    means = res_json['object']

    return True, means


def query_means_detail(phone_no, means, header, cookie):
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/hxx/market/queryMkcaseWayDetail'

    HTTPJSONKEY = {"means_id": means['means_id'], "choose_act_id": means['mkcaseid'], "yxzxflag": "YXZXFLAG",
                   "channel_type": means['channel_type'], "phone": phone_no}
    # print(HTTPJSONKEY)
    # print(header)
    # print(requests.post(api_url, headers=header, cookies=cookie, json=HTTPJSONKEY))
    # print(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
    try:
        # res_json = json.loads(requests.post(api_url, headers=header, cookies=cookie, json=HTTPJSONKEY).text)
        res_json = json.loads(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
    except:
        return False, '登录状态过期'
    print(res_json)
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


def get_res(phone, cookies, keyword, activity, means, wk, ws, res_path):
    headers = {
        'Host': 'hxx.anhuiyidong.com.cn:9004',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=' + cookies['JSESSIONID']
    }
    time.sleep(1.6)

    sign, phone_res = query_phone(phone, headers, cookies)
    if sign:

        # sign, activity_res = query_activity(phone, '膨胀', headers, cookies)
        sign, activity_res = query_activity(phone, keyword, headers, cookies)
        if sign:
            target_activity = ''
            for i in range(len(activity_res)):
                # if ('膨胀' in activity_res[i]['mkname']) and ('无忧版' in activity_res[i]['mkname']):
                # if activity in activity_res[i]['mkname']:
                if activity_res[i]['mkname'].find(activity) == 0:
                    target_activity = activity_res[i]
                    break

            if target_activity == '':
                return
            sign, means_res = query_means(phone, target_activity, headers, cookies)

            if sign:
                target_means = None
                for i in range(len(means_res)):
                    # if '当月生效' in means_res[i]['means_name']:
                    # if means in means_res[i]['means_name']:
                    if means_res[i]['means_name'].find(means) == 0:
                        target_means = means_res[i]
                        break
                if target_means is not None:
                    # return False, '无' + '当月生效'

                    sign, means_detail_res = query_means_detail(phone, target_means, headers, cookies)

                    if sign:
                        phone_details = [phone, target_activity['mkname'], target_means['means_name'],
                                         phone_res['REL_CUST_NAME'],phone_res['REL_ID_ICCID'],
                                         phone_res['PROD_PRC_NAME'], phone_res['OPEN_TIME'][:-6],
                                         float(phone_res['CUR_FEE']) / 100]
                        sign, details_res = query_details(phone, headers, cookies)
                        if sign:
                            phone_details.extend([details_res['user_status_name'], details_res['three_avg_total_fee'],
                                                  details_res['city_code'], details_res['area_code'],
                                                  details_res['grid_code']])
                            # phone_details.append(details_res['user_status_name'])
                            # phone_details.append(details_res['three_avg_total_fee'])
                            # phone_details.append(details_res['city_code'])
                            # phone_details.append(details_res['area_code'])
                            # phone_details.append(details_res['grid_code'])

                            # print(phone_details)
                            ws.append(phone_details)
                            wk.save(res_path)
    elif phone_res == '登录状态过期':
        print('***********************************')
        print('***********************************')
        print(phone_res)
        time.sleep(10000)


global cookies


def sql_thread(run):


    while True:
        time.sleep(10)
        seleninm.sql_update(run)
        if stop_threads:
            if not seleninm.db.is_closed():
                seleninm.db.close()
            break


def main():
    try:
        sign, run = seleninm.sql_start()
    except:
        print('******出错')
        return -1
    if sign:
        sign, res = license.start()
        if not sign:

            # else:
            print('******' + res)
            if not seleninm.db.is_closed():
                seleninm.db.close()
                return 0

    else:
        if not seleninm.db.is_closed():
            seleninm.db.close()
            return 0
    global stop_threads
    stop_threads = False
    t1 = threading.Thread(target=sql_thread, args=(run,))
    t1.start()
    time.sleep(60)
    try:
        source_path = input('请输入excel文件路径:').strip()
        # i = 1 / 0
        cookies = {'JSESSIONID': ''}
        cookies['JSESSIONID'] = input('请输入状态码：').strip()
        keyword = input('请输入要搜索的活动名：').strip()
        activity = input('请输入要选择的活动名：').strip()
        means = input('请输入要选择的营销方式名：').strip()

        start_time = datetime.datetime.now()
        print(start_time, 'Begin-----------------------')
        res_path = source_path.split('.')[0] + datetime.datetime.now().strftime('%Y%m%d %H-%M-%S') + '.xlsx'

        wk = init(res_path)

        df = pd.read_excel(source_path, header=None)

        phones = df[0].apply(str).values


        for phone in phones:
            get_res(phone, cookies, keyword, activity, means, wk, wk.active, res_path)
    except (Exception, BaseException) as e:
        print(e)
        return -1
    finally:
        if not seleninm.db.is_closed():
            seleninm.db.close()
        stop_threads = True
    end_time = datetime.datetime.now()
    total_time = str(end_time - start_time)
    print(end_time, 'Finish-----------------------共耗时', total_time)
    return 1
