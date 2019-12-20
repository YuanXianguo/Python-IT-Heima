from flask import Flask, request

app = Flask(__name__)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    """接受前端传送过来的文件"""
    file_obj = request.files.get("pic")
    path = "demo.png"
    file_obj.save(path)
    return "上传成功"


if __name__ == '__main__':
    app.run(debug=True)
