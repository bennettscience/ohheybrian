from flask import abort, current_app, Blueprint, redirect, render_template
from htmx_flask import make_response, request
from ohheybrian.extensions import db
from ohheybrian.models import Post, Post
from ohheybrian.templates.icons import icons


bp = Blueprint("blog", __name__)


@bp.get("/")
def index():
    posts = Post.query.all()
    return render_template("microblog/index.html", posts=posts)
