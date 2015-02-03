#!/bin/env python

#This is the same version as place_rent_bot,
#only the username and password are removed

import requests
from urllib.parse import quote

def login():
    global headers_get,headers_post,login_url,logout_url,data,proxy,record_url
    headers_get={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-tw,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Referer': 'https://sasystem.nctu.edu.tw/place_rent/main.php',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0'}
    headers_post={
        'Content-Length':'51',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-tw,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://sasystem.nctu.edu.tw/place_rent/main.php',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0'}
    login_url='https://sasystem.nctu.edu.tw/place_rent/main.php'
    logout_url='https://sasystem.nctu.edu.tw/place_rent/login.php'
    record_url='https://sasystem.nctu.edu.tw/place_rent/main.php?tp=applysplace&'
    data='loginuser=youruser&loginpw=yourpassword&test=test'
    #proxy={'https':'https://127.0.0.1:8080'} #debug
    global sess
    sess=requests.Session()
    sess.get(logout_url,headers=headers_get)
    sess.post(login_url,headers=headers_post,data=data)

def logout():
    global sess
    sess.get(logout_url,headers=headers_get)
    sess.close()


def record():
    global sess
    login()
    r=sess.get(record_url,headers=headers)
    logout()

def book(contact_man,phone,email,stuid,act_name,place,year_month,date,time):
    global sess
    act_name=quote(act_name.encode('big5'))
    contact_man=quote(contact_man.encode('big5'))
    book_url='https://sasystem.nctu.edu.tw/place_rent/send.php'
    data="rubric=1&activename={0}&touchman={1}&touchphone={2}&touchmail={3}\
    &stu_id={4}&mobile_tel={5}&splacename_d%5B0%5D={6}&ac1_d%5B0%5D={7}&ac2_d%5B0%5D={8}\
    &acslot_d%5B0%5D={9}&ac1_d%5B1%5D=&ac2_d%5B1%5D=&acslot_d%5B1%5D=&poiuytrewq=A&Bulletin_Serial="\
    .format(act_name,contact_man,phone,email,stuid,phone,place,year_month,date,time)
    login()
    r=sess.post(book_url,data=data,headers=headers_post)
    logout()
    return (r.content).decode('big5')
