'''登录、注册和主页显示相关内容'''
# from crypt import methods
import email
from email import header
import functools
from importlib.resources import contents
import re
import os
import time, datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from flaskr.db import get_db
from flaskr.tools import generateID, deleteID

import json

bp = Blueprint('auth', __name__, url_prefix = '/auth')

@bp.route('/index', methods = ('GET', 'POST'))
def index():
    db = get_db()
    articles = db.execute(
        "SELECT * FROM article ORDER BY creation_time DESC"
    ).fetchall()
    key = ''
    if request.method == 'POST':
        key = request.form['key']
        articles = db.execute(
            "SELECT * FROM article WHERE title LIKE '%'||?||'%' OR theme LIKE '%'||?||'%' ORDER BY creation_time DESC",
            (key, key, )
        ).fetchall()
    return render_template('index.html', articles = articles, key = key)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/advice', methods = ('GET', 'POST'))
def advice():
    if request.method == 'POST':
        content = request.form['content']
        contactWay = request.form['contactWay']
        error = None

        if not content:
            error = '反馈建议内容不得为空！'
        
        if error is None:
            db = get_db()
            db.execute(
                "INSERT INTO advice (content, contactWay) VALUES (?, ?)", 
                (content, contactWay, ),
            )
            db.commit()
            return redirect(url_for('auth.index'))

        flash(error)

    return render_template('advice.html')

@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        noneFile = False
        id = ''
        if request.files['setHeadshot'].filename == '':
            noneFile = True
        else:
            h = request.files['setHeadshot']
            headshot = secure_filename(h.filename)
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        phone = request.form['phone']
        code = request.form['code']
        email = request.form['email']
        age = request.form['age']
        sex = request.form['sex']
        status = '2'
        db = get_db()
        error = None

        if not username:
            error = '用户名不得为空！'
        elif not password:
            error = '密码不得为空！'
        elif not confirm:
            error = '确认密码不得为空！'
        elif not phone:
            error = '手机号不得为空！'
        elif not code:
            error = '验证码不得为空！'

        if error is None:
            try:
                if code == '0113':
                    id = generateID('user')
                    if noneFile:
                        headshot = 'default.jpg'
                    else:
                        headshotType = headshot.split('.')[-1]
                        headshot = f'headshot_{username}.{headshotType}'
                    db.execute(
                        "INSERT INTO user (id, username, headshot, sex, password, phone, email, age, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (id, username, 'images/headshot/' + headshot, sex, generate_password_hash(password), phone, email, age, status),
                    )
                    db.commit()
                    if not noneFile:
                        h.save(os.path.join('./flaskr/static/images/headshot', headshot))
                    session['user_id'] = id
                    return redirect(url_for('auth.index', headshot = headshot))
            except db.IntegrityError:
                deleteID(id)
                error = f"当前用户名或手机号已被注册！"

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        error = None
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ? OR phone = ?", (account, account),
        ).fetchone()

        if user is None:
            error = '用户名不存在！'
        elif not check_password_hash(user['password'], password):
            error = '密码错误！'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.route('/reset', methods = ('GET', 'POST'))
def reset():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        confirm = request.form['confirm']
        code = request.form['code']
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ? OR phone = ?", (account, account),
        ).fetchone()
        
        if user is None:
            error = '用户名不存在！'
        elif not password:
            error = '新密码不得为空！'
        elif not confirm:
            error = '确认密码不得为空！'
        elif password != confirm:
            error = '新密码与确认密码不一致！'
        elif not code:
            error = '验证码不得为空！'

        if error is None:
            if code == '0113':
                db.execute(
                    "UPDATE user SET password = ? WHERE username = ?", (generate_password_hash(password), user['username']),
                )
                db.commit()
                
            return redirect(url_for('auth.login'))

        flash(error)
    
    return render_template('auth/reset.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id, ),
        ).fetchone()

@bp.route('logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    
    return wrapped_view