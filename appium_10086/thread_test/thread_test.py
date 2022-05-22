# @Description: 线程共享变量 速度测试
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/26 14:43
# @File : thread_test.py
import datetime
import os
import threading
import time

import openpyxl
import pandas as pd

g_num = 0
# 创建一个互斥锁，默认为未上锁zhuangtai
mutex = threading.Lock()


def test1(num):
    global g_num

    for i in range(num):
        mutex.acquire()
        g_num += 1
        print("--test1, g_num = %d--" % g_num)
        mutex.release()
        time.sleep(0.02)


def test2(num):
    global g_num

    for i in range(num):
        mutex.acquire()
        g_num += 1
        print("--test2, g_num = %d--" % g_num)
        mutex.release()
        time.sleep(0.02)


# 100000次测试 分别开线程数 及 耗时（秒）
# 1：1584
# 2：793
# 4：398
# 8：202
# 10:163
def test3(index):
    global g_num

    while g_num < 100000:
        mutex.acquire()
        g_num += 1
        print('--test' + str(index) + ', g_num = %d--' % g_num)
        mutex.release()
        time.sleep(0.01)


def test4(index, wk, ws, res_path):
    global g_num

    while g_num < 100000:
        mutex.acquire()
        g_num += 1
        print('--test' + str(index) + ', g_num = %d--' % g_num)
        mutex.release()
        write(g_num, wk, ws, res_path)
        time.sleep(0.01)


def test5(index, wk, ws, res_path):
    global g_num

    while True:
        # while (g_num + 1) < 100000:
        mutex.acquire()
        if (g_num + 1) > 40000:
            mutex.release()
            break
        t_num = g_num
        g_num += 1

        mutex.release()
        # if t_num >= 100000:
        #     break
        print('--test' + str(index) + ', g_num = %d--' % t_num)
        write(t_num, wk, ws, res_path)
        time.sleep(0.01)


def test6(index, wk, ws, res_path):  # df 31分钟
    global g_num

    while True:
        # while (g_num + 1) < 100000:
        mutex.acquire()
        if (g_num + 1) > 100000:
            mutex.release()
            break
        t_num = g_num
        g_num += 1

        mutex.release()
        # if t_num >= 100000:
        #     break
        print('--test' + str(index) + ', g_num = %d--' % t_num)
        write(t_num, wk, ws, res_path)
        time.sleep(0.01)


def write(test_num, wk, ws, res_path):
    phone_details = [test_num, test_num + 1, test_num + 2, test_num + 3, test_num + 4, test_num + 5, test_num + 6]
    time.sleep(0.3)
    phone_details.extend([test_num + 7, test_num + 8, test_num * 1, test_num * 2, test_num * 10])

    # ws.append(phone_details)
    # wk.save(res_path)
    # phone_details = {'手机号': test_num, '营销活动': test_num + 1, '营销方式': test_num + 2, '姓名': test_num + 3,
    #                  '身份证号': test_num + 4, '主套餐': test_num + 5, '入网时间': test_num + 6}
    # phone_details2 = {'余额': test_num + 7, '用户状态': test_num + 8, '近三个月均话费': test_num * 1, '区县名称': test_num * 2,
    #                   '网格名称': test_num * 10}
    # phone_details.update(phone_details2)
    # df = df.append(phone_details, ignore_index=True)
    global df
    df2 = pd.DataFrame([phone_details], columns=('手机号', '营销活动', '营销方式', '姓名', '身份证号', '主套餐', '入网时间', '余额', '用户状态', '近三个月均话费', '区县名称', '网格名称'))
    mutex.acquire()
    df = pd.concat([df, df2], ignore_index=True)
    mutex.release()
    # print(df)

