from flask import g, current_app, jsonify, request, session
from . import api
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from ihome.models import User
from ihome import db


@api.route("/users/avatar", methods=["POST"])
@login_required
def set_user_avatar():

    """设置用户的头像"""
    user_id = g.user_id

    # 获取图片
    image_file = request.files.get("avatar")
    if image_file is None:
        return jsonify(errno=RET.PARAMERR, errmsg="未上传图片")

    # 保存图片
    image_data = image_file.read()
    fileurl = "static/images/avatars/%s.jpg" % user_id
    filename = "ihome/" + fileurl
    with open(filename, "wb") as f:
        f.write(image_data)

    # 保存图片到数据库
    try:
        User.query.filter_by(id=user_id).update({"avatar_url": fileurl})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片信息失败")
    return jsonify(errno=RET.OK, errmsg="保存成功", data={"avatar_url": fileurl})


@api.route("/users/name", methods=["PUT"])
@login_required
def set_user_name():

    user_id = g.get("user_id")
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    name = req_data.get("name")

    if not name:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    try:
        user = User.query.filter_by(name=name).first()
        if user:
            return jsonify(errno=RET.PARAMERR, errmsg="用户名已被使用")
    except Exception as e:
        current_app.logger.error(e)

    try:
        User.query.filter_by(id=user_id).update({"name": name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="设置用户错误")

    # 修改session数据中的name字段
    session["name"] = name

    return jsonify(errno=RET.OK, errmsg="保存成功", data={"name": name})


@api.route("/user")
@login_required
def show_user_info():

    user_id = g.get("user_id")
    try:
        user = User.query.filter_by(id=user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")
    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")

    return jsonify(errno=RET.OK, errmsg="成功", data=user.to_dict())


@api.route("/users/auth", methods=["GET", "POST"])
@login_required
def show_auth_info():
    if request.method == "GET":
        user_id = g.get("user_id")
        try:
            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")
        if user is None:
            return jsonify(errno=RET.NODATA, errmsg="无效操作")

        return jsonify(errno=RET.OK, errmsg="成功", data=user.auth_to_dict())

    user_id = g.get("user_id")
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    real_name = req_data.get("real_name")
    id_card = req_data.get("id_card")
    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    try:
        User.query.filter_by(id=user_id, real_name=None, id_card=None)\
            .update({"real_name": real_name, "id_card": id_card})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="设置用户错误")

    return jsonify(errno=RET.OK, errmsg="保存成功")

