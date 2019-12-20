from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/article/<id>')
def article(id):
    return '传入的参数是{}'.format(id)

if __name__ == '__main__':
    app.run()
