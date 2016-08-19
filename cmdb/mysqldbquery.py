#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import types
import re
from MySQLdb.constants import FIELD_TYPE
import os
import sys
import simplejson


reload(sys)
sys.setdefaultencoding('utf-8')

my_conv = {FIELD_TYPE.LONG: int,FIELD_TYPE.TIMESTAMP: str}
# 定义变量，用于在数据库连接的时候，将从数据库中取出的数据long转换成int，timestamp转换成str


class mysqlquery():
# 定义一个类，其中包含select和insert方法

    def __init__(self, host, user, password, dbname, port):   # 构造函数，初始化连接数据库的参数
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port

    def select(self, sql):   # 查询数据库的方法，参数为查询的sql语句
        conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.dbname, port=self.port,conv=my_conv)   # 连接数据库

    # 进行查询数据操作，如果出现错误，退出
        if conn:
            cur = conn.cursor()
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

    def insert(self, sql):  # 向数据库插入数据，参数为插入数据库的sql语句
        conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.dbname, port=self.port, charset='utf8')

        if conn:
            cur = conn.cursor()
            if cur:
                cur.execute('SET NAMES UTF8')
                cur.execute(sql)
                cur.close()
                conn.commit()    # 提交事务
                conn.close()

            else:
                print "mysql cursor error"
                exit(2)

        else:
            print 'connect mysqldb error'
            exit(1)


def sql_insert(tb, tu, data):  # tb:table name, tu:tables columns（字段） ,data:tuple
    # 用于构建插入表中数据的sql语句，实现一次插入多条记录
    # st = str(tu)
    sql = "insert into %s  %s values " % (tb, tu)
    # count = 1
    # for i in data:
    #     if count != len(data):
    #         sql = sql + ' ' + str(i) + ','
    #     else:
    #         sql = sql + ' ' + str(i) + ';'
    # return sql

    count = 0
    for i in data:   # 循环并判断数据的是否是最后一条，分开处理
        count = count + 1
        if count != len(data):
            sql = sql + " " + str(i) + ","
            # print sql
        else:
            sql = sql + " " + str(i) + ";"
    return sql


def cvm_infoo(s):  # os-->osid  zoneID--->zoneId 表的字段转换
    # 进行转换如下
    # +----+------+-----------------+------------------------------------+-------------+-------+
    # | id | osid | product         | description                        | releases    | width |
    # +----+------+-----------------+------------------------------------+-------------+-------+
    # | 1  | 1    | Ubuntu          | Ubuntu12.04.2LTS                   | 12.04       | 64    |
    # | 2  | 2    | CentOS          | CentOS6.4                          | 6.4         | 64    |
    # | 3  | 3    | CentOS          | CentOS6.3                          | 6.3         | 64    |
    # | 4  | 4    | Windows         | Windows2008                        | 2008        | 64    |
    # | 5  | 5    | Xserverwindows  | windows2012                        | 2012        | 64    |
    # | 6  | 6    | Centos6.5       | centos6.5                          | 6.5         | 64    |
    # | 7  | 7    | ubuntu          | ubuntu14.04                        | 14.04       | 64    |
    # | 8  | 8    | centos6.2       | centos6.2                          | 6.2         | 64    |
    # | 9  | 9    | centos7.0       | centos7.0                          | 7.0         | 64    |
    # | 10 | 10   | Xserver         | Xserver V8.1_64                    | V8.1_64     | 64    |
    # | 11 | 11   | Tencent  tlinux | Tencent tlinux release 1.2(Final)  | 1.2(Final)  | 64    |
    # +----+------+-----------------+------------------------------------+-------------+-------+

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

# 区号转换
#         | 100002 | 广州二区
#         | 300001 | 香港一区
#         | 200001 | 上海一区
#         | 100001 | 广州一区
#         | 400001 | 多伦多一区
#
    # +--------+----------+-----------+-----------+
    # | 1      | 一区      | 广州      | 腾讯云     |
    # | 2      | 二区      | 广州      | 腾讯云     |
    # | 3      | 一区      | 香港      | 腾讯云     |
    # | 4      | 一区      | 上海      | 腾讯云     |
    # | 5      | 一区      | 多伦多    | 腾讯云     |
    # +--------+----------+-----------+-----------+
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


