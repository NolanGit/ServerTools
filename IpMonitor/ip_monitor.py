#coding=utf-8
import os
import sys
import socket
import requests
import platform
import threading
sys.path.append('../')
sys.path.append('../../')
from Common.Global_Var import Global_Var
from Common.Mail_Sender import MailSender


def get_extranet_ip():
    for x in range(100):
        current_ip = os.popen("curl icanhazip.com").read()
        current_ip = str(current_ip.replace("\n", ""))

        if current_ip != None and current_ip != '':
            break
        else:
            print("WARNING: Current extranet IP is : " + current_ip)
            raise Exception("Bad requests !")

    print("Current extranet IP is : " + current_ip)
    return current_ip


def get_intranet_ip():
    ip_address = "0.0.0.0"
    sysstr = platform.system()

    if sysstr == "Windows":
        ip_address = socket.gethostbyname(socket.gethostname())
        print("Windows @ " + ip_address)
        return ip_address

    elif sysstr == "Linux":
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('www.baidu.com', 0))
            ip_address = s.getsockname()[0]
        except:
            ip_address = "x.x.x.x"
        finally:
            s.close()
        print("Linux @ " + ip_address)
        return ip_address

    elif sysstr == "Darwin":
        ip_address = socket.gethostbyname(socket.gethostname())
        print("Mac @ " + ip_address)
        return ip_address

    else:
        print("Other System @ some ip")
        return ("x.x.x.x")


def diff_extranet_ip(current_extranet_ip, current_intranet_ip):
    global_var = Global_Var()
    history_extranet_ip = global_var.get_value('current_extranet_ip')
    history_intranet_ip = global_var.get_value('current_intranet_ip')
    content = ''

    if (current_extranet_ip != history_extranet_ip or history_extranet_ip == None) and current_extranet_ip != None:
        global_var.set_value('current_extranet_ip', current_extranet_ip)
        content = content + 'New extranet IP is ' + '[' + current_extranet_ip + ']' + '\n' + 'History extranet IP is ' + '[' + history_extranet_ip + ']' + '\r'
    
    if (current_intranet_ip != history_intranet_ip or history_intranet_ip == None) and current_intranet_ip != None:
        global_var.set_value('current_intranet_ip', current_intranet_ip)
        content = content + 'New intranet IP is ' + '[' + current_intranet_ip + ']' + '\n' + 'History intranet IP is ' + '[' + history_intranet_ip + ']' + '\r'
    
    print('Content: '+content)
    
    if content != '':
        ms = MailSender('IP Monitor', 'IP changed!', content)
        ms.send_it()


current_extranet_ip = get_extranet_ip()
current_intranet_ip = get_intranet_ip()
diff_extranet_ip(current_extranet_ip, current_intranet_ip)
