from flask import Blueprint, redirect, render_template
from flask_login import current_user
from htmx_flask import make_response

from ohheybrian.extensions import db
from ohheybrian.models import Comment

bp = Blueprint("admin", __name__)


@bp.get("/admin")
def index():
    if current_user.is_anonymous:
        redirect(url_for("home.index"))
    comments = Comment.query.order_by(Comment.occurred.desc()).all()
    return render_template("admin/index.html", comments=comments)


# Get all posts
@bp.get("/posts")
def posts():
    pass


# Start a new post
@bp.get("/posts/new")
def create_post():
    pass


# Create the new post
@bp.post("/posts/new")
def save_new_post():
    pass


# Edit a post
@bp.get("/post/<int:post_id>")
def edit_post(post_id: int):
    pass
