from flask import Flask, render_template, request, g
from utils import login_log

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/')
def search():
    # 查询get提交的参数
    q = request.args.get('q')
    return '用户提交的参数是：{}'.format(q)

# 默认的视图函数，智能采用get请求，如果要次啊用post，需要写明
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    g.username = username
    login_log()
    return '提交的用户名为：{}，密码是：{}'.format(username, password)

if __name__ == '__main__':
    app.run()
