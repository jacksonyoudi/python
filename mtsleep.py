#!/usr/bin/env python
#coding:utf8

import thread
from time import sleep,ctime
loops=[4,2]



def loop(nloop,nsec,lock):   #定义loop（）函数，用于睡眠
    print 'start loop',nloop,'at:',ctime()  #打印开始时间
    sleep(nsec)                             #睡眠多少秒
    print 'loop',nloop,'done at:',ctime()   #打印完成时间
    lock.release()                          #释放锁机制

def main():          #定义主函数
    print 'start at:',ctime()  #打印主函数开始时间
    locks=[]                   #定义锁的
    nloops=range(len(loops))   #生成[0,1] 用于循环



    for i in nloops:
        lock=thread.allocate_lock()  #分配一个lockType的锁对象
        lock.acquire()                #捕获
        locks.append(lock)           #追加到列表中

    for i in nloops:                 #创建线程
        thread.start_new_thread(loop,(i,loops[i],locks[i]))

    for i in nloops:                  
        while locks[i].locked():pass

    print 'all Done at:',ctime()

if __name__ == '__main__':
    main()
