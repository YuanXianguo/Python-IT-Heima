def decorator(func):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        return "<h1>{}</h1>".format(res)
    return inner


def decorator2(func):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        return "<a>{}</a>".format(res)
    return inner


@decorator
@decorator2
def ha():
    return "haha"


print(ha())
