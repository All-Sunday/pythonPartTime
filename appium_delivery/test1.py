# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/3/19 12:19
# @File : test.py

# This sample code uses the Appium python client v2
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import pandas as pd

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
device_port = input('请输入模拟器端口').strip()
appium_port = input('请输入appium端口').strip()
excel_path = input('请输入excel路径').strip()
caps = {}
caps["platformName"] = "Android"
caps["appium:deviceName"] = device_port
caps["appium:appPackage"] = "cn.chinapost.jdpt.pda.pickup"
caps["appium:appActivity"] = ".activity.pdasplashlogin.LoginActivity"
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:newCommandTimeout"] = 3600
caps["appium:connectHardwareKeyboard"] = True

driver = webdriver.Remote("http://127.0.0.1:" + appium_port + "/wd/hub", caps)
driver.implicitly_wait(30)


time.sleep(30)

time.sleep(30)
el34 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/et_mail_no")
# df = pd.read_excel(r'【3.20漏扫补单】(1)(1).xlsx')
df = pd.read_excel(excel_path)
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

driver.quit()