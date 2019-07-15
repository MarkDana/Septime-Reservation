#!/usr/bin/python
# coding: utf-8
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import datetime,time,random

from prettytable import PrettyTable
from colorama import init,Fore
init(autoreset=True)
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import json
import requests
from config import *

# to check all the available dates: https://module.lafourchette.com/en_GB/resa/pick-date/2/10889-d34ca/54499
# to check times for a specific date: https://module.lafourchette.com/en_GB/resa/pick-time/2/2019-07-18/10889-d34ca/54499


def sendEmail(mail_host,mail_user,mail_pass,sender,receivers,theday,num_of_us):
    content = 'https://module.lafourchette.com/en_GB/cta/iframe/10889-d34ca#/54499/pdh?pax={}&date={}'.format(str(num_of_us),theday)
    title = '!!!SEPTIME HURRY!!!'

    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # ssl
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

def check_available():
    r = requests.get('https://module.lafourchette.com/en_GB/resa/pick-date/%d/10889-d34ca/54499'%(num_of_us),headers=header)
    c = json.loads(r.text)
    availableDateList = c['availableDateList']

    while (True):
        print("======="+datetime.datetime.now().strftime('%m.%d-%H:%M:%S')+"=======")
        table = PrettyTable(['DATE', 'LUNCH', 'DINER'])
        for availableDate in availableDateList:
            theday=availableDate['date']

            if(theday in my_wanted_days):sendEmail(mail_host,mail_user,mail_pass,sender,receivers,theday,num_of_us)

            url_time='https://module.lafourchette.com/en_GB/resa/pick-time/{}/{}/10889-d34ca/54499'.format(str(num_of_us),theday)
            r_time = requests.get(url_time,headers=header)
            c_time = json.loads(r_time.text)
            availableTimeslotList = c_time['availableTimeslotList']
            lunchstr, dinnerstr = '', ''
            for availableTimeslot in availableTimeslotList:
                if availableTimeslot['timeslots']:
                    if availableTimeslot['name']=="LUNCH":
                        for timeslot in availableTimeslot['timeslots']:
                            if(timeslot["sale_type_list"]['hasNormalSaleType']==1):lunchstr+=(Fore.RED+timeslot['time']+Fore.RESET+'/')
                            else: lunchstr+=(timeslot['time']+'/')
                    elif availableTimeslot['name'] == "DINER":
                        for timeslot in availableTimeslot['timeslots']:
                            if (timeslot["sale_type_list"]['hasNormalSaleType'] == 1):
                                dinnerstr += (Fore.RED + timeslot['time']  + Fore.RESET+ '/')
                            else:
                                dinnerstr += (timeslot['time'] + '/')
            table.add_row([theday,lunchstr if lunchstr else 'NONE',dinnerstr if dinnerstr else 'NONE'])
            time.sleep(random.uniform(1, 3))

        print(table)
        time.sleep(random.uniform(20,30))


if __name__ == '__main__':
    check_available()


