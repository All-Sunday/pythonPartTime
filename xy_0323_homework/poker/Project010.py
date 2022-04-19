# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/10 23:03
# @File : Project01.py

import random
import time


def setup():
    # 未洗的牌
    cards = []
    # 洗过的牌
    global cards_random
    cards_random = []
    # 花色
    global suits
    suits = ['♦', '♣', '♥', '♠', ]
    # 牌面
    global ranks
    ranks = ['3', '4', '5', '6', '7', '8',
             '9', '10', 'J', 'Q', 'K', 'A', '2', ]

    # 组合花色、牌面 形成未洗的牌
    for suit in suits:
        for rank in ranks:
            cards.append(suit + rank)
    print(cards)
    print(cards_random)

    # 洗牌 随机选取未洗的拍加入洗牌的list
    num = 52
    while num > 0:
        num -= 1
        i = int(random.randint(0, num))
        cards_random.append(cards[i])
        # 删除已经加入洗牌后的牌
        del cards[i]

    print(cards)
    print(cards_random)


# 抽牌
def get_one_card(cards):
    i = int(random.randint(0, len(cards) - 1))
    card = cards[i]
    # 删除已经抽中的牌
    del cards[i]
    return card


def compare(a, b):
    if ranks.index(a[1:]) > ranks.index(b[1:]):
        return True
    elif ranks.index(a[1:]) < ranks.index(b[1:]):
        return False
    else:
        if suits.index(a[0]) > suits.index(b[0]):
            return True
        elif suits.index(a[0]) < suits.index(b[0]):
            return False


if __name__ == '__main__':
    global cards_random
    setup()
    print('*****游戏开始*****')
    user_card_nums = [int(x) for x in input('请输入您想要的3张牌的牌号(1~52，用空格分隔不同牌号)：').split(' ')]
    user_card_nums.sort()
    print('--------------------')
    user_cards = []
    computer_cards = []
    for i in range(len(user_card_nums)):
        index = user_card_nums[i] - 1 - i
        user_cards.append(cards_random[index])
        del cards_random[index]
    print('您抽到的牌分别是：', user_cards)
    for i in range(3):
        index = int(random.randint(0, len(cards_random) - 1))
        computer_cards.append(cards_random[index])
        # 删除已经抽中的牌
        del cards_random[index]
    print('电脑抽到的牌分别是：', computer_cards)

    if compare(user_cards[0], user_cards[1]):
        if compare(user_cards[0], user_cards[2]):
            max_user_card = user_cards[0]
        else:
            max_user_card = user_cards[2]
    else:
        if compare(user_cards[1], user_cards[2]):
            max_user_card = user_cards[1]
        else:
            max_user_card = user_cards[2]

    if compare(computer_cards[0], computer_cards[1]):
        if compare(computer_cards[0], computer_cards[2]):
            max_computer_card = computer_cards[0]
        else:
            max_computer_card = computer_cards[2]
    else:
        if compare(computer_cards[1], computer_cards[2]):
            max_computer_card = computer_cards[1]
        else:
            max_computer_card = computer_cards[2]
    if compare(max_user_card, max_computer_card):
        result = '。你赢了......'
    else:
        result = '。你输了......'
    print('你最大的牌是：'+max_user_card + '，电脑最大的牌是' + max_computer_card + result)
    print('*****游戏结束*****')
    print(cards_random)
