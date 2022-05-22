# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/14 18:10
# @File : test.py
# from thresd import *
# import thresd
from t import thresd

row = thresd.insert(
    ['摩托手套（★） | 薄荷 (崭新出厂)', '55916', 88888.0, 85555.0, '摩托手套（★） | 薄荷 (崭新出厂) 售价为85555.0，buff为86666\n', '2'])
if row == 1:
    res = thresd.query()
    if res is not None:
        print('u')
        thresd.update(res, 1)
