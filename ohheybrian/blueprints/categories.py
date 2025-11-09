from flask import abort, Blueprint, redirect, request, render_template
from flask_login import current_user
from htmx_flask import make_response

from ohheybrian.extensions import db
from ohheybrian.models import Category

from ohheybrian.database import DBClient

client = DBClient(db)

bp = Blueprint("categories", __name__)


# Get all cats
@bp.get("/categories")
def categories():
    categories = client.get(Category).all()
    return render_template("category/index.html", categories=categories)


@bp.get("/categories/<int:cat_id>")
def get_category(cat_id):
    pass


# Start a new cat
@bp.get("/categories/new")
def create_category():
    return render_template("category/create.html")


# Create the new cat
@bp.post("/categories/new")
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
@bp.get("/categories/<int:cat_id>/edit")
def edit_category(cat_id: int):
    category = Category.query.filter(Category.id == cat_id).first()

    if not category:
        abort(404)

    return render_template("forms/edit.html", item=category)
