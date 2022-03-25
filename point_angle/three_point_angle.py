# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/3/25 15:58
# @File : four_point_angle.py
import math
import pandas as pd


def cal_angle(point_a, point_b, point_c):
    a_x, b_x, c_x = point_a[0], point_b[0], point_c[0]
    a_y, b_y, c_y = point_a[1], point_b[1], point_c[1]
    a_z, b_z, c_z = point_a[2], point_b[2], point_c[2]

    x1, y1, z1 = (a_x - b_x), (a_y - b_y), (a_z - b_z)
    x2, y2, z2 = (c_x - b_x), (c_y - b_y), (c_z - b_z)

    cos_b = (x1 * x2 + y1 * y2 + z1 * z2) / (
            math.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2) * (math.sqrt(x2 ** 2 + y2 ** 2 + z2 ** 2)))

    angle = math.degrees(math.acos(cos_b))
    return round(angle, 2)


if __name__ == '__main__':
    file = r'file\d-nz-1(1).csv'

    df = pd.read_csv(file)

    for row in df.itertuples():
        if row[0] < 2:
            continue
        row_ = [float(x) for x in row[:-3]]

        point_a = (row_[12], row_[13], row_[14])
        point_b = (row_[15], row_[16], row_[17])
        point_c = (row_[18], row_[19], row_[20])
        df.loc[row[0], '第一组'] = cal_angle(point_a, point_b, point_c)

        point_a = (row_[30], row_[31], row_[32])
        point_b = (row_[33], row_[34], row_[35])
        point_c = (row_[36], row_[37], row_[38])
        df.loc[row[0], '第二组'] = cal_angle(point_a, point_b, point_c)

        point_a = (row_[48], row_[49], row_[50])
        point_b = (row_[51], row_[52], row_[53])
        point_c = (row_[54], row_[55], row_[56])
        df.loc[row[0], '第三组'] = cal_angle(point_a, point_b, point_c)

    df.columns = ['', '', 'hand:zhang1', '', '', 'hand:zhang2', '', '', 'hand:zhang3', '',
                  '', 'hand:mz1', '', '', 'hand:mz2', '', '', 'hand:mz3', '', '',
                  'hand:zhang1', '', '', 'hand:zhang2', '', '', 'hand:zhang3', '',
                  '', 'hand:mz1', '', '', 'hand:mz2', '', '', 'hand:mz3', '',
                  '', 'hand:zhang1', '', '', 'hand:zhang2', '', '', 'hand:zhang3',
                  '', '', 'hand:mz1', '', '', 'hand:mz2', '', '', 'hand:mz3',
                  '', '', '第一组', '第二组', '第三组'
                  ]
    df.to_excel(file[:-5] + 'res.xlsx', index=None)