def qcloud_project(data):   # 由于原始数据是元组，需要改变对应字段的数值，先转成list，再修改，转成tuple
    d = []
    for i in data:
        t = []
        t.append(i[0])
        t.append(str(i[1]))
        d.append(t)

    for i in d:
        i[0] = int(i[0])

    m = []
    for i in d:
        m.append(tuple(i))

    return m


def trans_price(data, date):  # tuple --> list ,list ---> tuple
    d = []
    for i in data:
        t = []
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


def cvm_info():  # 表 cvm_info，即server_info表
    # qcloud_db(qcloud_cvm)------> ledou_cmdb(cvm_info)
    a = mysqlquery("119.29.183.216", "qcloud", "qcloud", "qcloud", 3306)  # 实例
    sql_qcloud = 'select uuid,instanceName,lanIP,wanIpSet,createTime,deadlineTime,projectId,os,zoneId from qcloud_cvm;'
    # sql语句
    c = a.select(sql_qcloud)  # 查询数据库
    da = cvm_infoo(c)  # 对应字段数据转换
    tu = '(uuid,instanceName,lanIp,wanIpSet,createTime,deadlineTime,projectId,osid,zoneId)'  # 插入数据的字段名
    sql_ledou = sql_insert("cvm_info",tu,da)  # 调用函数，构建插入sql语句

    b = mysqlquery("localhost","ledou","ledou","ledou_cmdb",3306) # 实例
    b.insert(sql_ledou)  # 调用实例方法插入


def project_info():  # 表project
    # qcloud_db(qcloud_project) ---> ledou_cmdd(project_info)
    qp = mysqlquery("119.29.183.216", "qcloud", "qcloud", "qcloud", 3306)
    sql_qp = "select projectId,projectName from qcloud_project;"
    result_qp = qp.select(sql_qp)  # 查询
    project_s = qcloud_project(result_qp) # 字段的数据转换
    # project_s=simplejson.dumps(project_st, encoding="UTF-8", ensure_ascii=False)
    # for i in project_s:
    #     print i
    # # exit(1)
    tb = "project_info"
    tu = '(projectid,projectName)'
    sql_project = sql_insert(tb, tu, project_s)  # 构建插入sql语句
    project_info = mysqlquery("localhost","ledou","ledou","ledou_cmdb",3306)
    project_info.insert(sql_project)


def money():  # server_cost表数据插入
    # qcloud_db(qcloud_price) ---> ledou_cmdd(project_cost)
    date = '2016-08-01'
    projectid = ['1000229', '1000230', '1000231', '1000232', '1000233', '1000234', '1000235', '1000236', '1000237', '1000238', '1000239', '1000240', '1000241', '1000247', '1000266', '1000293', '1000314', '1000325', '1000330', '1000346', '1000347', '1000363', '1000368', '1000380', '1000404', '1000497', '1000498', '1000499', '1000685', '0',  '1001183', '1001202', '1001391', '1002100', '1002220', '1002233',  '1002409', '1002542', '1002558', '1002603',  '1002761', '1002799']
    # project ID
    # | 1000229 | 三剑豪 |
    # | 1000230 | 坦克大战 |
    # | 1000231 | 水果忍者公版 |
    # | 1000232 | 神庙逃亡2 |
    # | 1000233 | 封神劫 |
    # | 1000234 | 极品滑板跑酷 |
    # | 1000235 | 卓游斗地主系列 |
    # | 1000236 | 纪念碑谷 |
    # | 1000237 | 地铁跑酷 |
    # | 1000238 | 烈焰遮天 |
    # | 1000239 | bfrc小鸟爆破狂热 |
    # | 1000240 | 暂用私有网络 |
    # | 1000241 | 公司压力测试机 |
    # | 1000247 | 战神奇迹 |
    # | 1000266 | 霹雳台球8ball |
    # | 1000293 | 奔跑吧兄弟 |
    # | 1000314 | 美人记 |
    # | 1000325 | 三国球霸 |
    # | 1000330 | 四驱三消 |
    # | 1000346 | 水果特工 |
    # | 1000347 | 坚守阵地2 |
    # | 1000363 | 全民大消除 |
    # | 1000368 | 圣斗士星矢 |
    # | 1000380 | Near2 |
    # | 1000404 | 粉碎冠军 |
    # | 1000497 | HeroNeverDie |
    # | 1000498 | 快乐点点消 |
    # | 1000499 | 音乐酷跑 |
    # | 1000501 | 空项目无资源5 |
    # | 1000685 | Ldlog |
    # | 1000804 | 资源池 |
    # | 1001182 | 空项目无资源4 |
    # | 1001183 | 部落英雄传 |
    # | 1001202 | 调教三国 |
    # | 1001391 | 果宝三国 |
    # | 1002100 | 乱斗之王 |
    # | 1002220 | 雷神之城 |
    # | 1002233 | 苍穹变 |
    # | 1002286 | 空项目无资源3 |
    # | 1002409 | 赛尔号 |
    # | 1002453 | 空项目无资源2 |
    # | 1002542 | buddyman |
    # | 1002558 | 虚幻战场 |
    # | 1002603 | 北美SDK |
    # | 1002669 | 空项目无资源1 |
    # | 1002761 | xrpg |
    # | 1002799 | 审核环境 |
    # | 1002879 | MTel |

    for i in projectid:
        price = mysqlquery("119.29.183.216", "qcloud", "qcloud", "qcloud", 3306)
        sql_price = "select c.projectId,sum(price) as money  from (select a.instanceId,a.price,b.projectId from qcloud_cvm_price as a,qcloud_cvm as b where a.instanceId = b.UnInstanceId) as c where c.projectId =%s;" %i
        # 查出每个项目的总费用
        result_price = price.select(sql_price)
        print result_price
        price_s = trans_price(result_price, date)
        tb_cost = "server_costs"
        tu_cost = "(projectId,date,money)"
        sql_cost = sql_insert(tb_cost, tu_cost, price_s)

        # 数据插入
        server_cost = mysqlquery("localhost", "ledou", "ledou", "ledou_cmdb", 3306)
        server_cost.insert(sql_cost)


