from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    user = {
        'name': 'daguo',
        'age': 18
    }
    web = ['baidu', 'google']
    return render_template('index.html', user=user, web=web)

@app.route('/books/')
def books():
    four_books = [
        {
            'name': '红楼梦',
            'author': '曹雪芹'
        },
        {
            'name': '西游记',
            'author': '吴承恩'
        },
        {
            'name': '三国演义',
            'author': '罗贯中'
        },
        {
            'name': '水浒传',
            'author': '施耐庵'
        },
    ]
    return render_template('books.html', books=four_books)


if __name__ == '__main__':
    app.run()
