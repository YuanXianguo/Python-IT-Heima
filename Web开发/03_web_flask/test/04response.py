from flask import Flask, make_response

app = Flask(__name__)


@app.route("/index")
def index():
    # 1.使用元组，返回自定义的响应信息
    # 响应体，状态码，响应头
    # return "index page", 400, [("Itcast", "python"), ("City", "hangzhou")]
    # return "index page", 400, {"Itcast": "python", "City": "hangzhou"}
    # return "index page", 666, {"Itcast": "python", "City": "hangzhou"}
    # return "index page", "666 itcast status", {"Itcast": "python", "City": "hangzhou"}
    # return "index page", "666 itcast status"

    # 2.使用make_response来构造响应信息
    res = make_response("index page 2")
    res.status = "999 itcast status"
    res.headers["city"] = "hangzhou"
    return res


if __name__ == '__main__':
    app.run(debug=True)
