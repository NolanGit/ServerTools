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

count = 0


def get_app_price(app_name_id):
    '''
        爬取数据：接收app的Url后缀，返回app价格。
    '''
    global count
    count += 1

    response = requests.get("https://itunes.apple.com/cn/app/" + app_name_id)
    time.sleep(3)
    soup = BeautifulSoup(response.text, 'lxml')

    app_name = soup.find(class_='product-header__title app-header__title')

    app_price = soup.find(class_='inline-list__item inline-list__item--bulleted')
    if app_price == None or app_price == '' or app_price = 'None':
        app_price = soup.find(class_='inline-list__item inline-list__item--bulleted app-header__list__item--price')

    if app_name == None or app_price == None:
        if count >= 10:
            globalvar = Global_Var()
            content = 'app name is ' + str(app_name) + 'app price is ' + str(app_price) + '\n' + response.text
            ms = MailSender('AppPriceMonitorError', 'Crawling data failed!!!', content)
            ms.send_it()
            globalvar.set_value('app_price_monitor_mail_flag', 0)
            threading.Timer(21600, count_time_thread).start()
            return (None, None)
        else:
            get_app_price(app_name_id)

    for name in app_name.strings:
        app_name = name.strip()
        break

    if app_price.text == '免费':
        app_price = 0
    else:
        app_price = float(app_price.text.split('¥')[1])

    return (app_name, app_price)


def app_price_monitor(app_dict):
    '''
        价格监控：接收格式化的app dict，如果超过阈值则触发邮件通知。
    '''
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
    '''
        防止推送邮件被多次触发设置的flag。
    '''
    globalvar = Global_Var()
    globalvar.set_value('app_price_monitor_mail_flag', 1)


def print_result_order_by_length(app_dict):
    '''
        按照app标题长度由短到长打印结果至控制台，无邮件通知逻辑：接收格式化的app dict，打印相关信息于控制台。
    '''
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Working...')
    
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
        print(str(result[x][0]) + ' : ' + '¥' + str(result[x][1]))

    print('=' * 59)


def get_app_price_and_count(app_name_id, app_target_price):
    '''
        适用于多线程的价格监控逻辑
    '''
    result = []
    app_name, app_price = get_app_price(app_name_id)
    result.append([app_name, app_price])


def mutiple_thread(app_dict):
    '''
        多线程爬取数据
    '''
    start_times = int(len(app_dict) / 5)
    start_times_left = len(app_dict) % 5
    for x in range(start_times):
        thread_dict = []
        for i in range(5):
            thread_dict.append(threading.Thread(target=get_app_price_and_count, args=(app_dict.popitem()[0], app_dict.popitem()[1])))


app_dict = {
    'webssh-pro/id497714887': 0,
    'lighten-si-wei-dao-tu/id1132539229': 0,
    'p.m.-splayer-free/id1009747025': 0,
    '7-billion-humans/id1393923918': 0,
    'pico-图像标注/id1395700699': 0,
    'app/id1207354572': 0,
    'app/id1372681079': 0,
    '我的足迹/id1299001064': 0,
    'gorogoa/id1269225754': 0
}

print_result_order_by_length(app_dict)
app_price_monitor(app_dict)