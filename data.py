#!/ust/bin/env python
#coding:utf-8

import urllib
import urllib2

values={"username":"root","password":"saltweb"}
data=urllib.urlencode(values)
url="http://139.129.47.28:9000/admin/"
request=urllib.Request(url,data)
response = urllib.urlopen(request)
print response.read()

print type(data)
print data
