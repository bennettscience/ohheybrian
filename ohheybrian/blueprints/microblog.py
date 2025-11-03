from flask import abort, current_app, Blueprint, redirect, render_template
from htmx_flask import make_response, request
from ohheybrian.extensions import db
from ohheybrian.models import Post, PostTag
from ohheybrian.templates.icons import icons

import nh3


bp = Blueprint("microblog", __name__)


@bp.get("/")
def microblog_index():
    posts = Post.query.all()
    return render_template("microblog/index.html", posts=posts)


@bp.get("/write")
def write_post():
    return render_template("")
