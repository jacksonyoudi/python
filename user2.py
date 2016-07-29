#!/usr/bin/env python
#coding: utf-8
import sys
import MySQLdb


def check5():
    if  len(sys.argv) != 5:
        print "\033[1;31;40mUsage: user.py  -u  username  -d  {date}  -m  {add/mod}\n       user.py  -u  username  -m del\n       -u 用户名 \n       -d [date] 日期格式：yyyymmdd\n       -m add 添加用户和过期日期  mod  修改用户过期时间   del  删除用户\n       -h 显示帮助\033[0m"
        return 1
    else:
        return 0


def check7():
    if (len(sys.argv)==2 and  sys.argv[1] == "-h") or len(sys.argv) != 7:
        print "\033[1;31;40mUsage: user.py  -u  username  -d  {date}  -m  {add/mod}\n       user.py  -u  username  -m del\n       -u 用户名 \n       -d [date] 日期格式：yyyymmdd\n       -m add 添加用户和过期日期  mod  修改用户过期时间   del  删除用户\n       -h 显示帮助\033[0m"
        return 1
    else:
        return 0



def argv5(a):
    u=a.index("-u")
    us=u+1
    user=a[us]


    m=a.index("-m")
    me=m+1
    method=a[me]

    arg = {'user':user,'method':method}

    return arg
    #print user,date,method

def argv7(a):
    u=a.index("-u")
    us=u+1
    user=a[us]

    d=a.index("-d")
    da=d+1
    date=a[da]

    m=a.index("-m")
    me=m+1
    method=a[me]

    arg = {'user':user,'date':date,'method':method}

    return arg
    #print user,date,method


def mysql(sql):
    c=MySQLdb.connect(host='localhost',user='userdate',passwd='userdate',db='userdate',port=3306)
    cur=c.cursor()
    cur.execute(sql)
    cur.close()
    c.commit()
    c.close()

def add(a):
    name=a['user']
    date=a['date']
    sql='insert into user(username,expire) values("%s","%s");' % (name,date)
    mysql(sql)

def mod(a):
    name=a['user']
    date=a['date']
    sql='update user set expire="%s" where username="%s";' %(date,name)
    mysql(sql)

def delete(a):
    name=a['user']
    sql='delete from user where username="%s";' % name
    mysql(sql)




if __name__ == "__main__":
    if "del" in sys.argv:
        a=check5()
        if a == 1:
            exit(1)
        else:
            b=argv5(sys.argv)
            delete(b)
    else:
        a=check7()
        if a == 1:
            exit(1)
        else:
            b=argv7(sys.argv)
            if b['method'] == 'add':
                add(b)
            if b['method'] == 'mod':
                mod(b)
