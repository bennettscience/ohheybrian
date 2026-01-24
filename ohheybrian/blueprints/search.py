from flask import Blueprint, render_template, request

from ohheybrian.extensions import db
from ohheybrian.models import Post

bp = Blueprint("search", __name__)


@bp.get("/search")
def search_index():
    param = request.args.get("q")

    if not param:
        results = ""
    else:
        search = "%{}%".format(param)
        
        stmt = db.select(Post).where(Post.title.like(search))
        results = db.session.scalars(stmt).all()

    return render_template("microblog/search.html", results=results, query=param)
