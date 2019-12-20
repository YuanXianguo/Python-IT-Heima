from flask import current_app, jsonify, make_response, request
import random

from . import api
from ihome import redis_db, constants
from ihome.utils.captcha.captcha import captcha
from ihome.utils.response_code import RET
from ihome.models import User


# GET /api/v1.0/image_codes/<image_code_id>
@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取图片验证码
    :param image_code_id: 图片验证码编号
    :return: 验证码图片
    """
    # 生成验证码图片
    # 名字，真实文本，图片数据
    name, text, image_data = captcha.generate_captcha()

    # 将验证码真实值与编号保存到redis中
    # redis_db.set("image_code_%s" % image_code_id, text)
    # redis_db.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
    try:
        redis_db.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg="save image code id filed")

    # 返回图片
    res = make_response(image_data)
    res.headers["Content-Type"] = "image/jpg"
    return res


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxx&image_code_id=xxx
@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信验证码"""
    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")

    # 校验参数
    if not all([image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 业务逻辑处理
    # 从redis中取出真实的图片验证码
    try:
        real_image_code = redis_db.get("image_code_%s" % image_code_id).decode("utf-8")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis数据异常")

    # 判断图片验证码是否过期
    if real_image_code is None:
        # 表示图片验证码没有或过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    # 删除redis中的图片验证码，防止用户使用用一个图片验证码验证多次
    try:
        redis_db.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 与用户填写的值进行对比
    if real_image_code.lower() != image_code.lower():
        # 表示用户填写错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断该手机号60s内记录
    try:
        send_flag = redis_db.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60s后重试")

    # 判断手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号已存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 如果手机号不存在，则生成短信验证码
    sms_code = str(random.randint(100000, 999999))

    # 保存真实的短信验证码
    try:
        redis_db.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送给这个手机号的记录，防止用户在60s内再次发送短信
        redis_db.setex("send_msg_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码失败")

    return jsonify(errno=RET.OK, errmsg="发送成功")
