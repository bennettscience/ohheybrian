from flask import Blueprint, render_template

# from ohheybrian.extensions import db
# from ohheybrian.models import Post

bp = Blueprint("home", __name__)


@bp.get("/")
def index():
    # Placeholder for doing more stuff later on the home page
    # stmt = db.select(Post).order_by(Post.created_on.desc())
    # latest_post = db.session.scalars(stmt).first()

    return render_template("home/index.html")


@bp.get("/about/contact")
def contact():
    return render_template("about/index.html")


@bp.get("/privacy/endnote.html")
def endnote_privacy():
    return render_template("privacy/index.html")
