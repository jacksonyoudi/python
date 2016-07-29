#!/usr/bin/env python
#coding: utf-8


import sys
reload(sys)
sys.setdefaultencoding("utf-8")


import urllib
import urllib2
import re
import json
from bs4 import BeautifulSoup
import os

url='http://www.idreamsky.com'
try:
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    htmldoc = response.read()
    #htmldoc = content.decode("utf8")

    soup=BeautifulSoup(htmldoc,'html.parser',from_encoding="utf8")
    a=soup.find_all('p',title=re.compile(ur"[\u4e00-\u9fa5]+"))
    b=soup.find_all('p',class_="blue")



    s=sys.stdout
    f=open('out.txt','w')
    sys.stdout=f
    for i in a:
        print i
    for i in b:
        print i
    sys.stdout=s
    f.close()

    f=open('out.txt','r')
    print f
    print type(f)
    d=[]
    for i in f:
        print i
        j=i.split("<")[1].split(">")[1]
        print j
        d.append(j)

    print d
    g=[]
    for i in range(0,12):
        g.append(d[i])
        print d[i]

    print g
    v=[]
    for i in range(26,38):
        v.append(d[i])
        print d[i]

    print v

    for i in range(0,12):
        print g[i],v[i]


    f.close()
    os.remove('./out.txt')



except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
