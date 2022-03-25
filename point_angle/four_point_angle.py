# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/3/25 15:58
# @File : four_point_angle.py
import math
import pandas as pd


def cal_angle(point_a, point_b, point_c, point_d):
    a_x, b_x, c_x, d_x = point_a[0], point_b[0], point_c[0], point_d[0]
    a_y, b_y, c_y, d_y = point_a[1], point_b[1], point_c[1], point_d[1]
    a_z, b_z, c_z, d_z = point_a[2], point_b[2], point_c[2], point_d[2]

    x1, y1, z1 = (b_x - a_x), (b_y - a_y), (b_z - a_z)
    x2, y2, z2 = (d_x - c_x), (d_y - c_y), (d_z - c_z)

    cos_b = (x1 * x2 + y1 * y2 + z1 * z2) / (
            math.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2) * (math.sqrt(x2 ** 2 + y2 ** 2 + z2 ** 2)))

    angle = math.degrees(math.acos(cos_b))
    return round(angle, 2)


if __name__ == '__main__':
    file = r'file\孟浩-坐标求角度(1).xlsx'

    df = pd.read_excel(file)
    for row in df.itertuples():
        if row[0] < 1:
            continue
        if (row[0] % 2) != 0:
            point_a = (row[3], row[4], row[5])
            point_c = (row[7], row[8], row[9])
        else:
            point_b = (row[3], row[4], row[5])
            point_d = (row[7], row[8], row[9])
            df.loc[row[0], '角度'] = cal_angle(point_a, point_b, point_c, point_d)

    df.columns = ['', '', '变换前', '', '', '', '变换后', '', '', '角度']
    df.to_excel(file[:-5] + 'res.xlsx', index=None)
