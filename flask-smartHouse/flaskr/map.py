'''功能地图'''
from asyncio.windows_events import NULL
from datetime import datetime
from distutils.log import error
from fileinput import filename
from genericpath import exists
import os
import readline
import string
from select import select
import time
from turtle import title, width
from flask import (
    Blueprint, Response, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('map', __name__, url_prefix = '/map')

# 文章库
article_filters = {
    "theme": ['全部', '法律法规', '装修风格', '家具建材', '价格估算', '经验分享', '健康家居'],
}

def read_md_file(filename):
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, 'static\\article\\bank\\' + filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def furnitureImagePath(model):
    path = ''
    if model == '门':
        path = 'interiorFinish/door/'
    elif model == '窗':
        path = 'interiorFinish/window/'
    elif model == '地面':
        path = 'interiorFinish/floor/'
    elif model == '墙面':
        path = 'interiorFinish/wall/'
    elif model == '结构部件':
        path = 'interiorFinish/structuralComponent/'
    elif model == '沙发':
        path = 'furniture/sofa/'
    elif model == '床':
        path = 'furniture/bed/'
    elif model == '桌子':
        path = 'furniture/desk/'
    elif model == '椅子|凳子':
        path = 'furniture/chair/'
    elif model == '柜架':
        path = 'furniture/cabinetRack/'
    elif model == '橱柜':
        path = 'kitchenAndBathroom/cupboard/'
    elif model == '浴室柜':
        path = 'kitchenAndBathroom/bathroomCabinet/'
    elif model == '洗手台':
        path = 'kitchenAndBathroom/washStand/'
    elif model == '马桶':
        path = 'kitchenAndBathroom/toilet/'
    elif model == '浴缸':
        path = 'kitchenAndBathroom/bathtub/'
    return path

@bp.route('/article/<string:filter>', methods = ('GET', 'POST'))
@login_required
def article(filter):
    if request.method == 'POST':
        return redirect(url_for('map.article', filter = filter, key = request.form.get('key', '%'), selected = request.form.get('theme', '全部')))
    key = request.args.get('key', '%')
    db = get_db()
    articles = db.execute(
        "SELECT * FROM article WHERE title LIKE '%'||?||'%' AND theme LIKE ? ORDER BY creation_time DESC",
        (key, '%' if filter == '全部' else filter, )
    ).fetchall()
    articles = list(map(dict, articles))
    for i in range(len(articles)):
        articles[i]['content'] =  read_md_file(articles[i]['content'])
    return render_template('map/article/article.html', article_filters = article_filters["theme"], key = key, articles = articles, selected = request.args.get('selected'))

@bp.route('/articleCreate', methods = ('GET', 'POST'))
@login_required
def articleCreate():
    return render_template('map/article/articleCreate.html')

@bp.route('/upload', methods =['POST'])
@login_required
def upload():
    file =  request.files.get('editormd-image-file')
    if not file:
        res = {
            'success' : 0,
            'message' : '上传失败'
        }
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        current_path = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_path, 'static\\article\\images\\')
        if not os.path.exists(filepath): # 文件夹不存在，则创建
            os.mkdir(filepath)
        file.save(os.path.join(filepath, filename))
        res = {
            'success' : 1,
            'message' : '上传成功',
            'url' : url_for('map.image', name = filename)
        }
    return jsonify(res)

@bp.route('/image/<name>')
@login_required
def image(name):
    current_path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(current_path, 'static\\article\\images\\')
    with open(os.path.join(filepath, name), 'rb') as f:
        resp = Response(f.read(), mimetype="image/jpeg")
    return resp

@bp.route('/save', methods = ['POST'])
@login_required
def save():
    title = request.form['title']
    theme = request.form['theme']
    content = request.form['content'].replace('\n','')
    filename = datetime.now().strftime('%Y%m%d%H%M%S')
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, 'static//article//bank//article_' + filename + '.md')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    db = get_db()
    db.execute(
        "INSERT INTO article (username, title, theme, content) VALUES (?, ?, ?, ?)", 
        (g.user['username'], title, theme, 'article_' + filename + '.md'),
    )
    db.commit()
    id = db.execute(
        "SELECT * FROM article WHERE content = ?",
        ('article_' + filename + '.md', )
    ).fetchone()['id']
    return redirect(url_for('map.article', filter = '全部', key = '', selected = '全部'))
@bp.route('/articleShow')
@login_required
def articleShow():
    id = request.args.get('id')
    db = get_db()
    article = db.execute(
        "SELECT * FROM article WHERE id = ?",
        (id,)
    ).fetchone()
    article = dict(article)
    article['content'] = read_md_file(article['content'])
    return render_template('map/article/articleShow.html', article = article)

