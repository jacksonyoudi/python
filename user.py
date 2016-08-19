#!/usr/bin/env python
# coding: utf-8
import sys  # 导入sys,使用sys.argv捕获参数
import MySQLdb  # 连接数据，进行sql操作


def avail():  # 当命令不合法输出
    print "\033[1;31;40m 输入命令不合法或命令不全，请看下面帮助文档\033[0m"
    print "\n"


def helpdoc():  # 打印帮助文档
    print "\033[1;31;40mUsage: user.py  -u  username  -d  {date}  -m  {add/mod}\n       user.py  -u  username  -m del\n       -u 用户名 \n       -d [date] 日期格式：yyyymmdd\n       -m add 添加用户和过期日期  mod  修改用户过期时间   del  删除用户\n       -h 显示帮助\033[0m"


def datecheck(a):  # 作日期合法性校验
    try:
        if len(a) == 8:
            year = int(a[0:4])
            month = int(a[4:6])
            date = int(a[6:8])
            if month in range(1, 13) and date in range(1, 32):
                return 0
            else:
                print "\033[1;31;40m 日期输入不合法！！！\033[0m"
                print "\n"
                helpdoc()
                exit(1)
        else:
            print "\033[1;31;40m 日期输入不合法！！！\033[0m"
            print "\n"
            helpdoc()
            exit(2)

    except Exception, e:
        print e


def check5():  # 当用户进行删除操作的时候，调用进行检查参数
    try:
        if "-u" in sys.argv and "-m" in sys.argv:
            if len(sys.argv) == 5:

                return 0
            else:
                print "\033[1;31;40m 执行删除操作语法：user.py  -u  username  -m del\n 下面是使用的帮助文档\n\033[0m"
                helpdoc()
                return 0
        else:
            avail()
            helpdoc()
            exit(3)

    except Exception, e:
        print e


def check7():  # 当用户进行添加和修改的时候，调用进行检查参数
    try:
        if ("-u" in sys.argv and "-d" in sys.argv and "-m" in sys.argv) and ("add" in sys.argv or "mod" in sys.argv):
            if (len(sys.argv) == 2 and sys.argv[1] == "-h") or len(sys.argv) != 7:
                helpdoc()
                return 1
            else:
                return 0
        else:
            avail()
            helpdoc()
            exit(4)
    except Exception, e:
        print e


def argv5(a):  # 当用户是删除操作的时候，参数是4个，分开操作。
    try:
        u = a.index("-u")
        us = u + 1
        user = a[us]

        m = a.index("-m")
        me = m + 1
        method = a[me]

        arg = {'user': user, 'method': method}

        return arg
        # print user,date,method
    except Exception, e:
        print e


def argv7(a):  # 当用户是添加和修改的时候，捕获参数，转化为字典的数据格式返回。
    try:
        u = a.index("-u")
        us = u + 1
        user = a[us]

        d = a.index("-d")
        da = d + 1
        date = a[da]

        datecheck(date)

        m = a.index("-m")
        me = m + 1
        method = a[me]

        arg = {'user': user, 'date': date, 'method': method}

        return arg
        # print user,date,method
    except Exception, e:
        print e


def mysql(sql):  # 连接数据库，进行sql操作
    try:
        c = MySQLdb.connect(host='localhost', user='userdate', passwd='userdate', db='userdate', port=3306)
        cur = c.cursor()
        cur.execute(sql)
        cur.close()
        c.commit()
        c.close()
    except Exception, e:
        print e


def add(a):  # 添加操作的函数
    try:
        name = a['user']
        date = a['date']
        sql = 'insert into user(username,expire) values("%s","%s");' % (name, date)
        mysql(sql)
    except Exception, e:
        print e


def mod(a):  # 修改操作的函数
    try:
        name = a['user']
        date = a['date']
        sql = 'update user set expire="%s" where username="%s";' % (date, name)
        mysql(sql)
    except Exception, e:
        print e


def delete(a):  # 删除操作函数
    try:
        name = a['user']
        sql = 'delete from user where username="%s";' % name
        mysql(sql)
    except Exception, e:
        print e


if __name__ == "__main__":  # 主函数
    try:
        if len(sys.argv) == 5 or len(sys.argv) == 7:
            if "del" in sys.argv:  # 对执行的命令进行分类，添加修改一类，删除另一类
                a = check5()  # 参数检查是否合法
                if a == 1:
                    exit(1)
                else:
                    b = argv5(sys.argv)  # 参数转化为字典
                    delete(b)
            else:
                a = check7()  # 参数检查是否合法
                if a == 1:
                    exit(1)
                else:
                    b = argv7(sys.argv)  # 参数转化为字典
                    if b['method'] == 'add':
                        add(b)
                    if b['method'] == 'mod':
                        mod(b)
        else:
            print "\033[1;31;40m 输入参数不合法，请看下面帮助文档\033[0m"
            print "\n"
            helpdoc()
    except Exception, e:
        print e
