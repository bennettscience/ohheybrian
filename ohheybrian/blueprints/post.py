from flask import abort, Blueprint, render_template

from ohheybrian.extensions import db
from ohheybrian.models import Post

bp = Blueprint("posts", __name__)


@bp.get("/posts")
def get_posts():
    query = db.select(Post)
    posts = db.session.scalars(query).all()

    return render_template("microblog/index.html", posts=posts)


@bp.get("/posts/<int:post_year>/<int:post_month>/<string:post_slug>")
def get_single_post(post_year, post_month, post_slug):
    stmt = db.select(Post).where(Post.slug == post_slug)
    post = db.session.scalars(stmt).first()

    if post:
        result = render_template("microblog/article.html", article=post)
    else:
        abort(404)

    return result
