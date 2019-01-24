# -*- coding:utf-8 -*-
import sys
import time
import requests
import threading
sys.path.append('../')
sys.path.append('../../')
from bs4 import BeautifulSoup
from Common.Tools import Tools
from Common.Mail_Sender import MailSender
from Common.Global_Var import Global_Var


def get_app_price(app_name_id):
    # 爬取数据
    response = requests.get("https://itunes.apple.com/cn/app/" + app_name_id)
    soup = BeautifulSoup(response.text, 'lxml')
    app_name = soup.find(class_='product-header__title app-header__title')
    app_price = soup.find(class_='inline-list__item inline-list__item--bulleted')
    for name in app_name.strings:
        app_name = name.strip()
        break
    #print(app_name + ' : ' + app_price.text)
    return (app_name, float(app_price.text.split('¥')[1]))


def app_price_monitor(app_dict):
    # 判断是否触发邮件通知阈值
    content = ''
    globalvar = Global_Var()
    for key in app_dict.keys():
        app_name, app_price = get_app_price(key)
        if app_price <= float(app_dict[key]):
            content = content + '\n' + '[' + app_name + ']' + ' is ¥' + str(app_price) + ' now !'
    if content != '':
        app_price_monitor_mail_flag = globalvar.get_value('app_price_monitor_mail_flag')
        if app_price_monitor_mail_flag == "None":
            globalvar.set_value('app_price_monitor_mail_flag', 1)
        if app_price_monitor_mail_flag == 1:
            ms = MailSender('AppPriceMonitor', 'App Discount!', content)
            ms.send_it()
            globalvar.set_value('app_price_monitor_mail_flag', 0)
            threading.Timer(21600, count_time_thread).start()


def count_time_thread():
    # 防止推送邮件被多次触发
    globalvar = Global_Var()
    globalvar.set_value('app_price_monitor_mail_flag', 1)


def print_result_order_by_length(app_dict):
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+' Working...')
    # 按照app标题长度由短到长打印结果至控制台
    result = []
    count = 0
    for key in app_dict.keys(): 
        Tools().show_process_bar(count, int(len(app_dict)))
        app_name, app_price = get_app_price(key)
        result.append([app_name, app_price])
        count += 1
    for x in range(len(result)):
        for y in range(len(result) - x - 1):
            if len(result[y][0]) > len(result[y + 1][0]):
                result[y][0], result[y + 1][0] = result[y + 1][0], result[y][0]
                result[y][1], result[y + 1][1] = result[y + 1][1], result[y][1]
    print('=' * 20 + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '=' * 20)
    for x in range(len(result)):
        print(result[x][0] + ' : ' + '¥' + str(result[x][1]))
    print('=' * 59)


app_dict = {
    'webssh-pro/id497714887': 0,
    'lighten-si-wei-dao-tu/id1132539229': 0,
    'p.m.-splayer-free/id1009747025': 0,
    '7-billion-humans/id1393923918': 0,
    'pico-图像标注/id1395700699': 0,
    'app/id1207354572': 0,
    'app/id1372681079': 0,
    '我的足迹/id1299001064': 0
    }
print_result_order_by_length(app_dict)
app_price_monitor(app_dict)

#'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&ch=&wd=App+Store+%E9%A2%84%E8%A7%88+shelly+appstore+site%3Aitunes.apple.com'
