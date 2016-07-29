#!/usr/bin/env python
from socket import *
from time import ctime


HOST=''
PORT=21567
BUFSIZ=1024
ADDR=(HOST,PORT)

s=socket(socket.AF_INET,SOCK_STREAM)
s.bind(ADDR)
s.listen(5)

while Ture:
    print 'waiting for connection.....'
    st,addr = s.accept()
    print '...connected from:',addr
    
    while Ture:
	data = st.recv(BUFSIZ)
        if not data:
            break
        st.send([])
