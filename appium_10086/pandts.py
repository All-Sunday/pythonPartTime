# @Description:
# @Author https://github.com/All-Sunday 1544781624 All-Sunday
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
        global ws
        ws = wk.active
        ws.append(['序号', '手机号', '营销活动', '营销方式', '姓名', '身份证号', '主套餐', '入网时间', '余额', '用户状态', '近三个月均话费', '区县名称', '网格名称',
                   '微网格名称'])
        wk.save(res_path)
    wk = openpyxl.load_workbook(res_path)
    return wk


def query_phone(phone_no, header, cookie):
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/blocks/sBscUsrInfoQry'
    HTTPJSONKEY = {"serviceno": phone_no}

    try:
        res_json = json.loads(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
    except (Exception, BaseException) as e:
        print(e)
        try:
            print(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY))
            print(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
        except (Exception, BaseException) as e:
            print(e)
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

    return True, means


def query_means_detail(phone_no, means, header, cookie):
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/hxx/market/queryMkcaseWayDetail'

    HTTPJSONKEY = {"means_id": means['means_id'], "choose_act_id": means['mkcaseid'], "yxzxflag": "YXZXFLAG",
                   "channel_type": means['channel_type'], "phone": phone_no}

    try:
        res_json = json.loads(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
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


def get_res(t_num, phone, cookies, keyword, activity, means, wk, res_path):
    headers = {
        'Host': 'hxx.anhuiyidong.com.cn:9004',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=' + cookies['JSESSIONID']
    }
    time.sleep(1.6)

    sign, phone_res = query_phone(phone, headers, cookies)
    if sign:

        sign, activity_res = query_activity(phone, keyword, headers, cookies)
        if sign:
            target_activity = ''
            for i in range(len(activity_res)):

                if activity_res[i]['mkname'].find(activity) == 0:
                    target_activity = activity_res[i]
                    break

            if target_activity == '':
                return
            sign, means_res = query_means(phone, target_activity, headers, cookies)

            if sign:
                target_means = None
                for i in range(len(means_res)):

                    if means_res[i]['means_name'].find(means) == 0:
                        target_means = means_res[i]
                        break
                if target_means is not None:

                    sign, means_detail_res = query_means_detail(phone, target_means, headers, cookies)

                    if sign:
                        phone_details = [t_num, phone, target_activity['mkname'], target_means['means_name'],
                                         phone_res['REL_CUST_NAME'], phone_res['REL_ID_ICCID'],
                                         phone_res['PROD_PRC_NAME'], phone_res['OPEN_TIME'][:-6],
                                         float(phone_res['CUR_FEE']) / 100]
                        sign, details_res = query_details(phone, headers, cookies)
                        if sign:
                            phone_details.extend([details_res['user_status_name'], details_res['three_avg_total_fee'],
                                                  details_res['city_code'], details_res['area_code'],
                                                  details_res['grid_code']])
                            global ws
                            # todo 加锁
                            mutex.acquire()
                            ws.append(phone_details)
                            mutex.release()

    elif phone_res == '登录状态过期':
        # wk.save(res_path)
        print('***********************************')
        print('***********************************')
        print(phone_res)
        global stop_threads
        stop_threads = True
        # time.sleep(10000)


global cookies


def sql_thread(times):
    last_time = int(time.time())
    while True:
        time.sleep(30)
        seleninm.sql_update(times)
        if stop_threads:
            if not seleninm.db.is_closed():
                seleninm.db.close()
            break
        if int(time.time()) - last_time > 1800:
            last_time = int(time.time())
            if not seleninm.db.is_closed():
                seleninm.db.close()


mutex = threading.Lock()
t_num = 0
ws = None  # 全局变量 加锁

def test(index, phones, cookies, keyword, activity, means, wk, res_path):
    global t_num

    phones_num = len(phones)
    while t_num < phones_num:
        if stop_threads:
            break
        mutex.acquire()
        phone = phones[t_num]
        t_num += 1
        mutex.release()

        get_res(t_num, phone, cookies, keyword, activity, means, wk, res_path)
    if not stop_threads:
        global stop_threads
        stop_threads = True

def stop_all_threads():
    while True:
        key = input('请输入stop以停止运行：').strip()
        if key == 'stop':
            global stop_threads
            stop_threads = True
            print('stop中...')
            time.sleep(20000)
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

            print('******' + res)
            if not seleninm.db.is_closed():
                seleninm.db.close()
                return 0

    else:
        if not seleninm.db.is_closed():
            seleninm.db.close()

    global stop_threads
    stop_threads = False
    t1 = threading.Thread(target=sql_thread, args=(run.times,))
    if not seleninm.db.is_closed():
        seleninm.db.close()
    t1.start()
    wk = None
    global ws
    # ws = None
    res_path = None
    try:
        source_path = input('请输入excel文件路径:').strip()
        cookies = {'JSESSIONID': ''}
        cookies['JSESSIONID'] = input('请输入状态码：').strip()
        keyword = input('请输入要搜索的活动名：').strip()
        activity = input('请输入要选择的活动名：').strip()
        means = input('请输入要选择的营销方式名：').strip()

        thread_num = int(input('请输入同时启动的线程数量：').strip())
        threads = []

        start_time = datetime.datetime.now()
        print(start_time, 'Begin-----------------------')
        res_path = source_path.split('.')[0] + datetime.datetime.now().strftime('%Y%m%d %H-%M-%S') + '.xlsx'

        wk = init(res_path)

        df = pd.read_excel(source_path, header=None)

        phones = df[0].apply(str).values

        global ws
        ws = wk.active
        for i in range(thread_num):
            t = threading.Thread(target=test,
                                 args=(i + 1, phones, cookies, keyword, activity, means, wk, res_path))
            threads.append(t)

        for t in threads:
            t.start()
            time.sleep(0.5)

        t2 = threading.Thread(target=stop_all_threads)
        t2.start()

        while len(threading.enumerate()) != 2:
            time.sleep(1)
        print('stop中...')
    except (Exception, BaseException) as e:
        print(e)
        return -1
    finally:
        global stop_threads
        stop_threads = True
        wk.save(res_path)
        print('数据保存成功！')
        if not seleninm.db.is_closed():
            seleninm.db.close()

    end_time = datetime.datetime.now()
    total_time = str(end_time - start_time)
    print(end_time, 'Finish-----------------------共耗时', total_time)
    return 1
