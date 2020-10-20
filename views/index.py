from . import index_blu
from flask import render_template


@index_blu.route("/")
def index():
    return render_template("index.html")


@index_blu.route("/index02.html")
def index02():
    return render_template("index02.html")


@index_blu.route("/index03.html")
def index03():
    return render_template("index03.html")


@index_blu.route("/user_list.html")
def user_list():
    return render_template("user_list.html")



