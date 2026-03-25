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
    origin = request.args.get("origin")
    param = form.get("search")

    if not param:
        page = request.args.get("page", 1, type=int)
        stmt = db.select(Post).order_by(Post.created_on.desc())
        pagination = db.paginate(stmt, page=page, per_page=25)

        results = pagination.items
        template = "shared/partials/admin-search-result.html"

    # Search the db by title only right now
    # Return a list of post objects
    search = handle_search(param)

    if origin:
        # Searching from the admin page needs the full post object returned.
        template = "shared/partials/admin-search-result.html"
        results = search
    else:
        # The inline search element only needs post titles and the URL
        template = "shared/partials/inline-search.html"
        results = [
            (
                post.title,
                url_for(
                    "post.get_single_post",
                    post_slug=post.slug,
                    year=post.created_year,
                    month=post.created_month,
                ),
            )
            for post in search
        ]

    return render_template(template, results=results)
