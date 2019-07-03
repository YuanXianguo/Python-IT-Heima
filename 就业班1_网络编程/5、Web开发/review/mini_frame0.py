import time

t = time.localtime()
t_str = time.strftime("%Y-%m-%d %H:%M:%S", t)


def login():
    return "login " + t_str


def register():
    return "register " + t_str


def application(file):
    if file == "/login.py":
        return login()
    elif file == "/register.py":
        return register()
    else:
        return "file not found"
