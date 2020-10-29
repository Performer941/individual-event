import hashlib
import time
from flask import session, render_template, jsonify, request
from models import db
from models.models import User
from . import user_blu


@user_blu.route("/personage")
def personage():
    return render_template("personage/user.html")


@user_blu.route("/user_base_info")
def user_base_info():
    return render_template("personage/user_base_info.html")


@user_blu.route("/user/basic", methods=["POST"])
def user_basic():
    # 获取用户的新的信息
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    # 获取当前用户的信息
    user_id = session.get("user_id")

    # 存储到数据库
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        ret = {
            "errno": 4002,
            "errmsg": "没有此用户"
        }

        return jsonify(ret)

    # 如果查询到此用户就修改数据
    user.nick_name = nick_name
    user.signature = signature
    user.gender = gender

    db.session.commit()

    ret = {
        "errno": 0,
        "errmsg": "修改成功..."
    }
    return jsonify(ret)


@user_blu.route("/user_pass_info")
def user_pass_info():
    return render_template("personage/user_pass_info.html")


@user_blu.route("/user/password", methods=["POST"])
def user_password():
    # 1. 提取旧密码以及新密码
    new_password = request.json.get("new_password")
    old_password = request.json.get("old_password")

    # 2. 提取当前用户的id
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "errno": 4001,
            "errmsg": "请先登录"
        })

    # 2. 判断用户输入的旧密码与数据库中的密码是否相同
    user = db.session.query(User).filter(User.id == user_id, User.password_hash == old_password).first()

    # 3. 如果相同，则修改
    if user:
        user.password_hash = new_password
        db.session.commit()
        ret = {
            "errno": 0,
            "errmsg": "修改成功"
        }
        session.clear()

    else:
        ret = {
            "errno": 4004,
            "errmsg": "原密码错误！"
        }

    # 4. 返回json
    return jsonify(ret)


@user_blu.route("/user_pic_info")
def user_pic_info():
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    return render_template("personage/user_pic_info.html", user=user)


@user_blu.route("/user/avatar", methods=["POST"])
def avatar():
    img = request.files.get("avatar")
    if img:
        # print(f.filename)
        # 为了防止多个用户上传的图片名字相同，需要将用户的图片计算出一个随机的用户名，防止冲突
        file_hash = hashlib.md5()
        file_hash.update((img.filename + time.ctime()).encode("utf-8"))
        file_name = file_hash.hexdigest() + img.filename[img.filename.rfind("."):]

        avatar_url = file_name

        # 将路径改为static/upload下
        file_name = "./static/upload/" + file_name
        # 用新的随机的名字当做图片的名字
        img.save(file_name)

        # 修改数据库中用户的头像链接（注意，图片时不放在数据库中的，数据库中存放的图片的名字或者路径加图片名）
        user_id = session.get("user_id")
        user = db.session.query(User).filter(User.id == user_id).first()
        user.avatar_url = avatar_url
        db.session.commit()

        ret = {
            "errno": 0,
            "errmsg": "成功"
        }
    else:
        ret = {
            "errno": 4003,
            "errmsg": "上传失败"
        }
    return jsonify(ret)
