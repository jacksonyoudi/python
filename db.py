#!/usr/bin/env python

#coding: utf8



import MySQLdb
from MySQLdb.constants import FIELD_TYPE


my_conv = {FIELD_TYPE.LONG: int,FIELD_TYPE.TIMESTAMP: str}
conn = MySQLdb.connect(host="localhost",
                       user="test",
                       passwd="test",
                       db="test",
                       port=3306,
                       conv=my_conv
                       )




cur =conn.cursor()
sql = 'select * from tb4;'
cur.execute(sql)
a=cur.fetchall()



"""
cur.close()

sql = "insert into tb3 (num,na,old) values "

l=len(a)
count = 0

import types



print a

d=[]


for j in a:
    l = []
    for i in j:
        if type(i) is types.LongType:
            l.append(int(i))
        else:
            l.append(i)
    d.append(l)


print d

t = []
for i in d:
    t.append(tuple(i))

print d


print t
for i in t:
    count = count + 1
    if count != len(t):
        sql = sql + " " + str(i)+','
    else:
        sql = sql + " " + str(i)

sql = sql + ";"

print sql


cur = conn.cursor()
a=cur.execute(sql)
conn.commit()
print a
print sql"""


print a
cur.close()
conn.close()


