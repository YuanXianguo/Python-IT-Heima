from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2017916@localhost/net_news?charset=utf8'
db = SQLAlchemy(app)

class News(db.Model):
    """声明模型"""
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime)
    types = db.Column(db.String(20), nullable=False)
    images = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(20))
    view_count = db.Column(db.Integer)
    is_valid = db.Column(db.Boolean)

    def __repr__(self):
        return '<News {}>'.format(self.title)


@app.route('/')
def index():
    """新闻的首页"""
    return render_template('index.html')

@app.route('/cat/<name>/')
def cat(name):
    """新闻的类别"""
    # 查询类别为name的新闻数据
    return render_template('cat.html', name=name)

@app.route('/detail/<int:new_id>/')
def detail(new_id):
    """新闻的详细信息"""
    return render_template('detail.html', new_id=new_id)

if __name__ == '__main__':
    app.run(debug=True)
