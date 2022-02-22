# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/1/18 10:02
# @File : test_proxy.py
import json
import time

import requests
from selenium import webdriver


class Proxy(object):
    def __init__(self):
        # api = 'https://api.xiaoxiangdaili.com/ip/get?appKey=800613442783694848&appSecret=04wGXLWh&cnt=&wt=json'
        # json_obj = json.loads(requests.get(api).text)
        # # self.proxy_ip = 'http://58.20.235.180:9091'
        # if json_obj['code'] == 200:
        #
        #     self.proxy_ip = json_obj['data'][0]['ip'] + ':' + str(json_obj['data'][0]['port'])
        #     print('成功', self.proxy_ip)
        # else:
        #     time.sleep(10)
        #     json_obj = json.loads(requests.get(api).text)
        #     self.proxy_ip = json_obj['data'][0]['ip']
        #     print('成功', self.proxy_ip)

        api = 'http://dev.qydailiip.com/api/?apikey=fd94ae68c02e164270039ac16bd994a6626c636f&num=3&type=json&line=win&proxy_type=putong&sort=1&model=all&protocol=http&address=&kill_address=&port=&kill_port=&today=true&abroad=1&isp=&anonymity='
        json_obj = json.loads(requests.get(api).text)
        # self.proxy_ip = 'http://58.20.235.180:9091'
        self.proxy_ip = json_obj[0]
        print('成功', self.proxy_ip)

        self.browser = self.getbrowser()
        self.getpage(self.browser)

    def getbrowser(self):
        options = webdriver.ChromeOptions()
        # 设置代理
        # desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
        # desired_capabilities['proxy'] = {
        #     "httpProxy": self.proxy_ip,
        #     # "ftpProxy": self.proxy_ip,  # 代理ip是否支持这个协议
        #     # "sslProxy": self.proxy_ip,  # 代理ip是否支持这个协议
        #     "noProxy": None,
        #     "proxyType": "MANUAL",
        #     "class": "org.openqa.selenium.Proxy",
        #     "autodetect": False
        # }
        # 使用无头模式
        # options.add_argument('--headless')
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:" + '9221')
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_argument("--proxy-server=http://"+self.proxy_ip)
        # options.add_argument('disable-infobars')
        browser = webdriver.Chrome(options=options,
                                   executable_path=r'E:\code_workplace\python\chromedriver.exe',
                                   # desired_capabilities=desired_capabilities
                                   )
        return browser

    def getpage(self, browser):
        # 打开目标网站
        # browser.get("https://www.baidu.com")
        # 对整个页面进行截图
        # browser.save_screenshot('百度.png')
        # 打印网站的title信息
        # print(browser.title)

        # 检测代理ip是否生效
        browser.get("https://httpbin.org/ip")
        # browser.get("https://ip.cn/")
        # 获取当前所有窗口集合(list类型) --- 因为打开多个窗口
        # handles = browser.window_handles
        # 切换到最新的窗口
        # browser.switch_to_window(handles[-1])
        # 打印新窗口网页的内容
        print(browser.page_source)

        # browser.get("https://www.ic.net.cn/search/CSD18532NQ5B.html?isExact=1")
        # browser.get("https://www.ic.net.cn")
        # browser.get("https://www.ic.net.cn")
        # browser.get("https://www.ic.net.cn")
        # browser.get("https://www.ic.net.cn/search/CSD18532NQ5B.html?isExact=1")
        # print(browser.page_source)
        # print(requests.get('https://www.ic.net.cn').text)
        time.sleep(100)


if __name__ == '__main__':
    Proxy()