from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Comment
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    # questions = db.session.query(Question).filter_by(is_valid=1).order_by(Question.create_time.desc())
    # 查询有效数据，并按时间降序排序
    questions = Question.query.filter(Question.is_valid == 1).order_by(Question.create_time.desc())
    return render_template('index.html', questions=questions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = db.session.query(User).filter_by(telephone=telephone).first()
        if not user:
            return '手机号不存在！'
        elif user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return '密码错误！'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    telephone = request.form.get('telephone')
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    user_ = db.session.query(User).filter_by(telephone=telephone).first()
    if user_:
        return '手机号码已经注册，请更换手机号码！'
    if password1 == password2 and password1:
        user = User(telephone=telephone, username=username, password=password1)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return '注册失败，两次密码不一致或为空！'


@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        user_id = session.get('user_id')
        title = request.form.get('title')
        content = request.form.get('content')
        question_ = Question(title=title, content=content, user_id=user_id)
        db.session.add(question_)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/comment/<question_id>/')
def comment(question_id):
    _question = Question.query.get(question_id)
    return render_template('comment.html', question=_question)


@app.route('/new_comment/', methods=['POST'])
@login_required
def new_comment():
    content = request.form.get('comment-content')
    question_id = request.form.get('question_id')
    user_id = session.get('user_id')
    _comment = Comment(content=content, user_id=user_id, question_id=question_id)
    db.session.add(_comment)
    db.session.commit()
    return redirect(url_for('comment', question_id=_comment.question.id))


@app.route('/user_info/<user_id>')
def user_info(user_id):
    # questions = Question.query.filter_by(user_id=user_id).order_by(Question.create_time.desc()).all()
    user = User.query.get(user_id)
    return render_template('user_info.html', user=user)


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
