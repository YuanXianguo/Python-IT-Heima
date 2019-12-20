from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    lis = [1, 2]
    return render_template('index.html', lis=lis)

if __name__ == '__main__':
    app.run()
