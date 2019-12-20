from flask import Flask, current_app, redirect, url_for
from werkzeug.routing import BaseConverter

# 创建flask的应用对象
# __name__表示当前的模块名字
# flask以这个模块所在的目录为总目录，默认这个目录中的static为静态目录，templates为模板目录
app = Flask(__name__,
            static_url_path="/static",  # 访问静态资源的url前缀，默认值是static
            )
# 配置参数的使用方式
# 1.使用配置文件
# app.config.from_pyfile("config.cfg")
# 2.使用对象配置参数


class Config(object):
    DEBUG = True
    ITCAST = "python"


app.config.from_object(Config)

# 3.直接操作config字典对象
# app.config["DEBUG"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    """定义的视图函数"""
    # 读取配置参数
    # 1.直接从全局对象app的config字典中取值
    print(app.config.get('ITCAST'))

    # 2.通过current_app
    print(current_app.config.get("ITCAST"))
    return "hello flask"


@app.route("/login")
def login():
    # url_for通过视图函数的名字找到视图对应得url路径
    url = url_for("index")
    return redirect(url)


# 转换器传参，int/float/path，默认是字符串类型
@app.route("/goods/<int:goods_id>")
def goods(goods_id):
    return str(goods_id)


# 自定义转换器
class RegexConverter(BaseConverter):
    def __int__(self, url_map, regex):
        super().__init__(url_map)
        self.regex = regex

    def to_python(self, value):
        # value是在路径进行正则表达式匹配得时候提取的参数
        return value

    def to_url(self, value):
        # value是url反转时对应的参数
        return value


# 将自定义转换器添加到flask应用中
app.url_map.converters["re"] = RegexConverter


@app.route("/send/<re(r'1[34578]\d{9}'):phone>")
def send_msg(phone):
    return phone


@app.route("/register")
def register():
    url = url_for("send_msg", phone="13333333333")
    return redirect(url)


if __name__ == '__main__':
    # 通过url_map可以查看整个flask中的路由信息
    print(app.url_map)
    app.run(host="0.0.0.0",
            port=5000,
            debug=True)

