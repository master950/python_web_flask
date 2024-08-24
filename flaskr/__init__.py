import os

from flask import Flask

def create_app(test_config=None):
    # 创建APP
    app = Flask(__name__,instance_relative_config=True)
    #配置
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    #确保App实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'hello'
    
    from . import db
    #初始化APP和sqlite3数据库
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp) #注册权限蓝图

    return app
