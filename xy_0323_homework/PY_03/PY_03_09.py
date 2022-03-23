leave, arrive = input("请输入出发和到达时间（两个时间用','分开）").split(',')
leave_minutes = int(leave[:2]) * 60 + int(leave[2:])
arrive_minutes = int(arrive[:2]) * 60 + int(arrive[2:])
if arrive_minutes < leave_minutes:
    arrive_minutes += 12 * 60
duration_minutes = arrive_minutes - leave_minutes
print('整个旅程时间是：%02d小时%02d分钟' % (duration_minutes // 60, duration_minutes % 60))
