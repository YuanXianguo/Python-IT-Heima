from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('login'))
    return '这是首页'

@app.route('/login/')
def login():
    return '这是登录页面'

if __name__ == '__main__':
    app.run(debug=True)
