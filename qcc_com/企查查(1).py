# coding=gbk
# -*- coding:uft-8 -*-
# 企查查

import requests
from time import sleep
from lxml import etree


def collect(key):
    url = f'https://www.qcc.com/web/search?key={key}'
    headers = {
        'Cookie': ck,
        'Referer': 'https://www.qcc.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    page = requests.get(url=url, headers=headers).content.decode('utf-8')
    tree = etree.HTML(page)
    name = ''.join(tree.xpath('(//a[@class="title copy-value"])[1]/span//text()'))
    state = tree.xpath('//table[@class="ntable ntable-list"]/tr[1]//div[@class="maininfo"]/div[1]/span[1]/span/text()')[0]
    phone = tree.xpath('//table[@class="ntable ntable-list"]/tr[1]//div[@class="maininfo"]/div[@class="relate-info"]/div/span/span/span/text()')[0]
    address = ''.join(tree.xpath('(//table[@class="ntable ntable-list"]/tr[1]//div[@class="maininfo"]/div[@class="relate-info"]//span[@class="copy-value"])[2]//text()'))
    email = (tree.xpath('//table[@class="ntable ntable-list"]/tr[1]//div[@class="maininfo"]/div[@class="relate-info"]/div/span[2]/a/text()') + [''])[0]
    website = (tree.xpath('//table[@class="ntable ntable-list"]/tr[1]//div[@class="maininfo"]/div[@class="relate-info"]/div/span[3]/span/a/text()') + [''])[0].strip()
    registered_capital = tree.xpath('//table[@class="ntable ntable-list"]/tr[1]//div[@class="maininfo"]/div[@class="relate-info"]/div[1]/span[2]/span/text()')[0]
    u = tree.xpath('//a[@class="title copy-value"]/@href')[0]
    sleep(1)
    page = requests.get(url=u, headers=headers).content.decode('utf-8')
    tree = etree.HTML(page)
    industry = (tree.xpath('//*[@id="cominfo"]/div[2]/table/tr[6]/td[2]/text()') + [''])[0].strip()
    area = (tree.xpath('//*[@id="cominfo"]/div[2]/table/tr[6]/td[4]/text()') + [''])[0].strip()
    scale = (tree.xpath('//*[@id="cominfo"]/div[2]/table/tr[7]/td[2]/text()') + [''])[0].strip()
    row = f'{name},{state},{phone},{area},{address},{registered_capital},{email},{website},{industry},{scale}'
    print(row)
    return row


if __name__ == '__main__':
    ua = 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/91.0.4472.106Safari/537.36'
    ck = 'qcc_did=fcf1e630-94f6-4eeb-8399-302500c4f7a0; UM_distinctid=17ecafa26f0c2b-0cd613a164a589-f791539-144000-17ecafa26f110a4; acw_tc=249cb38416443187902625662e3f0936d91ccadf849b96b43c2f877557; QCCSESSID=9d0f2b973814ba9438cdb18065; CNZZDATA1254842228=1514653814-1644081303-https%253A%252F%252Fwww.baidu.com%252F%7C1644308106'
    open('res.csv', 'a', encoding='utf-8-sig').write('公司名称,登记状态,电话,所属地区,地址,注册资本,邮箱,官网,所属行业,人员规模\n')
    ls = open('ori.csv', encoding='utf-8').readlines()[1:]
    ls = [li.split(',')[0] for li in ls if li]
    for li in ls:
        try:
            r = collect(li)
        except Exception as e:
            print(f'{li} 出错!')
            r = ''
        open('res.csv', 'a', encoding='utf-8-sig').write(r + '\n')
        sleep(2)
