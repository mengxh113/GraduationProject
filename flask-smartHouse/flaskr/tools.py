'''工具包'''
import random
import sqlite3
import string
import re

from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def generateID(type):
    # 生成用户ID
    ID = ''
    if type == 'user':
        for i in range(5):
            ID += random.choice(string.ascii_letters)
        if ID == 'ADMIN':
            return generateID(type)
    elif type == 'admin':
        ID += 'ADMIN'
    else:
        return ID
    for i in range(10):
        ID += random.choice(string.digits)
    db = get_db()
    id = db.execute(
        "SELECT * FROM user_id_list WHERE val = ?", (ID, ),
    ).fetchone()
    if not id:
        db.execute(
            "INSERT INTO user_id_list (val) VALUES (?)", (ID, ),
        )
        db.commit()
        return ID
    else:
        return generateID(type)

def deleteID(ID):
    # 删除ID
    db = get_db()
    db.execute(
        "DELETE FROM user_id_list WHERE val = ?", (ID, ),
    )
    db.commit()

def generatePWD():
    # 生成随机密码
    chars = string.ascii_letters + string.digits + '''.@!%*#_~?&^'''
    len = random.randint(6, 15)
    pwd = ''
    while not re.fullmatch('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z.@$!%*#_~?&^\d]{6,15}$', pwd):
        pwd = ''
        for i in range(len):
            pwd += random.choice(chars)
    return pwd