def test7(index):   # openpyxl 11分钟  ws也要上锁 涉及到修改的都要上锁
    global g_num

    while True:
        # while (g_num + 1) < 100000:
        mutex.acquire()
        if (g_num + 1) > 100000:
            mutex.release()
            break
        t_num = g_num
        g_num += 1

        mutex.release()
        # if t_num >= 100000:
        #     break
        print('--test' + str(index) + ', g_num = %d--' % t_num)
        write2(t_num)
        time.sleep(0.01)


def write2(test_num):
    phone_details = [test_num, test_num + 1, test_num + 2, test_num + 3, test_num + 4, test_num + 5, test_num + 6]
    time.sleep(0.3)
    phone_details.extend([test_num + 7, test_num + 8, test_num * 1, test_num * 2, test_num * 10])
    global ws
    mutex.acquire()
    ws.append(phone_details)
    mutex.release()
    # wk.save(res_path)
    # phone_details = {'手机号': test_num, '营销活动': test_num + 1, '营销方式': test_num + 2, '姓名': test_num + 3,
    #                  '身份证号': test_num + 4, '主套餐': test_num + 5, '入网时间': test_num + 6}
    # phone_details2 = {'余额': test_num + 7, '用户状态': test_num + 8, '近三个月均话费': test_num * 1, '区县名称': test_num * 2,
    #                   '网格名称': test_num * 10}
    # phone_details.update(phone_details2)
    # df = df.append(phone_details, ignore_index=True)
    # global df
    # df2 = pd.DataFrame([phone_details], columns=('手机号', '营销活动', '营销方式', '姓名', '身份证号', '主套餐', '入网时间', '余额', '用户状态', '近三个月均话费', '区县名称', '网格名称'))
    # mutex.acquire()
    # df = pd.concat([df, df2], ignore_index=True)
    # mutex.release()
    # print(df)


def init(res_path):
    if not os.path.exists(res_path):
        wk = openpyxl.Workbook()
        ws = wk.active
        ws.append(
            ['手机号', '营销活动', '营销方式', '姓名', '身份证号', '主套餐', '入网时间', '余额', '用户状态', '近三个月均话费', '区县名称', '网格名称', '微网格名称'])
        wk.save(res_path)
    wk = openpyxl.load_workbook(res_path)
    return wk


if __name__ == "__main__":

    print("--创建线程之前, g_num = %d--" % g_num)

    # t1 = threading.Thread(target=test1, args=(9999,))
    # t1.start()
    #
    # t2 = threading.Thread(target=test2, args=(9999,))
    # t2.start()

    # test3(999)

    df = pd.DataFrame(
        columns=('手机号', '营销活动', '营销方式', '姓名', '身份证号', '主套餐', '入网时间', '余额', '用户状态', '近三个月均话费', '区县名称', '网格名称'))
    source_path = 'test.xlsx'
    res_path = source_path.split('.')[0] + datetime.datetime.now().strftime('%Y%m%d %H-%M-%S') + '.xlsx'
    wk = init(res_path)
    thread_num = int(input('请输入多开的模拟器数量：').strip())
    threads = []
    start_time = datetime.datetime.now()
    print(start_time, 'Begin-----------------------')
    ws = wk.active
    for i in range(thread_num):
        # t = threading.Thread(target=test3, args=(i + 1,))
        # t = threading.Thread(target=test4, args=(i + 1, wk, wk.active, res_path))
        # t = threading.Thread(target=test5, args=(i + 1, wk, wk.active, res_path))
        # t = threading.Thread(target=test6, args=(i + 1, wk, wk.active, res_path))
        t = threading.Thread(target=test7, args=(i + 1,))
        threads.append(t)

    for t in threads:
        t.start()
        time.sleep(1)

    while len(threading.enumerate()) != 1:
        time.sleep(1)
    wk.save(res_path)
    df.to_excel('res.xlsx', index=None)
    print("最终结果为：g_num=%d" % g_num)
    end_time = datetime.datetime.now()
    total_time = str(end_time - start_time)
    print(end_time, 'Finish-----------------------共耗时', total_time)
