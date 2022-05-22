# @Description: TODO
# @Author https://github.com/All-Sunday  1544781624 All-Sunday
# @Time 2022/4/14 21:13
# @File : requestso.py


import openpyxl
import requests
from bs4 import BeautifulSoup


def init():
    wk = openpyxl.Workbook()
    ws = wk.active
    ws.append(['rank', 'PLAYER', '2020/21', '2020/21(*) '])

    return wk, ws


def get_res(ws):
    api_url = 'https://hoopshype.com/salaries/players/2020-2021/'

    html = requests.get(api_url)
    html.encoding = 'GBK'

    soup = BeautifulSoup(html.text, 'html.parser')

    target_trs = soup.tbody.find_all('tr')

    for tr in target_trs:
        rank = tr.contents[1].string.strip()[:-1]

        name = tr.contents[3].find('a').string.strip()

        money1 = tr.contents[5].string.strip()

        money2 = tr.contents[7].string.strip()
        ws.append([rank, name, money1, money2])


if __name__ == '__main__':
    wk, ws = init()

    get_res(ws)
    wk.save('res.xlsx')
