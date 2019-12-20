from flask import Flask, make_response, request

app = Flask(__name__)


@app.route("/set_cookie")
def set_cookie():
    res = make_response("success")
    # 设置cookie，默认有效期是临时，可以通过max_age设置有效期，单位：秒
    res.set_cookie("Itcast", "python", max_age=3600)
    return res


@app.route("/get_cookie")
def get_cookie():
    c = request.cookies.get("Itcast")
    return c


@app.route("/delete_cookie")
def delete_cookie():
    res = make_response("del success")
    res.delete_cookie("Itcast")
    return res


if __name__ == '__main__':
    app.run(debug=True)
