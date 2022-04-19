goods = ['薯片', '爆米花', '巧克力', '可口可乐'] # 模拟自动售货机的商品
price = [5.00, 7.50, 12.00, 3.50]
while True:
    for i in range(len(goods)):
        print('[' + str(i + 1) + ']' + goods[i])
    print('[0]退出')
    print('--------')
    while True:
        input_id = int(input('请输入商品编号：'))
        if input_id in (0, 1, 2, 3, 4):
            break
        print('输入编号错误，请重试……')

    if input_id == 0:
        print('=====购买结束！=====')
        break
    good_id = input_id - 1  # 输入的编号比list下标大1
    good_num = int(input('请输入商品数量：'))
    total_price = round(good_num * price[good_id], 2)
    print('您购买了' + str(good_num) + '份' + goods[good_id] + '，总价为：' + '%.2f' % total_price)
    print('--------')
