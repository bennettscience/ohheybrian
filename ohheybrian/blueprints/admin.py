import os

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import (
    abort,
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user
from werkzeug.utils import secure_filename
from htmx_flask import make_response

import markdown

from ohheybrian.extensions import db
from ohheybrian.functions.helpers import (
    parse_post_tags,
    validate_image,
    check_post_slug,
    check_edit_post_tags
)
from ohheybrian.models import Comment, Post

bp = Blueprint("admin", __name__)


@bp.before_request
def restricted():
    if current_user.is_anonymous:
        return redirect(url_for("home.index"))


@bp.get("/posts")
def admin_posts():
    if current_user.is_anonymous:
        redirect(url_for("home.index"))
    # gather stats from the database
    page = request.args.get("page", 1, type=int)
    stmt = db.select(Post).order_by(Post.created_on.desc())
    pagination = db.paginate(stmt, page=page, per_page=25)

    return render_template(
        "admin/posts_index.html", posts=pagination.items, pagination=pagination
    )


@bp.get("/comments")
def admin_comments():
    page = request.args.get("page", 1, type=int)
    stmt = db.select(Comment).order_by(Comment.occurred.desc())
    pagination = db.paginate(stmt, page=page, per_page=25)

    return render_template(
        "admin/comments_index.html", comments=pagination.items, pagination=pagination
    )


@bp.get("/tags")
def admin_tags():
    return redirect(url_for("admin.admin_posts"))


# Start a new post
@bp.get("/posts/add")
def create_post():
    return render_template("microblog/write.html", method="hx-post", editor_title="New Post", post=None)


@bp.post("/upload")
def save_new_image():
    # Set the current year to get the file into the right image folder
    year = str(datetime.now().year)

    # check that the path exists. This is mainly for new year photos
    savedir = os.path.join(current_app.config["UPLOAD_PATH"], year)

    if not os.path.exists(savedir):
        os.makedirs(savedir)

    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)
    if filename != "":
        file_ext = os.path.splitext(filename)[1]

        # Check for the extension sent in the config or that it is actuall an image:
        if file_ext not in current_app.config[
            "UPLOAD_EXTENSIONS"
        ] or file_ext != validate_image(uploaded_file.stream):
            abort(400)
        uploaded_file.save(os.path.join(savedir, filename))

        src = url_for("static", filename=f"images/{year}/" + filename)
        response = {"textarea": "#post_body", "value": src}
    return make_response(response, trigger={"insertImgSrc": response})


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

    # Check that the slug is unique and create
    # a new one if needed
    args["slug"] = check_post_slug(form.get("title"))

    # set the post publish date. include the timezone for RSS creation
    args["created_on"] = datetime.now(ZoneInfo("America/Indianapolis"))

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
    # This is redundant - assign directly if it works?
    # DISABLED FOR NOW
    # args["category"] = check_category(form.get("category"))
    # post.category = args["category"]

    # If the tags or category fail, flip the post to "draft" and flash and error?
    db.session.commit()

    return make_response(redirect=url_for("admin.admin_posts"))


# Edit a post
@bp.get("/posts/<int:post_id>")
def edit_post(post_id: int):
    from markdownify import markdownify

    stmt = db.select(Post).where(Post.id == post_id)
    post = db.session.scalars(stmt).first()

    # Turn the body back into markdown
    post_body = markdownify(post.post_body)
    tags = [tag.name for tag in post.tags] if post.tags else None

    return render_template(
        "microblog/write.html",
        post=post,
        tags=tags,
        post_body=post_body,
        method="hx-put",
        endpoint=url_for('admin.save_edit_post', post_id=post.id),
        editor_title="Edit Post"
    )

@bp.put("/posts/<int:post_id>")
def save_edit_post(post_id : int):
    args = {}
    form = request.form
    
    stmt = db.select(Post).where(Post.id == post_id)
    post = db.session.scalars(stmt).first()

    # To avoid duplicate tags, check that the post doesn't
    # already have a given tag attached to it and then
    # check for the new one.
    incoming_tags = form.get("tags").split(", ")
    current_tags = [tag.name for tag in post.tags]

    new_tags = check_edit_post_tags(current_tags, incoming_tags)

    if form.get("published") == "on":
        args["published"] = True
    else:
        args["published"] = False

    args["title"] = form.get("title")
    args["post_body"] = markdown.markdown(form.get("post_body"))

    # Send a dict of objects to update EXCEPT for tags!
    post.update(args)

    tags_to_add = parse_post_tags(new_tags)

    post.tags.extend(tags_to_add)

    return make_response(redirect=url_for("admin.admin_posts"))


# delete a post
@bp.delete("/posts/<int:post_id>")
def delete_post(post_id: int):
    stmt = db.select(Post).where(Post.id == post_id)
    post = db.session.scalars(stmt).first()

    db.session.delete(post)
    db.session.commit()
    
    return make_response(redirect=url_for("admin.admin_posts"))
