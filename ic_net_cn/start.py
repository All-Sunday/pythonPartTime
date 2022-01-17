# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/1/17 12:56
# @File : start.py

import selenium_openpyxl_9221
import pandas as pd

if __name__ == '__main__':
    file_path = r'E:\code_workplace\python\2022\january\data\ic_net_cn\20220112数据.xlsx'
    df = pd.read_excel(file_path)
    df = df[['品牌', '型号']]
    df_list = []
    for i in range(5):
        df_list.append(df.iloc[i * 1000: (i + 1) * 1000])
        print(len(df_list[i]))
    selenium_openpyxl_9221.main1(file_path, df_list[0])

