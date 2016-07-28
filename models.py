import flask_login
from run import app
from flask import request, redirect, url_for

login_manager = flask_login.LoginManager()  # 实例化登陆管理器
login_manager.init_app(app)

users = {'foo@bar.tld': {'pw': 'secret'}}  # 假设数据库中用户帐号密码


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


