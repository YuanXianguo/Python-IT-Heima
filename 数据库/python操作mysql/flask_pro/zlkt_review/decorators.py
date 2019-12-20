from flask import redirect, url_for, session
from functools import wraps


def login_requested(func):
    """登录限制的装饰器函数"""

    @wraps(func)
    def inner(*args, **kwargs):
        if session.get("user_id"):
            return func(*args, **kwargs)
        return redirect(url_for("login"))
    return inner
