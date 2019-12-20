from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<id>/')
def index(id):
    return render_template('index.html', id=id)

@app.route('/login/<id>/')
def login(id):
    return render_template('login.html', id=id)

if __name__ == '__main__':
    app.run(debug=True)
