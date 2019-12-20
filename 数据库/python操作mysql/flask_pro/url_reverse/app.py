from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def index():
    print(url_for('my_list'))
    print(url_for('article', id='abc'))
    return 'Hello World!'

@app.route('/list/')
def my_list():
    return 'list'

@app.route('/article/<id>/')
def article(id):
    return '请求id是{}'.format(id)


if __name__ == '__main__':
    app.run(debug=True)
