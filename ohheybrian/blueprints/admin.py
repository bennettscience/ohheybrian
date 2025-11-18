from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user
from slugify import slugify

import markdown

from ohheybrian.extensions import db
from ohheybrian.functions.helpers import (
    parse_post_tags,
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
    # TODO: Break this into a a helper function to process the new post?
    args = {}
    form = request.form

    args["title"] = form.get("title")
    # create the post slug from the title
    args["slug"] = slugify(form.get("title"))

    # set the post publish date - no scheduling yet.
    args["created_on"] = datetime.now()

    args["author"] = current_user

    args["post_body"] = markdown.markdown(form.get("post_body"))

    # check published - HTML sends "ok" for checkboxes
    if form.get("published") == "on":
        args["published"] = True
    else:
        args["published"] = False

    # At this point, the post is complete and can be added to the database.
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
    # check the tags and create new ones if necessary
    # Turn the tags field into a list
    args["tags"] = parse_post_tags(form.get("tags").split(", "))
    post.tags.extend(args["tags"])

    # check the post category
    # Can only be single, so checking here isn't awful
    # If the tags or category fail, flip the post to "draft" and flash and error?
    db.session.commit()

    return redirect(url_for("admin.admin_posts"))


# Edit a post
@bp.get("/posts/<int:post_id>")
def edit_post(post_id: int):
    pass
