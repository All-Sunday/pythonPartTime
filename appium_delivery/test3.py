# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/3/19 12:19
# @File : test.py

# This sample code uses the Appium python client v2
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python
import threading
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import pandas as pd

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

caps = {}
caps["platformName"] = "Android"
caps["appium:deviceName"] = '127.0.0.1:21513'
caps["appium:appPackage"] = "cn.chinapost.jdpt.pda.pickup"
caps["appium:appActivity"] = ".activity.pdasplashlogin.LoginActivity"
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:newCommandTimeout"] = 3600
caps["appium:connectHardwareKeyboard"] = True

caps2 = {}
caps2["platformName"] = "Android"
caps2["appium:deviceName"] = '127.0.0.1:21523'
caps2["appium:appPackage"] = "cn.chinapost.jdpt.pda.pickup"
caps2["appium:appActivity"] = ".activity.pdasplashlogin.LoginActivity"
caps2["appium:ensureWebviewsHavePages"] = True
caps2["appium:nativeWebScreenshot"] = True
caps2["appium:newCommandTimeout"] = 3600
caps2["appium:connectHardwareKeyboard"] = True

def task1():
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
    driver.implicitly_wait(30)

    time.sleep(30)

    time.sleep(30)
    el34 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/et_mail_no")
    df = pd.read_excel(r'【3.20漏扫补单】(1)(1).xlsx')
    success_num = 0
    fail_num = 0
    for row in df.itertuples():
        num = getattr(row, '单号')
        # print(num)
        try:
            el34.send_keys(num)
        except Exception:
            time.sleep(10)

        time.sleep(0.5)
        real_num = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/tv_num").text[1:-1]
        # print(int(real_num))
        real_num = int(real_num)
        # time.sleep(100)
        if real_num == success_num:
            fail_num += 1
        else:
            success_num += 1
        print('成功：', success_num, '\t失败：', fail_num)

def task2():
    driver = webdriver.Remote("http://127.0.0.1:4725/wd/hub", caps)
    driver.implicitly_wait(30)

    time.sleep(30)

    time.sleep(30)
    el34 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/et_mail_no")
    df = pd.read_excel(r'【3.20漏扫补单】(1)(1).xlsx')
    success_num = 0
    fail_num = 0
    for row in df.itertuples():
        num = getattr(row, '单号')
        # print(num)
        try:
            el34.send_keys(num)
        except Exception:
            time.sleep(10)

        time.sleep(0.5)
        real_num = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/tv_num").text[1:-1]
        # print(int(real_num))
        real_num = int(real_num)
        # time.sleep(100)
        if real_num == success_num:
            fail_num += 1
        else:
            success_num += 1
        print('成功：', success_num, '\t失败：', fail_num)


# driver.quit()

threads = []
t1 = threading.Thread(target=task1)
threads.append(t1)

t2 = threading.Thread(target=task2)
threads.append(t2)

for t in threads:
    t.start()
