from flask import Flask

# 初始化一个Flask对象，需要传递一个参数__name__
# 方便flask框架去寻找资源
# 方便flask插件比如flask-sqlalchemy出现错误的时候，寻找问题所在位置
app = Flask(__name__)

# 做一个url与视图函数的映射
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
