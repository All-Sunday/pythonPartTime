import matplotlib.pyplot as plt
import numpy as np

loss = []
acc = []
val_loss = []
val_acc = []
with open('epoch.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        data = line.split()
        loss.append(eval(data[0]))
        acc.append(eval(data[1]))
        val_loss.append(eval(data[2]))
        val_acc.append(eval(data[3]))

epochs = range(1, len(loss) + 1)

plt.rcParams['font.sans-serif'] = ['SimHei']

plt.figure(figsize=(8, 6), dpi=300)
ax1 = plt.axes([0.12, 0.5, 0.8, 0.4])
ax2 = plt.axes([0.12, 0.1, 0.8, 0.25])
plt.subplots_adjust(hspace=0.5)

ax1.set_title('训练集和验证集的准确率')
ax1.set_xlabel('训练轮数')
ax1.set_ylabel('准确率')
ax1.set_ylim(0.675, 1.025)
ax1.set_yticks(np.arange(0.70, 1.00, 0.05))

ax1.plot(acc, 'co', label='训练集准确率')
ax1.plot(val_acc, 'r', label='验证集准确率')
ax1.legend(loc='lower right')

ax2.set_title('训练集和验证集的损失值')
ax2.set_xlabel('训练轮数')
ax2.set_ylabel('损失值')
ax2.set_yticks(np.arange(0, 0.7, 0.2))

ax2.plot(loss, 'bo', label='训练集损失')
ax2.plot(val_loss, 'r', label='验证集损失')
ax2.legend(loc='upper right')

plt.show()
