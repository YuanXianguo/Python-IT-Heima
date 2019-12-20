from flask import session, g, jsonify
from werkzeug.routing import BaseConverter
from functools import wraps

from .response_code import RET


# 定义正则转换器
class ReConverter(BaseConverter):
    """"""
    def __init__(self, url_map, regex):
        super().__init__(url_map)
        self.regex = regex


def login_required(view_func):

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id is not None:
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    return wrapper
