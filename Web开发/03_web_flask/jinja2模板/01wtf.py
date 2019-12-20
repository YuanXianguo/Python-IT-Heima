from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)

app.config["SECRET_KEY"] = "afasofbadgaweiqewq23094hfasdlfna"


# 定义表单的模型类
class RegisterForm(FlaskForm):
    user_name = StringField(label="用户名", validators=[DataRequired("用户名不能为空")])
    password = PasswordField(label="密码", validators=[DataRequired("密码不能为空")])
    password2 = PasswordField(label="确认密码", validators=[DataRequired("确认密码不能为空"),
                                                     EqualTo("password", "密码不一致")])
    submit = SubmitField(label="提交")


@app.route("/register", methods=["GET", "POST"])
def register():
    # 创建表单对象，如果是post请求，flask会把前端发送的数据存放到form对象中
    form = RegisterForm()

    # 判断form中的数据是否合理，返回bool；get请求因为没有数据，会验证失败
    if form.validate_on_submit():
        # 验证合格，提取数据
        user_name = form.user_name.data
        pwd = form.password.data
        pwd2 = form.password2.data
        print(user_name, pwd, pwd2)
        session["uer_name"] = user_name
        return redirect(url_for("index"))

    # 验证失败或get请求返回
    return render_template("register.html", form=form)


@app.route("/index")
def index():
    user_name = session.get("user_name", "daguo")
    return "hello %s" % user_name


if __name__ == '__main__':
    app.run(debug=True)
