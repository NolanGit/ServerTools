# -*- coding:utf-8 -*-
import os
import sys
import time
import peewee
import datetime
import requests
import platform
import traceback
import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.append('../')
sys.path.append('../../')
from Common.wechat_sender import Wechat_Sender
from Common.ui_automation_common import CommonActions


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
KINDLE_LOGIN_URL = cf.get('config', 'KINDLE_LOGIN_URL')
KINDLE_lOGIN_USERNAME = cf.get('config', 'KINDLE_lOGIN_USERNAME')
KINDLE_lOGIN_PASSWORD = cf.get('config', 'KINDLE_lOGIN_PASSWORD')
KINDLE_MAIN_URL = cf.get('config', 'KINDLE_MAIN_URL')


def push():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        driver = webdriver.Chrome(executable_path=('/usr/bin/chromedriver'), chrome_options=chrome_options)

        driver.get(KINDLE_LOGIN_URL)
        common_actions = CommonActions(driver)
        common_actions.send('field-email_address',KINDLE_lOGIN_USERNAME)
        common_actions.send('field-password',KINDLE_lOGIN_PASSWORD)
        common_actions.click("//input[@class='submit-button']")
        time.sleep(5)
        driver.get(KINDLE_MAIN_URL)
        common_actions.click("//button[@class='button-secondary']")
    except Exception as e:
        print(e)
        traceback.print_exc()
    
    
push()