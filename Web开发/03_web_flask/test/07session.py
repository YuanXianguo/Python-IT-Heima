from flask import Flask, session

app = Flask(__name__)

# flask的session需要用到密钥
app.config["SECRET_KEY"] = "flifk05lutdu58ykuvh"


@app.route("/login")
def login():
    # 设置session
    session["name"] = "python"
    session["phone"] = "18811111111"
    return "login success"


@app.route("/index")
def index():
    # 获取session
    name = session.get("name")
    return "hello %s" % name


if __name__ == '__main__':
    app.run(debug=True)
