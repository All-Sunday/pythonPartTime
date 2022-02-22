# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/1/19 23:25
# @File : excel_processor.py
import os
import pandas as pd

def xlsx_processor(result_path):
    filelist = []
    res_df = pd.DataFrame()
    for root, dirs, files in os.walk(result_path):
        for name in files:
            if name[-4:] == 'xlsx':
                filelist.append(result_path + name)
                part = pd.read_excel(result_path + name)
                res_df = pd.concat([res_df, part])

    print(filelist)
    print(res_df)
    res_df.sort_values('i', inplace=True)
    # res_df.drop_duplicates(subset=['证券代码', '公司名称'], inplace=True)
    res_df.to_excel(result_path + 'all.xlsx', index=False)

if __name__ == '__main__':
    xlsx_processor(r'E:\code_workplace\python\2022\january\data\ic_net_cn\1\\')