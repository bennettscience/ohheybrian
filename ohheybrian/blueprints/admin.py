import os

from datetime import datetime

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
from slugify import slugify
from werkzeug.utils import secure_filename
from htmx_flask import make_response

import markdown

from ohheybrian.extensions import db
from ohheybrian.functions.helpers import check_category, parse_post_tags, validate_image
from ohheybrian.models import Category, Comment, Post, Tag

bp = Blueprint("admin", __name__)


@bp.get("/posts")
def admin_posts():
    if current_user.is_anonymous:
        redirect(url_for("home.index"))
    # gather stats from the database
    stmt = db.select(Post).order_by(Post.created_on.desc())
    posts = db.session.scalars(stmt).all()

    return render_template("admin/index.html", posts=posts)


@bp.get("/comments")
def admin_comments():
    comments = Comment.query.order_by(Comment.occurred.desc()).all()
    return render_template("admin/index.html", comments=comments)


# Start a new post
@bp.get("/posts/add")
def create_post():
    tags = db.session.scalars(db.select(Tag)).all()
    categories = db.session.scalars(db.select(Category)).all()

    return render_template("microblog/write.html", tags=tags, categories=categories)


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
    # This is redundant - assign directly if it works?
    args["category"] = check_category(form.get("category"))
    post.category = args["category"]

    # If the tags or category fail, flip the post to "draft" and flash and error?
    db.session.commit()

    return redirect(url_for("admin.admin_posts"))


# Edit a post
@bp.get("/posts/<int:post_id>")
def edit_post(post_id: int):
    pass
