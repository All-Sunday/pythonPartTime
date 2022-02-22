# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/1/27 11:56
# @File : pandas_drop.py

import pandas as pd

def sign_number(vowel):
    return any(i.isdigit() for i in vowel)

def sign_letter(vowel):
    return ('l' in vowel) or ('n' in vowel)

def processor(df):
    index_list = []
    for row in df.itertuples():
        index, vowel = getattr(row, 'Index'), getattr(row, 'vowel')
        # if index % 2 ==0:
        if vowel == 'n':
            if sign_number(df.loc[index - 1, 'vowel']) and sign_letter(df.loc[index + 1, 'vowel']):
                index_list.append(index)
    df.drop(index_list, axis=0, inplace=True)
    df.to_csv('res.csv', index=False)

if __name__ == '__main__':
    tsv_path = r'sample.tsv'
    df = pd.read_csv(tsv_path, sep='\t')
    processor(df.copy())
