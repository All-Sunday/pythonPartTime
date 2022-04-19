# @Description: TODO
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

    html = requests.get(df.loc[0, 0])
    html.encoding = 'GBK'
    soup = BeautifulSoup(html.text, 'html.parser')
    target_as = soup.find_all('a', title=regex.compile('.*上海镀锌管价格最新行情$'))
    if len(target_as) == 0:
        print('页面没有  1上海镀锌管价格最新行情（1上海镀锌管价格行情(新)不属于爬取目标）')
        return
    print(target_as[0]['href'])

    html = requests.get(target_as[0]['href'])
    html.encoding = 'GBK'
    soup = BeautifulSoup(html.text, 'html.parser')
    title = soup.select('.title')[0].h1.string
    print(title)
    target_trs = soup.tbody.find_all('tr')[1:]
    target_trs = [i for i in target_trs if '友发' in i('td')[4].string]

    types = df[1].values
    for tr in target_trs:
        for t in types:
            if tr('td')[2].string == t:
                df.loc[df[1] == t, 6] = float(tr('td')[5].string)

    df.to_excel(title + '.xlsx', index=None, header=None)


def main():
    # source_path = '主材基准价初稿(1).xlsx'
    source_path = input('请输入excel路径').strip()
    get_res(source_path)
    print('*****爬取结束*****')
    time.sleep(120)
