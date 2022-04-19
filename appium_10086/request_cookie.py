# @Description: api测试
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/15 23:01
# @File : request_cookie.py

import time
import datetime
import json
# import openpyxl
import requests


# 查询号码余额 及 号码是否存在且可用
def query_phone0(phone_no, header, cookie):
    # {
    #     "checkcode": "SUCCESS",
    #     "checklist": [],
    #     "fail": false,
    #     "object": {
    #         "checkcode": "SUCCESS",
    #         "checklist": [],
    #         "cust_name": "＊＊璐",
    #         "realbalancefee": "16.92"
    #     },
    #     "resultcode": "SUCCESS",
    #     "resultdesc": "SUCCESS!",
    #     "resultlist": [],
    #     "resultlistString": "",
    #     "success": true
    # }

    # 余额
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/tetephonepay/GBQ_ChargeInfo?phone_no=' + phone_no
    # api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/tetephonepay/GBQ_ChargeInfo?phone_no=13855996258&token=bbc75e83-1f07-4ba4-840f-cd2fc8511098'

    # j = requests.get(api_url, cookies=cookie).text
    # print(requests.get(api_url, cookies=cookie))
    # print(j)

    try:
        res_json = json.loads(requests.get(api_url, cookies=cookie).text)
    except:
        return False, '登录状态过期'
    print(res_json)
    # json_dicts = json.dumps(res_json, indent=4, ensure_ascii=False)
    # print(json_dicts)
    if res_json['fail']:
        return False, res_json['resultdesc']
    realbalancefee, name = res_json['object']['realbalancefee'], res_json['object']['cust_name']
    print(name, realbalancefee)
    return True, name, realbalancefee  # 名字 余额


