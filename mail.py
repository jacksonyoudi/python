#!/usr/bin/env python
# coding: utf8

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import time

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

mailto_list = ["18684541304@163.com", "liangchangyoujackson@gmail.com"]  # 邮件接收方的邮件地址
mail_host = "smtp.189.cn"  # 邮件传送协议服务器
mail_user = "18684541304@189.cn"  # 邮件发送方的邮箱账号
mail_pass = "719274671"  # 邮件发送方的邮箱密码


def send_mail(to_list, sub, content):
    me = "跳板机用户过期提醒" + "<" + mail_user + ">"
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub  # 邮件主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == '__main__':
    sub = "跳板机过期提醒"
    content = 'test'
    if send_mail(mailto_list, sub, content):
        print "发送成功"
    else:
        print "发送失败"
