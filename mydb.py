#!/usr/bin/python
#coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
#这两个的作用是设置python默认编码为utf8
import MySQLdb
import cgi

print "Content-Type: text/html charset=utf-8 \n"
print "<html><head><title>数据库列表</title></head>"
print "<body>"
print "<h1>数据库列表</h1>"
print "<ul>"
print '''
<FORM ACTION='host_db.py'>
<p><B>请选择要查询的类型: </B></p>
<INPUT TYPE=radio NAME=host_list VALUE="host_X1" > 数据库XXX
<INPUT TYPE=radio NAME=host_list VALUE="host_X2" > 数据库XXX
<INPUT TYPE=radio NAME=host_list VALUE="host_X3" > 数据库XXX
<INPUT TYPE=radio NAME=host_list VALUE="host_X4" > 数据库XXX

<p><B>请出入要查询的主机名: </B></p>
<INPUT TYPE=text NAME=hostname SIZE=15>
<INPUT TYPE=submit></FORM>
'''
#下面的函数,提供了主要的检索功能,其中修改了部分名字,大家可以参考一下思路.感兴趣的可以单独联系.
def SEL_HOST(HN='') :
    if HN == 'host_x':
        SQL_HOST = 'SELECT * FROM host_db'
        NUM_HOST = 'SELECT COUNT(DISTINCT hostname) FROM host_db'
    elif HN == 'host_x':
        SQL_HOST = 'SELECT * FROM host_db WHERE structure="XX" ORDER BY cluster'
        NUM_HOST = 'SELECT COUNT(DISTINCT hostname) FROM host_db WHERE structure="XX"'
    elif HN == 'host_x':
        SQL_HOST = 'SELECT * FROM host_db WHERE structure="XX" ORDER BY cluster'
        NUM_HOST = 'SELECT COUNT(DISTINCT hostname) FROM host_db WHERE structure="XX"'
    elif HN == 'host_x':
        SQL_HOST = 'SELECT * FROM host_db WHERE structure="XX" ORDER BY cluster'
        NUM_HOST = 'SELECT COUNT(DISTINCT hostname) FROM host_db WHERE structure="XX"'
    else:
        SQL_HOST = 'SELECT * FROM host_db WHERE hostname LIKE "%%%s%%"' % (HN)
    if 'NUM_HOST' in dir():
        CUR.execute(NUM_HOST)
        print "<p><B>所查询的主机数量: %s </B></p>" % CUR.fetchone()
    CUR.execute(SQL_HOST)
    for data in CUR.fetchall():
        print "<table bgcolor='#CCCCCC' border='1' style='border:black solid 1px;border-collapse:collapse' cellpadding='0' cellspacing='0'>"
        print "<tr> <td width='100'> 实例id</td> <td width='500'> %s </td> </tr>" % (data[0])
        print "<tr> <td width='100'> 机房</td> <td width='500'> %s </td> </tr>" % (data[1])
        print "<tr> <td width='100'> 主机名</td> <td width='500'> %s </td> </tr>" % (data[2])
        print "<tr> <td width='100'> 内网ip</td> <td width='500'> %s </td> </tr>" % (data[3])
        print "<tr> <td width='100'> 外网ip</td> <td width='500'> %s </td> </tr>" % (data[4])
        print "<tr> <td width='100'> 数据库类型</td> <td width='500'> %s </td> </tr>" % (data[5])
        print "<tr> <td width='100'> 数据库版本</td> <td width='500'> %s </td> </tr>" % (data[6])
        print "<tr> <td width='100'> 数据库端口</td> <td width='500'> %s </td> </tr>" % (data[7])
        print "<tr> <td width='100'> 架构</td> <td width='500'> %s </td> </tr>" % (data[8])
        print "<tr> <td width='100'> 架构名</td> <td width='500'> %s </td> </tr>" % (data[9])
        print "<tr> <td width='100'> 角色</td> <td width='500'> %s </td> </tr>" % (data[10])
        print "<tr> <td width='100'> vip</td> <td width='500'> %s </td> </tr>" % (data[11])
        print "<tr> <td width='100'> 开发负责人</td> <td width='500'> %s </td> </tr>" % (data[12])
        print "<tr> <td width='100'> 应用</td> <td width='500'> %s </td> </tr>" % (data[13])
        print "<tr> <td width='100'> 影响</td> <td width='500'> %s </td> </tr>" % (data[14])
        print "<tr> <td width='100'> 备注</td> <td width='500'> %s </td> </tr>" % (data[15])
        print "</table>"
        print "<P></P>"
def main() :
    form = cgi.FieldStorage()
# if form.has_key('hostname'):
    hostname = form['hostname'].value

if __name__ == '__main__':
    CON = MySQLdb.connect(host='192.168.250.253',user='dba_work',passwd='123456',db='dba_work',charset='utf8',use_unicode = True)
    CUR = CON.cursor()
    form = cgi.FieldStorage()
    if form.has_key('hostname'):
        hostname = form['hostname'].value
        SEL_HOST(hostname)
    elif form.has_key('host_list'):
        host_all = form['host_list'].value
        SEL_HOST(host_all)
    else:
        pass
    print "</ul>"
    print "</body></html>"
    CUR.close()
