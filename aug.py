#!/usr/bin/env python
#coding: utf-8

import MySQLdb

username='liangchangyou'

sql='select c.name from auth_user as a,auth_user_groups as b,auth_group as c where a.id=b.user_id and b.group_id = c.id and a.username="%s";' % username

def mysql(sql):   #连接数据库，进行sql操作
    try:
        c=MySQLdb.connect(host='localhost',user='saltweb',passwd='saltweb',db='saltweb',port=3306)
        cur=c.cursor()
        cur.execute(sql)
        t=cur.fetchall()
        cur.close()
        c.close()
        return t[0][0]
    except Exception,e:
        print e

if __name__ == "__main__":
    a=mysql(sql)
    print a


