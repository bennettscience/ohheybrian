from datetime import datetime

from flask import abort, Blueprint, redirect, render_template, url_for
from flask_login import current_user
from htmx_flask import make_response
from slugify import slugify
from webargs import fields

from webargs.flaskparser import parser

import markdown

from ohheybrian.extensions import db
from ohheybrian.functions.helpers import (
    parse_post_tags,
    check_tag_or_category_exists,
    create_new_category,
)
from ohheybrian.models import Comment, Post

bp = Blueprint("admin", __name__)


@bp.get("/posts")
def admin_posts():
    if current_user.is_anonymous:
        redirect(url_for("home.index"))
    # gather stats from the database
    posts = Post.query.all()
    return render_template("admin/index.html", posts=posts)


@bp.get("/comments")
def admin_comments():
    comments = Comment.query.order_by(Comment.occurred.desc()).all()
    return render_template("admin/index.html", comments=comments)


# Start a new post
@bp.get("/posts/add")
def create_post():
    return render_template("microblog/write.html")


# Create the new post
@bp.post("/posts/add")
def save_new_post():
    """
    Save a post to the database

    Create a new entry with submitted form data.
    """
    args = parser.parse(
        {
            "title": fields.String(),
            "post_body": fields.String(),
            "category": fields.String(),
            "tags": fields.String(),
            "published": fields.String(),
        },
        location="form",
    )

    # create the post slug from the title
    args["slug"] = slugify(args["title"])

    # set the post publish date - no scheduling yet.
    args["created_on"] = datetime.now()

    args["author"] = current_user

    args["post_body"] = markdown.markdown(args["post_body"])

    # check the tags and create new ones if necessary
    args["tags"] = parse_post_tags(args["tags"])

    # check published - HTML sends "ok" for checkboxes
    if args["published"] == "ok":
        args["published"] = True
    else:
        args["published"] = False

    post = Post(
        title=args["title"],
        slug=args["slug"],
        created_on=args["created_on"],
        author=args["author"].id,
        post_body=args["post_body"],
        published=args["published"],
    )

    db.session.add(post)

    # Add the tags to the new post object
    post.tags.extend(args["tags"])

    # check the post category
    # Can only be single, so checking here isn't awful
    db.session.commit()

    return redirect(url_for("admin.index"))


# Edit a post
@bp.get("/posts/<int:post_id>")
def edit_post(post_id: int):
    pass
