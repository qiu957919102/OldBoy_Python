#!/usr/bin/env python
# coding:utf-8
from conf import conf
from model import role


me = None
wanqing = None

def play_main():
    global me
    role_info = me.get_info()

    main_map = '''
返回主菜单(r)  存档(s)   查看背包(p)
%s: 生命 %s   声望 %s   现银 %s   银票 %s   欠账 %s   包裹 %s   穿越天数 %s
---------------------------------------------------------------------------------
                              北市(2)
                        |                    |
            钱庄(1)     |                    |      木婉清的家(3)
                        |                    |
    --------------------+                    +---------------------

西市(4)                           我                            东市(5)

    --------------------+                    +---------------------
                        |                    |
           医馆(6)      |                    |     丽春院(8)
                        |                    |
                             南市(7)
    ''' %(role_info[0], role_info[1], role_info[2], role_info[3], role_info[4], role_info[5], role_info[6], role_info[7])
    print(main_map)

def new_game():
    global me
    me = role.leading_role(conf.LEADING_ROLE_INIT_DATA)
    name = input('请输入玩家的姓名: ').strip()
    if name:
        me.name = name
    # input('我叫%s,' % me.name)
    # for item in conf.STORY:
    #     input(item)
    # wanqing = role.role('木婉清')
    # wanqing.say('太好了你终于醒了')
    # me.say('这里是哪儿？我为什么会在这里？')
    # wanqing.say('这是我的家，我在上山采药的时候发现了你。')
    # me.think('欧系吧！难道我穿越了？？')
    # input('从后来的交谈中，我知道她叫木婉清，是个苦命的女子，父母双亡')
    # wanqing.say('这里有现银%s，你拿去做个小生意吧' %me.cash)
    # me.say('姑娘，我今生必不负你')
    # input('木婉清脸上害羞的红了起来')
    # wanqing.say('嗯，...')
    # input('于是我出了姑娘的屋子，来到街上')
    main()
def main():
    global me
    flag = True
    while flag:
        play_main()
        chose = input('>> ').strip()
        main_menu_do = {"1" : bank, "2" : market, "4" : market, "5" : market, "6" : hospital, "7" : market}
        if chose in main_menu_do.keys():
            main_menu_do[chose](chose)
        if chose == 'r':
            flag = False

def buy_goods(seller, goods, price):
    global me
    import re
    while True:
        count = seller.say('你要多少(返回r)').strip()
        if count == 'r':
            return False
        me.say(count)
        if re.match('^\d+$', count):
            free_count = me.get_free_count()
            cash = me.get_cash()
            total = price * int(count)
            if int(total) <= cash:
                if int(count) <= free_count:
                    seller.say('好嘞，客官，这是您的%s个%s' %(count, goods['name']))
                    me.buy_goods(goods['name'], int(count), total)
                    return True
                else:
                    seller.say('客官，您的背包好像没那么多地儿啊')
                    me.say('对哦，我再考虑一下')
            else:
                seller.say('客官，您好像没那么多银子')
                me.say('对哦，我再考虑一下')
        else:
            seller.say('客官，我听不懂你说什么，Can you speak chinese？')
def sale_goods( seller, goods, price):
    global me
    import re
    while True:
        count = seller.say('你要卖多少(返回r)').strip()
        if count == 'r':
            return False
        me.say(count)
        if re.match('^\d+$', count):
            max_count = me.find_goods_count(goods['name'])
            #cash = me.get_cash()
            total = price * int(count)

            if int(count) <= max_count:
                seller.say('好嘞，客官，这是您的%s两银子' %total)
                #me.buy_goods(goods['name'], int(count), total)
                me.sale_goods(goods['name'], int(count), total)
                return True
            else:
                seller.say('客官，您的背包好像没有那么多%s吧' %goods['name'])
                me.say('对哦，我再考虑一下')
        else:
            seller.say('客官，我听不懂你说什么，Can you speak chinese？')


def hospital( *args):
    global me
    doctor = role.role('江湖郎中')
    doctor.say('老夫人称华佗在世，当年可是御医，专门给后宫的娘娘看妇科的')
    me.think('妇科？？什么鬼？')
    doctor.say('这位客官，有何贵干')
    me.think('废话，找你当然是看病了')
    me.say('大夫，我不太舒服')
    doctor.say('来来来，我给你号号脉')
    input('过了一盏茶的功夫')
    if me.get_hp() == 100:
        doctor.say('这位客官，我看你脉象平稳，不像得了什么病，您是来消遣老夫的吗？')
    else:
        doctor.say('这位客官，你没什么大碍，只是有些肾亏，我给你开几服药调养调养就好了')
        doctor.say('一共需要100两')
        if me.get_cash() > 100:
            me.pay(100)
            me.add_hp(5)
            me.say('啥？这么贵，真是黑心')
            input('不情愿的交了银子走了')
        else:
            me.say('我没那么多银子啊')
            doctor.say('没银子还来看病，滚')
            me.say('此处不留爷，自有留爷处')


def deposit(zhanggui):
    global me
    import re
    while True:
        money = zhanggui.say('您要开多少的银票>> ').strip()
        me.say(money)
        if re.match('^\d+$', money):
            if me.get_cash() >= int(money):
                zhanggui.say('客官，这是您%s两的银票，您收好了，欢迎您再来' %money)
                return True
            else:
                zhanggui.say('客官，您的现银好像不够吧')
                me.say('是哦，我在想想')
        else:
            zhanggui.say('客官，我听不懂你说什么，Can you speak chinese？')
def take_cash(zhanggui):
    pass

