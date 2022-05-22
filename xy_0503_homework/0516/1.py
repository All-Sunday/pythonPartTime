# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/16 11:31
# @File : 1.py
myDict = {"汉堡": 15, "鸡翅": 10, "薯条": 6}
print(type(myDict))
print(myDict["鸡翅"])
# print(myDict[0])
myDict["汉堡"] = 15.5
print(myDict)
myDict["奶茶"] = 12
print(myDict)
print("鸡块" in myDict)
print("鸡翅" in myDict)
print(myDict.pop("薯条"))
print(myDict)
print(myDict.get("鸡翅"))
# print(myDict.get("鸡腿"))
print(myDict.get("鸡腿", "抱歉，无此商品！"))
myDict.clear()
print(myDict)

print('(1): 会报错，KeyError: 0；  因为键值0在myDict中不存在。')
print('(2): 使用字典名[键]时，当键不存在会报错，使用get()方法时，不存在会返回None，且可以设置返回默认值。')
print('(3): myDict.pop("薯条")')
print('(4): myDict.clear()')


