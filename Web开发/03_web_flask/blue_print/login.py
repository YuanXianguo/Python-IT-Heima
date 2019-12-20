from flask import Blueprint

# 参数：蓝图的名称，所在模块
app_login = Blueprint("app_login", __name__)


# 注册蓝图路由
@app_login.route("get_login")
def get_login():
    return "login page"
