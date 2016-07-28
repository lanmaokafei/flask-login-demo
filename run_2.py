from datetime import datetime, timedelta
from flask import Flask, request, make_response, redirect, url_for, render_template

app = Flask(__name__)


@app.route('/setcookie/')
def set_cookie():
    resp = make_response(redirect(url_for('get_cookie')))
    resp.set_cookie('uname', value='scrapy',
                    # domain='gftong.com',
                    # path='/',
                    max_age=120,
                    expires=datetime.now() + timedelta(hours=7))  # 写入客户端硬盘信息
    return resp  # 写入硬盘


@app.route('/clearcookie/')
def clear_cooker():
    resp = make_response(redirect(url_for('get_cookie')))
    resp.set_cookie('uname', '', expires=datetime.now() + timedelta(hours=-1))
    return resp


@app.route('/getcookie/')
def get_cookie():
    ck = request.cookies['uname']

    return render_template('get-cookie.html', ck=ck)


if __name__ == '__main__':
    app.run(debug=True)
