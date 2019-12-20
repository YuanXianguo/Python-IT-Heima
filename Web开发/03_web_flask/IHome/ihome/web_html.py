from flask import Blueprint, current_app
from flask_wtf import csrf

# 提供静态文件的蓝图
html = Blueprint("web_html", __name__)


# 127.0.0.1:5000/favicon.ico  浏览器认为的网站标识，会自动请求
@html.route("/<re('.*'):html_file_name>")
def get_html(html_file_name):
    """提供html文件"""
    if not html_file_name:  # 如果为空，表示访问路径是/，请求的是主页
        html_file_name = "index.html"

    if html_file_name != "favicon.ico":
        html_file_name = "html/" + html_file_name

    # 创建一个csrf_token值
    csrf_token = csrf.generate_csrf()

    # flask提供的返回静态文件的方法
    res = current_app.send_static_file(html_file_name)

    # 设置cookie值
    res.set_cookie("csrf_token", csrf_token)

    return res
