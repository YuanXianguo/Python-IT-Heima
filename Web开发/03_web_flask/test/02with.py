from flask import Flask, request

app = Flask(__name__)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    """接受前端传送过来的文件"""
    file_obj = request.files.get("pic")
    path = "demo.png"
    file_obj.save(path)
    return "上传成功"


# with上下文管理器
class Foo(object):
    def __enter__(self):
        """进入with语句时候被with调用"""
        print("enter called")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开with语句时被with调用"""
        print("exit called")
        print("exc_type:%s" % exc_type)
        print("exc_val:%s" % exc_val)
        print("exc_tb:%s" % exc_tb)


with Foo() as foo:
    print("hello python")
    a = 1 / 0
    print("hello end")


if __name__ == '__main__':
    app.run(debug=True)
