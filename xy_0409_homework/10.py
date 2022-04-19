def reverse(l):
    if len(l) == 0:
        return []
    else:
        res = reverse(l[1:])
        res.append(l[0])
        return res


L = [1, 2, 3]
print(reverse(L))
