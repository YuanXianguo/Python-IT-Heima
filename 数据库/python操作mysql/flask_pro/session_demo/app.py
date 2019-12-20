from flask import Flask, session
import os
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # 用来加密
# 可以将过期时间设置为7天
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

@app.route('/')
def hello_world():
    # 添加数据到session中，操作session的时候，跟操作字典是一样的
    session['username'] = 'daguo'
    # 如果没有指定session的过期时间，那么默认是浏览器关闭后过期
    session.permanent = True  # 可以设置过期时间，默认为31天
    return 'Hello World!'

@app.route('/get/')
def get():  # 获取session中的数据
    return session.get('username')

@app.route('/delete/')
def delete():  # 删除session中的数据
    session.pop('username')
    return 'success'

@app.route('/clear/')
def clear():  # 删除session中的所有数据
    session.clear()
    return 'success'

if __name__ == '__main__':
    app.run()
