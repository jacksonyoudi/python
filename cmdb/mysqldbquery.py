#!/usr/bin/env python

# coding=utf-8
# -*- coding: utf-8 -*-

import MySQLdb
import types
import re
from MySQLdb.constants import FIELD_TYPE
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')




my_conv = {FIELD_TYPE.LONG: int,FIELD_TYPE.TIMESTAMP: str}


class mysqlquery():
    '''  '''
    def __init__(self,host,user,password,dbname,port):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port

    def select(self,sql):
        conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.dbname,port=self.port,conv=my_conv)

        if conn:
            cur =conn.cursor()
            if cur:
                cur.execute('SET NAMES UTF8')
                cur.execute(sql)
                a = cur.fetchall()
                cur.close()
                conn.close()
                return a
            else:
                print "mysql cursor error"
                exit(2)

        else:
            print 'connect mysqldb error'
            exit(1)

    def insert(self,sql):
        conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.dbname, port=self.port,charset='utf8')

        if conn:
            cur = conn.cursor()
            if cur:
                b = cur.execute(sql)
                cur.close()
                conn.commit()
                conn.close()
                print b
            else:
                print "mysql cursor error"
                exit(2)

        else:
            print 'connect mysqldb error'
            exit(1)


def sql_insert(tb,tu,data): #tb:table name,tu:tables columns ,data:tuple
    # st = str(tu)
    sql = "insert into %s  %s values " %(tb,tu)
    count = 0
    for i in data:
        count=count+1
        if count != len(data):
            sql = sql + " " + str(i) + ","
        else:
            sql = sql + " " + str(i) +";"
    return sql


def cvm_info(s):  # os-->osid  zoneID--->zoneId
    data = []
    for i in s:
        t = []
        for j in i:
            t.append(j)
        data.append(t)
    for i in data:
        if re.match('ubuntu12', i[7], flags=re.I):
            i[7] = "1"
        if re.match('centos6.4', i[7], flags=re.I):
            i[7] = "2"
        if re.match('centos6.3', i[7], flags=re.I):
            i[7] = "3"
        if re.match('Windows 2008', i[7], flags=re.I):
            i[7] = "4"
        if re.match('Xserver windows', i[7], flags=re.I):
            i[7] = "5"
        if re.match('centos6.5', i[7], flags=re.I):
            i[7] = "6"
        if re.match('ubuntu14', i[7], flags=re.I):
            i[7] = "7"
        if re.match('centos6.2', i[7], flags=re.I):
            i[7] = "8"
        if re.match('centos7.0', i[7], flags=re.I):
            i[7] = "9"
        if re.match('Xserver V8.1_64', i[7], flags=re.I):
            i[7] = "10"
        if re.match('Tencent', i[7], flags=re.I):
            i[7] = "11"

    # for i in data:
    #     i[8] = int(i[8])

    for i in data:
        if i[8] == 100001:
            i[8] = 1
        if i[8] == 100002:
            i[8] = 2
        if i[8] == 200001:
            i[8] = 3
        if i[8] == 300001:
            i[8] = 4
        if i[8] == 400001:
            i[8] = 5
    datat = []
    for i in data:
        datat.append(tuple(i))

    return datat

def qcloud_project(data):
    d = []
    for i in data:
        t = []
        for j in i:
            t.append(j)
        d.append(t)
    print d
    for i in d:
        i[0] = int(i[0])

    m = []
    for i in d:
        m.append(tuple(i))

    return m


def trans_price(data,date):
    d=[]
    for i in data:
        t=[]
        for j in i:
            t.append(j)
        d.append(t)

    m = []
    for i in d:
        t = []
        t.append(str(i[0]))
        t.append(date)
        t.append(int(i[1]))
        m.append(t)


    d = []
    for i in m:
        d.append(tuple(i))

    return d

def money():
    # qcloud_db(qcloud_price) ---> ledou_cmdd(project_cost)
    date = '2016-08-01'
    projectid = ['1000229', '1000230', '1000231', '1000232', '1000233', '1000234', '1000235', '1000236', '1000237', '1000238', '1000239', '1000240', '1000241', '1000247', '1000266', '1000293', '1000314', '1000325', '1000330', '1000346', '1000347', '1000363', '1000368', '1000380', '1000404', '1000497', '1000498', '1000499', '1000685', '0',  '1001183', '1001202', '1001391', '1002100', '1002220', '1002233',  '1002409', '1002542', '1002558', '1002603',  '1002761', '1002799']
    for i in projectid:
        price = mysqlquery("119.29.183.216", "qcloud", "qcloud", "qcloud", 3306)
        sql_price = "select c.projectId,sum(price) as money  from (select a.instanceId,a.price,b.projectId from qcloud_cvm_price as a,qcloud_cvm as b where a.instanceId = b.UnInstanceId) as c where c.projectId =%s;" %i
        result_price = price.select(sql_price)
        print result_price
        price_s = trans_price(result_price,date)
        tb_cost = "server_costs"
        tu_cost = "(projectId,date,money)"
        sql_cost = sql_insert(tb_cost,tu_cost,price_s)

        server_cost = mysqlquery("localhost","ledou","ledou","ledou_cmdb",3306)
        server_cost.insert(sql_cost)




if __name__ == "__main__":

    # qcloud_db(qcloud_cvm)------> ledou_cmdb(cvm_info)
    # a = mysqlquery("119.29.183.216", "qcloud", "qcloud", "qcloud", 3306)
    # sql_qcloud = 'select uuid,instanceName,lanIP,wanIpSet,createTime,deadlineTime,projectId,os,zoneId from qcloud_cvm;'
    # c = a.select(sql_qcloud)
    # da = cvm_info(c)
    # tu = '(uuid,instanceName,lanIp,wanIpSet,createTime,deadlineTime,projectId,osid,zoneId)'
    # sql_ledou = sql_insert("cvm_info",tu,da)
    #
    # b = mysqlquery("localhost","ledou","ledou","ledou_cmdb",3306)
    # b.insert(sql_ledou)

    # qcloud_db(qcloud_cvm)------> ledou_cmdb(cvm_info)
    # os.system('mysqldump -h119.29.183.216 -uqcloud -pqcloud qcloud qcloud_cvm  > qcloud_cvm.sql')
    # os.system('mysql -uledou -pledou -hlocalhost ledou_cmdb  < qcloud_cvm.sql')
    # os.system('rm -rf qcloud_cvm.sql')

    # qcloud_db(qcloud_project) ---> ledou_cmdd(project_info)
    # qp = mysqlquery("119.29.183.216", "qcloud", "qcloud", "qcloud", 3306)
    # sql_qp = "select projectId,projectName from qcloud_project;"
    # result_qp =  qp.select(sql_qp)
    # project_s = qcloud_project(result_qp)
    # tb = "project_info"
    # tu = '(projectid,projectName)'
    # sql_project = sql_insert(tb,tu,project_s)
    # print sql_project
    # project_info = mysqlquery("localhost","ledou","ledou","ledou_cmdb",3306)
    # project_info.insert(sql_project)

    money()