@bp.route('/edit', methods = ('GET', 'POST'))
@login_required
def edit():
    id = request.args.get('id')
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        theme = request.form['theme']
        content = request.form['content'].replace('\n','')
        current_path = os.path.abspath(os.path.dirname(__file__))
        filename = db.execute(
            "SELECT * FROM article WHERE id = ?",
            (id, )
        ).fetchone()['content']
        file_path = os.path.join(current_path, 'static\\article\\bank\\' + filename)
        db.execute(
            "UPDATE article SET title = ?, theme = ? WHERE id = ?",
            (title, theme, id, )
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        db.commit()
        return redirect(url_for('map.article', filter = '全部', key = '', selected = '全部'))
    article = db.execute(
        "SELECT * FROM article WHERE id = ?",
        (id,)
    ).fetchone()
    article = dict(article)
    article['content'] = read_md_file(article['content'])
    return render_template('map/article/articleEdit.html', article = article)

@bp.route('/delete')
@login_required
def delete():
    if request.args.get('type') == 'article':
        # 文章库
        id = request.args.get('id')
        db = get_db()
        current_path = os.path.abspath(os.path.dirname(__file__))
        filename = db.execute(
            "SELECT * FROM article WHERE id = ?",
            (id, )
        ).fetchone()['content']
        file_path = os.path.join(current_path, 'static\\article\\bank\\' + filename)
        os.remove(file_path)
        db.execute(
            "DELETE FROM article WHERE id = ?",
            (id, )
        )
        db.commit()
        return redirect(url_for('map.article', filter = '全部', key = '',selected = '全部'))
    elif request.args.get('type') == 'style':
        # 装修风格展示
        id = request.args.get('id')
        db = get_db()
        current_path = os.path.abspath(os.path.dirname(__file__))
        data = db.execute(
            "SELECT * FROM style WHERE id = ?",
            (id, )
        ).fetchone()
        filename = str(id) + '.' + data['filetype']
        db.execute(
            "DELETE FROM style WHERE id = ?",
            (id, )
        )
        for sty in data['style'].split('&'):
            file_path = os.path.join(current_path, 'static\\images\\buildStyle\\' + str(sty) + '\\' + filename)
            os.remove(file_path)
        db.commit()
        return redirect(url_for('map.styleDisplay', filter = filter, key = request.form.get('key', ''), type = request.form.get('type', '全部'), area = request.form.get('area', '全部'), style = request.form.get('style', '全部'), func = request.form.get('func', '全部')))
    elif request.args.get('type') == 'furniture':
        # 建材家具展示
        id = request.args.get('id')
        db = get_db()
        current_path = os.path.abspath(os.path.dirname(__file__))
        data = db.execute(
            "SELECT * FROM furniture WHERE id = ?",
            (id, )
        ).fetchone()
        filename = str(id) + '.' + data['filetype']
        db.execute(
            "DELETE FROM furniture WHERE id = ?",
            (id, )
        )
        file_path = os.path.join(current_path, 'static\\images\\model\\' + furnitureImagePath(data['model']) + filename)
        os.remove(file_path)
        db.commit()
        return redirect(url_for('map.furnitureDisplay', filter = filter, key = request.form.get('key', ''), model = request.form.get('model', '全部'), color = request.form.get('color', '全部'), material = request.form.get('material', '全部'), style = request.form.get('style', '全部')))

# 装修风格展示
style_filters = {
    "type": ['全部', '单层', '多层'],
    "area": ['全部', '50m²以下', '50-80m²', '80-100m²', '100-130m²', '130m²以上'],
    "style": ['全部', '美式', '田园式', '欧式', '港式', '简欧', '日式', '地中海式', '轻奢', '现代', '新中式', '北欧', '后现代'],
    "func": ['全部', '客厅', '厨房', '卧室', '卫生间']
}
def style_EN(filter):
    if filter == '美式':
        filter = 'Americano'
    elif filter == '田园式':
        filter = 'Arcadian'
    elif filter == '欧式':
        filter = 'European'
    elif filter == '港式':
        filter = 'HongKong'
    elif filter == '简欧':
        filter = 'JaneEuropean'
    elif filter == '日式':
        filter = 'Japanese'
    elif filter == '地中海式':
        filter = 'Mediterranean'
    elif filter == '轻奢':
        filter = 'MildLuxury'
    elif filter == '现代':
        filter = 'Modern'
    elif filter == '新中式':
        filter = 'NeoChinese'
    elif filter == '北欧':
        filter = 'NorthernEuropean'
    elif filter == '后现代':
        filter = 'Postmodern'
    return filter

@bp.route('/styleDisplay/<string:filter>', methods = ('GET', 'POST'))
@login_required
def styleDisplay(filter):
    if request.method == 'POST':
        return redirect(url_for('map.styleDisplay', filter = filter, key = request.form.get('key', '%'), type = request.form.get('type', '全部'), area = request.form.get('area', '全部'), style = request.form.get('style', '全部'), func = request.form.get('func', '全部')))
    key = request.args.get('key', '%')
    oldFilter = filter
    db = get_db()
    styles = db.execute(
        "SELECT * FROM style ORDER BY id DESC",
    ).fetchall()
    min = 0
    max = 999
    if request.args.get('area') == '50m²以下':
        max = 50
    elif request.args.get('area') == '50-80m²':
        min = 50
        max = 80
    elif request.args.get('area') == '80-100m²':
        min = 80
        max = 100
    elif request.args.get('area') == '100-130m²':
        min = 100
        max = 130
    elif request.args.get('area') == '130m²以上':
        min = 130
    if filter == key:
        styles = db.execute(
            "SELECT * FROM style WHERE title LIKE '%'||?||'%' AND (type LIKE ? AND (area > ? AND area <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND func LIKE ?) ORDER BY id DESC",
            (filter, '%' if request.args.get('type') == '全部' else request.args.get('type'), min, max, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('func') == '全部' else request.args.get('func'), )
        ).fetchall()
    elif filter == request.args.get('type'):
        styles = db.execute(
            "SELECT * FROM style WHERE title LIKE '%'||?||'%' AND (type LIKE ? AND (area > ? AND area <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND func LIKE ?) ORDER BY id DESC",
            (key, '%' if filter == '全部' else filter, min, max, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('func') == '全部' else request.args.get('func'), )
        ).fetchall()
    elif filter == request.args.get('area'):
        styles = db.execute(
            "SELECT * FROM style WHERE title LIKE '%'||?||'%' AND (type LIKE ? AND (area > ? AND area <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND func LIKE ?) ORDER BY id DESC",
            (key, '%' if request.args.get('type') == '全部' else request.args.get('type'), min, max, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('func') == '全部' else request.args.get('func'), )
        ).fetchall()
    elif filter == request.args.get('style'):
        filter = style_EN(filter)
        styles = db.execute(
            "SELECT * FROM style WHERE title LIKE '%'||?||'%' AND (type LIKE ? AND (area > ? AND area <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND func LIKE ?) ORDER BY id DESC",
            (key, '%' if request.args.get('type') == '全部' else request.args.get('type'), min, max, '%' if filter == '全部' else filter, '%' if filter == '全部' else filter, '%' if filter == '全部' else filter, '%' if request.args.get('func') == '全部' else request.args.get('func'), )
        ).fetchall()
    elif filter == request.args.get('func'):
        styles = db.execute(
            "SELECT * FROM style WHERE title LIKE '%'||?||'%' AND (type LIKE ? AND (area > ? AND area <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND func LIKE ?) ORDER BY id DESC",
            (key, '%' if request.args.get('type') == '全部' else request.args.get('type'), min, max, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if filter == '全部' else filter, )
        ).fetchall()
    return render_template('map/styleDisplay/styleDisplay.html', filters = style_filters, filter = oldFilter, key = key, styles = styles, type = request.args.get('type', '全部'), area = request.args.get('area', '全部'), style = request.args.get('style', '全部'), func = request.args.get('func', '全部'))

@bp.route('/uploadStyleImage', methods = ('GET', 'POST'))
@login_required
def uploadStyleImage():
    if request.method == 'POST':
        title = request.form['title']
        type = request.form['type']
        func = request.form['func']
        area = request.form['area']
        style = request.form.getlist('style')
        img = request.files['image']
        image = secure_filename(img.filename)
        style_str = ''
        for i in style:
            style_str += i
            style_str += '&'
        style_str = style_str[0: -1]
        db = get_db()
        exist = db.execute(
            "SELECT * FROM style WHERE title = ? AND type = ? AND func = ? AND area = ? AND style = ? AND filetype = ?",
            (title, type, func, area, style_str, image.split('.')[-1], ),
        ).fetchone()
        if exist is None:
            db.execute(
                "INSERT INTO style (title, type, func, area, style, filetype) VALUES (?, ?, ?, ?, ?, ?)",
                (title, type, func, area, style_str, image.split('.')[-1], ),
            )
            db.commit()
            data = db.execute(
                "SELECT * FROM style WHERE title = ? AND type = ? AND func = ? AND area = ? AND style = ? AND filetype = ?",
                (title, type, func, area, style_str, image.split('.')[-1], ),
            ).fetchone()
            filename = str(data['id']) + '.' + data['filetype']
            for sty in style_str.split('&'):
                img.save(os.path.join('./flaskr/static/images/buildStyle' + '/' + sty, filename))
        return redirect(url_for('map.styleDisplay', filter = filter, key = '', type = '全部', area = '全部', style = '全部', func = '全部'))

@bp.route('/styleShow')
@login_required
def styleShow():
    id = request.args.get('id')
    db = get_db()
    style = db.execute(
        "SELECT * FROM style WHERE id = ?",
        (id,)
    ).fetchone()
    return render_template('map/styleDisplay/styleShow.html', style = style)

# 建材家具展示
furniture_filters = {
    "model": ['全部', ['硬装', '门', '窗', '地面', '墙面', '结构部件'], ['家具', '沙发', '床', '桌子', '椅子|凳子', '柜架'], ['厨卫', '橱柜', '浴室柜', '洗手台', '马桶', '浴缸']],
    "color": ['全部', '红色', '橙色', '黄色', '绿色', '蓝色', '紫色', '黑色', '灰色', '粉色', '木色', '白色', '褐色', '米色'],
    "material": ['全部', '木质', '布料', '金属', '陶瓷', '石材', '玻璃', '塑料'],
    "style": ['全部', '美式', '田园式', '欧式', '港式', '简欧', '日式', '地中海式', '轻奢', '现代', '新中式', '北欧', '后现代']
}

@bp.route('/furnitureDisplay/<string:filter>', methods = ('GET', 'POST'))
@login_required
def furnitureDisplay(filter):
    if request.method == 'POST':
        return redirect(url_for('map.furnitureDisplay', filter = filter, key = request.form.get('key', '%'), model = request.form.get('model', '全部'), color = request.form.get('color', '全部'), material = request.form.get('material', '全部'), style = request.form.get('style', '全部')))
    key = request.args.get('key', '%')
    oldFilter = filter
    db = get_db()
    paths = []
    furnitures = db.execute(
        "SELECT * FROM furniture ORDER BY id DESC",
    ).fetchall()
    if filter == key:
        furnitures = db.execute(
            "SELECT * FROM furniture WHERE title LIKE '%'||?||'%' AND (model LIKE ? AND color LIKE ? AND material LIKE ? AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%')) ORDER BY id DESC",
            (filter, '%' if request.args.get('model') == '全部' else request.args.get('model'), '%' if request.args.get('color') == '全部' else request.args.get('color'), '%' if request.args.get('material') == '全部' else request.args.get('material'), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), )
        ).fetchall()
    elif filter == request.args.get('model'):
        furnitures = db.execute(
            "SELECT * FROM furniture WHERE title LIKE '%'||?||'%' AND (model LIKE ? AND color LIKE ? AND material LIKE ? AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%')) ORDER BY id DESC",
            (key, '%' if filter == '全部' else filter, '%' if request.args.get('color') == '全部' else request.args.get('color'), '%' if request.args.get('material') == '全部' else request.args.get('material'), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), )
        ).fetchall()
    elif filter == request.args.get('color'):
        furnitures = db.execute(
            "SELECT * FROM furniture WHERE title LIKE '%'||?||'%' AND (model LIKE ? AND color LIKE ? AND material LIKE ? AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%')) ORDER BY id DESC",
            (key, '%' if request.args.get('model') == '全部' else request.args.get('model'), '%' if filter == '全部' else filter, '%' if request.args.get('material') == '全部' else request.args.get('material'), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), )
        ).fetchall()
    elif filter == request.args.get('material'):
        furnitures = db.execute(
            "SELECT * FROM furniture WHERE title LIKE '%'||?||'%' AND (model LIKE ? AND color LIKE ? AND material LIKE ? AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%')) ORDER BY id DESC",
            (key, '%' if request.args.get('model') == '全部' else request.args.get('model'), '%' if request.args.get('color') == '全部' else request.args.get('color'), '%' if filter == '全部' else filter, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), )
        ).fetchall()
    elif filter == request.args.get('style'):
        filter = style_EN(filter)
        furnitures = db.execute(
            "SELECT * FROM furniture WHERE title LIKE '%'||?||'%' AND (model LIKE ? AND color LIKE ? AND material LIKE ? AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%')) ORDER BY id DESC",
            (key, '%' if request.args.get('model') == '全部' else request.args.get('model'), '%' if request.args.get('color') == '全部' else request.args.get('color'), '%' if request.args.get('material') == '全部' else request.args.get('material'), '%' if filter == '全部' else filter, '%' if filter == '全部' else filter, '%' if filter == '全部' else filter, )
        ).fetchall()
    for i in range(len(furnitures)):
        paths.append(furnitureImagePath(furnitures[i]['model']))
    furnitures = zip(furnitures, paths)
    return render_template('map/furnitureDisplay/furnitureDisplay.html', filters = furniture_filters, filter = oldFilter, key = key, furnitures = furnitures, model = request.args.get('model', '全部'), color = request.args.get('color', '全部'), material = request.args.get('material', '全部'), style = request.args.get('style', '全部'))

