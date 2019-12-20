from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<user>/')
def index(user):
    return render_template('index.html', username=user)

@app.route('/params/')
def index2():
    class Test():
        name = '果酱'
        age = 18
    t = Test()
    context = {
        'username': 'daguo',
        'gender': '男',
        'age': 18,
        'test': t,
        'web': {
            'baidu': '百度',
            'google': '谷歌'
        }
    }
    return render_template('index2.html', **context)

if __name__ == '__main__':
    app.run()
