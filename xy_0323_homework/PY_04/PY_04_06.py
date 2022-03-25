total_money = 0
people_num = 0
while True:
    money = float(input('请输入捐款金额（元）：'))
    if money < 0:
        print('===募捐活动圆满结束！===')
        print('本次募捐参与人数' + str(people_num) + '人、共得捐款总额%.2f' % total_money + '元')
        break
    elif money < 0.01:
        print('捐款最小金额是0.01元。')
    else:
        total_money += money
        people_num += 1
    print('最新捐款%.2f' % money + '元、捐款人数' + str(people_num) + '人、\n' + '\t捐款总额%.2f' % total_money + '元、平均每人捐款%.2f' %
        (total_money / people_num) + '元')
