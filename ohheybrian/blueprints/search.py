from flask import Blueprint, render_template, request, url_for

from ohheybrian.extensions import db
from ohheybrian.models import Post

bp = Blueprint("search", __name__)


def handle_search(param):
    search = "%{}%".format(param)
    stmt = db.select(Post).where(Post.title.like(search))
    results = db.session.scalars(stmt).all()

    return results

@bp.get("/search")
def search_index():
    param = request.args.get("q")

    results = handle_search(param)

    return render_template("microblog/search.html", results=results, query=param)

@bp.post("/search")
def search():
    form = request.form
    param = form.get("search")

    search = handle_search(param)

    results = [(post.title, url_for('post.get_single_post', post_slug=post.slug, year=post.created_year, month=post.created_month)) for post in search]
        

    return render_template("shared/partials/inline-search.html", results=results)
