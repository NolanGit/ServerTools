# -*- coding:utf-8 -*-
import os
import sys
import time
import peewee
import datetime
import requests
import platform
import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.append('../')
sys.path.append('../../')
from Common.Tools import Tools
from Common.model import Weather, AQI, City


def get_key():
    cf = configparser.ConfigParser()
    if 'Windows' in platform.platform() and 'Linux' not in platform.platform():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using C:/Users/sunhaoran/Documents/GitHub/ServerTools/ServerTools.config ...')
        cf.read('C:/Users/sunhaoran/Documents/GitHub/ServerTools/ServerTools.config')
    elif 'Linux' in platform.platform() and 'Ubuntu' not in platform.platform():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using /home/pi/Documents/Github/ServerTools/RaspberryPi.config ...')
        cf.read('/home/pi/Documents/Github/RaspberryPi.config')
    elif 'Ubuntu' in platform.platform():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using /root/Documents/GitHub/ServerTools/ServerTools.config ...')
        cf.read('/root/Documents/GitHub/ServerTools/ServerTools.config')
    key = (cf.get('config', 'KEY'))
    return key


def get_temp(key: str, location: str):
    payload = {'location': location, 'key': key}
    r = requests.get('https://free-api.heweather.com/s6/weather/forecast', params=payload)
    today_forecast = r.json()['HeWeather6'][0]['daily_forecast'][0]
    today_tmp_max = today_forecast['tmp_max']  # 今天最高气温
    today_tmp_min = today_forecast['tmp_min']  # 今天最低气温
    return (today_tmp_max, today_tmp_min)


def get_aqi(key: str, location: str):
    payload = {'location': location, 'key': key}
    r = requests.get('https://free-api.heweather.net/s6/air/now', params=payload)
    return (r.json()['HeWeather6'][0])


def save_temp(city_name, max_temp, min_temp):
    city_code = City.select().where(City.city_name == city_name)['id']
    p = Weather(city_code=city_code, max_temp=max_temp, min_temp=min_temp, date=datetime.datetime.now().date(), time=datetime.datetime.now().strftime('%H:%M:%S'))
    p.save()


def save_aqi(city_name, site_name, aqi, main, pm10, pm25, no2, so2, co, o3):
    city_code = City.select().where(City.city_name == city_name)['id']
    try:
        crawling_times = int(len(AQI.select().where((AQI.date == datetime.datetime.now().date()) & (AQI.site_name == site_name))))
    except Exception:
        crawling_times = 0
    p = AQI(
        city_code=city_code,
        site_name=site_name,
        aqi=aqi,
        main=main,
        pm10=pm10,
        pm25=pm25,
        no2=no2,
        so2=so2,
        co=co,
        o3=o3,
        crawling_times=crawling_times,
        date=datetime.datetime.now().date(),
        time=datetime.datetime.now().strftime('%H:%M:%S'))
    p.save()

key = get_key()


crawling_times = int(len(Weather.select().where((Weather.date == datetime.datetime.now().date()) & (Weather.city_code == '长春'))))
if crawling_times ==0:
    today_tmp_max, today_tmp_min = get_temp(key, 'changchun')
    save_temp('长春', today_tmp_max, today_tmp_min)
    print('TEMP: 长春 temperature saved')

aqi_json = get_aqi(key, 'changchun')
city_aqi = aqi_json['air_now_city']
city_aqi['site_name'] = '-'
save_aqi('长春', city_aqi['site_name'], city_aqi['aqi'], city_aqi['main'], city_aqi['pm10'], city_aqi['pm25'], city_aqi['no2'], city_aqi['so2'], city_aqi['co'], city_aqi['o3'])
print('AQI: 长春 '+ '[-]'+' saved')
site_aqi = aqi_json['air_now_station']
for single_aqi in site_aqi:
    site_name = single_aqi['air_sta']
    aqi = single_aqi['aqi']
    main = single_aqi['main']
    pm10 = single_aqi['pm10']
    pm25 = single_aqi['pm25']
    no2 = single_aqi['no2']
    so2 = single_aqi['so2']
    co = single_aqi['co']
    o3 = single_aqi['o3']
    save_aqi('长春', site_name, aqi, main, pm10, pm25, no2, so2, co, o3)
    print('AQI: 长春 '+ '['+site_name+']'+' saved')
