from flask import Flask, abort, Response

app = Flask(__name__)


@app.route("/login")
def login():
    name = ""
    if name != "daguo":
        # 使用abort函数可以立即终止视图函数的执行，并可以返回给前端特定的信息
        # 1.传递标准的http状态码
        abort(404)
        # 2.传递响应体对象
        abort(Response("login failed"))
    return "上传成功"


@app.errorhandler(404)
def handle_404_error(err):
    """自定义处理错误方法"""

    return "出现了404错误，错误信息：%s" % err


if __name__ == '__main__':
    app.run(debug=True)
