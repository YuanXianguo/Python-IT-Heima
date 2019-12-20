from flask import Flask
from login import app_login
from logout import app_logout

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(app_login, url_prefix="/user")
app.register_blueprint(app_logout, url_prefix="/user2")


@app.route("/")
def index():
    return "index page"


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
