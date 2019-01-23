#coding=utf-8
import os
import sys
import threading
sys.path.append('../')
sys.path.append('../../')
from Common.Mail_Sender import MailSender
from Common.Global_Var import Global_Var


def get_extranet_ip():
    for x in range(100):
        current_ip = os.popen("curl icanhazip.com").read()
        current_ip = str(current_ip.replace("\n", ""))
        if current_ip != None and current_ip !='':
            break
        else:
            print("WARNING: Current extranet IP is : " + current_ip)
            raise Exception("Bad requests !")
    print("Current extranet IP is : " + current_ip)
    return current_ip


def diff_extranet_ip(current_ip):
    global_var = Global_Var()
    history_ip = global_var.get_value('current_ip')
    if current_ip != history_ip or history_ip == None:
        global_var.set_value('current_ip', current_ip)
        content = 'New extranet IP is ' + '[' + current_ip + ']'+'\n'+ 'History IP is ' + '[' + history_ip + ']'
        ms = MailSender('IP Monitor', 'Extranet IP changed!', content)
        ms.send_it()


current_ip = get_extranet_ip()
diff_extranet_ip(current_ip)
