# -*- coding: utf-8 -*-
import time

from fastapi import FastAPI, Form
import sqlite3

app = FastAPI()

def getbin(s):
    return sqlite3.Binary(s.encode('utf-8'))

def getid(table):
    sql =sqlite3.connect("UserForm.db")
    cur=sql.cursor()
    cur.execute(f'SELECT id FROM {table}')
    rows = cur.fetchall()
    userid=0
    if len(rows) != 0:
        userid=max(rows)
        userid=userid[0]+1
        for i in range(len(rows)-1):
            if rows[i][0]+1!=rows[i+1][0]:
                userid=rows[i][0]+1

    else:
        userid = 0
    sql.close()
    return userid

@app.post("/login")
async def login(name=Form(None),password=Form(None)):
    try:
        sql = sqlite3.connect("UserForm.db")
        cur=sql.cursor()
        cur.execute(f'SELECT password FROM users WHERE name="{name}"')
        passwd=cur.fetchall()
        if passwd[0][0]==password:
            return {"message":"success"}
        else:
            return {"message":"error","error":"password is not right"}
    except IndexError:
        return {"message":"error","error":"don't have the user name"}
    finally:
        sql.close()

@app.post("/admin_login")
async def login(name=Form(None),password=Form(None)):
    try:
        sql = sqlite3.connect("UserForm.db")
        cur=sql.cursor()
        cur.execute(f'SELECT password FROM admin_users WHERE name="{name}"')
        passwd=cur.fetchall()
        if passwd[0][0]==password:
            return {"message":"success"}
        else:
            return {"message":"error","error":"password is not right"}
    except IndexError:
        return {"message":"error","error":"don't have the user name"}
    finally:
        sql.close()

@app.post("/join")
async def join(name=Form(None), password=Form(None)):
    try:
        sql = sqlite3.connect("UserForm.db")
        cur = sql.cursor()
        #判断是否重名
        cur.execute('SELECT name FROM users')
        names=cur.fetchall()
        for name_str in names:
            if name_str[0] == name:
                return {"message":"error","error":"same name"}
        #判断密码是否合法
        if len(password)!=6:
            return {"message": "error", "error": "the password is too long or to short"}
        userid=getid("users")
        cur.execute(f"REPLACE INTO users VALUES({userid},'{name}','{password}',0)")
        sql.commit()

        return {"message": "success"}

    finally:
        sql.close()
        print("create success")


@app.post("/admin")
async def admin(operation=Form("operation")):
    if operation=="get title":
        sql=sqlite3.connect("UserForm.db")
        cur=sql.cursor()
        cur.execute('SELECT id,error,create_data,owner FROM articles')
        row=cur.fetchall()
        sql.close()
        return {"title":row}

@app.post("/article")
async def article(id=Form(None)):
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f'SELECT error,reason,body FROM articles where id=={id}')
    row = cur.fetchall()
    sql.close()
    return {"article": row}

@app.post("/change_article")
async def change_article(id=Form(None),reason=Form(None),body=Form(None)):
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f"UPDATE articles SET reason='{reason}', body='{body}' WHERE id={id}")
    sql.commit()
    sql.close()
    return {"message": "success"}


@app.post("/delete_article")
async def change_article(id=Form(None)):
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f"DELETE FROM articles WHERE id={id}")
    sql.commit()
    sql.close()
    return {"message": "success"}

@app.post("/add_article")
async def add_article(owner=Form(None),error=Form(None),reason=Form(None),body=Form(None)):
    id = getid("articles")
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f'SELECT id FROM users WHERE name="{owner}"')
    owner_id = cur.fetchall()
    error=error.replace("'" , "''")
    cur.execute(f"REPLACE INTO articles values('{id}', '{error}', '{time.time()}','{owner}','{owner_id[0][0]}','{reason}','{body}' )")
    sql.commit()
    sql.close()
    return {"message":"success"}
