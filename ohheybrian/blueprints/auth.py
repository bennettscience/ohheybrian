from flask import Blueprint, current_app, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from htmx_flask import make_response
from webargs import fields
from webargs.flaskparser import parser

from ohheybrian.models import User

bp = Blueprint("auth", __name__)


@bp.get("/login")
def get_login():
    return render_template("shared/forms/login.html")


@bp.post("/login")
def login():
    args = parser.parse(
        {"email": fields.Str(), "password": fields.Str()}, location="form"
    )

    user = User.query.filter(User.email == args["email"]).first()
    if user is None or not user.check_password(args["password"]):
        return make_response(
            trigger={"showToast": "Usernmame or password is incorrect."}
        )

    login_user(user)
    return make_response(redirect=url_for("admin.index"))
