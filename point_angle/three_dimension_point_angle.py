# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/3/24 22:14
# @File : .py
import math


def cal_angle(point_a, point_b, point_c):
    """
    https://zhidao.baidu.com/question/588244934.html
    设a,b是两个不为0的向量，它们的夹角为<a,b> (或用α ,β, θ ,..,字母表示)

    1、由向量公式：cos<a,b>=a.b/|a||b|.①

    2、若向量用坐标表示，a=(x1,y1,z1), b=(x2,y2,z2),

    则,a.b=(x1x2+y1y2+z1z2).

    |a|=√(x1^2+y1^2+z1^2), |b|=√(x2^2+y2^2+z2^2).

    将这些代入②得到：

    cos<a,b>=(x1x2+y1y2+z1z2)/[√(x1^2+y1^2+z1^2)*√(x2^2+y2^2+z2^2)] ②

    上述公式是以空间三维坐标给出的，令坐标中的z=0,则得平面向量的计算公式。

    两个向量夹角的取值范围是：[0,π].

    夹角为锐角时，cosθ>0；夹角为钝角时,cosθ<0.
    根据三点坐标计算夹角
    :param point_a: 点1坐标
    :param point_b: 点2坐标
    :param point_c: 点3坐标
    :return: 返回点2夹角值
    """
    a_x, b_x, c_x = point_a[0], point_b[0], point_c[0]
    a_y, b_y, c_y = point_a[1], point_b[1], point_c[1]

    if len(point_a) == len(point_b) == len(point_c) == 3:
        # print("坐标点为3维坐标形式")
        a_z, b_z, c_z = point_a[2], point_b[2], point_c[2]
    else:
        a_z, b_z, c_z = 0, 0, 0
        # print("坐标点为2维坐标形式，z 坐标默认值设为0")

    x1, y1, z1 = (a_x - b_x), (a_y - b_y), (a_z - b_z)
    x2, y2, z2 = (c_x - b_x), (c_y - b_y), (c_z - b_z)

    cos_b = (x1 * x2 + y1 * y2 + z1 * z2) / (
            math.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2) * (math.sqrt(x2 ** 2 + y2 ** 2 + z2 ** 2)))

    B = math.degrees(math.acos(cos_b))
    return round(B, 2)


print(cal_angle((1, 1), (0, 0), (0, 1)))
print(cal_angle((0, 0, 1), (1, 1, 1), (0, 1, 1)))
print(cal_angle((-1, 1), (0, 0), (1, 1)))
