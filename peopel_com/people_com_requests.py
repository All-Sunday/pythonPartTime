# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/1/9 17:22
# @File : people_com.py
# -*- coding:utf-8 -*-
import requests
import json

postUrl = 'http://liuyan.people.com.cn/threads/queryThreadsList'
payloadData = {
    'fid': '569',
    'state': '4',
    'lastItem': '12372086'
}

# 请求头设置
payloadHeader = {
    'Host': 'liuyan.people.com.cn',
    'Origin': 'http://liuyan.people.com.cn',
    'Referer': 'http://liuyan.people.com.cn/threads/list?fid=569',
    'Content-Type': 'application/json',
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Cookie":""
}
cookie = '4de1d0bdb25d4625be2481a1b9e1350f=WyIxNzI3MjU0NjU3Il0; __jsluid_h=c19fbabbc1cf24580daaa9b7cdc970d5; wdcid=35cc11e91dc782ce; JSESSIONID=77B7BBFE103661FEC98E27A4C3A5E997; wdlast=1641724099; wdses=68db7d324ace8b4f'
cookies={}#初始化cookies字典变量
for line in cookie.split(';'):   #按照字符：进行划分读取
    #其设置为1就会把字符串拆分成2份
    name,value=line.strip().split('=',1)
    cookies[name]=value  #为字典cookies添加内容
r = requests.post(postUrl, data=json.dumps(payloadData), headers=payloadHeader, cookies=cookies).text

print(r)


