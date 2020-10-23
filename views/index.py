from models import db
from models.models import User
from . import index_blu
from flask import render_template, session


@index_blu.route("/")
def index():
    user_id = session.get("user_id")
    nick_name = session.get("nick_name", "")
    user = db.session.query(User).filter(User.id == user_id).first()
    return render_template("index.html", user=user, nick_name=nick_name)


@index_blu.route("/index02.html")
def index02():
    user_id = session.get("user_id")
    nick_name = session.get("nick_name", "")
    user = db.session.query(User).filter(User.id == user_id).first()
    return render_template("index02.html", user=user, nick_name=nick_name)


@index_blu.route("/index03.html")
def index03():
    user_id = session.get("user_id")
    nick_name = session.get("nick_name", "")
    user = db.session.query(User).filter(User.id == user_id).first()
    return render_template("index03.html", user=user, nick_name=nick_name)


@index_blu.route("/user_list.html")
def user_list():
    user_id = session.get("user_id")
    nick_name = session.get("nick_name", "")
    user = db.session.query(User).filter(User.id == user_id).first()
    return render_template("user_list.html", user=user, nick_name=nick_name)



