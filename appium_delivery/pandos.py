# This sample code uses the Appium python client v2
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python
import threading
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import pandas as pd
import xlrd

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def task1(*args):
    # device_port = input('请输入模拟器端口').strip()
    device_port = args[1]
    # appium_port = input('请输入appium端口').strip()
    appium_port = args[2]
    excel_path = input('模拟器' + device_port + '  请输入excel路径').strip()
    type = input('模拟器' + device_port + '  请输入选择：1(快速收寄)，2(离线收寄)').strip()
    caps = {}
    caps["platformName"] = "Android"
    caps["appium:deviceName"] = '127.0.0.1:' + device_port
    caps["appium:appPackage"] = "cn.chinapost.jdpt.pda.pickup"
    caps["appium:appActivity"] = ".activity.pdasplashlogin.LoginActivity"
    caps["appium:ensureWebviewsHavePages"] = True
    caps["appium:nativeWebScreenshot"] = True
    caps["appium:newCommandTimeout"] = 3600
    caps["appium:connectHardwareKeyboard"] = True
    caps["appium:noReset"] = True
    driver = webdriver.Remote("http://127.0.0.1:" + appium_port + "/wd/hub", caps)
    driver.implicitly_wait(30)

    time.sleep(90 * args[3])

    el34 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/et_mail_no")
    df = pd.read_excel(excel_path)
    nan_num = df['单号'].isnull().sum()
    print('模拟器' + device_port + '  *********空值数量：', nan_num)
    df.dropna(axis=0, subset=['单号'], inplace=True)
    # print(df['单号'].isnull().sum())
    success_num = 0
    fail_num = 0
    get_num = 0
    with open(device_port + ".txt", "w") as f:  # 写入txt
        f.write('模拟器' + device_port + '  *********空值数量：' + str(nan_num))  # 这句话自带文件关闭功能 不需要再写f.close()

    try:
        for row in df.itertuples():
            get_num = str(getattr(row, '单号'))
            if not is_number(get_num):
                print('模拟器' + device_port + '  ********不是数字：', get_num)
                with open(device_port + ".txt", "a") as f:  # 写入txt
                    f.write('\n模拟器' + device_port + '  ********不是数字：' + str(get_num))
                continue
            # print(get_num, type(get_num))
            # if get_num != get_num:
            #     print('空')
            #     continue

            num = str(int(float(get_num)))
            if len(num) != 13:
                print('模拟器' + device_port + '  ********不是13位：', get_num)
                with open(device_port + ".txt", "a") as f:  # 写入txt
                    f.write('\n模拟器' + device_port + '  ********不是13位：' + str(get_num))
                continue
            # print(num)

            try:
                el34.send_keys(num)
            except Exception:
                time.sleep(60)

            time.sleep(0.5)
            real_num = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/tv_num").text[1:-1]
            real_num = int(real_num)
            if real_num == success_num:
                fail_num += 1
            else:
                success_num += 1
            if (getattr(row, 'Index') % 10) == 0:
                print('模拟器' + device_port + '  成功：', success_num, '失败：', fail_num)
    finally:
        with open(device_port + ".txt", "a") as f:  # 写入txt
            f.write('\n模拟器' + device_port + '  成功：' + str(success_num) + '失败：' + str(fail_num))
    print('*******************结束*******************')


# driver.quit()
def main():
    thread_num = int(input('请输入多开的模拟器数量：').strip())
    threads = []
    for i in range(thread_num):
        t = threading.Thread(target=task1, args=(i + 1, str(21503 + i * 10), str(4723 + i * 2), thread_num))
        threads.append(t)

    for t in threads:
        t.start()
        time.sleep(30)
    time.sleep(100000)
