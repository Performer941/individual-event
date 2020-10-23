from models import db
from models.models import User
from . import passport_blu
from flask import render_template, request, jsonify, session, redirect, url_for


@passport_blu.route("/register.html")
def register():
    return render_template("register.html")


@passport_blu.route("/passport/register", methods=["GET", "POST"])
def register_commit():
    username = request.json.get('username')
    password = request.json.get('password')
    password2 = request.json.get('password2')

    print(username, password, password2)

    if db.session.query(User).filter(User.nick_name == username).first():

        return jsonify({
            "errno": 1001,
            "errmsg": "已经注册..."
        })
    elif password != password2:
        return jsonify({
            "errno": 1002,
            "errmsg": "两次密码不相同"
        })
    # 2.2 注册用户
    # 将新用户的数据插入到数据库
    user = User()
    user.nick_name = username
    # user.password_hash = password  # 未加密的方式，这样容易泄露用户名密码
    # user.password_hash = generate_password_hash(password)
    user.mobile = username
    user.password_hash = password
    try:
        db.session.add(user)
        db.session.commit()

        # 注册成功之后，立刻认为登录成功，也就说需要进行状态保持
        session['user_id'] = user.id
        session['nick_name'] = username

        ret = {
            "errno": 0,
            "errmsg": "注册成功..."
        }
        return jsonify(ret)
    except Exception as ret:
        print("---->", ret)
        db.session.rollback()  # 如果在将用户的信
        ret = {
            "errno": 1003,
            "errmsg": "注册失败..."
        }

        return jsonify(ret)


@passport_blu.route("/passport/login", methods=["GET", "POST"])
def login():
    # 1. 提取登录时的用户名，密码
    username = request.json.get("username")
    password = request.json.get("password")

    # 2. 查询，如果存在表示登录成功，否则失败
    user = db.session.query(User).filter(User.nick_name == username, User.password_hash == password).first()
    if user:
        ret = {
            "errno": 0,
            "errmsg": "登录成功"
        }

        session['user_id'] = user.id
        session['nick_name'] = username
    else:
        ret = {
            "errno": 2001,
            "errmsg": "用户名或者密码错误"
        }

    return jsonify(ret)


@passport_blu.route("/logout")
def logout():
    # 清空登录状态
    session.clear()

    return redirect(url_for('index_blu.index'))