# 查询号码余额 及 号码是否存在且可用  及 入网时间等
def query_phone(phone_no, header, cookie):
    # {
    #     "checkcode": "SUCCESS",
    #     "checklist": [],
    #     "fail": false,
    #     "object": {
    #         "RENT_DATE": "20180524203221",
    #         "CREDIT": "0",
    #         "CUST_ID": "19320001105772",
    #         "OWNER_TYPE": "1",
    #         "SIM_NO": "898600E1123205597455",
    #         "JELLY_MONTH": "",
    #         "VIP_CARD_NO": "1",
    #         "INTERNET_ACCESS": "",
    #         "CREDIT_CODE": "01",
    #         "BLONG_AREA": "黄山",
    #         "CREATE_LOGIN": "J0B245001",
    #         "PHONE_NO": "18705592233",
    #         "PROD_NAME": "任我用套餐2",
    #         "STOP_RENT_DATE": "20991231000000",
    #         "OLD_RUN": "C",
    #         "BAK_FIELD": "0",
    #         "CMD_RIGHT": "0",
    #         "OP_TIME": "20220301135233",
    #         "EFF_DATE": "",
    #         "PHOTO_FLAG": "N",
    #         "LIMIT_OWE": "0",
    #         "USER_LEVEL": "普通客户",
    #         "USER_ROLE_NAME": "融合群主角",
    #         "OPEN_TIME": "20180524203012",
    #         "VIP_CREATE_TYPE": "0",
    #         "BILL_MODE_NAME": "后付费",
    #         "CUR_SCORE": 6318,
    #         "STAR_LEVEL": "5",
    #         "GROUP_ID": "119054502",
    #         "RUN_TIME": "20210702141841",
    #         "OWNED_CHNL_ID": "119054502",
    #         "CREATE_DATE": "20180524203012",
    #         "IN_GROUP_NAME": "",
    #         "OWED_FLAG": "Y",
    #         "BILL_TYPE": "11",
    #         "USER_APPR_INFO": "已审核",
    #         "COMPLETED_DATE": "20180524203221",
    #         "ACCESS_TYPE": "002",
    #         "REL_CUST_NAME": "34292119",
    #         "CUR_FEE": "19252.0",
    #         "REGISTER_LEVEL": "F",
    #         "REAL_USE_NAME": "屯溪区",
    #         "PRODPRCINS_ID": "29004078249700",
    #         "SERVICE_GROUP": "119054502",
    #         "ID_NO": "19310005836611",
    #         "LOGIN_NO": "Y18610213",
    #         "JELLY_STATE": "",
    #         "PASSWD_TYPE": "1",
    #         "BILL_END_TIME": "20991231000000",
    #         "LOGIN_ACCEPT": "30006737414064",
    #         "MAIN_STATUS_CASH": "100",
    #         "RUN_CODE": "A",
    #         "CARD_TYPE": "1",
    #         "ASSURE_FLAG": "0",
    #         "GRADE_FLAG": "是",
    #         "ID_TYPE": "1",
    #         "CONTRACT_NO": "19410005985373",
    #         "NET_NO": "JJ002531819",
    #         "BILLING_CYCLE_TYPE_ID": "0",
    #         "BRAND_ID": "002",
    #         "RUN_NAME": "正常",
    #         "PROD_PRC_NAME": "全球通任我用198元（2018版）",
    #         "MASTER_SERV_NAME": "G网",
    #         "PROD_PRCID": "CP18W808",
    #         "PROD_ID": "CP18W8",
    #         "BILL_START_TIME": "20180524211419",
    #         "GROUP_FLAG": "N",
    #         "OP_CODE": "1114",
    #         "IS_4G": "否",
    #         "OPEN_NAME": "屯溪区",
    #         "USER_GRADE_CODE": "03",
    #         "CREATE_FLAG": "Y",
    #         "USER_PASSWD": "1fd8c477d83e80665a1f247451f2e44516142a88",
    #         "GROUP_NAME": "黄山",
    #         "MASTER_SERV_ID": "1001",
    #         "GROUP_LIMIT_OWE": 0.0,
    #         "FLAG_NAME": "正常",
    #         "BRAND_NAME": "全球通金卡",
    #         "STOP_FLAG": "Y",
    #         "FIRST_USEDATE": "20180524211419",
    #         "REL_ID_ICCID": "341024199206159529",
    #         "CUST_NAME": "＊＊露",
    #         "FINISH_FLAG": "N"
    #     },
    #     "resultcode": "SUCCESS",
    #     "resultlist": [],
    #     "resultlistString": "",
    #     "success": true
    # }

    # 入网时间等
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/blocks/sBscUsrInfoQry'
    HTTPJSONKEY = {"serviceno": phone_no}

    # j = requests.get(api_url, cookies=cookie).text
    # print(requests.get(api_url, cookies=cookie))
    # print(j)

    try:
        res_json = json.loads(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
    except:
        return False, '登录状态过期'
    # print(res_json)
    json_dicts = json.dumps(res_json, indent=4, ensure_ascii=False)
    print(json_dicts)
    if res_json['fail']:
        return False, res_json['resultdesc']
    details = res_json['object']
    # print(details)
    return True, details  # 返回入网时间等详细信息dict


# 查询营销活动
def query_activity(phone_no, mkname, header, cookie):
    # {
    #     "checkcode": "SUCCESS",
    #     "checklist": [],
    #     "fail": false,
    #     "object": [
    #         {
    #             "act_class": "35",
    #             "channel_type": "1",
    #             "checkcode": "SUCCESS",
    #             "checklist": [],
    #             "cust_group_id": "LAH0004075",
    #             "id_no": "19000114714933",
    #             "market_type": "00",
    #             "mkcaseid": "202204016629886424",
    #             "mkname": "【限时特惠】2022年全省话费膨胀专享5G包活动"
    #         },
    #         {
    #             "act_class": "35",
    #             "channel_type": "1",
    #             "checkcode": "SUCCESS",
    #             "checklist": [],
    #             "cust_group_id": "2021040108455062",
    #             "id_no": "19000114714933",
    #             "market_type": "00",
    #             "mkcaseid": "202112175087170349",
    #             "mkname": "2022年全省话费膨胀含权益活动（随心版）"
    #         },
    #         {
    #             "act_class": "35",
    #             "channel_type": "1",
    #             "checkcode": "SUCCESS",
    #             "checklist": [],
    #             "cust_group_id": "2021040108455062,2021040108455062",
    #             "id_no": "19000114714933",
    #             "market_type": "00",
    #             "mkcaseid": "202112165065427662",
    #             "mkname": "2022年全省话费膨胀活动（无忧版）"
    #         }
    #     ],
    #     "resultcode": "SUCCESS",
    #     "resultlist": [],
    #     "resultlistString": "",
    #     "success": true
    # }

    # 膨胀
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/hxx/market/fuzzyMkcaseQry'

    HTTPJSONKEY = {"qunflag": "0", "phone_no": phone_no, "flag": "4", "markobj_type": "00", "mkname": mkname,
                   "mktype": "营销执行"}

    # j = requests.get(api_url, cookies=cookie).text
    # print(requests.get(api_url, cookies=cookie))
    # print(j)

    try:
        res_json = json.loads(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
    except:
        return False, '登录状态过期'
    print(res_json)
    # json_dicts = json.dumps(res_json, indent=4, ensure_ascii=False)
    # print(json_dicts)
    if res_json['fail']:
        return False, res_json['resultdesc']
    activities = res_json['object']
    print(activities)
    return True, activities  # 返回 营销活动list


# 查询营销方式
def query_means(phone_no, activity, header, cookie):
    # {
    #     "checkcode": "SUCCESS",
    #     "checklist": [],
    #     "fail": false,
    #     "object": [
    #         {
    #             "channel_type": "1",
    #             "checkcode": "SUCCESS",
    #             "checklist": [],
    #             "means_id": "202112215163969258",
    #             "means_name": "（当月生效）话费膨胀30包打40（2年）可随时自主退订",
    #             "mkcaseid": "202112165065427662"
    #         },
    #         {
    #             "channel_type": "1",
    #             "checkcode": "SUCCESS",
    #             "checklist": [],
    #             "means_id": "202112215164009309",
    #             "means_name": "（次月生效）话费膨胀30包打40（2年）可随时自主退订",
    #             "mkcaseid": "202112165065427662"
    #         }
    #     ],
    #     "resultcode": "SUCCESS",
    #     "resultlist": [],
    #     "resultlistString": "",
    #     "success": true
    # }

    # 膨胀 无忧版
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/hxx/market/queryMkcaseWay'

    HTTPJSONKEY = {"phone": phone_no, "choose_act_id": activity['mkcaseid'],
                   "choose_cust_group_id": activity['cust_group_id'], "choose_channel_type": activity['channel_type'],
                   "choose_id_no": activity['id_no']}

    # j = requests.get(api_url, cookies=cookie).text
    # print(requests.get(api_url, cookies=cookie))
    # print(j)

    try:
        res_json = json.loads(requests.post(api_url, cookies=cookie, json=HTTPJSONKEY).text)
    except:
        return False, '登录状态过期'
    print(res_json)
    # json_dicts = json.dumps(res_json, indent=4, ensure_ascii=False)
    # print(json_dicts)
    if res_json['fail']:
        return False, res_json['resultdesc']
    means = res_json['object']
    for i in range(len(means)):
        if '当月生效' in means[i]['means_name']:
            target_means = means[i]['means_name']
            break
    print(target_means)
    return True, target_means  # 返回 一个 营销方式名称


# 查询营销方式是否可用
def query_means_detail(phone_no, means, header, cookie):



    # 点击营销方式
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


# 查询用户详情
def query_details(phone_no, header, cookie):
    # {
    #     "jsondata": {
    #         "retDesc": "查询号码信息成功",
    #         "retCode": "0000",
    #         "retVal": {
    #             "resultcode": "0000",
    #             "resultlist": [
    #                 {
    #                     "busi_limit_exp_date": "null",
    #                     "mgvolice_gold_ord_flag": "0",
    #                     "anxin_svc_flag": "0",
    #                     "busilimit_exp_date": "null",
    #                     "monitor_order_flag": "0",
    #                     "grid_code": "富合微网格",
    #                     "prod_5gmain_flag": "0",
    #                     "three_avg_gprs_total_fee": "0.42",
    #                     "three_avg_total_fee": "25.13",
    #                     "addr12_id": "null",
    #                     "is_hylimit_flag": "0",
    #                     "call_alert_arr_flag": "0",
    #                     "wide_limit_exp_date": "null",
    #                     "home_vnet_user_flag": "1",
    #                     "color_ring_arr_flag": "1",
    #                     "last3m_aver_arpu": "0",
    #                     "gprs_over_info_fee": "1.26",
    #                     "user_status_name": "正常",
    #                     "itv_vip_flag": "0",
    #                     "pre_term_5g_flag": "0",
    #                     "term_5g_flag": "1",
    #                     "ysp_sxb_flag": "0",
    #                     "migu_volice_gold_flag": "0",
    #                     "main_feeset": "神州行大众卡09版Y8",
    #                     "area_code": "歙县富合镇网格",
    #                     "family_wide_flag": "0",
    #                     "p5gqyb_order_flag": "0",
    #                     "midhigh_user_2020": "0",
    #                     "mon3_qual_flag": "0",
    #                     "and_eye_flag": "0",
    #                     "user_id": "19090395262698",
    #                     "avg_three_dura": "97",
    #                     "wide_exp_date": "null",
    #                     "super_mov_mem_flag": "0",
    #                     "avg_three_month_flow": "1.44",
    #                     "star_level": "一星",
    #                     "eparchy_code": "黄山",
    #                     "curimei_use_sum": "16",
    #                     "city_code": "歙县",
    #                     "apply_flag": "0",
    #                     "wide_band_speed": "null",
    #                     "internet_tv_flag": "0",
    #                     "ysp_sxb_qy_flag": "0",
    #                     "is_termcredit_flag": "0",
    #                     "stat_date": "2022-04-15",
    #                     "serial_number": "15212320559",
    #                     "mon_apply_flag": "0",
    #                     "is_term_act_flag": "0",
    #                     "term_double_flag": "0",
    #                     "dxbh_flag": "0",
    #                     "smart_gate_flag": "0"
    #                 }
    #             ],
    #             "resultdesc": "请求成功"
    #         }
    #     }
    # }

    # 用户详细信息
    api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/personalhomepage/queryPersonal?phoneno=' + phone_no
    # api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/finedo/personalhomepage/queryPersonal?phoneno=13855996258&token=bbc75e83-1f07-4ba4-840f-cd2fc8511098'

    # j = requests.get(api_url, cookies=cookie).text
    # print(requests.get(api_url, cookies=cookie))
    # print(j)

    try:
        res_json = json.loads(requests.get(api_url, cookies=cookie).text)
    except:
        return False, '登录状态过期'
    print(res_json)
    json_dicts = json.dumps(res_json, indent=4, ensure_ascii=False)
    print(json_dicts)
    if res_json['jsondata']['retVal']['resultcode'] == '0002':
        return False, '未查询到该用户信息'
    details = res_json['jsondata']['retVal']['resultlist'][0]
    print(details)
    return True, details  # 返回 用户详情dict


# 设置初始条件，开始获取数据
if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print(start_time, 'Begin-----------------------')

    # 页面
    # api_url = 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/sellstd_service/oneapp_jsp/personalhomepage/personalinquiry.jsp?phoneno=13855996258'

    # 啥也不是
    # api_url = 'http://hux.anhuiyidong.com.cn:9004/sellstd_webapp/sellstd_service/oneapp_jsp/yxzx/yxzxindex.jsp?token=bbc75e83-1f07-4ba4-840f-cd2fc8511098'

    # cookie = 'JSESSIONID=C9B91882B1847A8B9B87BC5121900873'
    # cookies = {}
    # for line in cookie.split(";"):
    #     print(line)
    #     if line.find("=") != -1:
    #         name,value = line.strip().split("=")
    #         cookies[name] = value
    # print(cookies)
    # timesp = int(time.time())
    cookies = {'JSESSIONID': 'F03E552ACFC31B39C2236349887C0774'}
    headers = {
        'Host': 'hxx.anhuiyidong.com.cn:9004',
        'Connection': 'keep-alive',
        # 'Content-Length': '125',
        # 'Pragma': 'no-cache',
        # 'Cache-Control': 'no-cache',
        # 'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; CDY-TN00 Build/HUAWEICDY-TN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Origin': 'http://hxx.anhuiyidong.com.cn:9004',
        # 'Referer': 'http://hxx.anhuiyidong.com.cn:9004/sellstd_webapp/sellstd_service/oneapp_jsp/yxzx/yxzxindex.jsp?token=bbc75e83-1f07-4ba4-840f-cd2fc8511098',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'JSESSIONID=C9B91882B1847A8B9B87BC5121900873',
    }
    # j = requests.get(api_url, cookies=cookies).text
    # print(requests.get(api_url, cookies=cookies))
    # print(j)

    # j = requests.get(api_url, cookies=cookies, data=HTTPJSONKEY).text
    # print(requests.get(api_url, cookies=cookies, data=HTTPJSONKEY))
    # print(j)
    # j = requests.post(api_url, cookies=cookies, json=HTTPJSONKEY).text
    # print(requests.post(api_url, cookies=cookies, json=HTTPJSONKEY))
    # print(j)

    # start_json = json.loads(j)
    # start_json = json.loads(requests.get(api_url).text)
    # print(start_json)
    # json_dicts = json.dumps(start_json, indent=4, ensure_ascii=False)
    # print(json_dicts)
    # 15212320559
    # 18755936548
    phone = '18705592233'
    phone = '13855932245'
    # sign, name, banlance = query_phone0(phone, headers, cookies)
    sign, res = query_phone(phone, headers, cookies)
    if sign:
        # 名字 主套餐名 入网时间 余额
        phone_details = [res['CUST_NAME'], res['PROD_PRC_NAME'], res['OPEN_TIME'][:-6], float(res['CUR_FEE']) / 100]
        # print(details)
        # time.sleep(100)
        sign, res = query_activity(phone, '膨胀', headers, cookies)
        if sign:
            for i in range(len(res)):
                if ('膨胀' in res[i]['mkname']) and ('无忧版' in res[i]['mkname']):
                    target_activity = res[i]
                    break
            print(target_activity)
            sign, res = query_means(phone, target_activity, headers, cookies)
            # sign, res = query_details('15000000000', headers, cookies)
            if sign:
                sign, res = query_details(phone, headers, cookies)
                if sign:
                    phone_details.append(res['user_status_name'])
                    phone_details.append(res['three_avg_total_fee'])
                    phone_details.append(res['city_code'])
                    phone_details.append(res['area_code'])
                    phone_details.append(res['grid_code'])
        # sign, res = query_details(phone, headers, cookies)
        print(phone_details)
    print('444')
    time.sleep(100)

    result_path = input('请输入excel文件路径')  # 结果保存路径

    end_time = datetime.datetime.now()
    total_time = str(end_time - start_time)
    print(end_time, 'Finish-----------------------共耗时', total_time)
