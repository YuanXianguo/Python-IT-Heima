from flask import Blueprint


app_logout = Blueprint("app_logout", __name__, template_folder="templates", static_folder="static")

# 在__init__.py文件被执行时，把视图加载进来，让蓝图与应用程序知道
from .logout import get_logout
