from flask import abort, Blueprint, render_template

from ohheybrian.models import Post

bp = Blueprint("posts", __name__)


@bp.get("/posts/<int:post_id>")
def get_single_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if post:
        result = render_template("microblog/post_base.html", post=post)
    else:
        abort(404)

    return result
