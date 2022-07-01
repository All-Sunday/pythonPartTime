import matplotlib.pyplot as plt

sales=[15.5, 9.7, 18.5, 16.1, 18.7, 23.0, 22.2, 24.9, 33.4, 31.7, 37.9, 47.5]
fig, axes = plt.subplots(ncols=1, nrows=2)
axes[0].set_ylabel('销售额')
axes[0].plot(sales, 'Dr',ls='-')
plt.show()