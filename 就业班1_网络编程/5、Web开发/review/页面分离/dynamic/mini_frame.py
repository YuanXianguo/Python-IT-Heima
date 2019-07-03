URL_DICT = dict()


def route(url):
    def decorator(func):
        URL_DICT[url] = func  # URL_DICT["/index.py"] = index
        
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return decorator


@route("/index.py")
def index():
    with open("./templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@route("/center.py")
def center():
    with open("./templates/center.html", "r", encoding="utf-8") as f:
        return f.read()


def application(env, get_response):
    get_response("200 OK", [("Content-Type", "text/html;charset=utf-8")])
    file = env["file"]
    try:
        func = URL_DICT[file]
        return func()
    except:
        return "hello world 你好中国"
