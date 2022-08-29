import sqlite3

import requests

def join(name,passwd):
    re=requests.post("http://127.0.0.1:1024/user/join",data={"name":name,"password":passwd}).json()
    return re

def login(name,passwd):
    re=requests.post("http://127.0.0.1:1024/user/login",data={"name":name,"password":passwd}).json()
    return re

def add_article(username,error,reason,body):
    re=requests.post("http://127.0.0.1:1024/article/add",data={"owner":username,"error":error.encode('utf-8'),"reason":reason.encode('utf-8'),"body":body.encode("utf-8")}).json()
    return re

if __name__=="__main__":
    add_article("yunqi","测试'","测试bug","cc")