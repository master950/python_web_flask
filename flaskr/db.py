import sqlite3

import click
from flask import current_app, g, Flask

#g 是存储多个程序的复用数据

#获取数据库连接
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

#关闭数据库连接
def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#运行sql
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('初始化数据库')

def init_app(app:Flask):
    app.teardown_appcontext(close_db) #返回响应清理时执行 close_db 函数
    app.cli.add_command(init_db_command) #添加一个命令