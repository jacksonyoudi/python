#!/usr/bin/env python
# coding: utf-8

import MySQLdb
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import time
import os
import sys

# 保证输入中文，不会乱码
reload(sys)
sys.setdefaultencoding("utf-8")

# 定义邮件方面的变量
mailto_list = ["18684541304@163.com", "liangchangyoujackson@gmail.com"]  # 邮件接收方的邮件地址
# 把提醒邮件发送给多人，如用户本人和管理员。
# 另外，用户的邮件地址可以从一个保存用户基本信息的数据库进行提取。


# 定义邮件发件人地址等。
mail_host = "smtp.189.cn"  # 邮件传送协议服务器
mail_user = "18684541304@189.cn"  # 邮件发送方的邮箱账号
mail_pass = "719274671"  # 邮件发送方的邮箱密码


# 定义发送邮件的函数
def send_mail(to_list, sub, content):
    me = "跳板机用户邮件提醒" + "<" + mail_user + ">"
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


# 定义函数，完成到数据库中提取用户信息，主要是用户名和过期时间
def mysqlselect():  # 连接数据库，进行sql操作
    try:
        sql = 'select * from user where active = 0;'  # 过滤出所有未锁定用户信息。
        c = MySQLdb.connect(host='localhost', user='userdate', passwd='userdate', db='userdate', port=3306,
                            charset='utf8')
        cur = c.cursor()
        cur.execute(sql)
        t = cur.fetchall()
        cur.close()
        c.close()
        return t
    except Exception, e:
        print e


# 数据的表结构如下，其中 active主要是用来标记用户是否被锁定。
# mysql> desc user;
# +----------+-------------+------+-----+---------+----------------+
# | Field    | Type        | Null | Key | Default | Extra          |
# +----------+-------------+------+-----+---------+----------------+
# | uid      | int(11)     | NO   | PRI | NULL    | auto_increment |
# | username | varchar(30) | NO   | UNI | NULL    |                |
# | expire   | date        | NO   |     | NULL    |                |
# | active   | tinyint(4)  | NO   |     | 0       |                |
# +----------+-------------+------+-----+---------+----------------+


# mysql> select * from user;
# +-----+----------+------------+--------+
# | uid | username | expire     | active |
# +-----+----------+------------+--------+
# |   1 | youdi    | 2016-08-20 |      0 |
# |   2 | xiong    | 2016-08-21 |      0 |
# |   3 | hui      | 2016-08-22 |      1 |
# |   4 | jackson  | 2017-01-20 |      0 |
# |   5 | chen     | 2016-08-18 |      1 |
# |   6 | nihao    | 2016-08-19 |      1 |
# +-----+----------+------------+--------+


# 定义函数 用来计算今天和过期时间的差。
def lastdays(day):
    today = datetime.date.today()
    days = (day - today).days
    return days


# 修改数据库中的active的值。0 表示未锁定， 1 表示锁定。
def modactive(user):
    try:
        sql = "update user set active = 1 where username = '%s' " % user
        c = MySQLdb.connect(host='localhost', user='userdate', passwd='userdate', db='userdate', port=3306,
                            charset='utf8')
        cur = c.cursor()
        cur.execute(sql)
        c.commit()
        cur.close()
        c.close()
        return t
    except Exception, e:
        print e


if __name__ == '__main__':
    data = mysqlselect()  # 获取所有未锁定用户信息
    for i in data:   # 遍历
        days = lastdays(i[2])  # 算出距离过期的时间
        if days > 7:   # 如果  距离过期时间是大于7天，进行下一个用户的遍历
            continue
        elif days == 0:  # 如果 今天是过期时间，进行以下操作
            name = i[1]
            sub = "跳板机用户锁定通知"
            content = '%s,您的跳板机登录的权限已经过期，已经禁止登录了。' % name
            cmd = 'usermod -L %s' % name
            stat = os.system(cmd)   # 使用 usermod -L username  锁定用户
            if stat == 0:
                print '%s 用户锁定成功' % name
                # 用户锁定以后要在数据库中将active字段改为1
                modactive(name)       # 修改 数据库中active的值
            else:
                print '%s 用户锁定失败，请您处理' % name

            if send_mail(mailto_list, sub, content):   # 发送邮件
                print "发送成功"
            else:
                print "发送失败"
        else:      # 如果 过期时间是在 0--7天之内的话。发送邮件提醒即将过期。
            name = i[1]
            sub = "跳板机用户过期提醒"
            content = '%s,您的跳板机登录的权限即将过期，剩余%s天，%s就会禁止登录' % (name, days, i[2])
            if send_mail(mailto_list, sub, content):
                print "发送成功"
            else:
                print "发送失败"
