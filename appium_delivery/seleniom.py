

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
type = input('请输入选择：1(快速收寄)，2(离线收寄)').strip()

caps = {}
caps["platformName"] = "Android"
caps["appium:deviceName"] = '127.0.0.1:' + device_port
caps["appium:appPackage"] = "cn.chinapost.jdpt.pda.pickup"
caps["appium:appActivity"] = ".activity.pdasplashlogin.LoginActivity"
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:newCommandTimeout"] = 3600
caps["appium:connectHardwareKeyboard"] = True

driver = webdriver.Remote("http://127.0.0.1:" + appium_port + "/wd/hub", caps)
driver.implicitly_wait(30)

# el1 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/empCode")
# el1.send_keys("4210008648619")
# el2 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/empPassword")
# el2.send_keys("@Abc123456789")
# el3 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/btn_login")
# el3.click()
# time.sleep(6)
# el4 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/btnPositive")
# el4.click()
# el5 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/btnPositive")
# el5.click()
# time.sleep(5)
# el6 = driver.find_element(by=AppiumBy.CLASS_NAME, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[1]")
# el6.click()
# time.sleep(0.6)
# el7 = driver.find_element(by=AppiumBy.CLASS_NAME, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[4]/android.widget.RelativeLayout/android.widget.TextView")
# el7.click()
# time.sleep(0.6)
# el8 = driver.find_element(by=AppiumBy.CLASS_NAME, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.TextView")
# el8.click()
time.sleep(30)
# el10 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/rl_show_product")
# el10.click()
# el11 = driver.find_element(by=AppiumBy.CLASS_NAME, value="/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView")
# el11.click()
#
# el15 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/et_product")
# el15.send_keys("国内EMS促销物品")
# el16 = driver.find_element(by=AppiumBy.CLASS_NAME, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.RelativeLayout[2]/android.widget.TextView[2]")
# el16.click()
# el17 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/et_sender")
# el17.click()
# el18 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/post_code")
# el18.send_keys("衡阳乖孩子电子商务有限公司")
# el19 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/sub_chargedweight2")
# el19.click()
# el20 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/tvTransType")
# el20.click()
# el21 = driver.find_element(by=AppiumBy.CLASS_NAME, value="/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.GridView/android.widget.TextView[10]")
# el21.click()
#
# el23 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/toggleBtnLockWeight")
# el23.click()
# el24 = driver.find_element(by=AppiumBy.ID, value="cn.chinapost.jdpt.pda.pickup:id/etLockWeight")
# el24.send_keys("200")

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
# for i in range(10):
#     el34.send_keys("1251310274451")
#     time.sleep(0.5)
#     el34.send_keys("5484156185415")
#     time.sleep(0.5)
print('*******************结束*******************')
time.sleep(10000)
# driver.quit()