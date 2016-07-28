from flask import Flask, render_template, session, redirect, url_for, request, flash
import models
import flask_login


app = Flask(__name__)
app.config['ADMIN'] = 'TOM'
app.config['PASSWORD'] = '123456'
app.config['SECRET_KEY'] = 'sdifkjaleshr;qo'


@app.route('/login2/', methods=['GET', 'POST'])
def login2():
    if request.method == 'GET':
        return '''
               <form action='#' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = request.form['email']
    if request.form['pw'] == models.users.get(email, {'pw': ''}).get('pw', None):
        user = models.User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/protected/')
@models.flask_login.login_required
def protected():
    return 'Logged in as: ' + models.flask_login.current_user.id


@app.route('/logout2/')
def logout2():
    models.flask_login.logout_user()
    return 'Logged out'


def yanz(func):
    def wrapper():
        if 'admin' not in session:
            return redirect(url_for('login'))
        else:
            pass

    return wrapper



@app.route('/admin/posts/')
@yanz
def post_list():
    return render_template('admin/post-list.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return render_template('admin/index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        pwd = request.form.get('pwd', None)
        if username == app.config['ADMIN'] and pwd == app.config['PASSWORD']:
            # 创建用户表示
            session['admin'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误', '错误')
    return render_template('login.html')


@app.route('/logout/')
def logout():
    session.pop('admin')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
