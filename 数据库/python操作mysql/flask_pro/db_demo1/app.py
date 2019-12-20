from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

class Article(db.Model):
    """创建模型"""
    __tablename__ = 'article'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/add/')
def add_data():
    article = Article(title='aaa', content='bbb')
    db.session.add(article)
    db.session.commit()
    return 'Hello World!'

@app.route('/query/')
def query_data():
    # 方法1：返回的是第一个Article对象
    # article = Article.query.filter(Article.title == 'aaa').first()
    # 方法2：get()参数是id
    article = db.session.query(Article).get(1)
    return '{}:{}'.format(article.title, article.content)

@app.route('/update/')
def update_data():
    # 先找到需要修改的数据；对相应属性修改；提交事务
    article = db.session.query(Article).get(1)
    article.title = 'new title'
    db.session.commit()
    article_new = Article.query.filter(Article.id == 1).first()
    return '{}:{}'.format(article_new.title, article_new.content)

@app.route('/delete/')
def delete_data():
    # 先找到需要删除的数据；删除对应数据；提交事务
    article = db.session.query(Article).get(1)
    db.session.delete(article)
    db.session.commit()
    return ''

if __name__ == '__main__':
    app.run(debug=True)