@bp.route('/uploadFurnitureImage', methods = ('GET', 'POST'))
@login_required
def uploadFurnitureImage():
    if request.method == 'POST':
        title = request.form['title']
        model = request.form['model']
        color = request.form['color']
        material = request.form['material']
        style = request.form.getlist('style')
        price = request.form['price']
        unit = request.form['unit']
        size = request.form.get('size', '')
        img = request.files['image']
        image = secure_filename(img.filename)
        style_str = ''
        for i in style:
            style_str += i
            style_str += '&'
        style_str = style_str[0: -1]
        db = get_db()
        exist = db.execute(
            "SELECT * FROM furniture WHERE title = ? AND model = ? AND color = ? AND material = ? AND style = ? AND price = ? AND unit = ? AND size = ? AND filetype = ?",
            (title, model, color, material, style_str, price, unit, size, image.split('.')[-1], ),
        ).fetchone()
        if exist is None:
            db.execute(
                "INSERT INTO furniture (title, model, color, material, style, price, unit, size, filetype) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (title, model, color, material, style_str, price, unit, size, image.split('.')[-1], ),
            )
            db.commit()
            data = db.execute(
                "SELECT * FROM furniture WHERE title = ? AND model = ? AND color = ? AND material = ? AND style = ? AND price = ? AND unit = ? AND size = ? AND filetype = ?",
                (title, model, color, material, style_str, price, unit, size, image.split('.')[-1], ),
            ).fetchone()
            filename = str(data['id']) + '.' + data['filetype']
            img.save(os.path.join('./flaskr/static/images/model/' + furnitureImagePath(model), filename))
        return redirect(url_for('map.furnitureDisplay', filter = filter, key = '', model = '全部', color = '全部', material = '全部', style = '全部'))
    
