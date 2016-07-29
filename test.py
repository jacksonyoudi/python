#!/usr/bin/env python
#coding: utf-8
import sys

#print sys.argv
#print sys.argv[0]
#print sys.argv[1]
#print len(sys.argv)


def check():
    if (len(sys.argv)==2 and  sys.argv[1] == "-h") or len(sys.argv) != 7:
        print "\033[1;31;40mUsage: test.py  -u  username  -d  {date}  -m  {add/mod/del}\n-u 用户名 \n-d [date] 日期格式：yyyymmdd\n-m add 添加用户和过期日期  mod  修改用户过期时间   del  删除用户\n-h 显示帮助\033[0m"
        return 1
    else:
        return 0


def argv(a):





if __name__ == "__main__":
    a=check()
    print a



