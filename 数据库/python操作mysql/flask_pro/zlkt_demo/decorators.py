from flask import session, redirect, url_for
from functools import wraps


def login_required(func):
    """登录限制的装饰器"""
    @wraps(func)
    def deco(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return deco
