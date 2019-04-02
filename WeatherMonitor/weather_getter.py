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
    city_code = City.select('id').where(City.city_name == city_name)
    p = Weather(city_code=city_code, max_temp=max_temp, min_temp=min_temp, date=datetime.datetime.now().date(), time=datetime.datetime.now().strftime('%H:%M:%S'))
    p.save()
    print('data saved...')


def save_aqi(city_name, site_name, aqi, main, pm10, pm25, no2, so2, co, o3):
    city_code = City.select('id').where(City.city_name == city_name)
    p = AQI(city_code=city_code, site_name=site_name, aqi=aqi, main=main, pm10=pm10, pm25=pm25, no2=no2, so2=so2, co=co, o3=o3, date=datetime.datetime.now().date(), time=datetime.datetime.now().strftime('%H:%M:%S'))
    p.save()
    print('data saved...')


key = get_key()
today_tmp_max, today_tmp_min = get_temp(key, 'changchun')
#save_temp('changchun',today_tmp_max, today_tmp_min)

aqi_json = get_aqi(key, 'changchun')
city_aqi = aqi_json['air_now_city']
city_aqi['site_name'] = '-'
print(city_aqi)
site_aqi=aqi_json['air_now_station']
for single_aqi in site_aqi:
    print('site_name= '+single_aqi['air_sta']) 
    print('aqi= '+single_aqi['aqi']) 
    print('main= '+single_aqi['main']) 
    print('pm10= '+single_aqi['pm10']) 
    print('pm25= '+single_aqi['pm25']) 
    print('no2= '+single_aqi['no2']) 
    print('so2= '+single_aqi['so2']) 
    print('co= '+single_aqi['co']) 
    print('o3= '+single_aqi['o3'])
    print('='*10)
    