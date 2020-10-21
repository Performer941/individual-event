from models import db
from . import passport_blu
from flask import render_template


@passport_blu.route("/login.html")
def login():
    return render_template("login.html")
