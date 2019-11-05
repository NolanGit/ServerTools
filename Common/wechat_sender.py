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
        send()
    '''

    def __init__(self):
        pass

    def send(self, title, content):
        '''向微信推送通知
            
        Args:
            title (str)
            content (str)

        Returns:
            code（str）
        '''
        payload = {'text': title, 'desp': content}
        r = requests.get('https://sc.ftqq.com/' + SCKEY + '.send', params=payload)
        print(eval(r.text)['errmsg'])
        if eval(r.text)['errno']==0:
            return 'success'
        else:
            from .Mail_Sender import MailSender
            ms=MailSender('Administrator','push wechat failed!',content)
            ms.send_it()
            return 'failed'
        return str(r)