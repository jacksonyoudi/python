#!/usr/bin/env python

# -*- coding: utf-8 -*-
#coding:utf8


import xlsxwriter
import MySQLdb

def getdata(b):
    c=MySQLdb.connect(host='localhost',user='ledou',passwd='ledou',db='ledou',port=3306, charset='utf8')
    cur=c.cursor()
    a=b

    sql='select date,money from (select b.projectName,a.date,a.money from server_costs as a join project_info as b on a.projectId=b.projectid) as c where projectName="%s" order by date;' %a
    cur.execute(sql)
    t=cur.fetchall()
    cur.close()
    c.close()
    return t

ldzwt=getdata('\xe4\xb9\xb1\xe6\x96\x97\xe4\xb9\x8b\xe7\x8e\x8b')
cqbt=getdata('\xe8\x8b\x8d\xe7\xa9\xb9\xe5\x8f\x98')
tkzzt=getdata('\xe5\x9d\xa6\xe5\x85\x8b\xe4\xb9\x8b\xe6\x88\x98')

d=[]
ldzwl=[]
for i in ldzwt:
    d.append(str(i[0]))
    ldzwl.append(int(i[1]))

cqbl=[]
for i in cqbt:
    cqbl.append(int(i[1]))

tkzzl=[]
for i in tkzzt:
    tkzzl.append(int(i[1]))




workbook = xlsxwriter.Workbook('demo8.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column('A:A',20)
bold = workbook.add_format({'bold': True})

top=workbook.add_format({'border':6,'align':'center','bg_color':'cccccc','font_size':13,'bold':True})
title=['date','ldzw_fee','cqb_fee','tkzz_fee']
worksheet.write_row('A1',title,top)


for i in range(2,len(d)+2):
    p='A'+str(i)
    q='B'+str(i)
    m='C'+str(i)
    n='D'+str(i)

    j=i-2

    worksheet.write(p,d[j])
    worksheet.write(q,ldzwl[j])
    worksheet.write(m,cqbl[j])
    worksheet.write(n,tkzzl[j])

chart = workbook.add_chart({'type': 'column'})
worksheet.insert_chart('A13',chart)

chart.add_series({
    'categories': '=Sheet1!$A$2:$A$8',
    'values':      '=Sheet1!$B$2:$B$8',
    'line':       {'color': 'red'},
})

chart.add_series({
    'categories': '=Sheet1!$A$2:$A$8',
    'values':      '=Sheet1!$C$2:$C$8',
    'line':       {'color': 'red'},
})

chart.add_series({
    'categories': '=Sheet1!$A$2:$A$8',
    'values':      '=Sheet1!$D$2:$D$8',
    'line':       {'color': 'red'},
})

chart.set_x_axis({
    'name': 'date',
    'name_font': {'size':14,'bold':True},
})

chart.set_size({'width':720,'height':576})
chart.set_title({'name':'Game Progrom Fee'})




workbook.close()

