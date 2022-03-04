# @Description: 1、文件要保留前八列，也就是H列，然后后面“20xx.月份.FTE”要保留下个月的那一列，也就是按今天三月一号来算，要保留前八列和2022.04.FTE。
# 2、对保留下来的2022.04.FTE里面的数保留四位小数，并且判断sum并且判断是否为整，不为整的显示出来
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
            series = df[columns[-1]]  # df获取某列数据 格式为Series
            res = 0  # 记录总和

            for value in series:  # 遍历
                res += value  # 累加
            res = Decimal(res).quantize(Decimal("0.0000"))  # Decimal保留四位小数
            # print(res, res % 1 == 0)
            if res % 1 != 0:  # 判断是否是整数
                file_list.append(name)  # 不是整数 则将文件名加入list

            df.to_excel(result_path + name, index=False)  # df输出excel 覆盖源文件
            wk = openpyxl.load_workbook(result_path + name)  # openpyxl读取以修改excel单元格数据类型
            ws = wk.active
            a = ws['I']  # 获取第I列
            for b in a:
                b.number_format = '0.0000'  # openpyxl设置单元格格式
            wk.save(result_path + name)  # openpyxl保存

    print(file_list)


if __name__ == '__main__':
    target_date = (datetime.datetime.now() + relativedelta(months=1)).strftime(
        '%Y.%m.') + 'FTE'  # 获取下一月 并转换格式'2022.04.FTE'
    columns = ['Project Name', 'Pool Name', 'Position Code', 'Position Name', 'Position Role', 'Work Type',
               'Backlog Work', 'Username', target_date]  # 要保留的字段的字段名
    xlsx_processor(r'E:\code_workplace\python\2022\january\tb_excel_filter\\', columns)