@bp.route('/furnitureShow')
@login_required
def furnitureShow():
    id = request.args.get('id')
    db = get_db()
    furniture = db.execute(
        "SELECT * FROM furniture WHERE id = ?",
        (id,)
    ).fetchone()
    return render_template('map/furnitureDisplay/furnitureShow.html', path = furnitureImagePath(furniture['model']), furniture = furniture)

price_estimate = [
    {'高品质': '1800-3000元/m²', '中等': '1500-1800元/m²', '简单': '1000-1500元/m²'},
    {'高品质': '1500-2500元/m²', '中等': '1200-1500元/m²', '简单': '900-1200元/m²'},
    {'高品质': '1200-2000元/m²', '中等': '1000-1200元/m²', '简单': '800-1000元/m²'},
]
floor_price = {
    "强化复合地板": '160-300元/m²',
    "实木复合地板": '200-400元/m²',
    "实木地板": '380-500元/m²'
}
door_price = {
    "复合门": '1300-1500元/个',
    "免漆门": '800-3000元/个',
    "实木门": '3500-20000元/个',
    "镁铝合金推拉门": '700-800元/个'
}

@bp.route('/priceEstimate', methods = ('GET', 'POST'))
@login_required
def priceEstimate():
    db = get_db()
    price = 0
    if request.method == 'POST':
        min = 0
        max = 0
        if request.args.get('type') == 'rough':
            # 粗略估价
            area = request.form['area']
            cityid = request.form['city']
            level = request.form['level']
            lines = db.execute(
                "SELECT * FROM cities WHERE cityid = ?",
                (cityid, ),
            ).fetchone()['lines']
            min = int(price_estimate[lines - 1][level].split('-')[0]) * float(area)
            max = int(price_estimate[lines - 1][level].split('-')[1].split('元')[0]) * float(area)
            min = '{:.2f}'.format(min)
            max = '{:.2f}'.format(max)
            price = str(min) + '-' + str(max) + '元'
        else:
            # 细致估价
            area = request.form['area']
            area = float(area)
            cityid = request.form['city']
            level = request.form['level']
            parlourArea = request.form['parlourArea']
            parlourArea = float(parlourArea)
            kitchenArea = request.form['kitchenArea']
            kitchenArea = float(kitchenArea)
            bedroomArea = request.form['bedroomArea']
            bedroomArea = float(bedroomArea)
            bathroomArea = request.form['bathroomArea']
            bathroomArea = float(bathroomArea)
            floor = request.form['woodenFloor']
            door = request.form['door']
            doorNum = request.form['doorNum']
            doorNum = float(doorNum)
            lines = db.execute(
                "SELECT * FROM cities WHERE cityid = ?",
                (cityid, ),
            ).fetchone()['lines']
            min = int(price_estimate[lines - 1][level].split('-')[0]) * area * 0.65
            max = int(price_estimate[lines - 1][level].split('-')[1].split('元')[0]) * area * 0.65
            # 水电工程费用
            min += 50 * parlourArea * 0.3 + 50 * kitchenArea * 0.7 + 50 * bedroomArea * 0.3 + 50 * bathroomArea * 0.8
            max += 50 * parlourArea * 0.3 + 50 * kitchenArea * 0.7 + 50 * bedroomArea * 0.3 + 50 * bathroomArea * 0.8
            # 油漆费用
            min += 35 * parlourArea * 3.5 * 0.8 + 35 * kitchenArea * 3.5 * 0.3 + 35 * bedroomArea * 3.5 * 0.5 + 35 * bathroomArea * 3.5 * 0.2
            max += 80 * parlourArea * 3.5 * 0.8 + 80 * kitchenArea * 3.5 * 0.3 + 80 * bedroomArea * 3.5 * 0.5 + 80 * bathroomArea * 3.5 * 0.2
            # 地砖费用
            min += (120 * parlourArea * 0.1 + 120 * kitchenArea * 0.7 + 120 * bedroomArea * 0.1 + 120 * bathroomArea * 0.8) / 0.97
            max += (300 * parlourArea * 0.1 + 300 * kitchenArea * 0.7 + 300 * bedroomArea * 0.1 + 300 * bathroomArea * 0.8) /0.92
            # 找平
            min += 15 * area
            max += 15 * area
            # 木地板
            min += int(floor_price[floor].split('-')[0]) * parlourArea * 1 + int(floor_price[floor].split('-')[0]) * kitchenArea * 0 + int(floor_price[floor].split('-')[0]) * bedroomArea * 1 + int(floor_price[floor].split('-')[0]) * bathroomArea * 0
            max += int(floor_price[floor].split('-')[1].split('元')[0]) * parlourArea * 1 + int(floor_price[floor].split('-')[1].split('元')[0]) * kitchenArea * 0 + int(floor_price[floor].split('-')[1].split('元')[0]) * bedroomArea * 1 + int(floor_price[floor].split('-')[1].split('元')[0]) * bathroomArea * 0
            # 吊顶
            min += 240 * parlourArea * 0.6 + 240 * kitchenArea * 0 + 240 * bedroomArea * 0.4 + 240 * bathroomArea * 0.1
            max += 250 * parlourArea * 0.6 + 250 * kitchenArea * 0 + 250 * bedroomArea * 0.4 + 250 * bathroomArea * 0.1
            # 橱柜
            min += 8000
            max += 10000
            # 卫生间
            min += 5000
            max += 8000
            # 门
            min += int(door_price[door].split('-')[0]) * doorNum
            max += int(door_price[door].split('-')[1].split('元')[0]) * doorNum
            min = '{:.2f}'.format(min)
            max = '{:.2f}'.format(max)
            price = str(min) + '-' + str(max) + '元'
    provinces = db.execute(
        "SELECT * FROM provinces"
    ).fetchall()
    cities = db.execute(
        "SELECT * FROM cities"
    ).fetchall()
    return render_template('map/priceEstimate/priceEstimate.html', price = price, provinces = provinces, cities = list(map(dict, cities)))

