'''用户个人信息管理相关页面'''
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flaskr.auth import login_required

from flaskr.db import get_db

bp = Blueprint('infoManagement', __name__, url_prefix = '/infoManagement')

@bp.route('/information', methods = ('GET', 'POST'))
@login_required
def information():
    if request.method == 'POST':
        noneFile = False
        if request.files['setHeadshot'].filename == '':
            headshot = g.user['headshot'].split('/')[-1]
            noneFile = True
        else:
            h = request.files['setHeadshot']
            headshot = secure_filename(h.filename)
        username = request.form['username']
        phone = request.form['phone']
        email = request.form['email']
        age = request.form['age']
        sex = request.form['sex']
        db = get_db()
        error = None

        if not username:
            error = '用户名不得为空！'
        elif not phone:
            error = '手机号不得为空！'

        if error is None:
            try:
                if not noneFile:
                    headshotType = headshot.split('.')[-1]
                    headshot = f'headshot_{username}.{headshotType}'
                    oldHeadshot = g.user['headshot'].split('/')[-1]
                    if oldHeadshot != 'default.jpg' and oldHeadshot != 'default1.jpg':
                        print(oldHeadshot)
                        os.remove('./flaskr/static/images/headshot/' + oldHeadshot)
                db.execute(
                    "UPDATE user SET headshot = ?,username = ?, phone = ?, email = ?, age = ?, sex = ? WHERE id = ?",
                    ('images/headshot/' + headshot, username, phone, email, age, sex, g.user['id']),
                )
                db.commit()
                if not noneFile:
                    h.save(os.path.join('./flaskr/static/images/headshot', headshot))
                    g.user = get_db().execute(
                        "SELECT * FROM user WHERE id = ?", (g.user['id'], ),
                    ).fetchone()
                id = g.user['id']
                session.clear()
                session['user_id'] = id
                return redirect(url_for('infoManagement.information'))
            except db.IntegrityError:
                error = f"当前用户名或手机号已被注册！"

        flash(error)
    return render_template('infoManagement/information.html')

@bp.route('/favorite', methods = ('GET', 'POST'))
@login_required
def favorite():
    return render_template('infoManagement/favorite.html')

@bp.route('/modifyPassword', methods = ('GET', 'POST'))
@login_required
def modifyPassword():
    if request.method == 'POST':
        oldPassword = request.form['oldPassword']
        password = request.form['password']
        confirm = request.form['confirm']
        db = get_db()
        error = None

        if not oldPassword:
            error = '旧密码不得为空！'
        elif not password:
            error = '新密码不得为空！'
        elif not confirm:
            error = '确认密码不得为空！'
        elif not check_password_hash(g.user['password'], oldPassword):
            error = '旧密码错误！'

        if error is None:
            db.execute(
                "UPDATE user SET password = ? WHERE id = ?",
                (generate_password_hash(password), g.user['id'], )
            )
            db.commit()
            session.clear()
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('infoManagement/modifyPassword.html')

@bp.route('/userManagement')
@login_required
def userManagement():
    db = get_db()
    users = db.execute(
        "SELECT * FROM user WHERE status = '2'"
    ).fetchall()
    return render_template('infoManagement/userManagement.html', users = users)

@bp.route('/queryUsers')
@login_required
def queryUsers():
    type = request.args.get('type');
    paras = request.args.get('paras');
    para0 = paras.split('-')[0]
    if para0 != paras:
        para1 = paras.split('-')[1]
    else:
        para1 = ''
    db = get_db()
    users = ''
    if type == 'username':
        if not para0:
            users = db.execute(
                "SELECT * FROM user WHERE status = 2",
            ).fetchall()
        else:
            users = db.execute(
                "SELECT * FROM user WHERE username LIKE '%'||?||'%' AND status = 2",
                (para0, )
            ).fetchall()
    elif type == 'age':
        if para0 == '' and para1 == '':
            users = db.execute(
                "SELECT * FROM user WHERE status = 2",
            ).fetchall()
            return render_template('infoManagement/userManagement.html', users = users)
        if para0 == '':
            min = 0
        else:
            min = int(para0)
        if para1 == '':
            max = 120
        else:
            max = int(para1)
        print(min)
        print(max)
        users = db.execute(
            "SELECT * FROM user WHERE age >= ? AND age <= ? AND status = 2",
            (min, max, )
        ).fetchall()
    elif type == 'sex':
        if not para0:
            users = db.execute(
                "SELECT * FROM user WHERE status = 2",
            ).fetchall()
        else:
            users = db.execute(
                "SELECT * FROM user WHERE sex = ? AND status = 2",
                (para0,  )
            ).fetchall()
    return render_template('infoManagement/userManagement.html', users = users)

@bp.route('/deleteUser')
@login_required
def deleteUser():
    id = request.args.get('id')
    db = get_db()
    headshot = db.execute(
        "SELECT * FROM user WHERE id = ?",
        (id,)
    ).fetchone()['headshot']
    db.execute(
        "DELETE FROM user WHERE id = ?",
        (id, )
    )
    db.commit()
    oldHeadshot = headshot.split('/')[-1]
    if oldHeadshot != 'default.jpg' and oldHeadshot != 'default1.jpg':
        os.remove('./flaskr/static/images/headshot/' + oldHeadshot)
    return redirect(url_for('infoManagement.userManagement'))

