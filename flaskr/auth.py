import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, make_response
)
from werkzeug.security import check_password_hash,generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')

#注册
@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        # 获取注册表单数据
        username = request.form['username']
        psd = request.form['psd']
        #获取数据库连接
        db = get_db()
        #错误对象
        error = None

        if not username:
            error = '用户名是必须的'
        elif not psd:
            error = '密码是必须的'
        #如果检验通过
        if error is None:
            try:
                #执行sql语句
                db.execute(
                    'INSERT INTO user (username,password) VALUES (?,?)',
                    (username,generate_password_hash(psd)),
                )
                db.commit() #提交事务
            except db.IntegrityError:
                error = f'User {username} is already registered'
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return make_response('注册成功',200)
