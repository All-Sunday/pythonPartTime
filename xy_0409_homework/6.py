# 求解高次方程的根，[a,b]为区间，e是误差限，k为计算的轮次，x为得到的数值解
def dichotomize(a, b, e):
    global x
    k = 0
    while abs(a - b) / 2 >= e:
        k = k + 1
        x = (a + b) / 2
        if func(x) < 0:
            a = x
        elif func(x) > 0:
            b = x
        else:
            break
    return x, k


def func(x):
    res = 2 * pow(x, 3) - 4 * pow(x, 2) + 3 * x - 6
    return res


print(round(dichotomize(-10, 10, 1e-6)[0], 2))
