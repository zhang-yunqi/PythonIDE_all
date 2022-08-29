import sqlite3
import  os

#os.system("del .\\UserForm.db")
sql = sqlite3.connect("UserForm.db")
cur = sql.cursor()
cur.execute("CREATE TABLE articles(id integer PRIMARY KEY, error text,create_data date, owner text, ownerid int, reason text, body text)")
sql.commit()