from flask import Flask, render_template, session, redirect, url_for, request, flash, abort
import models
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdifkjaleshr;qo'
app.config['ADMIN'] = 'TOM'
app.config['PASSWORD'] = '123456'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 当未登录的用户尝试访问一个 login_required 装饰的视图，Flask-Login 会闪现一条消息并且重定向到登录视图。同url_for()一样用法
login_manager.login_message = '请登陆'  # 自定义未登陆消息提示
login_manager.login_message_category = '错误'  # 定义未登录消息提示的分类


class User(UserMixin):
    '''用户模型从UserMixin中继承，可以自定义，实际使用也是需要自定义'''
    pass


@login_manager.user_loader
def load_user(userid):
    '''
    这个回调用于从会话中存储的用户 ID 重新加载用户对象。
    它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
    一般用于“记住我”后cookies中记录用户ID，直接从
    '''
    if userid not in app.config['ADMIN']:
        return
    user = User()
    user.id = app.config['ADMIN']
    return user


@login_manager.request_loader
def request_loader(request):
    '''
    有时你想要不使用 cookies 情况下登录用户，
    比如使用 HTTP 头或者一个作为查询参数的 api 密钥。
    这种情况下，你应该使用 request_loader 回调。
    这个回调和 user_loader 回调作用一样，
    但是 user_loader 回调只接受 Flask 请求而不是一个 user_id。
    '''
    username = request.form.get('username')  # 从前端获取用户名
    if username not in app.config:  # 判断用户名是否在数据库中
        return
    user = User()
    user.name = username
    user.is_authenticated = request.form['password'] == app.config[
        'PASSWORD']  # 当用户通过验证时，也即提供有效证明时返回 True 。（只有通过验证的用户会满足 login_required 的条件。）
    return user


@app.route('/admin/posts/')
@login_required
def post_list():
    return render_template('admin/post-list.html')


@app.route('/admin/')
@login_required
def dashboard():
    return render_template('admin/index.html', current_user=current_user)


def next_is_valid(next):
    '''验证下一跳是否合法'''
    return True


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        pwd = request.form.get('pwd', None)
        if username == app.config['ADMIN'] and pwd == app.config['PASSWORD']:  # 应对比数据库中结果,保存ID
            user = User()
            user.id = username
            login_user(user)  # 让用户登录
            next = request.args.get('next')  # 假如非访问index转跳到该页面
            if not next_is_valid(next):  # 需要验证next是否合法，定义了函数但没写内容，实际运行需要验证 警告: 你必须验证 next 参数的值。如果不验证的话，你的应用将会受到重定向的攻击。
                return abort(400)
            return redirect(next or url_for('dashboard'))
        else:
            flash('用户名或密码错误', '错误')
    return render_template('login.html')


@app.route('/logout')
def logout():
    '''用户登出'''
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
