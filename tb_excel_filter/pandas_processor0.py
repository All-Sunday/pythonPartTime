# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/3/1 17:26
# @File : pandas_processor.py


import datetime
from decimal import Decimal
import openpyxl
from dateutil.relativedelta import relativedelta
import os
import pandas as pd


def xlsx_processor(result_path, columns):
    file_list = []  # 用于保存不符合条件的文件名
    source_files = os.listdir(result_path)  # 获取文件夹的所有文件及文件夹的命名
    for name in source_files:  # 遍历
        if name[-4:] == 'xlsx':  # 通过后缀判断是否是excel文件
            df = pd.read_excel(result_path + name)[columns].copy()  # 使用pandas读取所需字段  并使用copy 强制副本模式
            # df[columns[-1]] = df[columns[-1]].astype('string')   # df修改数据类型
            # print(df, df.dtypes)   # df输出数据类型
            # print(Decimal('4.1') + Decimal('2.3'))
            series = df[columns[-1]]  # df获取某列数据 格式为Series
            res = 0  # 记录总和

            for value in series:  # 遍历
                # print(value, type(value))
                # res += Decimal(value)
                res += value  # 累加
            res = Decimal(res).quantize(Decimal("0.0000"))  # Decimal保留四位小数
            print(res, res % 1 == 0)
            if res % 1 != 0:  # 判断是否是整数
                file_list.append(name)  # 不是整数 则将文件名加入list
            # df.round({'2022.04.FTE': 4})
            # df[columns[-1]] = df[columns[-1]].apply(lambda x: '%.4f'%x)   # df保留四位小数
            # df[columns[-1]] = df[columns[-1]].round(decimals=4)
            df.to_excel(result_path + 'all' + name, index=False)   # df输出excel
            wk = openpyxl.load_workbook(result_path + 'all' + name)   # openpyxl读取以修改excel单元格数据类型
            ws = wk.active
            a = ws['I']  # 获取第I列
            for b in a:
                b.number_format = '0.0000'  # openpyxl设置单元格格式
            wk.save(result_path + 'all' + name)  # openpyxl保存

    print(file_list)


if __name__ == '__main__':
    target_date = (datetime.datetime.now() + relativedelta(months=1)).strftime(
        '%Y.%m.') + 'FTE'  # 获取下一月 并转换格式'2022.04.FTE'
    columns = ['Project Name', 'Pool Name', 'Position Code', 'Position Name', 'Position Role', 'Work Type',
               'Backlog Work', 'Username', target_date]  # 要保留的字段的字段名
    xlsx_processor(r'E:\code_workplace\python\2022\january\tb_excel_filter\\', columns)
