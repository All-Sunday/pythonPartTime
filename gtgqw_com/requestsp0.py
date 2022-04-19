# @Description: requests + BeautifulSoup 爬取数据  pandas
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/14 21:13
# @File : requestsp.py

import time

import pandas as pd
import regex
import requests
from bs4 import BeautifulSoup


def get_res(source_path):
    df = pd.read_excel(source_path, header=None).copy()

    html = requests.get(df.loc[0, 0])  # df读取特定行列值
    html.encoding = 'GBK'  # requests设置编码
    # print(html)
    soup = BeautifulSoup(html.text, 'html.parser')  # BeautifulSoup解析html
    # print(soup, type(soup))
    target_as = soup.find_all('a', title=regex.compile('.*上海镀锌管价格最新行情$'))  # BeautifulSoup查找所有元素 正则
    if len(target_as) == 0:
        print('页面没有  1上海镀锌管价格最新行情（1上海镀锌管价格行情(新)不属于爬取目标）')
        return
    print(target_as[0]['href'])

    html = requests.get(target_as[0]['href'])  # BeautifulSoup获取属性
    html.encoding = 'GBK'
    soup = BeautifulSoup(html.text, 'html.parser')
    # print(soup, type(soup))
    title = soup.select('.title')[0].h1.string  # BeautifulSoup获取内容
    print(title)
    target_trs = soup.tbody.find_all('tr')[1:]  # BeautifulSoup查找子元素
    target_trs = [i for i in target_trs if '友发' in i('td')[4].string]  # list筛选
    # print(target_trs, len(target_trs))

    types = df[1].values
    for tr in target_trs:
        for t in types:
            if tr('td')[2].string == t:
                # print(df[1][6])
                df.loc[df[1] == t, 6] = float(tr('td')[5].string)  # df特定行列赋值
    print(df.loc[:, 6])
    df.to_excel(title + '.xlsx', index=None, header=None)  # df输出excel 不含表头


if __name__ == '__main__':
    source_path = '主材基准价初稿(1).xlsx'
    get_res(source_path)
    print('*****爬取结束*****')
    time.sleep(120)