template_filters = {
    "func": ['全部', '客厅', '厨房', '卧室', '卫生间'],
    "style": ['全部', '美式', '田园式', '欧式', '港式', '简欧', '日式', '地中海式', '轻奢', '现代', '新中式', '北欧', '后现代'],
    "width": ['全部', '0-2m', '2-4m', '4-6m', '6m以上'],
    "height": ['全部', '0-2m', '2-4m', '4-6m', '6m以上'],
    "demand": ['全部', '宽敞', '适中', '拥挤']
}

@bp.route('/smartLayout/<string:filter>', methods = ('GET', 'POST'))
@login_required
def smartLayout(filter):
    if request.method == 'POST':
        return redirect(url_for('map.furnitureDisplay', filter = filter, key = request.form.get('key', '%'), func = request.form.get('func', '全部'), style = request.form.get('style', '全部'), width = request.form.get('width', '全部'), height = request.form.get('height', '全部'), demand = request.form.get('demand', '全部')))
    key = request.args.get('key', '%')
    oldFilter = filter
    db = get_db()
    templates = db.execute(
        "SELECT * FROM template ORDER BY id DESC",
    ).fetchall()
    wmin = 0
    wmax = 10
    if request.args.get('width') == '0-2m':
        wmax = 2
    elif request.args.get('width') == '2-4m':
        wmin = 2
        wmax = 4
    elif request.args.get('width') == '4-6m':
        wmin = 4
        wmax = 6
    elif request.args.get('width') == '6m以上':
        wmin = 6
    hmin = 0
    hmax = 10
    if request.args.get('height') == '0-2m':
        hmax = 2
    elif request.args.get('height') == '2-4m':
        hmin = 2
        hmax = 4
    elif request.args.get('height') == '4-6m':
        hmin = 4
        hmax = 6
    elif request.args.get('height') == '6m以上':
        hmin = 6
    if filter == key:
        templates = db.execute(
            "SELECT * FROM template WHERE title LIKE '%'||?||'%' AND (func LIKE ? AND (width > ? AND width <= ?) AND (height > ? AND height <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND demand LIKE ?) ORDER BY id DESC",
            (filter, '%' if request.args.get('func') == '全部' else request.args.get('func'), wmin, wmax, hmin, hmax, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('demand') == '全部' else request.args.get('demand'), )
        ).fetchall()
    elif filter == request.args.get('func'):
        templates = db.execute(
            "SELECT * FROM template WHERE title LIKE '%'||?||'%' AND (func LIKE ? AND (width > ? AND width <= ?) AND (height > ? AND height <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND demand LIKE ?) ORDER BY id DESC",
            (key, '%' if filter == '全部' else filter, wmin, wmax, hmin, hmax, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('demand') == '全部' else request.args.get('demand'), )
        ).fetchall()
    elif filter == request.args.get('width'):
        templates = db.execute(
            "SELECT * FROM template WHERE title LIKE '%'||?||'%' AND (func LIKE ? AND (width > ? AND width <= ?) AND (height > ? AND height <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND demand LIKE ?) ORDER BY id DESC",
            (key, '%' if request.args.get('func') == '全部' else request.args.get('func'), wmin, wmax, hmin, hmax, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('demand') == '全部' else request.args.get('demand'), )
        ).fetchall()
    elif filter == request.args.get('height'):
        templates = db.execute(
            "SELECT * FROM template WHERE title LIKE '%'||?||'%' AND (func LIKE ? AND (width > ? AND width <= ?) AND (height > ? AND height <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND demand LIKE ?) ORDER BY id DESC",
            (key, '%' if request.args.get('func') == '全部' else request.args.get('func'), wmin, wmax, hmin, hmax, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('demand') == '全部' else request.args.get('demand'), )
        ).fetchall()
    elif filter == request.args.get('style'):
        filter = style_EN(filter)
        templates = db.execute(
            "SELECT * FROM template WHERE title LIKE '%'||?||'%' AND (func LIKE ? AND (width > ? AND width <= ?) AND (height > ? AND height <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND demand LIKE ?) ORDER BY id DESC",
            (key, '%' if request.args.get('func') == '全部' else request.args.get('func'), wmin, wmax, hmin, hmax, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('demand') == '全部' else request.args.get('demand'), )
        ).fetchall()
    elif filter == request.args.get('demand'):
        templates = db.execute(
            "SELECT * FROM template WHERE title LIKE '%'||?||'%' AND (func LIKE ? AND (width > ? AND width <= ?) AND (height > ? AND height <= ?) AND (style LIKE ? OR style LIKE '%'||?||'&%' OR style LIKE '%&'||?||'%') AND demand LIKE ?) ORDER BY id DESC",
            (key, '%' if request.args.get('func') == '全部' else request.args.get('func'), wmin, wmax, hmin, hmax, '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('style') == '全部' else style_EN(request.args.get('style')), '%' if request.args.get('demand') == '全部' else request.args.get('demand'), )
        ).fetchall()
    templates = list(map(dict, templates))
    return render_template('map/smartLayout/smartLayout.html', filters = template_filters, filter = oldFilter, key = request.args.get('key', ''), templates = templates, func = request.args.get('func', '全部'), style = request.args.get('style', '全部'), width = request.args.get('width', '全部'), height = request.args.get('height', '全部'), demand = request.args.get('demand', '全部'))
    
@bp.route('/templateShow')
@login_required
def templateShow():
    id = request.args.get('id')
    db = get_db()
    template = db.execute(
        "SELECT * FROM template WHERE id = ?",
        (id,)
    ).fetchone()
    return render_template('map/smartLayout/templateShow.html', template = template)

@bp.route('/smartLayout_createTemplate', methods = ('GET', 'POST'))
@login_required
def smartLayout_createTemplate():
    if request.method == 'POST':
        title = request.form['title']
        func = request.form['func']
        width = request.form['width']
        height = request.form['height']
        style = request.form['style']
        remark = request.form['remark']
        db = get_db()
        db.execute(
            "INSERT INTO template (title, func, width, height, style, remark) VALUES (?, ?, ?, ?, ?, ?)",
            (title, func, width, height, style, remark, ),
        )
        db.commit()
        return render_template('map/smartLayout/smartLayout.html')
    # grid_scale = request.args.get('grid_scale', '20')
    # return render_template('map/smartLayout/createTemplate.html', grid_scale = grid_scale)
    db = get_db()
    models = db.execute(
        "SELECT * FROM model",
    ).fetchall()
    return render_template('map/smartLayout/createTemplate.html', models = models)

@bp.route('/smartLayout_createModel', methods = ('GET', 'POST'))
@login_required
def smartLayout_createModel(): 
    if request.method == 'POST':
        name = request.form['modelName']
        type = request.form['modelType']
        minGrow = request.form['modelMinGrow']
        maxGrow = request.form['modelMaxGrow']
        code = request.form['modelCode']
        db = get_db()
        db.execute(
            "INSERT INTO model (name, type, minGrow, maxGrow, code) VALUES (?, ?, ?, ?, ?)",
            (name, type, minGrow, maxGrow, code, ),
        )
        db.commit()
        return redirect(url_for('map.smartLayout_createTemplate'))
    name = request.args.get('name', '')
    type = request.args.get('type', '')
    min = request.args.get('min', '')
    max = request.args.get('max', '')
    code = request.args.get('code', '')
    return render_template('map/smartLayout/createModel.html', name = name, type = type, min = min, max = max, code = code)

@bp.route('/smartLayout_deleteModel', methods = ('GET', 'POST'))
@login_required
def smartLayout_deleteModel(): 
    id = request.args.get('id')
    db = get_db()
    db.execute(
        "DELETE FROM model WHERE id = ?",
        (id, ),
    )
    db.commit()
    models = db.execute(
        "SELECT * FROM model",
    ).fetchall()
    return render_template('map/smartLayout/createTemplate.html', models = models)

def furnitureCN(model):
    cn = ''
    if model == 'door':
        cn = '门'
    elif model == 'window':
        cn = '窗'
    elif model == 'sofa':
        cn = '沙发'
    elif model == 'bed':
        cn = '床'
    elif model == 'desk':
        cn = '桌子'
    elif model == 'chair':
        cn = '椅子|凳子'
    elif model == 'cabinetRack':
        cn = '柜架'
    elif model == 'cupboard':
        cn = '橱柜'
    elif model == 'bathroomCabinet':
        cn = '浴室柜'
    elif model == 'washStand':
        cn = '洗手台'
    elif model == 'toilet':
        cn = '马桶'
    elif model == 'bathtub':
        cn = '浴缸'
    return cn

@bp.route('/smartLayout_searchTemplate', methods = ('GET', 'POST'))
@login_required
def smartLayout_searchTemplate(): 
    func = request.form['func']
    width = float(request.form['width'])
    height = float(request.form['height'])
    locate = request.form['locate']
    demand = request.form.get('demand', '%')
    near1 = request.form.get('near1', '%')
    near2 = request.form.get('near2', '%')
    if near1 == near2:
        near = ''
    else:
        near = furnitureCN(near1) + '与' + furnitureCN(near2) + '相近'
    db = get_db()
    template = db.execute(
        "SELECT * FROM template WHERE func = ? AND (width >= ? AND width <= ?) AND (height >= ? AND height <= ?) AND locate = ? AND demand LIKE '%'||?||'%' AND near LIKE '%'||?||'%'",
        (func, width - 1, width + 1, height - 1, height + 1, locate, demand, near, ),
    ).fetchone()
    if template is None:
        error = "暂无匹配模板！"
        flash(error)
        return redirect(url_for('map.smartLayout', filter = '全部', key = '', func = '全部', style = '全部', width = '全部', height = '全部', demand = '全部'))
    return render_template('map/smartLayout/templateShow.html', template = template);