from flask import Blueprint, render_template
from flask_login import current_user
from htmx_flask import make_response

from ohheybrian.extensions import db
from ohheybrian.models import Comment

bp = Blueprint("admin", __name__)


@bp.get("/admin")
def index():
    if current_user.is_anonymous:
        redirect(url_for("home.index"))
    comments = Comment.query.all()
    return render_template(
        "admin/index.html",
        comments=comments
    )
