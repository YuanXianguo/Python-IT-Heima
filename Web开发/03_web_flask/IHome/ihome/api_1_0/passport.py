from . import api
from flask import request, jsonify, current_app, session
from sqlalchemy.exc import IntegrityError
import re

from ihome.utils.response_code import RET
from ihome import redis_db, db, constants
from ihome.models import User


@api.route("/users", methods=["POST"])
def register():

    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("sms_code")
    password = req_dict.get("password")

    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="密码错误")

    try:
        real_sms_code = redis_db.get("sms_code_%s" % mobile).decode("utf-8")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取验证码异常")

    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码失效")

    try:  # 防止重复校验
        redis_db.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)

    if real_sms_code != sms_code:
        return jsonify(error=RET.DATAERR, errmsg="短信验证码错误")

    user = User(name=mobile, mobile=mobile)
    user.password = password

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    # 保存登录状态到session中
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id

    return jsonify(errno=RET.OK, errmsg="注册成功")


@api.route("/sessions", methods=["POST"])
def login():

    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="密码错误")

    # 限制请求次数
    user_ip = request.remote_addr  # 用户的ip地址
    try:
        access_nums = redis_db.get("access_nums_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍后重试")

    # 从数据库中根据手机号查询用户的数据对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    # 验证用户手机和密码
    if user is None or not user.check_password(password):
        # 如果验证错误，记录错误次数
        try:
            redis_db.incr("access_num_%s" % user_ip)
            redis_db.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")

    # 如果验证通过，保存登录状态在session中
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id

    return jsonify(errno=RET.OK, errmsg="登录成功")


@api.route("/session", methods=["GET", "DELETE"])
def check_login():

    if request.method == "GET":
        # 尝试从session中获取用户的名字
        name = session.get("name")
        # 如果session中数据name名字存在，则表示用户已登录
        if name is not None:
            return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg="false")

    elif request.method == "DELETE":
        # 清除session数据
        session.clear()
        return jsonify(errno=RET.OK, errmsg="OK")
