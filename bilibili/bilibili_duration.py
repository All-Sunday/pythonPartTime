# @Description: 获取B站视频选集时长，输出excel     request获取json
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/1/7 20:04
# @File : bilibili_duration.py

# json数据示例
# {
#     "code":0,
#     "message":"0",
#     "ttl":1,
#     "data":[
#         {
#             "cid":299710389,
#             "page":1,
#             "from":"vupload",
#             "part":"0000_韩顺平Java_内容介绍",
#             "duration":1804,
#             "vid":"",
#             "weblink":"",
#             "dimension":{
#                 "width":1920,
#                 "height":1080,
#                 "rotate":0
#             }
#         },
#     ]
# }

import datetime

import requests
import json
import pandas as pd

def get_res(api, columns):
    json_obj = json.loads(requests.get(api).text)
    # print(type(json_obj))  # dict
    # print(json_obj['data'])
    data = json_obj['data']
    df = pd.DataFrame.from_dict(data)    # dict转df
    # print(df)
    res_to_excel(df, columns)

def time_format(seconds):  # 根据 秒数 返回 时分秒
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h == 0:
        if m == 0:
            return "0:00:%d" % s
        else:
            return "0:%02d:%02d" % (m, s)
    else:
        return "%d:%02d:%02d" % (h, m, s)

def res_to_excel(df, columns):
    df = df[columns].copy()   # 强制副本模式   否则出现SettingWithCopyWarning  pandas分不清是在原始数据上修改，还是赋值的数据上修改
    df.loc[0, 'total_duration'] = [time_format(df['duration'].sum())]
    # df.duration = df.duration.apply(lambda x: time_format(x))   # 避免链式索引操作
    df.loc[:, 'duration'] = df.duration.apply(lambda x: time_format(x))  # df 列apply函数
    print(df)
    print(df.dtypes)  # df数据类型
    # df['duration'] = df.duration.astype('int')  # 不可用
    df['duration'] = pd.to_timedelta(df.duration)   # excel设置单元格格式为时间(或自定义：[h]:mm:ss） 可方便进行统计
    df.loc[0, 'total_duration'] = pd.to_timedelta(df.loc[0, 'total_duration'][0])
    # df['duration'] = df.duration.apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time())  # 结果为字符串格式 不方便excel统计
    print(df.dtypes)  # df数据类型
    print(df)
    df.to_excel(id + '.xlsx', index=None)    # df输出excel

if __name__ == '__main__':
    id = 'BV1Fi4y1S7ix'
    api = 'https://api.bilibili.com/x/player/pagelist?bvid=' + id + '&jsonp=jsonp'
    columns = ['page', 'duration']  # 要保存的json数据的列名
    get_res(api, columns)
