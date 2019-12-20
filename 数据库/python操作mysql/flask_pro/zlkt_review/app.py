from flask import Flask, render_template, request, redirect, url_for, session
import config
from exts import db
from models import User, Question, Comment
from decorators import login_requested

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    questions = Question.query.order_by(Question.create_time.desc()).all()
    return render_template("index.html", questions=questions)


@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    telephone = request.form.get("telephone")
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    user = User.query.filter(User.telephone == telephone).first()
    if user:
        return "手机号码已存在，请更换手机！"
    if password1 == password2 and password1:
        new_user = User(telephone=telephone, username=username, password=password1)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return "注册失败！两次密码不一致或密码为空！"


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    telephone = request.form.get("telephone")
    password = request.form.get("password")
    user = User.query.filter(User.telephone == telephone).first()
    if user:
        if user.password == password:
            session["user_id"] = user.id
            return redirect(url_for("index"))
        return "密码错误！"
    return "手机号不存在！"


@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/question/", methods=["GET", "POST"])
@login_requested
def question():
    if request.method == "GET":
        return render_template("question.html")
    title = request.form.get("title")
    content = request.form.get("content")
    user_id = session.get("user_id")
    question_ = Question(title=title, content=content, author_id=user_id)
    db.session.add(question_)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/detail/<question_id>/", methods=["GET", "POST"])
@login_requested
def detail(question_id):
    if request.method == "GET":
        question_ = Question.query.filter(Question.id == question_id).first()
        return render_template("detail.html", question=question_)
    content = request.form.get("content")
    new_comment = Comment(content=content, user_id=session.get("user_id"), question_id=question_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {"user": user}
    return {}


if __name__ == '__main__':
    app.run()
