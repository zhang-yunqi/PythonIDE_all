# -*- coding: utf-8 -*-
import time

from fastapi import FastAPI, Form,Header,Body
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.post("/user/login")
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



@app.post("/user/join")
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


@app.post("/article/get_error")
async def admin():
    sql=sqlite3.connect("UserForm.db")
    cur=sql.cursor()
    cur.execute('SELECT id,error FROM articles')
    row=cur.fetchall()
    sql.close()
    if len(row)>1:
        for error in range(row):
            if len(row[error][1])>=40:
                row[error]=[row[error][0],str(row[error][1])[:40]+"···"]
    elif len(row)==1:
        if len(row[0][1]) >= 40:
            row[0] = [row[0][0],str(row[0][1])[:40]+"···"]
    return {"error_name":row}


@app.post("/user/getname")
async def admin():
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute('SELECT id,name FROM users')
    row = cur.fetchall()
    sql.close()
    return {"usernames":row}

@app.post("/user/user_details")
async def admin(body=Body(None)):
    id=body["id"]
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f'SELECT name,password,level FROM users where id={id}')
    row = cur.fetchall()
    sql.close()
    print(row)
    return {"userdetails":row}

@app.post("/article/article_details")
async def article(body=Body(None)):
    id=body["id"]
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f'SELECT error,reason,body FROM articles where id=={id}')
    row = cur.fetchall()
    sql.close()
    return {"articledetails": row}

@app.post("/article/change")
async def change_article(body=Body(None)):
    id=body["id"]
    reason=body["reason"]
    body_item=body["body"]
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f"UPDATE articles SET reason='{reason}', body='{body_item}' WHERE id={id}")
    sql.commit()
    sql.close()
    return {"message": "success"}

@app.post("/user/change")
async def change_user(body=Body(None)):
    name=body["name"]
    password=body["password"]
    level=body["level"]
    id=body["id"]
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f"UPDATE users SET name='{name}', password='{password}', level='{level}' WHERE id={id}")
    sql.commit()
    sql.close()
    return {"message": "success"}

@app.post("/user/delete")
async def delete(body=Body(None)):
    id=body["id"]
    print(id)
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f"DELETE FROM users WHERE id={id}")
    sql.commit()
    sql.close()
    return {"message": "success"}



@app.post("/article/delete")
async def delete(body=Body(None)):
    id=body["id"]
    sql = sqlite3.connect("UserForm.db")
    cur = sql.cursor()
    cur.execute(f"DELETE FROM articles WHERE id={id}")
    sql.commit()
    sql.close()
    return {"message": "success"}

@app.post("/article/add")
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
