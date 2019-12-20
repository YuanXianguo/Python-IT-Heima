import time

t = time.localtime()
t_str = time.strftime("%Y-%m-%d %H:%M:%S", t)


def login():
    return "这是首页" + t_str


def register():
    return "这是注册页面" + t_str


def application(env, get_response):
    get_response("200 OK", [("Content-Type", "text/html;charset=utf-8")])
    file = env["file"]
    if file == "/login.py":
        return login()
    elif file == "/register.py":
        return register()
    return "hello world 你好中国"
