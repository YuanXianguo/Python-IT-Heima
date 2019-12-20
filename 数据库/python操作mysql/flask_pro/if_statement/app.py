from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<is_login>/')
def index(is_login):
    if is_login == '1':
        user = {
            'name': 'daguo',
            'age': 18
        }
        return render_template('index.html', user=user)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
