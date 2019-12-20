from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(100), default='images/zlkt.jpg')
    is_valid = db.Column(db.Boolean, default=1)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_valid = db.Column(db.Boolean, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref(
        'questions', order_by=create_time.desc()))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_valid = db.Column(db.Boolean, default=1)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref(
        'comments', order_by=create_time.desc()))
    question = db.relationship('Question', backref=db.backref(
        'comments', order_by=create_time.desc()))
