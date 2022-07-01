import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.rcParams['font.sans-serif'] = ['SimHei']
labels = ['学习用品', '日常用品', '伙食费', '通讯费', '娱乐费', '其他开支']
percentage = [0.1, 0.2, 0.5, 0.05, 0.1, 0.05]
plt.title("月消费支出饼图")
explode = (0.2, 0, 0, 0, 0, 0)
plt.axis("equal")
plt.pie(percentage, explode, autopct='%.1f%%', labels=labels)
plt.legend(bbox_to_anchor=(1, 0.6))
plt.show()
