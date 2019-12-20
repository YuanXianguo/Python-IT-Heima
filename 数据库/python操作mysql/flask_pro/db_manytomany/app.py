from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

article_tag = db.Table('article_tag',
        db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)

    tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('articles'))

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

db.create_all()

@app.route('/')
def hello_world():
    article1 = Article(title='python1')
    article2 = Article(title='python2')

    tag1 = Tag(name='a1')
    tag2 = Tag(name='a2')

    article1.tags.append(tag1)
    article1.tags.append(tag2)

    article2.tags.append(tag1)
    article2.tags.append(tag2)

    db.session.add(article1)
    db.session.add(article2)
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.commit()

    return 'Hello World!'

@app.route('/query/')
def query():
    article1 = db.session.query(Article).filter_by(title='python1').first()
    tags = [tag.name for tag in article1.tags]
    tag1 = db.session.query(Tag).filter_by(name='a1').first()
    articles = [article.title for article in tag1.articles]

    return '文章标题title="python1"的标签有{}，标签名字tag="a1"的文章有{}'.format(tags, articles)

if __name__ == '__main__':
    app.run()
