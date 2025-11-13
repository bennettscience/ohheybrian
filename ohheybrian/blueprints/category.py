from flask import abort, Blueprint, redirect, request, render_template
from flask_login import current_user
from htmx_flask import make_response

from ohheybrian.extensions import db
from ohheybrian.models import Category

from ohheybrian.database import DBClient

client = DBClient(db)

bp = Blueprint("category", __name__)


# Get all cats
@bp.get("/category")
def categories():
    categories = client.get(Category).all()
    return render_template("category/index.html", categories=categories)


@bp.get("/category/<int:cat_id>")
def get_category(cat_id):
    stmt = db.select(Category).where(Category.id == cat_id)
    category = db.session.scalars(stmt).one()

    return render_template("category/single.html", category=category)


# Start a new cat
@bp.get("/category/new")
def create_category():
    return render_template("category/create.html")


# Create the new cat
@bp.post("/category/new")
def save_new_category():
    """
    Expect a form with `name` property
    """
    name = request.form.get("name")
    if not name:
        abort(422)

    # Abstract into DB runner later
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return "ok"


# Edit a cat
@bp.get("/category/<int:cat_id>/edit")
def edit_category(cat_id: int):
    stmt = db.session.get(Category, cat_id)
    category = db.session.scalars(stmt).all()

    if not category:
        abort(404)

    return render_template("forms/edit.html", item=category)