#
# def zone_info():


# 主函数
if __name__ == '__main__':

    # qcloud_db(qcloud_cvm)------> ledou_cmdb(cvm_info)
    # os.system('mysqldump -h119.29.183.216 -uqcloud -pqcloud qcloud qcloud_cvm  > qcloud_cvm.sql')
    # os.system('mysql -uledou -pledou -hlocalhost ledou_cmdb  < qcloud_cvm.sql')
    # os.system('rm -rf qcloud_cvm.sql')



#    cvm_info()
 #   project_info()
    money()


# 备注：其他的表是自己填入的数据，其中数据如下：
#                                           os_info
# +----+------+-----------------+------------------------------------+-------------+-------+
# | id | osid | product         | description                        | releases    | width |
# +----+------+-----------------+------------------------------------+-------------+-------+
# | 1  | 1    | Ubuntu          | Ubuntu12.04.2LTS                   | 12.04       | 64    |
# | 2  | 2    | CentOS          | CentOS6.4                          | 6.4         | 64    |
# | 3  | 3    | CentOS          | CentOS6.3                          | 6.3         | 64    |
# | 4  | 4    | Windows         | Windows2008                        | 2008        | 64    |
# | 5  | 5    | Xserver windows | windows2012                        | 2012        | 64    |
# | 6  | 6    | Centos 6.5      | centos6.5                          | 6.5         | 64    |
# | 7  | 7    | ubuntu          | ubuntu14.04                        | 14.04       | 64    |
# | 8  | 8    | centos 6.2      | centos6.2                          | 6.2         | 64    |
# | 9  | 9    | centos7.0       | centos7.0                          | 7.0         | 64    |
# | 10 | 10   | Xserver         | Xserver V8.1_64                    | V8.1_64     | 64    |
# | 11 | 11   | Tencent  tlinux | Tencent tlinux release 1.2(Final)  | 1.2(Final)  | 64    |
# +----+------+-----------------+------------------------------------+-------------+-------+

#                   zone_info
# +--------+----------+-----------+-----------+
# | zoneid | zoneName | Region    | idcName   |
# +--------+----------+-----------+-----------+
# |      1 | 一区      | 广州      | 腾讯云    |
# |      2 | 二区      | 广州      | 腾讯云    |
# |      3 | 一区      | 香港      | 腾讯云    |
# |      4 | 一区      | 上海      | 腾讯云    |
# |      5 | 一区      | 多伦多    | 腾讯云    |
# +--------+----------+-----------+-----------+

