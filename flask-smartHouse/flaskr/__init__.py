'''应用初始化相关操作'''
import os
import datetime

from flask import Flask

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = datetime.timedelta(seconds = 1)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import infoManagement
    app.register_blueprint(infoManagement.bp)

    from . import map
    app.register_blueprint(map.bp)

    return app