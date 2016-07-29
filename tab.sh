#!/usr/bin/env python

# encoding: utf-8
import re,sys
print('''Welecom to test
it's a test mod!
''')
while True:
    x=input('>')
    
    if x=='exit':
        print('Good bye!')
        break
    if x=='match':
        text=input('Please input test char:')
        match=input('Please input match rule:')
        m=re.match(match,text)
        if m is not None:
            print("The rule \" "+match+"\"is match to:"+m.group())
        else:
            print("it's not match!")
    if x=='mtext':
        match=input('Please/input/your/match/rule:')
        while True:
            text=input('Please/input/some/text/#')
            m=re.match(match,text)
            if m is not None:
                print("The rule \" "+match+"\"is match to:"+m.group())
            else:
                print("it's not match!")
            if text=='again':
                match=input('Please/input/your/match/rule:')
            if text=='exit':
                break
    if x=='mrule':
        text=input('Please/input/some/text/#')
        while True:
            match=input('Please/input/your/match/rule:')
            m=re.match(match,text)
            if m is not None:
                print("The rule \" "+match+"\"is match to:"+m.group())
            else:
                print("it's not match!")
            if text=='again':
                text=input('Please/input/some/text/#')
            if text=='exit':
                break
