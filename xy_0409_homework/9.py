# 进制转化 十进制数转换为r（2-9）进制
def convert(d, r):
    convertString = '0123456789'
    # if d < r:
    #     return convertString[d]
    # else:
    #     return convert(d // r, r) + convertString[d % r]
    Q = d // r
    L = convertString[d % r]
    if Q != 0:
        L = convert(Q, r) + L
    return L


res = convert(10, 8)
print(res, type(res))
