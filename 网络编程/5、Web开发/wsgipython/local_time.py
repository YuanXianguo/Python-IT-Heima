import time


def application(env, start_response):
    print(env)
    status = "200 OK"
    headers = [
        ("Content-Type", "text/plain")
    ]
    start_response(status, headers)
    t = time.localtime()
    res_t = time.strftime("%Y-%m-%d %H:%M:%S", t)
    return res_t

