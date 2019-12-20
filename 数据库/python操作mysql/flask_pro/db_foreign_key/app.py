from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 给Article这个模型添加一个author属性，可以访问这篇文章的作者的数据，像访问普通模型一样
    # backref是定义反向引用，可以通过User.articles访问某个作者所写的所有文章
    author = db.relationship('User', backref=db.backref('articles'))

db.create_all()

@app.route('/')
def add_user():
    # user1 = User(username='daguo')
    # db.session.add(user1)
    # db.session.commit()
    article1 = Article(title='python1', content='python1111', author_id=1)
    article2 = Article(title='python2', content='python2222')
    article2.author = db.session.query(User).get(1)
    db.session.add(article1)
    db.session.add(article2)
    db.session.commit()
    return 'Hello World!'


@app.route('/query_user')
def query_user():
    # 找到第一个article对象
    article = db.session.query(Article).filter_by(title='python1')[0]
    username = article.author.username
    # 找到第一个user对象
    user = db.session.query(User).filter_by(username=username)[0]
    articles = [article_.title for article_ in user.articles]
    return 'title="python1"的文章是{}写的，他所有的文章有{}'.format(username, articles)


if __name__ == '__main__':
    app.run()
