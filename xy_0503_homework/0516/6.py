# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/16 12:04
# @File : 3.py
set1 = {1, 2, 3, 4, 5}
set2 = {2, 3, 5, 6}
print(set1 & set2)
print(set1 | set2)
print(set1 ^ set2)
print(set1 - set2)
print(set2 - set1)
set3 = {2, 3, 5}
print(set1 >= set3)
# print(set1.issuperset(set3))
set3.add(6)
print(set3)
print(set2 < set3)
# print(set2.issubset(set3))
set3.add((7, 8))
# set3.add([7, 8])
print(set3)
set3.remove(2)
print(set3)
set3.clear()
print(set3)

print('(1): set1.intersection(set2)\n'
      'set1.union(set2)\n'
      'set1.symmetric_difference(set2)\n'
      'set1.difference(set2)\n'
      'set2.difference(set1)\n'
      'set1.issuperset(set3)\n')
print("(2): 会报错，TypeError: unhashable type: 'list'   因为set中的元素必须是不可变类型的，list是可变类型。")
print('(1): set1、set2的交集\n'
      'set1、set2的并集\n'
      'set1、set2的补集\n'
      'set1、set2的差集，输出set1中有而set2中没有的元素\n'
      'set2、set1的差集，输出set2中有而set1中没有的元素\n'
      'set3是否是set1的子集，或两者相同\n')


