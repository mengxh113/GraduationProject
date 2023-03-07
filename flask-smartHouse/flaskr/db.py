'''数据库操作相关内容'''
import sqlite3
import click
import os
import re
import flaskr.tools as tools
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e = None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    files = os.listdir('./flaskr/static/images/headshot')
    for file in files:
        if file != 'default.jpg' and file != 'default1.jpg':
            os.remove('./flaskr/static/images/headshot/' + file)

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('初始化数据库。')

@click.command('manage-db')
@with_appcontext
def manage_db_command():
	# 管理数据库
	db=get_db()
	while True:
		s=input('>>>')
		order=s.lower().split() or [None]
		if order[0]=='chmod':
			db.execute("update user set [group]=? where username=?",(order[2],order[1]))
			db.commit()
		elif order[0]=='newuser':
			db.execute('insert into user (workId,realName,password) values(?,?,?)',(*order[1:3],generate_password_hash(order[3]),))
			db.commit()
		elif order[0]=='exit':
			break
		elif order[0]:
			print('\n'.join(map(str,map(dict,db.execute(s).fetchall()))))
		else:
			pass

@click.command('create-admin')
@with_appcontext
def create_admin_command():
    # 创建管理员用户
    db = get_db()
    click.echo('[username]:[phone]')
    while True:
        s = input('>')
        order = s.split(':') or [None]
        if order is None:
            continue
        if order[0] == 'exit':
            break
        if order[1] is None:
            break
        if not re.fullmatch('^[\u4e00-\u9fa5_a-zA-Z0-9_]{1,10}$', order[0]):
            click.echo('用户名格式错误!')
            continue
        if not re.fullmatch('^((13[0-9])|(14[0-9])|(15[0-9])|(17[0-9])|(18[0-9]))\d{8}$', order[1]):
            click.echo('手机号格式错误!')
            continue
        e = db.execute(
            "SElECT * FROM user WHERE username = ? OR phone = ?", (order[0], order[1])
        ).fetchone()
        if e is not None:
            click.echo('当前用户名或手机号已被注册！')
            continue

        # 进入注册管理员环节
        password = tools.generatePWD()
        while True:
            click.echo('已为当前管理员账号生成密码为：\n' + password)
            s = input('确认创建用户名为 ' + order[0] + ' 绑定手机号为 ' + order[1] + ' 的管理员吗[Y/N]?\n')
            confirm = s.lower().split() or [None]
            if confirm[0] == 'n':
                break
            elif confirm[0] == 'y':
                id = tools.generateID('admin')
                db.execute(
                    "INSERT INTO user (id, username, password, phone, status) VALUES (?, ?, ?, ?, 1)",
                    (id, order[0], generate_password_hash(password), order[1]),
                )
                db.commit()
                click.echo('管理员创建成功！')
                break
            else:
                pass

        

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(manage_db_command)
    app.cli.add_command(create_admin_command)