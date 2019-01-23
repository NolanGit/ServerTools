# -*- coding:utf-8 -*-
import os
import sys
import time
import requests
import platform
import configparser
sys.path.append('../')
sys.path.append('../../')
from Common.Mail_Sender import MailSender


def get_key():
    cf = configparser.ConfigParser()
    if 'Windows' in platform.platform() and 'Linux' not in platform.platform():
        print('Reading C:/Users/sunhaoran/Documents/GitHub/ServerTools/ServerTools.config ...')
        cf.read('C:/Users/sunhaoran/Documents/GitHub/ServerTools/ServerTools.config')
    elif 'Linux' in platform.platform() and 'Ubuntu' not in platform.platform():
        print('Reading /home/pi/Documents/Github/ServerTools/ServerTools.config ...')
        cf.read('/home/pi/Documents/Github/ServerTools/ServerTools.config')
    elif 'Ubuntu' in platform.platform():
        print('Reading /root/Documents/GitHub/ServerTools/ServerTools.config ...')
        cf.read('/root/Documents/GitHub/ServerTools/ServerTools.config')
    key = (cf.get('config', 'KEY'))
    return key


def get_weather(key):
    payload = {'location': 'beijing', 'key': key}
    r = requests.get('https://free-api.heweather.com/s6/weather/forecast', params=payload)
    today_forecast = r.json()['HeWeather6'][0]['daily_forecast'][0]
    tomorow_forecast = r.json()['HeWeather6'][0]['daily_forecast'][1]
    today_code_n = today_forecast['cond_code_n']
    tomorow_code_d = tomorow_forecast['cond_code_d']
    print('today_code_n = ' + today_code_n)
    print('tomorow_code_d = ' + tomorow_code_d)
    weather_content = air_content = temprature_content = ''
    today_txt_n = today_forecast['cond_txt_n']  # 今天夜间天气状况文字
    tomorow_txt_d = tomorow_forecast['cond_txt_d']  # 明天白天天气状况文字
    today_tmp_max = today_forecast['tmp_max']  # 今天最高气温
    today_tmp_min = today_forecast['tmp_min']  # 今天最低气温
    tomorow_tmp_max = tomorow_forecast['tmp_max']  # 明天最高气温
    tomorow_tmp_min = tomorow_forecast['tmp_min']  # 明天最低气温
    if (int(today_code_n) > 299 and int(today_code_n) < 500) or (int(tomorow_code_d) > 299 and int(tomorow_code_d) < 500):
        weather_content = '降水注意：今天夜间天气为【' + today_txt_n + '】，最高气温：' + str(today_tmp_max) + '°C，最低气温：' + str(today_tmp_min) + '°C；' + '\n' + '明天白天天气为【' + tomorow_txt_d + '】，最高气温' + str(tomorow_tmp_max) + '°C，最低气温' + str(
            tomorow_tmp_min) + '°C。'
    if (int(today_code_n) > 501 and int(today_code_n) < 900) or (int(tomorow_code_d) > 501 and int(tomorow_code_d) < 900):
        air_content = '空气质量注意：今天夜间天气为【' + today_txt_n + '】；' + '\n' + '明天白天天气为【' + tomorow_txt_d + '】'
    current_month = time.strftime("%m", time.localtime())
    if (int(current_month) > 0 and int(current_month) < 5) or (int(current_month) > 8 and int(current_month) <= 12):
        print('当前是%s月%s日' % (current_month,time.strftime("%d", time.localtime())))
        if (int(tomorow_tmp_min) - int(today_tmp_min)) <= -5:
            temprature_content = '温度注意：明日最低气温为' + tomorow_tmp_min + '°C！'
    if int(current_month) > 4 and int(current_month) < 9:
        print('当前是%s月%s日' % (current_month,time.strftime("%d", time.localtime())))
        if (int(tomorow_tmp_max) - int(today_tmp_max)) >= 5:
            temprature_content = '温度注意：明日最高气温为' + tomorow_tmp_max + '°C！'

    return weather_content + air_content + temprature_content

print('=' * 10 + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '=' * 10)
key = get_key()
content = get_weather(key)
print(content)
if content != '':
    ms = MailSender('WeatherMonitor', 'Weather Anomaly!', content)
    ms.send_it()
print('='*39)
