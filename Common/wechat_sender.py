#coding=utf-8
import os
import sys
import time
import requests
import platform
import configparser

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
SCKEY = cf.get('config', 'SCKEY')


class Wechat_Sender(object):

    '''
        使用服务"Server酱"(http://sc.ftqq.com)，感谢大佬。
    '''

    def __init__(self):
        pass

    def send(self, text, desp):
        '''向微信推送通知
            
        Args:
            text (str)
            desp (str)

        Returns:
            code（str）
        '''
        payload = {'text': text, 'desp': desp}
        r = requests.get('https://sc.ftqq.com/' + SCKEY + '.send', params=payload)
        return str(r)