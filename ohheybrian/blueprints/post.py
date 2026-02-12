from datetime import datetime

from flask import abort, Blueprint, render_template, request, url_for
from sqlalchemy import extract

from ohheybrian.extensions import db
from ohheybrian.models import Post

bp = Blueprint("post", __name__)


@bp.get("/")
def posts_index():
    page = request.args.get("page", 1, type=int)
    query = db.select(Post).where(Post.published).order_by(Post.created_on.desc())
    posts = db.paginate(query, page=page, per_page=20)

    return render_template("microblog/index.html", endpoint='post.posts_index', pagination=posts)

@bp.get("/<int:year>/")
@bp.get("/<int:year>")
def get_posts_by_year(year):
    page = request.args.get("page", 1, type=int)

    stmt = db.select(Post).where(extract("year", Post.created_on) == year).order_by(Post.created_on.desc())

    posts = db.paginate(stmt, page=page, per_page=20)

    return render_template(
        "microblog/archive.html", pagination=posts, endpoint='post.get_posts_by_year', year=year, title="All posts for {}".format(year)
    )

@bp.get("/otd")
@bp.get("/otd/")
def on_this_day():
    page = request.args.get("page", 1, type=int)
    date = datetime.today()

    stmt = db.select(Post).where(extract("month", Post.created_on) == date.month).where(extract("day", Post.created_on) == date.day).order_by(Post.created_on.desc())


    posts = db.paginate(stmt, page=page, per_page=20)

    return render_template("microblog/index.html", pagination=posts, title="On this day...")


@bp.get("/<string:year>/<string:month>/<string:post_slug>/")
@bp.get("/<string:year>/<string:month>/<string:post_slug>")
def get_single_post(year, month, post_slug):
    stmt = db.select(Post).where(Post.slug == post_slug)
    post = db.session.scalars(stmt).first()

    # Load the neighbor posts
    post.load_neighbors()

    if post:
        result = render_template("microblog/article.html", article=post)
    else:
        abort(404)

    return result
