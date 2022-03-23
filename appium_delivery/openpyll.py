import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import pandas as pd
import threading
import xlrd
# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

import pandos

if __name__ == '__main__':  # 只能由一个main函数
    pandos.main()
