#!/usr/bin/env python
import MySQLdb

c=MySQLdb.connect(host='localhost',user='fee',passwd='fee',db='fee',port=3306)
cur=c.cursor()
cur.execute('select * from cost;')
t=cur.fetchall()
cur.close()
c.close()

b=['#6a6aff', '#82d900', '#984b4b', '#ff0000', '#46a3ff', '#f9f900', '#a5a552', '#ff79bc', '#00ffff', '#ff00ff', '#02f78f', '#ff8000', '#5a5aad', '#8600ff', '#00bb00', '#bb3d00', '#a5c2d5', '#cbab4f', '#76a871', '#a56f8f', '#c12c44', '#9f7961', '#6f83a5']
z=zip(t,b)

a=[]

for i in z:
    a.append({'name':i[0][1],'value':int(i[0][2]),'color':i[1]})

print a