def bank(*args):
    global me
    import re
    zhanggui = role.role('钱庄掌柜')
    chose = zhanggui.say('客官，您是开银票(1)还是兑换银票(2)(退出0)>> ').strip()
    chose_do = {"1" : deposit, "2" : take_cash}
    flag = True
    flag2 = True
    while flag:
        if chose in chose_do.keys():
            if chose == '1':
                me.say('开银票')
                if deposit(zhanggui):

                    break
            else:
                me.say('兑换银票')
            if chose_do[chose](zhanggui):
                break

        elif chose == '0':
            break
        else:
            chose = zhanggui.say('客官，我听不懂你说什么，Can you speak chinese？您是开银票(1)还是兑换银票(2)(退出0)>> ')


def market( market_id):
    global me
    import random
    is_do = False
    goods_list = conf.GOODS_list
    # for( i = 0; i < GOODS_LIST_MAX; i++ ){
    #
	# 	plist[i] = goods_list[rlist[i]].min_price + rand32() % ( abs( goods_list[rlist[i]].max_price - goods_list[rlist[i]].min_price ) + 1 );
	# }
    # prices = []
    # for num, goods in enumerate(goods_list, 1):
    #     price = goods['min'] + random.random() * (goods['max'] - goods['min'] + 1)
    #
    #     prices.append(int(price))
    names = {"2" : "北市商贩", "4" : "西市商贩", "5" : "东市商贩", "7" : "南市商贩"}
    seller = role.seller(names[market_id])

    # seller.say(random_news(prices))
    seller.say_news()
    prices = seller.get_prices()

    seller.say('客官，您需要点什么，我这里应有皆有，价格公道')
    me.say('我看看')

    # print(goods_list)
    # print(enumerate(goods_list, 1))





    while True:
        for num, goods in enumerate(goods_list, 1):
            print('%s %s %s' %(num, goods['name'], prices[num - 1]))
        print('0 退出')
        chose = input('>> ').strip()
        #chose in map(lambda x:str(int(x)+1),select_list)
        chose_do_menu = {'1' : buy_goods, '2' : sale_goods }
        if chose in map(lambda x:str(x), range(1, len(goods_list))):
            print(chose)
            chose_goods = goods_list[int(chose) - 1]
            print(chose_goods)
            me.say('%s' %chose_goods['name'])
            chose_do = seller.say('%s？您是买(1)还是卖(2)(返回0) >>' %chose_goods['name']).strip()
            while True:
                if chose_do in chose_do_menu.keys():
                    if(chose_do_menu[chose_do](seller, chose_goods, prices[int(chose) - 1])):
                        seller.say('客官您还看点啥')
                        is_do = True
                        break
                    else:
                        me.say('不不，还是不要%s了'  %chose_goods['name'])
                        seller.say('那您要啥？')
                        break
                elif chose_do == '0':
                    me.say('不要')
                    seller.say('不要您说什么，拿我消遣')
                    break
                else:
                    me.say(chose_do)
                    chose_do = seller.say('客官，我听不懂你说什么，Can you speak chinese？您是买(1)还是卖(2)(返回0) >> ').strip()
        elif chose == '0':
            if is_do:
                seller.say("客官，欢迎您下次再来")
            else:
                seller.say('啥都不干进来干吗，去去去')
                me.say('此处不留爷，自有留爷处')
            me.go_one_day()
            print(me.goods_list)
            break
        else:
            me.say(chose)
            seller.say('客官，Can you speak chinese？')




# def random_news(prices):
#     import random
#     news_list = conf.NEWS_LIST
#     # int rd = rand32() % GOODS_LIST_MAX;
#     #
# 	# system( "cls" );
#     #
# 	# puts( "-北京新闻播报-\n" );
#     #
# 	# //随机选择新闻
# 	# int news_id = rlist[rd] * 4 + rand32() % 4;
#     rd = random.randrange(0, len(prices))
#     news_id = rd * 4 + random.randrange(0, 4)
#     # print(len(news_list))
#     #news = news_list[random.randrange(0, 35585 ) % len(news_list)]
#     news = news_list[news_id]
#     # if( news_list[news_id].impact > 0 ){
#     #
# 	# 	plist[rd] = ( int )( plist[rd] * news_list[news_id].impact );
# 	# }
# 	# else if( news_list[news_id].impact < 0 ){
#     #
# 	# 	plist[rd] = ( int )( plist[rd] / ( -news_list[news_id].impact ) );
# 	# }
#
#     if news['impact'] > 0:
#         # print(prices[news['id']])
#         prices[news['id']] = int(prices[news['id']] * news['impact'])
#         # print(prices[news['id']])
#     else:
#         # print(prices[news['id']])
#         prices[news['id']] = int(prices[news['id']] / (-news['impact']))
#         # print(prices[news['id']])
#     #print('---世界消息---')
#     # input(news['msg'])
#     return news['msg']





def reload_game():
    pass
def exit_game():
    pass
def print_game_info():
    pass
def exit_game():
    pass

def print_main_menu():
    #main_menu = {1:"新的游戏", 2:"旧的记忆", 3:"制作人员", 4:"退出游戏"}
    main_menu = ['新的游戏', '旧的记忆', '制作人员', '退出游戏']

    #print(enumerate(main_menu))
    for menu in enumerate(main_menu):
        print(menu[0]+1, menu[1])


def run():
    # role_1 = role.leading_role(conf.LEADING_ROLE_INIT_DATA)
    # print(role_1.get_name)

    # role_1.say('testing')
    main_menu_do = {"1":new_game, "2":reload_game, "3":print_game_info, "4":exit_game}

    flag = True
    while flag:
        print_main_menu()
        chose = input('\n>> ')
        if chose in main_menu_do.keys():
            main_menu_do[chose]()