from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    print('before_request')
    return 'index'

@app.before_request
def my_before_request():
    print('hello world')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.context_processor
def my_context_processor():
    return {'username': 'daguo'}

if __name__ == '__main__':
    app.run()
