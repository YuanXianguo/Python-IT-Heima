from flask import render_template
from . import app_logout


# 注册蓝图路由
@app_logout.route("/get_logout")
def get_logout():
    return render_template("logout.html")
