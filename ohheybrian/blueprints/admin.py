from flask import abort, Blueprint, redirect, render_template, url_for
from flask_login import current_user
from htmx_flask import make_response
from webargs import fields

from webargs.flaskparser import parser

from ohheybrian.extensions import db
from ohheybrian.models import Comment, Post

bp = Blueprint("admin", __name__)


@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)


@bp.get("/")
def index():
    if current_user.is_anonymous:
        redirect(url_for("home.index"))
    # gather stats from the database
    posts = Post.query.count()
    comments = Comment.query.order_by(Comment.occurred.desc()).all()
    return render_template("admin/index.html", posts=posts, comments=comments)


# Get all posts
@bp.get("/posts")
def posts():
    pass


# Start a new post
@bp.get("/posts/new")
def create_post():
    return render_template("microblog/write.html")


# Create the new post
@bp.post("/posts/new")
def save_new_post():
    args = parser.parse(
        {
            "title": fields.String(),
            "content": fields.String(),
            "category": fields.String(),
            "tags": fields.String(),
            "published": fields.String(),
        },
        location="form",
    )

    return "ok"


# Edit a post
@bp.get("/post/<int:post_id>")
def edit_post(post_id: int):
    pass
