from flask import abort, Blueprint, render_template, request

from ohheybrian.extensions import db
from ohheybrian.models import Post

bp = Blueprint("post", __name__)


@bp.get("/")
def posts_index():
    page = request.args.get("page", 1, type=int)
    query = db.select(Post).where(Post.published).order_by(Post.created_on.desc())
    posts = db.paginate(query, page=page, per_page=2)

    return render_template("microblog/index.html", pagination=posts)


@bp.get("/posts/<string:post_slug>")
def get_single_post(post_slug):
    stmt = db.select(Post).where(Post.slug == post_slug)
    post = db.session.scalars(stmt).first()

    if post:
        result = render_template("microblog/article.html", article=post)
    else:
        abort(404)

    return result
