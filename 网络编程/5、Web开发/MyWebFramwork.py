import time


HTML_ROOT_DIR = "./html"


class Application(object):
    """框架的核心部分"""
    def __init__(self, urls):
        # 设置路由信息
        self.urls = urls

    def __call__(self, *args, **kwargs):
        (env, start_response) = args
        path = env.get("PATH_INFO", "/")
        if path.startswith("/static"):  # 如果是访问静态文件
            file_name = path[7:]
            try:
                with open(HTML_ROOT_DIR + file_name, "r", encoding="utf-8") as f:
                    data = f.read()
                    status = "200 OK"
                    headers = []
                    start_response(status, headers)
                    return data
            except:
                pass

        # 访问动态文件
        for url, app in self.urls:
            if path == url:
                return app(env, start_response)

        # 如果未找到路由信息，404错误
        status = "404 Not Found"
        headers = []
        start_response(status, headers)
        return "not found"


def show_time(env, start_response):
    status = "200 OK"
    headers = [
        ("Content-Type", "text/plain")
    ]
    start_response(status, headers)
    return time.ctime()


def say_hello(env, start_response):
    status = "200 OK"
    headers = [
        ("Content-Type", "text/plain")
    ]
    start_response(status, headers)
    return "hello daguo"


urls = [
    ("/", say_hello),
    ("/ctime", show_time),
    ("/sayhello", say_hello)
]
app = Application(urls)

